import cv2

num_cams = 3
caps = []

x = 1920
y = 1080

for i in range(num_cams):
    new_cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    new_cap.set(cv2.CAP_PROP_FRAME_WIDTH, x)
    new_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)
    caps.append(new_cap)


ret = False
frame = None
running = True
while running:
    for i in range(num_cams):
        ret, frame = caps[i].read()
        if frame is None or not ret:
            running = False
            break
        try:
            cv2.imshow("Cam " + str(i), frame)
        except Exception as e:
            running = False
        keypress = cv2.waitKey(1) % 0xFF
        if keypress == ord('q'):
            running = False

for i in range(num_cams):
    caps[i].release()
cv2.destroyAllWindows()
