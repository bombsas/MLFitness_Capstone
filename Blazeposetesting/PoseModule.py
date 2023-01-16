import time

import cv2
import mediapipe as mp
import sys
import numpy as np
import matplotlib.pyplot as plt
#this is just the class to find and create the pose
class poseDetector():

    def __init__(self, mode=False,modcomp = 2, smooth=True,segmen=True, smoothseg=True,
                 detectionCon=0.7, trackCon=0.7):

        self.mode = mode
        self.modcomp = modcomp
        self.smooth = smooth
        self.segmen = segmen
        self.smoothseg = smoothseg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils #this is for drawing everything
        self.mpPose = mp.solutions.pose # this is for a model
        self.pose = self.mpPose.Pose(self.mode, self.modcomp, self.smooth, self.segmen, self.smoothseg,  self.detectionCon, self.trackCon) #this is for determining pose of person

    #this function tries to find a pose and draws it out
    #a pose is just the human body using lines and dots
    #dots are landmarks
    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #attempting to draw segmentation on image.
        annotated_img = img.copy()
        # this is the condition on making it either grey or not
        condition = np.stack((self.results.segmentation_mask,) * 3, axis =-1)> 0.1
        bg_img = np.zeros(img.shape, dtype = np.uint8)
        bg_img[:] = (192,192,192)
        annotated_img = np.where(condition,annotated_img, bg_img)
        #print(results.pose_landmarks) print all landmarks aka points every frame

        if self.results.pose_landmarks:
            if draw:
                #landmarks are for the dots on the body there are 32 dots and self.mpPose.POSE_CONNECTIONS connects the dots
                self.mpDraw.draw_landmarks(annotated_img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS) 
                #self.mpDraw.plot_landmarks(self.results.pose_world_landmarks,self.mpPose.POSE_CONNECTIONS)
        return annotated_img

    #this will be used to get each position of each landmark and label them
    def findPosition(self,img, draw=True):
        lmList =[] #landmark list
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape # we need this because
                #print(id, lm)
                cx, cy, cc = int(lm.x * w), int(lm.y * h), int(lm.z) #this gives the pixel point of the landmarks
                lmList.append([id,cx,cy,cc])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
                    #cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        return lmList
    
    def threeDimendionalplot(self,img):
        ax = plt.axes(projection = "3d")
        ax.scatter(3,5,7)
        plt.pause(0.001)
        return plt
    
    def findWorldPosition(self,img, draw=True):
        lmList =[] #landmark list
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_world_landmarks.landmark):
                h, w, c = img.shape # we need this because
                #print(id, lm)
                cx, cy, cc = int(lm.x * w), int(lm.y * h), int(lm.z) #this gives the pixel point of the landmarks
                lmList.append([id,cx,cy,cc])
                #if found checks if can draw it if can draw
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)#this will over lay on points if seeing properly it would be blue
                    #cv2.putText(img,str(id),(cx,cy),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        return lmList

def main():
    #comment only one line out videocapture of 0 is webcam videocapture than file is for vid
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(sys.path[0]+'/motioncapture/SquatV1side.mp4')  # the video sys.path[0] is the current path of the file
    pTime = 0
    detector = poseDetector()
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    data = np.empty((3,32,length))
    frame_num = 0
    success = True
    
    while success:
        #this sees if it can read the frame that it is given
        success, img = cap.read()
        constant_height = 500
        # img.shape is a list of the dimensions of the frame 0 = height
        # 1 = width, 2 = number of chnnels for image
        height = img.shape[0]
        width = img.shape[1]
        height_percentage = float(constant_height/int(height))
        modded_width = int(float(width)*height_percentage)
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        world_lmList = detector.findWorldPosition(img)
        for i in range(len(lmList)):
            if lmList[i][0] == 12:
                x1 = int(lmList[i][1])
                y1 = int(lmList[i][2])
                pt1 = (x1,y1)
            elif lmList[i][0] == 24:
                x2 = int(lmList[i][1])
                y2 = int(lmList[i][2])
                pt2 = (x2 ,y2)
        cv2.line(img,pt1,pt2,(139,0,0),2)
        slope = ((y2-y1)*(x2-x1))
        y_inter = (y1-(slope*x1)) 
        print(f"slope: {slope}, y_inter: {y_inter}, x1: {x1}, y1: {y1}, x2: {x2}, y2: {y2}")
        #prints list of landmarks from 1 to 32 look at mediapipe diagram to know what landmark is which bodypart
        #print(lmList)
        #the landmarks i want for side are 12 and 24 to get line and slope
        #plotting= detector.threeDimendionalplot(img)
        #print(world_lmList)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        #resize is width than height
        resize = cv2.resize(img, (modded_width, constant_height))
        cv2.imshow("Image", resize)
        cv2.waitKey(1)  # millisecond delays
    return

if __name__ == "__main__":
    main()