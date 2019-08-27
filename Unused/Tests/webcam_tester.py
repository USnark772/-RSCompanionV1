from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.online_webcams = QCameraInfo.availableCameras()
        if not self.online_webcams:
            pass #quit
        self.exist = QCameraViewfinder()
        self.exist.show()
        self.setCentralWidget(self.exist)

        # set the default webcam.
        self.current_cam_index = 0
        self.get_webcam(self.current_cam_index)
        self.setWindowTitle("WebCam")
        self.show()

    def keyPressEvent(self, event):
        if event.key() == 0x4e:
            self.change_webcam(True)
        elif event.key() == 0x50:
            self.change_webcam()

    def change_webcam(self, increment=False):
        if increment:
            if self.current_cam_index + 1 < len(self.online_webcams):
                self.current_cam_index += 1
                self.get_webcam(self.current_cam_index)
        else:
            if self.current_cam_index - 1 >= 0:
                self.current_cam_index -= 1
                self.get_webcam(self.current_cam_index)

    def get_webcam(self, i):
        self.my_webcam = QCamera(self.online_webcams[i])
        self.my_webcam.setViewfinder(self.exist)
        self.my_webcam.setCaptureMode(QCamera.CaptureStillImage)
        self.my_webcam.error.connect(lambda: self.alert(self.my_webcam.errorString()))
        self.my_webcam.start()

    def alert(self, s):
        """
        This handles errors and displays alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("WebCam")

    window = MainWindow()
    app.exec_()