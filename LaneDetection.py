##Lane Detection File
##By Luke Aldred - Started 05/06/2020
##GitHub: You do not have permission to download, edit, redistribute or pull from my code and this file.

import cv2
import numpy as np
import matplotlib.pyplot as plt #Imports the modules needed for the project

def RegionOfInterest(Image): #sets the area of the screen that the system needs to process (reduces time for result as the whole image does not need to be processed) 
    Mask = np.zeros_like(Image) #fills the image with a black screen
    Vertices = [np.array([(0,700),(0,650),(200,400),(350,400),
                         (600,500),(600,700)])] #the coordinates for the ROI
    cv2.fillPoly(Mask, Vertices, 255)
    MaskedImage = cv2.bitwise_and(Image, Mask) #combines the black screen with the original image in the area specified in the Vertices list
    return MaskedImage #returns the combined image

def DrawRoadLines(Image, ImageLines):
    #Right lane = highest x and highest y in RightLane, smallest x and smallest y in RightLane
    #Left Lane = smallest x and highest y in LeftLane, highest x and smallest y
    BlankImage = np.zeros_like(Image)
    try:
        Right = []
        Left = []
        for Line in ImageLines:
            x1, y1, x2, y2 = Line[0]
            if (x2-x1) / (y2-y1) < 0: #if the gradient is negative, then the line would be pointing to the left (on the right side of the road)
                Right.append((x1, y1, x2, y2))
            else: #if the gradient is positive, then the line would be pointing right (on the left side of the road)
                Left.append((x1, y1, x2, y2))
        
        Right.sort() #sorts the lists from largest to smallest
        Left.sort()
        FinalRightCoord1 = (Right[0][0], Right[0][1])
        FinalRightCoord2 = (Right[len(Right)-1][2], Right[len(Right)-1][3])
        FinalLeftCoord1 = (Left[0][0], Left[0][1])
        FinalLeftCoord2 = (Left[len(Left)-1][2], Left[len(Left)-1][3])
        cv2.line(BlankImage, FinalRightCoord1, FinalRightCoord2, (0,255,0), 3) #draws a line between the smallest and largest x,y coordinates 
        cv2.line(BlankImage, FinalLeftCoord1, FinalLeftCoord2, (0,255,0), 3)
        #Gradient = delta x / delta y ((x2 - x1) / (y2 - y1))
        RightGradient = (FinalRightCoord2[0] - FinalRightCoord1[0]) / (FinalRightCoord2[1] - FinalRightCoord1[1])
        LeftGradient = (FinalLeftCoord2[0] - FinalLeftCoord1[0]) / (FinalLeftCoord2[1] - FinalLeftCoord1[1])
        if (RightGradient < 0) and (LeftGradient < 0): #steering module
            DirectionText = "Left"
        elif (RightGradient > 0) and (LeftGradient > 0):
            DirectionText = "Right"
        elif (RightGradient < 0) and (LeftGradient > 0):
            DirectionText = "Forward"
        cv2.putText(BlankImage, DirectionText, (0,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 5) #places the text onto the image

        LaneCoordinates = np.array([(0,700), FinalRightCoord1, FinalRightCoord2, FinalLeftCoord1, FinalLeftCoord2, (600,700)], dtype=np.int32)
        cv2.fillConvexPoly(BlankImage, LaneCoordinates, (0,0,255)) #draws the road area onto the image
    except:
        pass
    return BlankImage
    
Image = cv2.imread("Road.jpg") #loads in the image
Image = cv2.resize(Image, (600,700)) #resizes the image
ImageCopy = np.copy(Image) #copies the image
GreyImage = cv2.cvtColor(ImageCopy, cv2.COLOR_BGR2GRAY) #converts the image to grey
CannyImage = cv2.Canny(GreyImage, 200, 500)
ImageROI = RegionOfInterest(CannyImage) 
ImageLines = cv2.HoughLinesP(ImageROI, 2, np.pi/180, 100, np.array([]), 100, 55) #90,10
ImageWithLines = DrawRoadLines(ImageCopy, ImageLines)
OutputImage = cv2.addWeighted(ImageCopy, 0.8, ImageWithLines, 1, 1) #combines the image
cv2.imshow("Road", OutputImage) #outputs the image
