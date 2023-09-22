import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

while True:
    check, frame = video.read()
    #Change frame to gray
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #blurness
    gray_frame_gua = cv2.GaussianBlur(gray_frame, (21,21), 0)

    #Get first frame, store it to compare frames
    if first_frame is None:
        first_frame = gray_frame_gua

    #Compare first frame with most recent frame (_gua)
    delta_frame = cv2.absdiff(first_frame, gray_frame_gua)

    thresh_frame = cv2.threshold(delta_frame, 80, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("my video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0))

    cv2.imshow("video",frame)

    key = cv2.waitKey(1)

    # if user clicks 'q', webcam closes/ends
    if key == ord('q'):
        break


video.release()



