# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QDockWidget, QHBoxLayout, QWidget
from PySide2.QtCore import Qt
from View.DockWidget.exp_buttoner import ExpButtoner
from View.DockWidget.key_flagger import KeyFlagger
from View.DockWidget.note_taker import NoteTaker
from View.DockWidget.info_displayer import InfoDisplayer


class ControlDock(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(850, 160)
        self.setFeatures(
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetVerticalTitleBar)
        self.setAllowedAreas(Qt.TopDockWidgetArea)
        self.setWidget(QWidget())
        self.widget().setLayout(QHBoxLayout())

        self.__control_box = ExpButtoner(self)
        self.widget().layout().addWidget(self.__control_box)

        self.__flagger = KeyFlagger(self)
        self.widget().layout().addWidget(self.__flagger)

        self.__note_box = NoteTaker(self)
        self.widget().layout().addWidget(self.__note_box)

        self.__info = InfoDisplayer(self)
        self.widget().layout().addWidget(self.__info)

        self.__set_texts()

    def __set_texts(self):
        self.setWindowTitle("Control")

    def set_start_time(self, time):
        self.__info.set_start_time(time)

    def reset_start_time(self):
        self.__info.reset_start_time()

    def get_note(self):
        return self.__note_box.get_note()

    def clear_note(self):
        self.__note_box.clear_note()

    def set_key_flag(self, key):
        self.__flagger.set_flag(key)

    def get_key_flag(self):
        return self.__flagger.get_flag()

    def get_condition_name(self):
        return self.__control_box.get_condition_name()

    def toggle_post_button(self, is_active):
        self.__note_box.toggle_post_button(is_active)

    def add_post_handler(self, func):
        self.__note_box.add_post_handler(func)

    def add_create_end_button_handler(self, func):
        self.__control_box.add_create_button_handler(func)

    def add_start_button_handler(self, func):
        self.__control_box.add_start_button_handler(func)

    def add_note_box_changed_handler(self, func):
        self.__note_box.add_note_box_changed_handler(func)
