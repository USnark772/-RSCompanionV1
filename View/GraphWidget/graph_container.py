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
        contents = QWidget(self)
        contents.setGeometry(QRect(0, 0, 335, 499))
        contents.setLayout(QVBoxLayout())
        self.__scroll_area.setWidget(contents)
        self.__list_of_graphs = []

    def add_graph(self, graph):
        self.__list_of_graphs.append(graph)
        self.__refresh()

    def remove_graph(self, graph):
        if graph in self.__list_of_graphs:
            self.__list_of_graphs.remove(graph)
        self.__refresh()

    def __refresh(self):
        new_contents = QWidget(self)
        new_contents.setGeometry(QRect(0, 0, 335, 499))
        new_contents.setLayout(QVBoxLayout())
        for graph in self.__list_of_graphs:
            new_contents.layout().addWidget(graph)
        self.__scroll_area.setWidget(new_contents)
