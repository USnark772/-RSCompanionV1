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

        self.msg_callback = msg_callback
        self.buttons = {}

    def add_close_button(self, button_id, controller_callback):
        self.buttons[button_id] = CloseButtonFrameOBJ(button_id, self.close_button_pressed, controller_callback)
        self.addWidget(self.buttons[button_id])

    def close_button_pressed(self, button_id):
        self.msg_callback(button_id)
        self.buttons[button_id].deleteLater()
        # del(self.buttons[button_id])


class CloseButtonFrameOBJ(QFrame):
    def __init__(self, button_id, msg_callback, controller_callback):
        super().__init__()
        self.setMinimumSize(QSize(50, 80))
        self.setMaximumSize(QSize(250, 100))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout())
        self.graph_label = QLabel(self)
        self.graph_label.setAlignment(Qt.AlignCenter)
        self.graph_label.setWordWrap(True)
        self.graph_label.setText(button_id[0] + " on " + button_id[1])
        self.close_button = QPushButton(self)
        self.close_button.setText("Close File")
        self.layout().addWidget(self.graph_label)
        self.layout().addWidget(self.close_button)

        self.close_button.clicked.connect(self.__callback)
        self.msg_callback = msg_callback
        self.cont_callback = controller_callback
        self.button_id = button_id

    def __callback(self):
        self.cont_callback(self.button_id)
        self.msg_callback(self.button_id)
