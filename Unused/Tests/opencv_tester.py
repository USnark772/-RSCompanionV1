import cv2
from traceback import print_stack


index = 0
cams = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        cams.append(cap)
    index += 1

while True:
    # Capture frame-by-frame
    for b in range(len(cams)):
        ret, frame = cams[b].read()
        cv2.imshow('Camera ' + str(b), frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
