import cv2
import os
import numpy as np
from datetime import datetime
import csv
import threading
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3

# Voice setup
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ORB & Matcher setup
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
known_faces_path = 'images'
known_faces = []

# Load images
for file in os.listdir(known_faces_path):
    path = os.path.join(known_faces_path, file)
    img = cv2.imread(path, 0)
    kp, des = orb.detectAndCompute(img, None)
    if des is not None:
        known_faces.append((kp, des, os.path.splitext(file)[0]))

# Attendance dictionary
attendance = {}
def mark_attendance(name):
    if name not in attendance:
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance[name] = time_now
        with open('attendance.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, time_now])
        status_label.config(text=f"{name} marked present at {time_now}")
        attendance_listbox.insert(tk.END, f"✔ {name}")
        speak(f"{name} marked present")

# GUI Setup
root = tk.Tk()
root.title("Face Recognition Attendance")
root.geometry("850x680")
root.configure(bg="#2c3e50")
root.resizable(True, True)

tk.Label(root, text="Face Recognition Attendance", font=("Helvetica", 24, "bold"),
         bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

video_frame = tk.Frame(root, bg="#34495e", bd=2, relief=tk.RIDGE)
video_frame.pack(padx=20, pady=10, fill="both", expand=True)
video_label = tk.Label(video_frame)
video_label.pack(padx=10, pady=10)

status_label = tk.Label(root, text="Click Start to begin", font=("Helvetica", 14),
                        fg="#ecf0f1", bg="#2c3e50")
status_label.pack(pady=10)

# Live attendance list
live_frame = tk.Frame(root, bg="#2c3e50")
live_frame.pack(pady=5)

tk.Label(live_frame, text="✔ Marked Students", font=("Helvetica", 14, "bold"),
         bg="#2c3e50", fg="white").pack()

attendance_listbox = tk.Listbox(live_frame, width=40, height=8,
                                font=("Helvetica", 12), bg="#34495e", fg="lime", selectbackground="#2c3e50")
attendance_listbox.pack(pady=5)

# Face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Camera loop
running = False
def camera_loop():
    global running
    cap = cv2.VideoCapture(0)
    while running:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        recognized_names = set()

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            kp2, des2 = orb.detectAndCompute(roi, None)

            best_match = "Unknown"
            max_matches = 0

            for kp1, des1, name in known_faces:
                if des1 is not None and des2 is not None:
                    matches = bf.match(des1, des2)
                    if len(matches) > max_matches and len(matches) > 50:
                        max_matches = len(matches)
                        best_match = name

            if best_match != "Unknown":
                if best_match not in recognized_names:
                    mark_attendance(best_match)
                    recognized_names.add(best_match)
                color = (0, 255, 0)
                label = best_match
            else:
                color = (0, 0, 255)
                label = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, color, 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        root.update_idletasks()
        root.update()

    cap.release()
    status_label.config(text="Camera stopped")

# Start/Stop Buttons
def start_camera():
    global running
    if not running:
        running = True
        status_label.config(text="Camera started")
        threading.Thread(target=camera_loop, daemon=True).start()

def stop_camera():
    global running
    if running:
        running = False
        status_label.config(text="Stopping camera...")

btn_frame = tk.Frame(root, bg="#2c3e50")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start", command=start_camera, width=12,
          bg="#2ecc71", fg="white", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=20)

tk.Button(btn_frame, text="Stop", command=stop_camera, width=12,
          bg="#e74c3c", fg="white", font=("Helvetica", 14, "bold")).grid(row=0, column=1, padx=20)

root.mainloop()
