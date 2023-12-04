import cv2
import time
from mail import send_mail
import glob
import os
from threading import Thread

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
    # Starts capturing
    check, frame = video.read()

    # Since we are calculating the difference greyscale is enough
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # To avoid precision Noise we are blurring
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    # Setting a fixed frame to compare
    if first_frame is None:
        first_frame = grey_frame_gau

    # Filtering the difference and refining it
    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # after processing we are getting a border around the change
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # measuring the contour marked and removing false alarms by removing small objects
    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        # getting coordinates and drawing a rectangle
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            pic_to_sent = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        mail_thread = Thread(target=send_mail, args=(pic_to_sent,))
        mail_thread.daemon = True

        mail_thread.start()

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True



    cv2.imshow('My Video', frame)


    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
clean_folder()
