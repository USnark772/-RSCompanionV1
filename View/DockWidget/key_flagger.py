# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel
from PySide2.QtGui import QFont, QGuiApplication
from PySide2.QtCore import Qt


class KeyFlagger(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setFixedSize(80, 120)
        self.__flag = QLabel(self)
        font = QFont()
        font.setPointSize(16)
        self.__flag.setFont(font)
        self.layout().addWidget(self.__flag, 0, Qt.AlignHCenter)

        self.__set_texts()
        self.__set_tooltips()

    def set_flag(self, text):
        self.__flag.setText(text)

    def get_flag(self):
        return self.__flag.text()

    def __set_texts(self):
        self.setTitle("Key Flag")
        self.__flag.setText("None")

    def __set_tooltips(self):
        self.__flag.setToolTip("The most recent key pressed for reference in save file")
