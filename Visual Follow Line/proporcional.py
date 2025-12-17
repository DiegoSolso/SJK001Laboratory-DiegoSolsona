import WebGUI
import HAL
import Frequency
import cv2

k_speed = 0.032
k_turn = 0.007
BRAKE_AGGRESSION = 2.3

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

    if cX > 0:
        err = 320 - cX  
        turn = k_turn * err
        normalized_error = abs(err) / 320.0
        speed_factor = (1.0 - normalized_error) ** BRAKE_AGGRESSION
        vel = (k_speed * 320) * speed_factor
        HAL.setV(vel)
        HAL.setW(turn)
        #print('vel: %.5f   turn: %.5f' % (vel,turn))

    WebGUI.showImage(img)
