# Rescue People - Autonomous Drone Operation

## Mission Overview
This project, in the **drone.py** file, contains the solution for the "Rescue People" exercise. The goal is to program an autonomous drone to explore a maritime area, search for castaways (represented by floating dummies), and report their positions to the station.

The solution implements a state-machine architecture to handle takeoff, spiral search patterns, face detection using Computer Vision (Haar Cascades), and automatic return-to-home logic.

## Prerequisites & Technologies
* **Python 3.x**
* **OpenCV (`cv2`):** For image processing and face detection.
* **NumPy:** For vector calculations.
* **HAL & GUI:** Specific APIs for the drone simulation environment.

## Simulation Scenario
![Scenario View](Captura desde scenario.png)
*Figure 1: Third-person view of the drone searching for victims in the water.*

## How it Works (Algorithm)

The logic is structured around a **Finite State Machine (FSM)** with the following states:

1.  **TAKEOFF:** The drone rises to a target altitude of **4 meters**.
2.  **TRAVEL:** The drone moves quickly to the defined search center coordinates `[33.0, -35.0]`.
3.  **SEARCH (The Spiral Strategy):**
    * Once at the center, the drone initiates an **Archimedean Spiral** movement.
    * This is achieved by calculating the velocity vectors based on a growing radius:
      `current_radius = SPIRAL_GROWTH * spiral_angle`
    * This pattern ensures complete coverage of the area, expanding outwards efficiently.
4.  **DETECTION (Computer Vision):**
    * The drone captures images from the ventral camera.
    * **Rotation Logic:** To improve detection of victims floating in random orientations, the system rotates the analyzed frame in **30-degree increments** (0° to 360°).
    * If a face is detected using the `haarcascade_frontalface_default.xml`, the position is logged.
5.  **FINISHED / RTL:** Once the target number of victims (**MAX_VICTIMS = 6**) is found, the drone stops and returns to the launch point.
6.  **LANDING:** The drone lands safely.

## Detection & Results

The system successfully located **6/6 victims** in the simulation.

### Computer Vision Output
When a victim is detected, the system draws a visual indicator on the screen to validate the detection event.

| Detection Example 1 | Detection Example 2 |
| :---: | :---: |
| ![Detection 1](Captura desde detection1.png) | ![Detection 2](Captura desde detection2.png) |

### Mission Report
The final output logs the GPS coordinates of all survivors found before returning to base.

![Console Log](Captura desde console.png)

## Limitations & Known Issues

**Visual Feedback & Precision:**
* **Center-Fixed Visualization:** Currently, when the Haar Cascade classifier detects a face, the visual feedback (green circle) is drawn at the center of the image `(width/2, height/2)` rather than bounding the specific face coordinates. This signals that a detection occurred in that frame, but does not pinpoint the pixel location.
* **Coordinate Accuracy:** Consequently, the system logs the **drone's current GPS position** as the victim's location. While this introduces a minor offset compared to the victim's exact center, the margin of error is within the logic's threshold (< 4.0 meters) to successfully distinguish between unique victims.







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
