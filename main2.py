import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)

#importing the CSV file:
pathCSV = 'mcqs2.csv'
with open(pathCSV, newline='\n') as f:
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
print(len(dataAll))

start_time = time.time()
reset_button = (1100, 600, 1200, 650)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    mcq = mcqList[1]
    img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
    img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
    img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
    img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
    img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)
    cv2.rectangle(img, (reset_button[0], reset_button[1]), (reset_button[2], reset_button[3]), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "Reset", (reset_button[0] + 10, reset_button[1] + 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        length, info, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        print(length)

        if length < 60:
            print("Clicked")
            mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
            print(mcq.userAns)
            if reset_button[0] < cursor[0] < reset_button[2] and reset_button[1] < cursor[1] < reset_button[3]:
                print("Reset button clicked")
                start_time = time.time()  # reset the timer

    elapsed_time = time.time() - start_time
    remaining_time = int(60 - elapsed_time)
    if remaining_time <= 0:
        print("Time's up!")
        remaining_time = 0
    cv2.putText(img, f'Time left: {remaining_time}s', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
