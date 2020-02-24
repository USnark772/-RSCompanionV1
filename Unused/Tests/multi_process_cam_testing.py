import cv2
from multiprocessing import Process
from threading import Thread
from queue import Queue
import time

small = (640, 480)
big = (1920, 1080)
# Still not doing it the way I want. 5 fps from usb cams and 30 fps from builtin cams.
# Threaded frame grabbing doesn't seem to make a difference.
# Suspicion is that compression is the hangup


def get_frames(cap_obj, frame_queue):
    for i in range(1000):
        ret, frame = cap_obj.read()
        if ret and frame is not None:
            frame_queue.put(frame)
        else:
            print("thread breaking")
            break


def show_feed(index: int):
    size = big
    print("running size:", size)
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    # Get frame sizes
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
    # frame_queue = Queue(maxsize=25)
    # frame_getter = Thread(target=get_frames, args=(cap, frame_queue,))
    # frame_getter.start()
    start = time.time()
    num_frames = 0
    while True:
        # if not frame_queue.empty():
        #     frame = frame_queue.get()
        ret, frame = cap.read()
        if ret and frame is not None:
            cv2.imshow("Cam " + str(index), frame)
            num_frames += 1
        keypress = cv2.waitKey(1) % 0xFF
        if keypress == ord('q'):
            break
    end = time.time()
    seconds = end - start
    if seconds > 0:
        fps = num_frames / seconds
    else:
        fps = 0
    print("time taken:", seconds, "fps:", fps, "camera:", index, "frames handled:", num_frames)
    cap.release()


if __name__ == '__main__':
    first_index = 0
    last_index = 2
    workers = []
    for i in range(first_index, last_index):
        print("Making process:", i)
        workers.append(Process(target=show_feed, args=(i,)))
    for j in range(len(workers)):
        print("Starting process:", j)
        workers[j].start()
    for k in range(len(workers)):
        print("Joining process:", k)
        workers[k].join()
