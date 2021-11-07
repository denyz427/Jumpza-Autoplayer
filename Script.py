import pyautogui as pyg
import cv2
import numpy as np
import time
import win32api

time.sleep(5)
PrevMasktot = []
thetot = [[1,1],[1,1]]
while True:
    #Screenshot1
    timeDiv = time.time()
    sct_img1 = pyg.screenshot(region=(640, 344, 640, 735))   
    sct_img = cv2.resize(np.array(sct_img1),(160,147))
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_RGB2HSV)
    masknorm = cv2.inRange(sct_img, (35,175,111), (43,255,167))
    masktram = cv2.inRange(sct_img, (86,142,146), (92,255,172))
    masksups = cv2.inRange(sct_img, (18,227,237), (20,255,255))
    masktot = masknorm+masktram+masksups
                
    cntstot = cv2.findContours(masktot.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    thetot = []
    
    if len(cntstot) > 0:
        for cnt in cntstot:         
            if cv2.contourArea(cnt) > 16:
                thetot.append((cv2.minEnclosingCircle(cnt)[0][0]*4+640,cv2.minEnclosingCircle(cnt)[0][1]*5+344))
                
    if (len(thetot)<2):
        continue
        
    maskplayer = cv2.inRange(sct_img,(149,245,245),(151,255,255))
    cntstotplayer = cv2.findContours(maskplayer.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cntstotplayer)>0:
        for c in cntstotplayer:
            if cv2.contourArea(c)>50:
                yp1 = int(cv2.minEnclosingCircle(c)[0][1]*5)+344
                break
    
    #Screenshot2
    SecondSStime = time.time()
    sct_img1 = pyg.screenshot(region=(640, 344, 640, 735)) 
    timeDiv = SecondSStime-timeDiv
      
    sct_img = cv2.resize(np.array(sct_img1),(160,147))
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_RGB2HSV)
    masknorm = cv2.inRange(sct_img, (35,175,111), (43,255,167))
    masktram = cv2.inRange(sct_img, (86,142,146), (92,255,172))
    masksups = cv2.inRange(sct_img, (18,227,237), (20,255,255))
    masktot = masknorm+masktram+masksups
    
    cntstot = cv2.findContours(masktot.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    thetot2 = []
                    
    if len(cntstot) > 0:
        for cnt in cntstot:      
            if cv2.contourArea(cnt) > 16:
                thetot2.append((cv2.minEnclosingCircle(cnt)[0][0]*4+640,cv2.minEnclosingCircle(cnt)[0][1]*5+344))
                
    if (len(thetot2)<2):
        win32api.SetCursorPos((int(thetot[1][0]),int(thetot[1][1])))
        continue
        
    maskplayer = cv2.inRange(sct_img,(149,245,245),(151,255,255))
    cntstotplayer = cv2.findContours(maskplayer.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cntstotplayer)>0:
        for c in cntstotplayer:
            if cv2.contourArea(c)>50:
                yp = int(cv2.minEnclosingCircle(c)[0][1]*5)+344
                break
        
    if yp1<=yp and yp+84<thetot[1][1] and yp+257>thetot[1][1]:
        if(thetot[1][1]==thetot2[1][1]):
            dt=(((time.time()-SecondSStime)/timeDiv)+0.5)
            difX1=thetot2[1][0]+(thetot2[1][0]-thetot[1][0])*dt
            if(difX1<709):
                difX1=1418-difX1
            elif(difX1>1203):
                difX1=2406-difX1
            thetot[1]=(difX1,thetot[1][1])
        
        win32api.SetCursorPos((int(thetot[1][0]),int(thetot[1][1])))
    else:
        if(thetot[0][1]==thetot2[0][1]):
            dt=(((time.time()-SecondSStime)/timeDiv)+0.5)
            difX0=thetot2[0][0]+(thetot2[0][0]-thetot[0][0])*dt
            if(difX0<709):
                difX0=1418-difX0
            elif (difX0>1207):
                difX0=2414-difX0
            thetot[0]=(difX0,thetot[0][1])
        
        win32api.SetCursorPos((int(thetot[0][0]),int(thetot[0][1])))
