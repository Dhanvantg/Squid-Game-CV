import cv2
import mediapipe as mp
import pyautogui
import winsound

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
screen_w, screen_h = pyautogui.size()
body_coords = []
old_x, old_y = 0, 0

cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring no Video in Camera Frame!")
            continue

        frame_h, frame_w, _ = image.shape
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        landmarks = results.pose_landmarks

        if not results.pose_landmarks:
            continue
        landmark = landmarks.landmark
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #
        for id, mark in enumerate([landmark[0], landmark[11], landmark[12], landmark[13], landmark[14], landmark[15],
                                            landmark[16], landmark[23], landmark[24], landmark[25],
                                            landmark[26], landmark[27], landmark[28]]):
            x = int(mark.x * screen_w)
            y = int(mark.y * screen_h)
            try:
                old_x, old_y = body_coords[id][0], body_coords[id][1]
            except:
                body_coords.append([x, y])
            cv2.circle(image, (int(mark.x * frame_w), int(mark.y * frame_h)), 3, (0, 255, 0))
            diff = abs(x - old_x) + abs(y - old_y)
            if diff > 10 and old_x != 0:
                print('DEAD')
                winsound.Beep(440, 250)
            body_coords[id][0], body_coords[id][1] = x, y


        cv2.imshow('Squid Game', cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()