import cv2
 
capture = cv2.VideoCapture('C:/Users/P-Cateli-01/Documents/RaspyProject/20221003/180257.avi')
frameNr = 0
 
while (True):
    success, frame = capture.read()
    if success:
        cv2.imwrite(f'C:/Users/P-Cateli-01/Documents/RaspyProject/frame_{frameNr}.jpg', frame)
 
    else:
        break
    frameNr = frameNr+1
 
capture.release()