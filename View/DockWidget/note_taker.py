# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QGroupBox, QGridLayout, QTextEdit, QPushButton


class NoteTaker(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QGridLayout())
        self.setFixedSize(250, 120)
        self.__text_edit = QTextEdit()
        self.layout().addWidget(self.__text_edit, 0, 1, 1, 1)
        self.__post_button = QPushButton()
        self.layout().addWidget(self.__post_button, 1, 1, 1, 1)

        self.__set_texts()
        self.__set_button_state()
        self.__set_tooltips()

    def get_note(self):
        return self.__text_edit.toPlainText()

    def clear_note(self):
        self.__text_edit.clear()

    def toggle_post_button(self, is_active):
        self.__post_button.setEnabled(is_active)

    def add_post_handler(self, func):
        self.__post_button.clicked.connect(func)

    def add_note_box_changed_handler(self, func):
        self.__text_edit.textChanged.connect(func)

    def __set_texts(self):
        self.setTitle("Note")
        self.__post_button.setText("Post")
        self.__text_edit.setPlaceholderText("Enter note here")

    def __set_button_state(self):
        self.__post_button.setEnabled(False)

    def __set_tooltips(self):
        self.__post_button.setToolTip("Post note")
