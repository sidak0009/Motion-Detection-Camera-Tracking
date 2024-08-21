import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret1, frame1 = cap.read()

left, center, right = False, False, False
x = 300

mask = np.zeros((200, 400))

while True:

    ret2, frame2 = cap.read()
    g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(g1, g2)

    ret3, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    contr, ret4 = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contr)>0:
        largest_contr = max(contr, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contr)
        cv2.rectangle(frame1, (x, y), (x+w, y+h),(0, 255, 0), 2)

    if not(left) and not(right):
        if x < 100:
            left = True

        elif x > 500:
            right = True
    elif left:
        if x > 100 and x < 500 and not(center):
            center = True
        if x > 500:
            if center:
                mask = np.zeros((200, 400))
                cv2.putText(mask,"to right",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255),3)

                print("motion towards right  taken place")
                center=False
                left=False
            else:
                right=True
                left=False

    elif right:
        if x>100 and x<500 and not(center):
            center=True
        if x<100:
            if center:
                mask = np.zeros((200, 400))
                cv2.putText(mask,"to left",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255),3)
                print("motion towards left taken place")
                center=False
                right=False
            else:
                left=True
                right=False

    cv2.imshow('frame', frame1)
    cv2.imshow('f',thresh)
    cv2.imshow("mask",mask)

    ret1, frame1 = cap.read()

    if cv2.waitKey(1) == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
