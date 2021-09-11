import cv2
import mediapipe as mp
from os import system

cls = lambda: system('cls')
# def cls():
#     print ('\n' * 5)
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
with mp_face_detection.FaceDetection(
    min_detection_confidence=0.959595) as face_detection:

    with mp_face_mesh.FaceMesh(
        min_detection_confidence=0.959595,
        min_tracking_confidence=0.01) as face_mesh:
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = face_mesh.process(image)
        results1 = face_detection.process(image)
        if results1.detections and switch != 1:
            print("You're too close to the display")
            switch = 1
            cls()
        else:
            switch = 0



        # Draw the face mesh annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
          for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec)
        if results1.detections:
            for detection in results1.detections:
                mp_drawing.draw_detection(image, detection)
        cv2.imshow('MediaPipe FaceMesh', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
cap.release()

