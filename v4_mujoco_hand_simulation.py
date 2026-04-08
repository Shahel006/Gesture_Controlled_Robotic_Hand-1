import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = detector.detect(mp_image)

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        tip = hand[8]     # index finger tip
        base = hand[5]    # index finger base

        dist = np.linalg.norm([
            tip.x - base.x,
            tip.y - base.y
        ])

        print("Index finger bend:", dist)

    cv2.imshow("Hand Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()