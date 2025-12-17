import cv2
import numpy as np
import math
import time
import WebGUI as GUI
import HAL

# CENTRO
CENTER_X = 33.0
CENTER_Y = -35.0

# Altura de vuelo
ALTITUDE = 4.0

SPIRAL_VELOCITY = 2.0       # m/s
MAX_VICTIMS = 6.0           # Victimas finales
SPIRAL_GROWTH = 0.2         # Crecimiento

spiral_angle = 0.0          # Ángulo acumulado
current_radius = 0.0        # Radio actual


cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

state = "TAKEOFF"
found_victims = []
last_time = time.time()

def rotate_image_gray(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

print(f"Misión: Espiral centrada en [{CENTER_X}, {CENTER_Y}]")

while True:
    current_time = time.time()
    dt = current_time - last_time
    if dt <= 0: dt = 0.01
    last_time = current_time

    img = HAL.get_ventral_image()
    pos = HAL.get_position()
    current_x, current_y, current_z = pos

    if img is None: continue

    # DETECCIÓN DE CARAS
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_in_this_frame = False

    # Probamos rotaciones cada 30 grados
    for angle in range(0, 360, 30):
        if angle == 0:
            img_check = gray
        else:
            img_check = rotate_image_gray(gray, angle)

        faces = face_cascade.detectMultiScale(img_check, 1.2, 3)

        if len(faces) > 0:
            detected_in_this_frame = True
            break

    if detected_in_this_frame:
        h, w = img.shape[:2]
        cv2.circle(img, (int(w/2), int(h/2)), 30, (0, 255, 0), 3)

        if state == "SEARCH":
            is_new = True
            for v in found_victims:
                dist_v = math.sqrt((current_x - v[0])**2 + (current_y - v[1])**2)
                if dist_v < 4.0:
                    is_new = False
                    break

            if is_new:
                print(f"¡VÍCTIMA! Pos: ({current_x:.2f}, {current_y:.2f})")
                found_victims.append([current_x, current_y])

    GUI.showImage(img)


    if state == "TAKEOFF":
        HAL.takeoff()
        if current_z < (ALTITUDE - 0.2):
            HAL.set_cmd_vel(0, 0, 1.5, 0)
        else:
            state = "TRAVEL"

    elif state == "TRAVEL":
        dx = CENTER_X - current_x
        dy = CENTER_Y - current_y
        dist = math.sqrt(dx**2 + dy**2)
        hold_z = (ALTITUDE - current_z) * 0.5

        if dist < 1.0:
            print("Centro alcanzado. INICIANDO ESPIRAL ANCLADA.")
            state = "SEARCH"
            HAL.set_cmd_vel(0, 0, 0, 0)
        else:
            v_x = max(min(dx * 0.5, 3.0), -3.0)
            v_y = max(min(dy * 0.5, 3.0), -3.0)
            HAL.set_cmd_vel(v_x, v_y, hold_z, 0)

    elif state == "SEARCH":
        current_radius = SPIRAL_GROWTH * spiral_angle

        if len(found_victims) >= MAX_VICTIMS:
            state = "FINISHED"
            HAL.set_cmd_vel(0, 0, 0, 0)
        else:
            if current_radius < 0.1:
                current_radius = 0.1

            omega = SPIRAL_VELOCITY / current_radius
            spiral_angle += omega * dt

            target_spiral_x = CENTER_X + (current_radius * math.cos(spiral_angle))
            target_spiral_y = CENTER_Y + (current_radius * math.sin(spiral_angle))

            error_x = target_spiral_x - current_x
            error_y = target_spiral_y - current_y

            vx_cmd = error_x * 1.0
            vy_cmd = error_y * 1.0


            speed_limit = 2.5
            vx_cmd = max(min(vx_cmd, speed_limit), -speed_limit)
            vy_cmd = max(min(vy_cmd, speed_limit), -speed_limit)

            hold_z = (ALTITUDE - current_z) * 0.5

            HAL.set_cmd_vel(vx_cmd, vy_cmd, hold_z, 0)

    elif state == "FINISHED":
        print("       INFORME DE MISION       ")
        print(f"Víctimas encontradas: {len(found_victims)}")
        print("-" * 40)
        for i, v in enumerate(found_victims):
            print(f" [{i+1}] X={v[0]:.2f}, Y={v[1]:.2f}")

        print("Volviendo a casa...")
        HAL.set_cmd_pos(0,0,ALTITUDE,0)
        state = "LANDING"

    elif state == "LANDING":
        dist = math.sqrt(current_x**2 + current_y**2)

        if dist < 1.0:
            HAL.land()
            print("Dron en tierra. Fin del programa.")
            break
