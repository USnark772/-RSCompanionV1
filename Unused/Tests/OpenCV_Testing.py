import cv2
print(cv2.getVersionString())
cap = cv2.VideoCapture('C:/Users/phill/Desktop/Cari BFaN ballets/Aladdin video.mp4')
cap2 = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    if not ret and not ret2:
        break
    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('frame2', frame2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
