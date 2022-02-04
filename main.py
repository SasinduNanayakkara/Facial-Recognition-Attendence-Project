from tkinter import *
import cv2
import numpy as np
import os
import time
from datetime import datetime

window = Tk()
window.title("Facial Recognition attendance")
window.minsize(width=1000, height=700)

def capture_image():
    video = cv2.VideoCapture(0)


    while True:
        time.sleep(3)
        success, image = video.read()
        image = np.fliplr(image)
        cv2.imshow("image", image)
        cv2.imwrite(f"student-images/{inputText.get(1.0,'end-1c')}.png", image)

        cv2.waitKey(0)

def printInput():
    input = inputText.get(1.0, "end-1c")
    lbl.config(text= "name: " + input)


inputText = Text(window, height=5, width=20)
inputText.pack()

printButton = Button(window, text="Print", command=printInput)
printButton.pack()
button = Button(text="capture image", command=capture_image)
button.pack()

lbl = Label(window, text="")
lbl.pack()

window.mainloop()