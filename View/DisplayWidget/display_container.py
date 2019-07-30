# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide2.QtCore import QRect


class DisplayContainer(QWidget):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.__callback = callback
        self.setLayout(QVBoxLayout())
        self.__scroll_area = QScrollArea(self)
        self.__scroll_area.verticalScrollBar().valueChanged.connect(self.__slider_changed_notifier)
        self.__scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.__scroll_area)
        contents = QWidget(self)
        contents.setGeometry(QRect(0, 0, 335, 499))
        contents.setLayout(QVBoxLayout())
        self.__scroll_area.setWidget(contents)
        self.__list_of_displays = []

    def add_display(self, display):
        self.__list_of_displays.append(display)
        self.__refresh()

    def remove_display(self, display):
        if display in self.__list_of_displays:
            self.__list_of_displays.remove(display)
        self.__refresh()

    def __refresh(self):
        new_contents = QWidget(self)
        new_contents.setGeometry(QRect(0, 0, 335, 499))
        new_contents.setLayout(QVBoxLayout())
        for display in self.__list_of_displays:
            new_contents.layout().addWidget(display)
        self.__scroll_area.setWidget(new_contents)

    def __slider_changed_notifier(self):
        self.__callback()
