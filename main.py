import cv2
import time
from threading import Thread
import glob
import os
from emailing import send_email

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0
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

    #Add square around movement
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue

        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
        #if motion detected, show 1 on list
        if rectangle.any():
            status = 1

            #When object is in frame, save the frame as an image
            #Counter works to identify the different images
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1

            #List of images where object in frame
            all_pics = glob.glob("images/*.png")

            #retrieve the middle image from the file
            index = int(len(all_pics)/2)
            image_w_object = all_pics[index]

            #Get last two from status_list
    status_list.append(status)
    status_list = status_list[-2:]

    #object detected and left the camera frame
    if status_list[0] == 1 and status_list[1] == 0:
        #allows email to send in the bacjgrouns
        email_thread = Thread(target=send_email, args=(image_w_object, ))
        email_thread.daemon = True

        #Clean folder in the background
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        #start email thread
        email_thread.start()

    cv2.imshow("video",frame)
    key = cv2.waitKey(1)

    # if user clicks 'q', webcam closes/ends
    if key == ord('q'):
        break


video.release()
#Start clean stread
clean_thread.start()




