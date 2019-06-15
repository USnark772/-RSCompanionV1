# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QDockWidget, QHBoxLayout, QWidget
from PySide2.QtCore import Qt


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

        self.__set_texts()

    def add_widget(self, widget):
        self.widget().layout().addWidget(widget)

    def __set_texts(self):
        self.setWindowTitle("Control")
