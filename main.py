import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check, frame = video.read()
    #Change frame to gray
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #blurness
    gray_frame_gua = cv2.GaussianBlur(gray_frame, (21,21), 0)
    cv2.imshow("my video", gray_frame)

    key = cv2.waitKey(1)

    # if user clicks 'q', webcam closes/ends
    if key == ord('q'):
        break


video.release()



