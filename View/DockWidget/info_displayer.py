# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QLabel, QGridLayout, QGroupBox
from PySide2.QtCore import Qt


class InfoDisplayer(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(230, 120)
        self.setLayout(QGridLayout())

        '''
        self.name_label = QLabel()
        self.name_label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(self.name_label, 0, 0, 1, 1)

        self.name_val = QLabel()
        self.name_val.setAlignment(Qt.AlignRight)
        self.layout().addWidget(self.name_val, 0, 1, 1, 1)
        '''

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

    '''
    def set_name(self, name):
        self.name_val.setText(name)

    def reset_name(self):
        self.name_val.setText("")
    '''

    def __set_texts(self):
        self.setTitle("Information")
        '''
        self.name_label.setText("Experiment name:")
        self.reset_name()
        '''
        self.__start_time_label.setText("Experiment start time:")
        self.reset_start_time()
