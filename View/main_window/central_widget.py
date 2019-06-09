# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QVBoxLayout, QFrame


class CentralWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.__sep_line = QFrame()
        self.__sep_line.setFrameShape(QFrame.HLine)
        self.__sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.__sep_line)
