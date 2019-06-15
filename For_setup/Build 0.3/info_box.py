# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QLabel, QGridLayout, QGroupBox
from PySide2.QtCore import Qt


class InfoBox(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(230, 120)
        self.setLayout(QGridLayout())

        self.__start_time_label = QLabel()
        self.__start_time_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.__start_time_label, 1, 0, 1, 1)

        self.__start_time_val = QLabel()
        self.__start_time_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self.__start_time_val, 1, 1, 1, 1)

        self.__set_texts()

    def set_start_time(self, time):
        self.__start_time_val.setText(time)

    def reset_start_time(self):
        self.__start_time_val.setText("00:00:00")

    def __set_texts(self):
        self.setTitle("Information")
        self.__start_time_label.setText("Experiment start time:")
        self.reset_start_time()
