import cv2
import os
import numpy as np
from datetime import datetime
import csv

# Path to folder with known face images
known_faces_path = 'images'
orb = cv2.ORB_create()

# Load and compute ORB features for each known face
known_faces = []
names = []

for file in os.listdir(known_faces_path):
    img_path = os.path.join(known_faces_path, file)
    img = cv2.imread(img_path, 0)  # grayscale
    keypoints, descriptors = orb.detectAndCompute(img, None)
    known_faces.append((keypoints, descriptors, os.path.splitext(file)[0]))
    names.append(os.path.splitext(file)[0])

# Initialize webcam
cap = cv2.VideoCapture(0)

# Attendance record
attendance = {}

import pyttsx3

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def mark_attendance(name):
    if name not in attendance:
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance[name] = time_now
        with open('attendance.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, time_now])
        print(f"{name} marked present at {time_now}")
        speak(f"{name} marked present")


# Matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kp2, des2 = orb.detectAndCompute(gray, None)

    best_match_name = "Unknown"
    max_matches = 0

    for kp1, des1, name in known_faces:
        if des1 is not None and des2 is not None:
            matches = bf.match(des1, des2)
            if len(matches) > max_matches and len(matches) > 15:
                max_matches = len(matches)
                best_match_name = name

    if best_match_name != "Unknown":
        mark_attendance(best_match_name)
        cv2.putText(frame, best_match_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Unknown", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Face Matcher Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
