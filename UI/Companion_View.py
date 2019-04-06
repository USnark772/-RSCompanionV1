# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific

import sys
from UI.RS_Companion_Window_Class import *


def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    companion_app = QtWidgets.QMainWindow()
    ui = Companion_Window(companion_app)
    companion_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":main()