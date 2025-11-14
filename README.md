# Visual Follow Line Solutions

This repository contains three different control strategies to solve the *Visual Follow Line* challenge (Formula 1), based on tracking a red line using computer vision.

## Code Description

The objective is to keep the vehicle centered on the red line by calculating the error between the image center and the centroid of the detected contour. Three control levels have been implemented:

* **Proporcional.py:** Basic `P` control. Adjusts turning proportionally to the current error.
* **PD.py:** `PD` control. Adds a derivative term to reduce oscillations and anticipate curves.
* **PID.py:** `PID` control. Includes the integral term to correct accumulated error over time.

## Chosen Parameters

All algorithms implement a **dynamic braking** system that reduces speed based on the magnitude of the error for sharp corners.

* **Base Speed (`k_speed`):** `0.032`
* **Brake Aggression:** `2.3`
* **Control Constants:**
    * `Kp`: `0.007`
    * `Kd`: `0.03`
    * `Ki`: `0.0000001`


**Note on Screenshots:** No screenshots of the execution are included. I did not take them during the sessions, and due to hardware limitations, the simulation required the full processing power of the classroom computers, making it impossible to reproduce it at home.
