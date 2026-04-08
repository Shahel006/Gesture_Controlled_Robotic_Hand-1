import cv2
import mediapipe as mp
import time

# =========================
# MEDIAPIPE SETUP
# =========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# =========================
# 5 VIRTUAL SERVOS
# =========================
# Thumb, Index, Middle, Ring, Pinky
servo = [90, 90, 90, 90, 90]

def clamp(v):
    return max(0, min(180, v))

# =========================
# FINGER STATE DETECTION
# =========================
def get_finger_states(hand_landmarks):
    fingers = []

    # Thumb (x-axis)
    fingers.append(
        hand_landmarks.landmark[4].x <
        hand_landmarks.landmark[3].x
    )

    # Other fingers (y-axis)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    for tip, pip in zip(tips, pips):
        fingers.append(
            hand_landmarks.landmark[tip].y <
            hand_landmarks.landmark[pip].y
        )

    return fingers

# =========================
# CAMERA (macOS SAFE)
# =========================
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
time.sleep(1)

if not cap.isOpened():
    print("Camera not opened")
    exit()

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            finger_states = get_finger_states(hand_landmarks)

            for i in range(5):
                if finger_states[i]:
                    servo[i] += 2
                else:
                    servo[i] -= 2
                servo[i] = clamp(servo[i])

            cv2.putText(
                frame,
                f"Thumb:{servo[0]} Index:{servo[1]} Middle:{servo[2]} Ring:{servo[3]} Pinky:{servo[4]}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imshow("Gesture Control – Software Only", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()