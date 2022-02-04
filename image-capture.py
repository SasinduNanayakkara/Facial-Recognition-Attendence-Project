import cv2
import numpy as np

video = cv2.VideoCapture(0)

while True:
    success, image = video.read()
    image = np.fliplr(image)
    cv2.imshow("image", image)

    cv2.imwrite("name.png", image)

    cv2.waitKey(0)


video.release()
cv2.destroyAllWindows()