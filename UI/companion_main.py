# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific

import sys
from UI.rs_companion_view import *
import Serial.rs_device_com as serial
import Serial.device_defs as defs

# TODO: Document code
class CompanionController:
    def __init__(self):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        self.app = QtWidgets.QApplication(sys.argv)
        self.companion_app = QtWidgets.QMainWindow()
        self.ui = CompanionWindow(self.companion_app)
        self.companion_app.show()
        self.device_manager = serial.ControllerSerial(defs.devices, self.callback_1)
        self.update_timer = QtCore.QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.device_update)
        self.update_timer.start(1)

    def device_update(self):
        self.device_manager.update()

    def callback_1(self, device, add_or_remove):
        if add_or_remove == 1:
                self.ui.add_rs_device_handler(device)
        else:
                self.ui.remove_rs_device_handler(device)


def main():
    master_control = CompanionController()
    sys.exit(master_control.app.exec_())


if __name__ == "__main__":
    main()
