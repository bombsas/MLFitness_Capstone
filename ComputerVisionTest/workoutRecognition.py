'''
#Idea 1 (using standard deviation as threshhold)
#Algorithm on detecting/learning workouts (manual approach)

    #feed tracking data,
        
        #find angle cicles (the hard part)

            #for each joint, find changes in increase or decrease of angle
                - get first frame

                - compare with second frame to label as increase/decrease
                
                - keep comparing until the label is wrong
                
                - get frame, change label and repeat

            #save type of repetition in a list
                #repetitions with the same joint changes together

            get the closest sets with the number of repetitions and include the rest (hopefully all, maybe a different approach is more obvious)
            match with other sets with simmilar angles and maybe height coordinates(assuming straightup camera)
            compare with existing model if one exists

            return successfull repetitions that match the number given.

    Train model

        model is stored with average angles, standard deviation for each angle, and the number of repetitions used to train it.

        each repetition recorded are used to update the average angles and the standard deviation. (this is why we store the number of reps used)

    Correct reps should have their angles fall in the thresh hold of the standard deviarion, while incorrect ones  
            
    


'''
import cv2
import mediapipe as mp
import numpy as np
import math
import statistics
import os
import binomialFitting.KeyframeExtraction as KeyframeExtraction
import mp_drawing_modified
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

MENU = "Select the joints that cycle separated by commas \n\
    Ex. for push ups: 4,5\n\n\
1   neck\n\
2   right shoulder\n\
3   left shoulder\n\
4   right elbow\n\
5   left elbow\n\
6   right wrist\n\
7   left wrist\n\
8   right hip\n\
9   left hip\n\
10  right knee\n\
11  left knee\n\
12  right foot\n\
13  right foot"

choiceList = {
    "1":    [0,1],
    "2":    [2,3],
    "3":    [4,5],
    "4":    [6,7],
    "5":    [8,9],
    "6":    [10],
    "7":    [11],
    "8":    [16],
    "9":    [17],
    "10":   [18,19,20],
    "11":   [21,22,23],
    "12":   [24,25],
    "13":   [26,27]
}

def getJoint(angle):
    a = int(angle)
    if a in range(10) or a == 12 or a == 13:
        return a//10 +1
    elif a == 10 or a == 11:
        return a - 4
    elif a == 16 or a == 17:
        return a - 8
    elif a == 18 or a == 19 or a == 20:
        return 10
    elif a == 21 or a == 22 or a == 23:
        return 11

def getKeyFramesFromVideo(video, show = False):
    cap = cv2.VideoCapture(video)
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
            if show:
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

    rSquared = 0.8

    print(f"RSquared: {rSquared}")
    extracted, allangles = KeyframeExtraction.extractFrames(allFrames, rSquared, True)
    print(f"{len(extracted)} frames extracted")
    return extracted, allangles

def getReps(keyFrames, allAngles, reps, workout = None):
    # if not workout:
    #     model, importantJoints = setupNewWorkout()
    nFrames = len(keyFrames)
    reptypes = [[] for i in range(nFrames)] 
    
    for curve in range(len(allAngles)):
        angle1, angle2, increase = None, None, None
        if getJoint(curve) in 
        for frame in range(nFrames): #TODO Only include important Joints

            angle2 = allAngles[curve][keyFrames[frame][1]] #all angles includes all Frames

            if(angle1 != 0 and not angle1): #if first angle
                angle1 = angle2
            else: #get direction change and angle difference
                #if last frame was a decrese and now it's increasing
                if (angle1 < angle2) and increase == False: #can be None
                    increase = True
                    reptypes[frame].append([angle2, curve, increase, angle2 - angle1])
                    angle1 = angle2

                #if last frame was an increase and now it's a decrease
                elif (angle1 > angle2) and increase:
                    increase = False
                    reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                    angle1 = angle2

                #if comparing with first frame
                elif (increase == None):
                    if angle1 < angle2:
                        increase = True
                        reptypes[frame].append([angle2, curve, increase, angle2 - angle1])
                        reptypes[0].append([angle1, curve, False, 0])
                        angle1 = angle2
                    
                    else:
                        increase = False
                        reptypes[frame].append([angle2, curve, increase, angle1 - angle2])
                        reptypes[0].append([angle1, curve, True, 0])
                        angle1 = angle2
                    
    #check important joint changes
    i = 1
    symetrical = []
    for change in reptypes:
        increase = 0
        decrease = 0
        max = 0
        maxFrom = 0
        for angle in change:
            #print(f"angle change on {angle}: {angle[3]}")
            if angle[2]:
                increase += 1
            else:
                decrease += 1
            if max < angle[3]:
                max = angle[3]
                maxFrom = angle[1]
        print(f"frame {i} with {len(change)} changes: {increase} increase and {decrease} decrease with a max angle change of {max} from {maxFrom}")

        i+=1

    return



def setupNewWorkout():
    models = os.listdir("/models")
    print(models)
    name = input("Name of new workout: ").strip()
    while (len(name) > 0) and (name + ".json") not in models:

        name = input("Model already exists or the name is invalid! \n\
Please provide a new name of new workout: ").strip()

    print(MENU)
    choices = input("Choice(s): ").split(",")

    return name, choices


print("Analyzing video...")
extracted, allAngles = getKeyFramesFromVideo("ComputerVisionTest/videos/Pushupangleview.mp4")

reps = getReps(extracted, allAngles, 4)
n = input("Frame to display: ")
while n != "no":
  
  n = int(n)-1
  mp_drawing_modified.plot_landmarks(extracted[n][0].pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
  n = input("Frame to display: ")