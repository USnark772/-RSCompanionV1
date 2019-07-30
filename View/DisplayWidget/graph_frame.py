# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QPushButton


class GraphFrame(QFrame):
    def __init__(self, parent, canvas):
        super().__init__(parent)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout(self))
        self.__visible = True
        self.__canvas = canvas
        self.__show_hide_button = QPushButton(self)
        self.__show_hide_button.setFixedSize(150, 30)
        self.__show_hide_button.clicked.connect(self.__set_graph_visibility)
        self.layout().addWidget(self.__show_hide_button)
        self.__navbar_height = 100
        self.__canvas_height = 400
        self.__show_hide_button.setText("Hide " + self.__canvas.get_title() + " graph")
        self.layout().addWidget(self.__canvas)
        self.layout().addWidget(self.__canvas.get_nav_bar())
        self.setFixedHeight(self.__navbar_height + self.__canvas_height)

    def set_graph_height(self, height):
        self.__canvas_height = height

    def __set_graph_visibility(self):
        self.__visible = not self.__visible
        if self.__visible:
            self.layout().removeWidget(self.__canvas.get_nav_bar())
            self.layout().addWidget(self.__canvas)
            self.layout().addWidget(self.__canvas.get_nav_bar())
            self.setFixedHeight(40 + self.__navbar_height + self.__canvas_height)
            self.__show_hide_button.setText("Hide " + self.__canvas.get_title() + " graph")
        else:
            self.layout().removeWidget(self.__canvas)
            self.layout().removeWidget(self.__canvas.get_nav_bar())
            self.setFixedHeight(40)
            self.__show_hide_button.setText("Show " + self.__canvas.get_title() + " graph")

    def get_graph(self):
        return self.__canvas
