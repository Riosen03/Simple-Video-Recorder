import numpy as np
import cv2 as cv

video = cv.VideoCapture('rtsp://210.99.70.120:1935/live/cctv001.stream')
if video.isOpened():
    while True:
        valid, img = video.read()
        if not valid:
            break
        cv.imshow('Video Player', img)
        key = cv.waitKey(1)
        if key == 27: # ESC
            break
    cv.destroyAllWindows()