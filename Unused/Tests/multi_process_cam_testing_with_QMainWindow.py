import cv2
import imutils
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
import time
import sys
from PySide2.QtWidgets import *
from View.MainWindow.central_widget import CentralWidget

small = (640, 480)
big = (1920, 1080)
backend = cv2.CAP_DSHOW

cap_codec_one = cv2.VideoWriter_fourcc(*'mjpg')
cap_codec = cv2.VideoWriter_fourcc(*'MJPG')


def show_feed(index: int, pipe: Connection):
    name = "Cam " + str(index)
    size = small
    print("running size:", size)
    cap = cv2.VideoCapture(index, backend)
    ret = cap.set(cv2.CAP_PROP_FOURCC, cap_codec_one)  # TODO: Figure out wtf is going on here and how to integrate to project!
    print(ret)
    ret = cap.set(cv2.CAP_PROP_FOURCC, cap_codec)
    print(ret)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
    cap.set(cv2.CAP_PROP_SETTINGS, 1)
    # save_dir = "C:/users/phill/companion app save folder/"
    # vid_ext = ".avi"
    # codec = "DIVX"
    # frame_size = big
    # fps = 30

    # writer = cv2.VideoWriter()
    # self.writer = cv2.VideoWriter(save_dir + timestamp + self.name + '_output' + vid_ext,
    #                               cv2.VideoWriter_fourcc(*codec), fps, frame_size)
    start = time.time()
    num_frames = 0
    resize = 0
    while True:
        if pipe.poll():
            msg = pipe.recv()
            if msg == "small":
                resize = 1
            elif msg == "big":
                resize = 2
            elif msg == "reset":
                resize = 0
            elif msg == "close":
                cv2.destroyWindow(name)
                cap.release()
                break
        ret, frame = cap.read()
        if ret and frame is not None:
            if resize == 1:
                frame = imutils.resize(frame, width=small[0])
            elif resize == 2:
                frame = imutils.resize(frame, width=big[0])
            cv2.imshow(name, frame)
            num_frames += 1
        else:
            print("Cam failed")
            cv2.destroyWindow(name)
            cap.release()
            break
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
        self.first_index = 2
        self.last_index = 3
        self.workers = []
        self.pipes = []
        self.make_workers()
        self.start_workers()

    def make_workers(self):
        for i in range(self.first_index, self.last_index):
            print("Making process:", i)
            my_side, their_side = Pipe()
            self.pipes.append(my_side)
            self.workers.append(Process(target=show_feed, args=(i, their_side,)))

    def start_workers(self):
        for j in range(len(self.workers)):
            print("Starting process:", j)
            self.workers[j].start()

    def cleanup(self):
        for k in range(len(self.workers)):
            print("Joining process:", k)
            try:
                self.pipes[k].send("close")
                self.workers[k].join()
            except:
                pass


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(300, 200)
        self.setCentralWidget(CentralWidget(self))
        self.layout = QHBoxLayout(self)
        self.small_button = QPushButton(self)
        self.small_button.setText("Make small")
        self.small_button.clicked.connect(self.make_small)
        self.big_button = QPushButton(self)
        self.big_button.setText("Make big")
        self.big_button.clicked.connect(self.make_big)
        self.reset_button = QPushButton(self)
        self.reset_button.setText("Reset")
        self.reset_button.clicked.connect(self.reset_size)
        self.layout.addWidget(self.small_button)
        self.layout.addWidget(self.big_button)
        self.layout.addWidget(self.reset_button)
        self.centralWidget().layout().addLayout(self.layout)
        self.cams = Cams()

    def make_small(self):
        for pipe in self.cams.pipes:
            pipe.send("small")

    def make_big(self):
        for pipe in self.cams.pipes:
            pipe.send("big")

    def reset_size(self):
        for pipe in self.cams.pipes:
            pipe.send("reset")

    def closeEvent(self, event):
        self.cams.cleanup()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
