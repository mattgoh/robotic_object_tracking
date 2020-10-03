import numpy as np
import cv2
import TrainingClass as train
import serial

ser = serial.Serial("/dev/ttyACM0",baudrate=9600,timeout=1.0)
#if ser.isOpen():
#    ser.close()
ser.close()
ser.open()
#ser.isOpen()

cap = cv2.VideoCapture(0)
# Reduce the size of video to 320x240 so rpi can process faster
cap.set(3,240)
cap.set(4,240)
# construct the argument parse and parse the arguments
t = train.training()
t.parseConfig()
classData = ['background']*5;
i = 5
while(True):
    if i == 5:
        i = 0
    # Capture frame-by-frame
    __, frame = cap.read()

    #compute the ratio of the old height
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    frame2, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]
    screenCnt = None
    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if our approximated contour has four points, then
    # we can assume that we have found our screen
   
    if(len(cnts) !=0):
        print (len(cnts))
        area = cv2.contourArea(cnts[0])
        print(area)
        mask = np.zeros(frame.shape[:2], dtype = "uint8")
        #cv2.drawContours(mask, cnts, -1, 255, -1)
        #cv2.rectangle(mask,(self.nw_col, self.nw_row),(self.se_col, self.se_row),255,-1)
        #mask = cv2.erode(mask, None, iterations = 2)
        if (area>=2000):
            cv2.drawContours(mask, cnts, -1, 255, -1)
            mask = cv2.erode(mask, None, iterations = 2)

            #t.classifyMean(mean)
            # compute the center of the contour
            M = cv2.moments(cnts[0])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
         
            # draw the contour and center of the shape on the image
            cv2.circle(frame, (cX, cY), 7, (0, 255, 0), -1)
            cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.rectangle(mask,(0, 0),(80, 240), 255,-1)
            mask = cv2.erode(mask, None, iterations = 2)
            mean = cv2.mean(frame, mask = mask)[:3]
            #t.classifyMean(mean)
            # print("background")
        mask = cv2.erode(mask, None, iterations = 2)
        mean = cv2.mean(frame, mask = mask)[:3]
        objClass = t.classifyMean(mean)
        classData[i] = objClass
        i = i+1

        classofInterest = max(set(classData), key = classData.count)
        if classofInterest == 'background':
            outputClass = 0
        elif classofInterest == 'line':
            outputClass = 1
        elif classofInterest == 'avoid':
            outputClass = 2
        elif classofInterest == 'goal':        
            outputClass = 3
        ser.write(str(outputClass).encode())
        #print(outputClass)
        print(classofInterest)
    #print area

    # mean = cv2.mean(frame, mask = mask)[:3]

    cv2.imshow('cnt',frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
