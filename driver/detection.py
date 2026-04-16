import cv2
import mediapipe as mp
import numpy as np
import pygame
from threading import Thread
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize pygame for sound playback
pygame.mixer.init()
ALERT_SOUND_PATH = "alert.wav"  # Make sure this file is in the same folder

# Email settings (Gmail in this case)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "example.sender@gmail.com"
SENDER_PASSWORD = "YOUR_APP_PASSWORD"  # You may want to use an app-specific password for security
RECIPIENT_EMAIL = "example.receiver@gmail.com"

# Constants
EAR_THRESHOLD = 0.25
EAR_CONSEC_FRAMES = 20

COUNTER = 0
ALERT_ON = False


def send_email_alert():
    """Function to send email alert."""
    try:
        # Create message object instance
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "Drowsiness Detection Alert"

        # Add body to email
        body = "Warning: Drowsiness detected! Please take action immediately."
        msg.attach(MIMEText(body, 'plain'))

        # Setup the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Encrypts the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send email
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def play_alert_sound():
    """Function to play an alert sound when drowsiness is detected."""
    try:
        pygame.mixer.music.load(ALERT_SOUND_PATH)
        pygame.mixer.music.play()
    except Exception as e:
        print("Failed to play sound:", e)


def eye_aspect_ratio(eye):
    """Calculate the Eye Aspect Ratio (EAR)."""
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)


def start_detection():
    global COUNTER, ALERT_ON

    # Setup face mesh from MediaPipe
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

    # Eye landmark indices from MediaPipe
    LEFT_EYE = [362, 385, 387, 263, 373, 380]
    RIGHT_EYE = [33, 160, 158, 133, 153, 144]

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = np.array([(int(p.x * w), int(p.y * h)) for p in face_landmarks.landmark])
                left_eye = landmarks[LEFT_EYE]
                right_eye = landmarks[RIGHT_EYE]

                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)
                ear = (left_ear + right_ear) / 2.0

                if ear < EAR_THRESHOLD:
                    COUNTER += 1
                    if COUNTER >= EAR_CONSEC_FRAMES:
                        if not ALERT_ON:
                            ALERT_ON = True
                            Thread(target=play_alert_sound).start()
                            Thread(target=send_email_alert).start()  # Send the email alert
                        cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
                else:
                    COUNTER = 0
                    ALERT_ON = False

                # Draw eyes
                for pt in left_eye:
                    cv2.circle(frame, tuple(pt), 2, (0, 255, 0), -1)
                for pt in right_eye:
                    cv2.circle(frame, tuple(pt), 2, (0, 255, 0), -1)

        cv2.imshow("Drowsiness Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_detection()
