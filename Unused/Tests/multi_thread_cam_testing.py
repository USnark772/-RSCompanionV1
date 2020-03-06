import cv2
from threading import Thread
import time

small = (640, 480)
big = (1920, 1080)


def show_feed(index: int):
    size = big
    print("running size:", size)
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
    start = time.time()
    num_frames = 0
    while True:
        ret, frame = cap.read()
        if frame is None or not ret:
            break
        try:
            cv2.imshow("Cam " + str(index), frame)
            num_frames += 1
        except Exception as e:
            break
        keypress = cv2.waitKey(1) % 0xFF
        if keypress == ord('q'):
            break
    end = time.time()
    seconds = end - start
    fps = num_frames / seconds
    print("time taken:", seconds, "fps:", fps, "camera:", index)


if __name__ == '__main__':
    first_index = 0
    last_index = 4
    workers = []
    for i in range(first_index, last_index):
        print("Making thread:", i)
        workers.append(Thread(target=show_feed, args=(i,)))
    for j in range(len(workers)):
        print("Starting thread:", j)
        workers[j].start()
    for k in range(len(workers)):
        print("Joining thread:", k)
        workers[k].join()
