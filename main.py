import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4 , 720)
detector = HandDetector(detectionCon=0.8)

class MCQ():
    def __init__(self , data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs):
        for x , bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns = x+1
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),cv2.FILLED)


#importing the CSV file:
pathCSV = 'mcqs2.csv'
with open(pathCSV,newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# creating objects
mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))

print(len(mcqList))

qNo = 0
qTotal = len(dataAll)
print(dataAll)
print(len(dataAll ))
while True:
    success , img = cap.read()
    img = cv2.flip(img , 1)
    hands, img = detector.findHands(img , flipType=False)

    mcq = mcqList[1]
    img, bbox = cvzone.putTextRect(img,mcq.question,[100,100],2,2 , offset=50, border=5)
    img, bbox1 = cvzone.putTextRect(img,mcq.choice1,[100,250],2,2 , offset=50, border=5)
    img, bbox2 = cvzone.putTextRect(img,mcq.choice2,[400,250],2,2 , offset=50, border=5)
    img, bbox3 = cvzone.putTextRect(img,mcq.choice3,[100,400],2,2 , offset=50, border=5)
    img, bbox4 = cvzone.putTextRect(img,mcq.choice4,[400,400],2,2 , offset=50, border=5)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        # print(length)

        if length<60:
            print("Clicked")
            mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
            print(mcq.userAns)
            if mcq.userAns is not None:
                time.sleep(0.3)
                qNo += 1

    barvalue=150 + (950//qTotal)*qNo
    cv2.rectangle(img,(150,600),(barvalue, 650),(0,255,0), cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100, 650),(255,0,255), 5)


    cv2.imshow("Img" , img)
    cv2.waitKey(1)