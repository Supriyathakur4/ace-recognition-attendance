 Face Recognition Attendance System — Project Report
1. Project Title
Face Recognition Attendance System with a User-Friendly GUI

2. Objective
The goal of this project is to create an easy-to-use attendance system that automatically detects and recognizes faces using a webcam. It helps schools or organizations take attendance quickly and accurately, without the hassle of manual roll calls.

3. Overview
This system uses computer vision to identify people in real-time from a webcam feed. It compares the faces it sees with a folder of known student photos, and when it recognizes someone, it marks them as present automatically. The system also shows a live video feed with detected faces highlighted, plus a list of who’s marked present. To make it friendlier, it even gives voice confirmation when it recognizes someone.

4. Technologies Used
Python 3 — the main programming language

OpenCV — for detecting and processing faces

Tkinter — to build the graphical user interface (GUI)

pyttsx3 — for the voice confirmation feature

Haar Cascade Classifier — to detect faces in video frames

ORB and BFMatcher — to compare and recognize faces

CSV — to save attendance records

5. Features
Real-time face detection and recognition

Automatic attendance marking in a CSV file

Voice feedback when someone is recognized

Clean and simple GUI displaying the video feed and attendance list

Easy to add or update student photos

Can handle multiple students

6. How It Works
The system loads all student photos from the images folder and processes them to learn unique features.

It turns on the webcam and captures live video frames continuously.

Each frame is scanned for faces using Haar Cascade detection.

Detected faces are compared to the known student faces using feature matching.

When a match is found, the student’s attendance is marked with the current time.

The live feed shows boxes around faces with names, and the attendance list updates in real-time.

A friendly voice confirms the attendance as soon as someone is recognized.

7. How to Run
Make sure you have Python installed along with the required libraries:

bash
Copy
Edit
pip install opencv-python pillow pyttsx3
Add clear photos of students inside the images folder.

Run the main program by opening a command prompt in the project folder and typing:

bash
Copy
Edit
python face_recog_gui.py
The GUI window will open, webcam will start, and attendance will be tracked automatically.


9. Future Improvements
Export attendance reports in Excel or PDF formats

Add user login for system security

Support multiple cameras or mobile devices

Improve recognition accuracy using advanced deep learning models

Build a mobile app version for remote attendance marking

10. About Me
I’m Supriya Thakur, a passionate developer eager to build smart, practical projects that solve real-world problems.
Feel free to check out my GitHub: https://github.com/supriyahappy
Email: supriyathakur744@gmail.com