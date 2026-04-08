import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import mujoco
import mujoco.viewer
import numpy as np
import time

# -----------------------------
# MediaPipe Setup
# -----------------------------
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

# -----------------------------
# MuJoCo Setup
# -----------------------------
model = mujoco.MjModel.from_xml_path("right_hand.xml")
data = mujoco.MjData(model)

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

viewer = mujoco.viewer.launch_passive(model, data)

prev_ctrl = np.zeros(model.nu)


# -----------------------------
# Finger angle function
# -----------------------------
def finger_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    ba = a - b
    bc = c - b

    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1, 1))

    return angle


# -----------------------------
# Unified bend (INVERTED FIX)
# -----------------------------
def get_bend(angle):
    bend = np.interp(angle, [0.2, 1.7], [0, 2.0])
    bend = np.clip(bend, 0, 2.0)
    return 2.0 - bend   # 🔥 THIS FIXES ALL FINGERS


# -----------------------------
# Main Loop
# -----------------------------
while viewer.is_running():

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    ctrl = np.zeros(model.nu)

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        # -----------------------------
        # THUMB (INVERTED FIX)
        # -----------------------------
        thumb_tip = hand[4]
        thumb_base = hand[2]

        thumb_dist = np.linalg.norm([
            thumb_tip.x - thumb_base.x,
            thumb_tip.y - thumb_base.y
        ])

        thumb_bend = np.clip(
            np.interp(thumb_dist, [0.05, 0.30], [0, 1.5]),  # 🔥 FIXED
            0,
            1.5
        )

        ctrl[4] = thumb_bend * 0.4
        ctrl[5] = thumb_bend * 0.7
        ctrl[6] = thumb_bend
        ctrl[7] = thumb_bend

        # -----------------------------
        # INDEX
        # -----------------------------
        index_angle = finger_angle(hand[5], hand[6], hand[8])
        ctrl[8:11] = get_bend(index_angle)

        # -----------------------------
        # MIDDLE
        # -----------------------------
        middle_angle = finger_angle(hand[9], hand[10], hand[12])
        ctrl[11:14] = get_bend(middle_angle)

        # -----------------------------
        # RING
        # -----------------------------
        ring_angle = finger_angle(hand[13], hand[14], hand[16])
        ctrl[14:17] = get_bend(ring_angle)

        # -----------------------------
        # PINKY
        # -----------------------------
        pinky_angle = finger_angle(hand[17], hand[18], hand[20])
        ctrl[17:20] = get_bend(pinky_angle)

    # -----------------------------
    # Smooth movement
    # -----------------------------
    ctrl = 0.7 * prev_ctrl + 0.3 * ctrl

    data.ctrl[:] = ctrl
    prev_ctrl = ctrl

    mujoco.mj_step(model, data)
    viewer.sync()

    time.sleep(0.01)

cap.release()
