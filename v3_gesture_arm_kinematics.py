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
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# -------------------------
# Virtual servo angles
# -------------------------
angles = [90, 90, 90, 90, 90]
filtered_finger_angles = [90, 90, 90, 90]

def clamp(v):
    return max(20, min(160, v))

# -------------------------
# Calculate joint angle
# -------------------------
def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

    return angle

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
lengths = [2, 2, 1.5, 1.2, 1]

def draw_arm(angles):
    ax.clear()
    x, y = 0, 0
    theta = 0

    xs = [0]
    ys = [0]

    for i in range(5):
        theta += math.radians((angles[i] - 90) * 1.2)
        x += lengths[i] * math.cos(theta)
        y += lengths[i] * math.sin(theta)
        xs.append(x)
        ys.append(y)

    ax.plot(xs, ys, '-o', linewidth=4)
    ax.scatter(xs[-1], ys[-1], s=120)

    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.set_title("Gesture Controlled Robotic Arm Simulation")
    ax.grid(True)

    plt.draw()
    plt.pause(0.01)

# -------------------------
# Control parameters
# -------------------------
SMOOTHING = 0.15
DEADZONE = 1.5
THUMB_RANGE = 0.12
INPUT_FILTER = 0.6
SNAP_THRESHOLD = 0.8   # <-- new stability snap threshold

prev_time = 0

# -------------------------
# Main loop
# -------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            # -------------------------
            # THUMB (with snap lock)
            # -------------------------
            thumb_tip = lm[4]
            thumb_base = lm[2]

            thumb_x_diff = thumb_tip.x - thumb_base.x
            normalized = thumb_x_diff / THUMB_RANGE
            normalized = max(-1, min(1, normalized))

            thumb_target = 90 + (normalized * 70)

            thumb_error = thumb_target - angles[0]

            if abs(thumb_error) < SNAP_THRESHOLD:
                angles[0] = thumb_target
            elif abs(thumb_error) > DEADZONE:
                angles[0] += thumb_error * SMOOTHING

            angles[0] = clamp(angles[0])

            # -------------------------
            # OTHER FINGERS
            # -------------------------
            finger_joints = [
                (5, 6, 8),
                (9, 10, 12),
                (13, 14, 16),
                (17, 18, 20)
            ]

            for i, (a, b, c) in enumerate(finger_joints):

                human_angle = calculate_angle(lm[a], lm[b], lm[c])

                # Input filtering
                filtered_finger_angles[i] = (
                    INPUT_FILTER * filtered_finger_angles[i]
                    + (1 - INPUT_FILTER) * human_angle
                )

                target = np.interp(
                    filtered_finger_angles[i],
                    [50, 160],
                    [20, 160]
                )

                error = target - angles[i+1]

                if abs(error) < SNAP_THRESHOLD:
                    angles[i+1] = target
                elif abs(error) > DEADZONE:
                    angles[i+1] += error * SMOOTHING

                angles[i+1] = clamp(angles[i+1])

            draw_arm(angles)

    # -------------------------
    # Overlay Information
    # -------------------------
    angle_text = (
        f"T:{int(angles[0])}  "
        f"I:{int(angles[1])}  "
        f"M:{int(angles[2])}  "
        f"R:{int(angles[3])}  "
        f"P:{int(angles[4])}"
    )

    cv2.putText(frame, angle_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Gesture Control – Simulation Mode", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()