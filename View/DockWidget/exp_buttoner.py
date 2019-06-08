# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QSize


class ExpButtoner(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setFixedSize(205, 120)
        self.__button_layout = QHBoxLayout()

        self.__create_end_button = QPushButton()
        self.__create_end_button.setFixedSize(60, 40)
        self.__start_pause_button = QPushButton()
        self.__start_pause_button.setFixedSize(120, 40)
        self.__button_layout.addWidget(self.__create_end_button)
        self.__button_layout.addWidget(self.__start_pause_button)
        self.__text_entry = QLineEdit()
        self.layout().addLayout(self.__button_layout)
        self.layout().addWidget(self.__text_entry)

        self.__play_icon = QIcon()
        self.__play_icon.addPixmap(QPixmap("../Images/green_arrow.png"))
        self.__pause_icon = QIcon()
        self.__pause_icon.addPixmap(QPixmap('../Images/red_vertical_bars.png'))
        self.__playing = False
        self.__set_texts()
        self.__set_button_states()
        self.__set_tooltips()
        self.__set_handlers()

    def get_condition_name(self):
        return self.__text_entry.text()

    def add_create_button_handler(self, func: 'Slot function'):
        self.__create_end_button.clicked.connect(func)

    def add_start_button_handler(self, func):
        self.__start_pause_button.clicked.connect(func)

    def __set_texts(self):
        self.setTitle("Experiment")
        self.__text_entry.setPlaceholderText("Optional condition name")
        self.__create_end_button.setText("Create")
        self.__start_pause_button.setIcon(self.__play_icon)
        self.__start_pause_button.setIconSize(QSize(32, 32))

    def __set_button_states(self):
        self.__start_pause_button.setEnabled(False)

    def __set_tooltips(self):
        self.__create_end_button.setToolTip("Create a new experiment")
        self.__start_pause_button.setToolTip("Begin experiment")

    def __set_handlers(self):
        self.__create_end_button.clicked.connect(self.__toggle_create_button)
        self.__start_pause_button.clicked.connect(self.__toggle_start_button)

    def __toggle_create_button(self):
        if self.__create_end_button.text() == "Create":
            self.__create_end_button.setText("End")
            self.__create_end_button.setToolTip("End experiment")
            self.__start_pause_button.setEnabled(True)
        else:
            self.__create_end_button.setText("Create")
            self.__create_end_button.setToolTip("Create a new experiment")
            self.__start_pause_button.setToolTip("Begin experiment")
            self.__start_pause_button.setEnabled(False)

    def __toggle_start_button(self):
        if self.__playing:
            self.__playing = False
            self.__start_pause_button.setIcon(self.__play_icon)
            self.__start_pause_button.setIconSize(QSize(26, 26))
            self.__create_end_button.setEnabled(True)
            self.__start_pause_button.setToolTip("Resume experiment")
        else:
            self.__playing = True
            self.__start_pause_button.setIcon(self.__pause_icon)
            self.__start_pause_button.setIconSize(QSize(36, 36))
            self.__create_end_button.setEnabled(False)
            self.__start_pause_button.setToolTip("Pause experiment")
