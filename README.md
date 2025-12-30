# Gesture Based Volume Control Using Computer Vision

A real time hand gesture controlled volume system built with Computer Vision and MediaPipe.  
This project enables users to control system volume by adjusting the distance between their thumb and index finger, captured via a live camera feed.

<img width="712" height="965" alt="1" src="https://github.com/user-attachments/assets/163c0cd6-32a9-440e-854d-6cd6fcb7bdaf" />


## Project Overview
This application demonstrates the practical use of computer vision and human computer interaction.  
It combines real time hand tracking with system level audio control to create a touchless and intuitive user experience.


## Key Features
* Real time hand landmark detection using MediaPipe
* Smooth and responsive volume control
* Visual volume indicator and percentage display
* Supports IP camera streams such as DroidCam
* Multi threaded architecture for better performance
* Clean and modular Python code


## Technologies and Libraries
* Python
* OpenCV
* MediaPipe
* NumPy
* PyCaw for Windows audio control
* Comtypes
* Threading

## Project Structure
```
gesture_volume_control/
volume_changer.py
HandDetector.py
README.md
```


## Camera Configuration
The system uses an IP camera stream. Example using DroidCam

```python
url = "http://192.168.1.9:4747/video"
```

Ensure that both the camera device and the PC are connected to the same local network.


## How It Works
1. Captures live video frames from the camera
2. Detects hand landmarks in real time
3. Tracks thumb tip landmark 4 and index finger tip landmark 8
4. Calculates the Euclidean distance between the two points
5. Maps the distance to the system volume range
6. Displays real time visual feedback

<img width="370" height="400" alt="2" src="https://github.com/user-attachments/assets/ae619ab8-dbec-47ff-9003-37e414b9f6d7" />
<img width="400" height="400" alt="3" src="https://github.com/user-attachments/assets/b1464a8f-27f8-42c5-b542-d5b9feb4103a" />



## Running the Application
```bash
python volume_changer.py
```

Press Q to safely exit the application.


## Dependencies
```
opencv-python
numpy
mediapipe
pycaw
comtypes
```

## Platform Compatibility
Operating system Windows  
Reason PyCaw uses Windows audio endpoints

## Use Cases
* Touchless system control
* Accessibility applications
* Computer vision learning projects
* Human computer interaction demonstrations
* Smart environment interfaces

## License
This project is licensed under the MIT License.

## Author
Ali Hassoneh

