# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide2.QtCore import QRect


class GraphContainer(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.__scroll_area = QScrollArea(self)
        self.__scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.__scroll_area)
        self.__contents = QWidget(self)
        self.__contents.setGeometry(QRect(0, 0, 335, 499))
        self.__contents.setLayout(QVBoxLayout())
        self.__scroll_area.setWidget(self.__contents)

    def add_graph(self, graph):
        self.__contents.layout().addWidget(graph)

    def remove_graph(self, graph):
        self.__contents.layout().removeWidget(graph)
