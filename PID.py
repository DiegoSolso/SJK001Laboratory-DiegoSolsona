import WebGUI
import HAL
import Frequency
import cv2

k_speed = 0.032
BRAKE_AGGRESSION = 2.3

K_TURN_P = 0.007
K_TURN_D = 0.03

K_TURN_I = 0.0000001
integral_err = 0

last_err = 0
while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])
    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
    else:
        cX, cY = 0, 0

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        
        if M["m00"] != 0:
            cX = M["m10"] / M["m00"]
        else:
            cX = 320
        
        err = 320 - cX 
        deriv_err = err - last_err
        integral_err = integral_err + err
            
        turn = (K_TURN_P * err) + (K_TURN_I * integral_err) + (K_TURN_D * deriv_err)
        last_err = err

        normalized_error = abs(err) / 320.0
        speed_factor = (1.0 - normalized_error) ** BRAKE_AGGRESSION
        vel = (k_speed * 320) * speed_factor
        
        HAL.setV(vel)
        HAL.setW(turn)
        #print('vel: %.5f  turn: %.5f  err: %.1f  deriv: %.1f' % (vel,turn, err, deriv_err))

    else:
        HAL.setV(0)
        HAL.setW(0)
        last_err = 0

    WebGUI.showImage(img)
