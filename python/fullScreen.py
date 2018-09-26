import cv2
import numpy as np

file_name = "/Users/kiriti/Downloads/test2.mp4"
window_name = "Live"
interframe_wait_ms = 3
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

cap = cv2.VideoCapture(file_name)
if not cap.isOpened():
    print "Error: Could not open video."
    exit()

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while (True):
    ret, frame = cap.read()
    if not ret:
        print "Reached end of video, exiting."
        break

    cv2.putText(frame,'Kiriti Gowda', 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)
    cv2.imshow(window_name, frame)
    if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
        print "Exit requested."
        break

cap.release()
cv2.destroyAllWindows()
