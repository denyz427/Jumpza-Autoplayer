import pyautogui as pyg
import cv2
import numpy as np
import time
import win32api

time.sleep(5)
yNow=0
PrevMasktot = []
thetot = [[1,1],[1,1]]
a=0
while True:
    #Screenshot1
    timeDiv = time.time()
    sct_img1 = pyg.screenshot()    
    sct_img1 = cv2.cvtColor(np.array(sct_img1), cv2.COLOR_RGB2BGR)
    sct_img = cv2.cvtColor(sct_img1, cv2.COLOR_BGR2HSV)
    masknorm = cv2.inRange(sct_img, (35,175,111), (43,255,167))
    masktram = cv2.inRange(sct_img, (86,142,146), (92,255,172))
    masksups = cv2.inRange(sct_img, (18,227,237), (20,255,255))
    masktot = masknorm+masktram+masksups
    
    if(np.array_equal(masktot, PrevMasktot, equal_nan=True) and yNow==thetot[1][1]):
        continue
    PrevMasktot=masktot
                
    cntstot = cv2.findContours(masktot.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    thetot = []
    
    if len(cntstot) > 0:
        for cnt in cntstot:         
            if cv2.contourArea(cnt) > 400:
                thetot.append((cv2.minEnclosingCircle(cnt)[0]))
    
    maskplayer = cv2.inRange(sct_img,(149,245,245),(151,255,255))
    cntstotplayer = cv2.findContours(maskplayer.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cntstotplayer)>0:
        for c in cntstotplayer:
            if cv2.contourArea(c)>400:
                yp1 = int(cv2.minEnclosingCircle(c)[0][1])
                break
    
    #Screenshot2
    SecondSStime = time.time()
    sct_img1 = pyg.screenshot() 
    timeDiv = SecondSStime-timeDiv
    
    sct_img1 = cv2.cvtColor(np.array(sct_img1), cv2.COLOR_RGB2BGR)
    sct_img = cv2.cvtColor(sct_img1, cv2.COLOR_BGR2HSV)
    masknorm = cv2.inRange(sct_img, (35,175,111), (43,255,167))
    masktram = cv2.inRange(sct_img, (86,142,146), (92,255,172))
    masksups = cv2.inRange(sct_img, (18,227,237), (20,255,255))
    masktot = masknorm+masktram+masksups
    
    cntstot = cv2.findContours(masktot.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    thetot2 = []
                    
    if len(cntstot) > 0:
        for cnt in cntstot:      
            if cv2.contourArea(cnt) > 400:
                thetot2.append((cv2.minEnclosingCircle(cnt)[0]))
    
    maskplayer = cv2.inRange(sct_img,(149,245,245),(151,255,255))
    cntstotplayer = cv2.findContours(maskplayer.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cntstotplayer)>0:
        for c in cntstotplayer:
            if cv2.contourArea(c)>400:
                yp = int(cv2.minEnclosingCircle(c)[0][1])
                break
                
    timeNow = time.time()-SecondSStime              
    if(thetot[0][1]==thetot2[0][1] and thetot[1][1]==thetot2[1][1]):
        difX0=thetot2[0][0]+(thetot2[0][0]-thetot[0][0])*timeNow/timeDiv
        difX1=thetot2[1][0]+(thetot2[1][0]-thetot[1][0])*timeNow/timeDiv

        if(difX0<709):
            difX0=1418-difX0
        elif (difX0>1207):
            difX0=2414-difX0

        if(difX1<709):
            difX1=1418-difX1
        elif(difX1>1203):
            difX1=2406-difX1

        thetot[0]=(difX0,thetot[0][1])
        thetot[1]=(difX1,thetot[1][1])
           
    #v0t + 1/2 2401 t^2            
    if(yp>yp1):
        deltaY=(yp-yp1)*((timeNow/timeDiv)+0.5)+1200.5*((timeNow+timeDiv/2)**2)
    else:
        deltaY=58
            
        #665-581 +58
    if yp+84+deltaY<thetot[1][1]:
        win32api.SetCursorPos((int(thetot[1][0]),int(thetot[1][1])))
        yNow=thetot[1][1]
    else:
        win32api.SetCursorPos((int(thetot[0][0]),int(thetot[0][1])))
        yNow=thetot[0][1]
