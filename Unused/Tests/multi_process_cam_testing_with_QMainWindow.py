import cv2
from multiprocessing import Process, Pipe
import time
import sys
from PySide2.QtWidgets import *

small = (640, 480)
big = (1920, 1080)


def show_feed(index: int, pipe):
    size = big
    print("running size:", size)
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
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


class Cams:
    def __init__(self):
        self.first_index = 0
        self.last_index = 2
        self.workers = []
        self.pipes = []
        self.make_workers()
        self.start_workers()

    def make_workers(self):
        for i in range(self.first_index, self.last_index):
            print("Making process:", i)
            my_side, their_side = Pipe()
            self.pipes.append(my_side)
            print(type(my_side), type(their_side))
            self.workers.append(Process(target=show_feed, args=(i, their_side,)))

    def start_workers(self):
        for j in range(len(self.workers)):
            print("Starting process:", j)
            self.workers[j].start()

    def cleanup(self):
        for k in range(len(self.workers)):
            print("Joining process:", k)
            self.workers[k].join()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(300, 50)
        self.record_button = QPushButton(self)
        self.record_button.setText("Record video")
        self.record_button.clicked.connect(self.say_hello)
        self.cams = Cams()

    def say_hello(self):
        print("Hello")

    def closeEvent(self, event):
        self.cams.cleanup()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
