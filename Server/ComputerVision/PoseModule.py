import cv2
import mediapipe as mp
import numpy as np
import binomialFitting.KeyframeExtraction as KeyframeExtraction
import mp_drawing_modified
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = ["ComputerVisionTest/images/pushup.jpg"]
BG_COLOR = (192, 192, 192) # gray
with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
      continue
    print(
        f'Nose coordinates: ('
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].z})'
    )

    print(results.pose_world_landmarks.landmark[11])
    print(KeyframeExtraction.getAngle(results, 14, "x"))
    
    annotated_image = image.copy()
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    annotated_image = np.where(condition, annotated_image, bg_image)
    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
    # Plot pose world landmarks.
    # mp_drawing.plot_landmarks(
    #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# For webcam input:
cap = cv2.VideoCapture("ComputerVisionTest/videos/Pushupangleview.mp4")
allFrames = []
with mp_pose.Pose(
    min_detection_confidence=0.1,
    min_tracking_confidence=0.1) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      break

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    allFrames.append(results)
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 2))
    if cv2.waitKey(5) & 0xFF == 27:
      break

fps = cap.get(cv2.CAP_PROP_FPS)
cap.release()
print(f"frames: {len(allFrames)}")
print(f"framerate: {fps}")

rSquared = 0.5

print(f"RSquared: {rSquared}")
extracted = KeyframeExtraction.extractFrames(allFrames, rSquared)
print(f"{len(extracted)} frames extracted")
print(extracted)

n = input("Frame to display: ")
while n != "no":
  
  n = int(n)-1
  mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
  n = input("Frame to display: ")