import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import math
import time

# -------------------------
# MediaPipe setup
# -------------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# -------------------------
# Virtual servo angles
# Thumb, Index, Middle, Ring, Pinky
# -------------------------
angles = [90, 90, 90, 90, 90]

def clamp(v):
    return max(0, min(180, v))

# -------------------------
# Finger detection
# -------------------------
def get_finger_states(hand_landmarks):
    fingers = []

    # Thumb
    fingers.append(
        hand_landmarks.landmark[4].x <
        hand_landmarks.landmark[3].x
    )

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    for tip, pip in zip(tips, pips):
        fingers.append(
            hand_landmarks.landmark[tip].y <
            hand_landmarks.landmark[pip].y
        )

    return fingers  # [Thumb, Index, Middle, Ring, Pinky]

# -------------------------
# Camera
# -------------------------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
time.sleep(1)

# -------------------------
# Matplotlib setup
# -------------------------
plt.ion()
fig, ax = plt.subplots()

lengths = [2, 2, 1.5, 1.2, 1]  # arm segment lengths

def draw_arm(angles):
    ax.clear()
    x, y = 0, 0
    theta = 0

    xs = [0]
    ys = [0]

    for i in range(5):
        # Bigger and clearer rotation
        theta += math.radians((angles[i] - 90) * 1.2)
        x += lengths[i] * math.cos(theta)
        y += lengths[i] * math.sin(theta)
        xs.append(x)
        ys.append(y)

    ax.plot(xs, ys, '-o', linewidth=3)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_title("Gesture Controlled Robotic Arm")
    ax.grid(True)
    plt.draw()
    plt.pause(0.01)

# -------------------------
# Control parameters
# -------------------------
OPEN_ANGLE = 160
CLOSED_ANGLE = 20
SMOOTHING = 0.15

# -------------------------
# Main loop
# -------------------------
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
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            fingers = get_finger_states(hand_landmarks)

            # One finger → one joint
            for i in range(5):
                target = OPEN_ANGLE if fingers[i] else CLOSED_ANGLE
                angles[i] += (target - angles[i]) * SMOOTHING
                angles[i] = clamp(angles[i])

            draw_arm(angles)

    cv2.imshow("Gesture Input", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()