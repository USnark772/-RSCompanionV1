# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QScrollBar
from PySide2.QtCore import Qt


class GraphObj(QFrame):
    def __init__(self, name, x_label, y_label):
        super().__init__()
        self.__name = name
        self.__x_label = x_label
        self.__y_label = y_label
        self.__data = {}
        self.__line_names = []

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFixedHeight(400)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout())

        self.__graph = self.PlotCanvas(self)
        self.layout().addWidget(self.__graph)

        self.__scrollbar = QScrollBar()
        self.__scrollbar.setOrientation(Qt.Horizontal)
        self.__scrollbar.setValue(self.__scrollbar.maximum())
        self.__scrollbar.valueChanged.connect(self.__move_graph)
        self.layout().addWidget(self.__scrollbar)

    def add_line(self, name):
        self.__data[name] = [[], []]
        self.__line_names.append(name)

    def add_data(self, name, x, y):
        for e in x:
            self.__data[name][0].append(e)
        for a in y:
            self.__data[name][1].append(a)
        self.__refresh_plot()

    def reset_data(self):
        self.__clear_data()
        self.__refresh_plot()

    def __move_graph(self):
        print("Implement slider handler")

    def __clear_data(self):
        for line in self.__data:
            self.__data[line] = []

    def __refresh_plot(self):
        self.__graph.plot(self.__data, self.__name, self.__x_label, self.__y_label, self.__line_names)

    class PlotCanvas(Canvas):
        def __init__(self, parent=None, width=5, height=4, dpi=100):
            Canvas.__init__(self, Figure(figsize=(width, height), dpi=dpi))
            self.setParent(parent)
            Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.axes = self.figure.add_subplot(111)

        def plot(self, data, title, xlabel, ylabel, line_names):
            self.__reset_plot(title, xlabel, ylabel)
            for name in line_names:
                arr = data[name]
                if len(arr) == 2:  # Has x and y coordinates
                    self.axes.plot(arr[0], arr[1], label=name)
            self.figure.autofmt_xdate()
            self.figure.legend(loc='upper left')
            self.draw()

        def __reset_plot(self, title, xlabel, ylabel):
            self.axes.clear()
            self.axes.set_title(title)
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylabel(ylabel)
