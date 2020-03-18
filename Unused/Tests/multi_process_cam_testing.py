import cv2
from multiprocessing import Process, Pipe
import time
from Model.general_defs import cap_codec, cap_temp_codec

small = (640, 480)
big = (1920, 1080)


def show_feed(index: int, pipe):
    size = big
    print("running size:", size)
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FOURCC, cap_temp_codec)
    cap.set(cv2.CAP_PROP_FOURCC, cap_codec)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
    start = time.time()
    num_frames = 0
    while True:
        if pipe.poll():
            print(pipe.recv())
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
    last_index = 3
    workers = []
    pipes = []
    for i in range(first_index, last_index):
        print("Making process:", i)
        my_side, their_side = Pipe()
        pipes.append(my_side)
        print(type(my_side), type(their_side))
        workers.append(Process(target=show_feed, args=(i, their_side,)))
    for j in range(len(workers)):
        print("Starting process:", j)
        workers[j].start()
    for a in range(len(workers)):
        print("sending message to:", a)
        pipes[a].send("Hello from main()")
    for k in range(len(workers)):
        print("Joining process:", k)
        workers[k].join()
