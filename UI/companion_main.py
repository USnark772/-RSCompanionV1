# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import sys
from UI.companion_view import *
import Serial.companion_device_com as serial


# TODO: Document code
class CompanionController:
    def __init__(self):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        self.app = QtWidgets.QApplication(sys.argv)
        self.companion_app = QtWidgets.QMainWindow()
        self.ui = CompanionWindow(self.companion_app, self.send_msg_to_manager)
        self.companion_app.show()
        self.device_manager = serial.ControllerSerial(self.send_msg_to_ui)
        self.update_timer = QtCore.QTimer()
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
