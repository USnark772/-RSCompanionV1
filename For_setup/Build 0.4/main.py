# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from controller import CompanionController


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    CompanionController()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()