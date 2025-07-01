import cv2
import csv
from datetime import datetime

# Load the Haar cascade XML file
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

# Dictionary to store attendance
attendance = {}

# Function to mark attendance in CSV
def mark_attendance(name):
    if name not in attendance:
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance[name] = time_now
        with open('attendance.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, time_now])
        print(f"{name} marked present at {time_now}")

print("Face Detection Running... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        mark_attendance("Person")

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
s