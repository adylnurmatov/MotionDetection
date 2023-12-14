import imutils  # we use imutils to manipulation of the frame
import cv2  # we use open cv to computer vision
import threading  # we use threading because we need multiple threads
import winsound  # winsound one of the signal methods

# cap = capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# there we set size of our frame
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# there we resize first frame
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

# this variable indicate is an alarm active
alarm = False
alarm_mode = False
# if counter > 0 we use winsound
alarm_counter = 0

# this function triggers a signal


def beep_alarm():
    global alarm
    for i in range(5):
        if not alarm_mode:
            break
        print("beep")
        winsound.Beep(2500, 1000)
    alarm = False


# in this block of code we start our program
while True:
    # read is means start reading data from the camera
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)
    # if alarm mode is true we convert our frame to gray and gaussian blur
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)
        # there we count difference
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        # if our sum of threshold > 10000 counter raise
        if threshold.sum() > 100000:
            alarm_counter += 1

        else:
            if alarm_counter > 0:
                alarm_counter -= 1
        # threshold means this white colors when we start use our program
        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)
    # if difference enough we start use our method beep_alarm
    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()
    # if key == t we stop and if key q we break our program
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break
cap.release()
cv2.destroyAllWindows()
