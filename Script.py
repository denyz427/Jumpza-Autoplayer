import pyautogui as pyg
import cv2
import numpy as np
import time
from timeit import default_timer as timer
import win32api

time.sleep(5)
PrevMasktot = []
thetot = [[1,1],[1,1]]
thetot2 = [[0,0],[0,0]]
lastY0=0
lastY1=0
lastSpeed0 = []
lastSpeed1 = []
lasttimeDiv=0

while True:
    #Screenshot1
    timeDiv = timer()
    sct_img1 = pyg.screenshot(region=(640, 279, 640, 800))   
    sct_img = cv2.resize(np.array(sct_img1),(160,160))
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_RGB2HSV)
    masknorm = cv2.inRange(sct_img, (35,175,111), (43,255,167))
    masktram = cv2.inRange(sct_img, (86,142,146), (92,255,172))
    masksups = cv2.inRange(sct_img, (18,227,237), (20,255,255))
    masktot = masknorm+masktram+masksups
                
    cntstot = cv2.findContours(masktot.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    thetot = []
    
    if len(cntstot) > 0:
        for cnt in cntstot:         
            if cv2.contourArea(cnt) > 7:
                if(len(thetot)!=1 or cv2.minEnclosingCircle(cnt)[0][1]*5+279!=thetot[0][1]):
                    thetot.append((cv2.minEnclosingCircle(cnt)[0][0]*4+640,cv2.minEnclosingCircle(cnt)[0][1]*5+279))

    if (len(thetot)==1):
        win32api.SetCursorPos((int(thetot[0][0]),int(thetot[0][1])))
        continue
    elif(len(thetot)==0):
        continue
        
    maskplayer = cv2.inRange(sct_img,(149,245,245),(151,255,255))
    cntstotplayer = cv2.findContours(maskplayer.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cntstotplayer)>0:
        for c in cntstotplayer:
            if cv2.contourArea(c)>50:
                yp = int(cv2.minEnclosingCircle(c)[0][1]*5)+279
                break
    
    if(thetot2[1][0]!=0):
        speed1=2.5*(thetot[1][0]-thetot2[1][0])/(timeDiv-lasttimeDiv)
        if(thetot[1][1]==lastY1):
            lastSpeed1.append(abs(speed1))
            if(speed1<0):
                speed1=-sum(lastSpeed1)/len(lastSpeed1)
            else:
                speed1=sum(lastSpeed1)/len(lastSpeed1)
        else:
            lastY1=thetot[1][1]
            lastSpeed1 = []
            lastSpeed1.append(abs(speed1))  
    else:
        speed1=0
        lastY1=thetot[1][1]
    
    if(thetot2[0][0]!=0):
        speed0=2.5*(thetot[0][0]-thetot2[0][0])/(timeDiv-lasttimeDiv) 
        if(thetot[0][1]==lastY0):
            lastSpeed0.append(abs(speed0))
            if(speed0<0):
                speed0=-sum(lastSpeed0)/len(lastSpeed0)
            else:
                speed0=sum(lastSpeed0)/len(lastSpeed0)
        else:
            lastY0=thetot[0][1]
            lastSpeed0 = []
            lastSpeed0.append(abs(speed0))
    else:
        speed0=0
        lastY0=thetot[0][1]
        
    lasttimeDiv = timeDiv
    thetot2[1]=thetot[1]
    thetot2[0]=thetot[0]
    
    #if yp1<=yp and yp+84<thetot[1][1] and yp+283>thetot[1][1]:
    if yp+84<thetot[1][1]:
        if(thetot[1][1]==thetot2[1][1]):   
            difX1=thetot2[1][0]+speed1*(timer()-timeDiv)*2
            while (difX1<706 or difX1>1206):
                if(difX1<706):
                    difX1=1412-difX1
                if(difX1>1206):
                    difX1=2412-difX1

            thetot[1]=(difX1,thetot[1][1])
        
        win32api.SetCursorPos((int(thetot[1][0]),int(thetot[1][1])))
    else:
        if(thetot[0][1]==thetot2[0][1]):
            difX0=thetot2[0][0]+speed0*(timer()-timeDiv)*2
            while (difX0<706 or difX0>1206):
                if(difX0<706):
                    difX0=1412-difX0
                if (difX0>1206):
                    difX0=2412-difX0
                    
            thetot[0]=(difX0,thetot[0][1])
        
        win32api.SetCursorPos((int(thetot[0][0]),int(thetot[0][1])))
