from tkinter import *
import cv2
import face_recognition
import numpy as np
import os
import time
from datetime import date
from datetime import datetime

today = date.today()

window = Tk()
window.title("Facial Recognition attendance")
window.minsize(width=1000, height=700)

def openNewWindow():
    newWindow = Toplevel(window)
    newWindow.title("new student registration")
    newWindow.geometry("300x300")

    def capture_image():
        video = cv2.VideoCapture(0)

        while True:
            success, image = video.read()
            image = np.fliplr(image)
            cv2.imshow("image", image)
            cv2.imwrite(f"student-images/{inputName.get(1.0, 'end-1c')}-{inputID.get(1.0, 'end-1c')}.png", image)
            video.release()
            cv2.waitKey(0)

    def printInput():
        input_name = inputName.get(1.0, "end-1c")
        lblName.config(text="name: " + input_name)

        input_id = inputID.get(1.0, "end-1c")
        lblID.config(text="ID number: " + input_id)

    nameLabel = Label(newWindow, text="Name")
    nameLabel.pack()

    inputName = Text(newWindow, height=1, width=20)
    inputName.pack()

    IDLabel = Label(newWindow, text="ID Number")
    IDLabel.pack()

    inputID = Text(newWindow, height=1, width=20)
    inputID.pack()

    printButton = Button(newWindow, text="Print", command=printInput)
    printButton.pack()


    lblName = Label(newWindow, text="")
    lblName.pack()

    lblID = Label(newWindow, text="")
    lblID.pack()

    button = Button(newWindow, text="capture image", command=capture_image)
    button.pack()


def attendanceFunction():
    path = "student-images"
    images = []
    classNames = []
    myList = os.listdir(path)

    for cl in myList:
        currentImg = cv2.imread(f"{path}/{cl}")
        images.append(currentImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            encode = face_recognition.face_encodings(img)[0]
            encodList.append(encode)
        return encodList

    def markAttendence(name):
        with open(f"attendance-{today}.csv", "r+") as file:
            myDataList = file.readlines()
            nameList = []

            for line in myDataList:
                entry = line.split(",")
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime("%H:%M:%S")
                file.writelines(f"\n{name},{dtString}")

    encodeListKnown = findEncodings(images)
    print("Encoding complete")

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_RGB2BGR)

        facesCurrentFrame = face_recognition.face_locations(imgS)
        encodingCurrentFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

        for encodeFce, faceLoc in zip(encodingCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFce)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFce)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.rectangle(img, (x1,y2 - 35), (x2,y2), (0,255,0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                markAttendence(name)

        cv2.imshow("webcam", img)
        cv2.waitKey(1)


newStudentBtn = Button(text="Register new student", command=openNewWindow)
newStudentBtn.pack()

attenceButton = Button(text="Mark the attendance", command=attendanceFunction)
attenceButton.pack()


window.mainloop()