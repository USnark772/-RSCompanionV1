import cv2
import time

# cap = cv2.VideoCapture(1)
# # tic = time.monotonic()
# # print(tic)
# # frames = 0
# # now = time.monotonic()
# # while (True):
# #     # Capture frame-by-frame
# #     ret, frame = cap.read()
# #     print(cap.get(3), cap.get(4), cap.get(18))
# #     print(time.monotonic() - now)
# #     now = time.monotonic()
# #
# #     # Our operations on the frame come here
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #     # Display the resulting frame
# #     cv2.imshow('frame', gray)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break
# # # When everything done, release the capture
# # cap.release()
# # cv2.destroyAllWindows()

cap = cv2.VideoCapture(1)
cap.set(3, 320)
cap.set(4, 240)
print(cap.get(3), cap.get(4))
tic = time.monotonic()
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(time.monotonic() - tic)
    tic = time.monotonic()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

