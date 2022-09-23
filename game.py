import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pygame


pygame.mixer.init()

cap = cv2.VideoCapture(0)
cap.set(3, 1366)
cap.set(4, 768)


# Importing all images
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

#Resizing Background and gameOver pictures according to camera's resolution
imgBackground = cv2.resize(imgBackground, (640, 480))
imgGameOver = cv2.resize(imgGameOver, (640, 480))

#Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

#Variables
ballPos = [100, 100]
speedX = 10
speedY = 10                     #Y-axis is inverted here -> down(more) and up(less)
score = [0, 0]
gameOver = False

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)#0->vertical flip && 1->horizontal flip
    imgRaw = img.copy()

    '''print(img.shape[1])=640-->These 2 lines show print your webcam's resolution
    print(img.shape[0])=480'''

    #Find the hands
    hands, img = detector.findHands(img, flipType=False) #draw=False to avoid draw

    #Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    #Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 10, 250)

            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (25, y1))
                if 25 < ballPos[0] < 25+w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] += 10
                    score[0] += 1
                    pygame.mixer.music.load('Hit.wav')
                    pygame.mixer.music.play()
            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (590, y1))
                if 590 - 50 < ballPos[0] < 590-30 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] -= 10
                    score[1] += 1
                    pygame.mixer.music.load('Hit.wav')
                    pygame.mixer.music.play()
    #Check if game is over
    if ballPos[0] <= 5 or ballPos[0] >= 590:
        gameOver = True
        pygame.mixer.music.load('Game Over.wav')
        pygame.mixer.music.play(0)
        ballPos[0] = 100                #done to prevent music from playing infinite times
    if gameOver:
        img = imgGameOver  #zfill(2) puts 0 before score if score <10
        cv2.putText(img, str(score[0]+score[1]).zfill(2), (279, 240), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 5)
    else:
        #Move the ball
        if ballPos[1] >= 320 or ballPos[1] <= 10:
            speedY = -speedY
        ballPos[0] += speedX
        ballPos[1] += speedY

        #Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        #Putting score
        cv2.putText(img, str(score[0]), (80, 450), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (500, 450), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    # img[300:420, 20:233] = cv2.resize(imgRaw, (213, 120)) ->uncomment if you want see what cam is recording

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    #Restart's Code
    if key == ord('r'):
        ballPos = [100, 100]
        speedX = 10
        speedY = 10
        score = [0, 0]
        gameOver = False
        imgGameOver = cv2.imread("Resources/gameOver.png")
        imgGameOver = cv2.resize(imgGameOver, (640, 480))
    elif key == ord('q'):
        exit()


   