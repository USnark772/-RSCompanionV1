# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QFrame, QLabel, QPushButton
from PySide2.QtCore import QSize, Qt


class TabContents(QVBoxLayout):
    def __init__(self, parent, msg_callback):
        super().__init__(parent)

        self.__msg_callback = msg_callback
        self.__buttons = {}

    def add_close_button(self, button_id, controller_callback):
        self.__buttons[button_id] = CloseButtonFrameOBJ(button_id, self.close_button_pressed, controller_callback)
        self.addWidget(self.__buttons[button_id])

    def close_button_pressed(self, button_id):
        self.__msg_callback(button_id)
        self.__buttons[button_id].deleteLater()


class CloseButtonFrameOBJ(QFrame):
    def __init__(self, button_id, msg_callback, controller_callback):
        super().__init__()
        self.setMinimumSize(QSize(50, 80))
        self.setMaximumSize(QSize(250, 100))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout())
        self.__graph_label = QLabel(self)
        self.__graph_label.setAlignment(Qt.AlignCenter)
        self.__graph_label.setWordWrap(True)
        self.__graph_label.setText(button_id[0] + " on " + button_id[1])
        self.__close_button = QPushButton(self)
        self.__close_button.setText("Close File")
        self.layout().addWidget(self.__graph_label)
        self.layout().addWidget(self.__close_button)

        self.__msg_callback = msg_callback
        self.__cont_callback = controller_callback
        self.__button_id = button_id

        self.__set_handlers()

    def __set_handlers(self):
        self.__close_button.clicked.connect(self.__callback)

    def __callback(self):
        self.__cont_callback(self.__button_id)
        self.__msg_callback(self.__button_id)
