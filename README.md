# Driver Drowsiness Detection System 🚗😴

This project is a **Driver Drowsiness Detection System** developed using **Python, OpenCV, and MediaPipe Face Mesh**.  
It detects whether the driver is feeling sleepy by monitoring the driver's eye movement in real-time through a webcam.

The system calculates the **Eye Aspect Ratio (EAR)**. If the driver’s eyes remain closed continuously for a certain number of frames, the system triggers a warning alert.

When drowsiness is detected, the system:
- Plays an alarm sound (`alert.wav`)
- Displays **"DROWSINESS ALERT!"** on the screen
- Sends an email notification to the registered recipient

This project is useful for accident prevention by alerting the driver immediately.

---

## 📌 Features
- Real-time webcam monitoring
- Face and eye landmark detection using MediaPipe Face Mesh
- Eye Aspect Ratio (EAR) based drowsiness detection
- Alarm sound alert using Pygame
- Email alert notification using SMTP (Gmail)
- Eye landmarks displayed on screen
- Works continuously until ESC key is pressed

---

## 🛠️ Technologies Used
- Python
- OpenCV
- MediaPipe
- NumPy
- Pygame
- SMTP (Email Service)
- Threading

---

## 📂 Project Files
- `detection.py` → Main Python program
- `alert.wav` → Alarm sound file
- `README.md` → Project documentation

---

## ⚙️ Working Method (How it Works)
1. Webcam captures real-time video frames.
2. MediaPipe Face Mesh detects face landmarks.
3. Eye landmarks are extracted from detected face.
4. Eye Aspect Ratio (EAR) is calculated using eye points.
5. If EAR value goes below the threshold continuously:
   - Drowsiness alert message is displayed
   - Alarm sound is played
   - Email alert is sent to the recipient

---

## 📌 Eye Aspect Ratio (EAR)
EAR is used to detect eye closure.  
If EAR becomes smaller than the threshold value, it means the driver’s eyes are closing.

Threshold used in this project:
- `EAR_THRESHOLD = 0.25`
- `EAR_CONSEC_FRAMES = 20`

---

## ▶️ How to Run the Project

### Step 1: Install Required Libraries
```bash
pip install opencv-python mediapipe numpy pygame
