# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import sys
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import Qt
from UI.companion_main_window_view import CompanionWindow
import Serial.companion_device_com_controller as serial


# TODO: Document code
class CompanionController:
    def __init__(self):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        self.app = QApplication(sys.argv)
        self.companion_app = QMainWindow()
        self.ui = CompanionWindow(self.companion_app, self.send_msg_to_manager)
        self.companion_app.show()
        self.device_manager = serial.ControllerSerial(self.send_msg_to_ui)
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.device_update)
        self.update_timer.start(1)

    def device_update(self):
        self.device_manager.update()

    def send_msg_to_manager(self, msg):
        self.device_manager.handle_msg(msg)

    def send_msg_to_ui(self, msg):
        self.ui.handle_msg(msg)



def main():
    master_control = CompanionController()
    sys.exit(master_control.app.exec_())


if __name__ == "__main__":
    main()
