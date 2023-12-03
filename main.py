import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

while True:
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
        if cv2.contourArea(contour) < 10000:
            continue
        # getting coordinates and drawing a rectangle
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow('My Video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
