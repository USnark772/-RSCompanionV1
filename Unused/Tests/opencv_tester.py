import cv2

index = 0
cams = []
while True:
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if cap is None or not cap.isOpened():
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
for a in cams:
    a.release()
cv2.destroyAllWindows()
