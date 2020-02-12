import sys
from PySide2.QtCore import Signal, QObject, QThread
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton


class WorkerSig(QObject):
    sig = Signal(int)


class Worker(QThread):
    def __init__(self, loop_range):
        QThread.__init__(self)
        self.signal = WorkerSig()
        self.loop_range = loop_range

    def run(self):
        for i in range(self.loop_range):
            print("Worker running")
            self.signal.sig.emit(i)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.loop_range = 50
        self.worker = Worker(self.loop_range)
        self.worker.signal.sig.connect(self.print_it)
        self.setCentralWidget(QWidget(self))
        self.vbox = QVBoxLayout(self)
        self.pause_button = QPushButton(self)
        self.pause_button.setText('pause for a few seconds')
        self.pause_button.clicked.connect(self.pause_for_a_bit)
        self.centralWidget().setLayout(self.vbox)
        self.worker.start(priority=QThread.LowestPriority)
        self.values = []

    def print_it(self, value):
        # self.values.append("not paused:" + str(value))
        print("not paused:", value)
        if value == 10:
            self.pause_for_a_bit()
        if value == self.loop_range - 1:
            print("waiting on worker")
            self.worker.wait()
            # self.show_result()

    def show_result(self):
        for element in self.values:
            print(element)

    def pause_for_a_bit(self):
        for i in range(200):
            print("main thread paused", i)
            # self.values.append("paused" + str(i))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
