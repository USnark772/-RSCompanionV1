# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QScrollBar
from PySide2.QtCore import Qt
from datetime import datetime, timedelta
from CompanionLib.time_funcs import round_time


class GraphObj(QFrame):
    def __init__(self, name, x_label, y_label):
        super().__init__()
        self.__name = name
        self.__x_label = x_label
        self.__y_label = y_label
        self.__data = {}
        self.__line_names = []
        time = datetime.now()
        self.__x_bounds = self.__get_range_on_x_val(time)
        self.__scrolling = False
        self.__adding_point = False
        self.__x_vals = []

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
        self.__scrollbar.setRange(0, 0)
        self.__scrollbar.setOrientation(Qt.Horizontal)
        self.__scrollbar.setValue(self.__scrollbar.maximum())
        self.__scrollbar.valueChanged.connect(self.__move_graph)
        self.layout().addWidget(self.__scrollbar)

    def add_line(self, name):
        self.__data[name] = [[], []]
        self.__line_names.append(name)

    def add_data(self, name, x, y):
        self.__adding_point = True
        for e in x:
            self.__data[name][0].append(e)
            new_e = round_time(e, 1)
            if new_e not in self.__x_vals:
                self.__x_vals.append(new_e)
                self.__update_scrollbar()
        for a in y:
            self.__data[name][1].append(a)
        self.__refresh_plot()
        self.__adding_point = False

    def reset_data(self):
        self.__clear_data()
        self.__refresh_plot()

    def __move_graph(self):
        if self.__adding_point:
            return
        if self.__scrollbar.value() != self.__scrollbar.maximum():
            self.__scrolling = True
            self.__x_bounds = self.__get_range_on_x_val(self.__x_vals[self.__scrollbar.value()])
        else:
            self.__scrolling = False
        self.__refresh_plot()

    def __clear_data(self):
        for line in self.__data:
            self.__data[line] = []
        self.__x_vals = []
        self.__scrollbar.setRange(0, 0)

    def __refresh_plot(self):
        if not self.__scrolling:
            self.__check_x_bounds()
            self.__graph.plot(self.__data, self.__name, self.__x_label, self.__y_label, self.__line_names)
        self.__graph.axes.set_xbound(self.__x_bounds[0], self.__x_bounds[1])
        self.__graph.draw()

    def __check_x_bounds(self):
        self.__x_bounds = self.__get_range_on_x_val(self.__x_vals[len(self.__x_vals) - 1])

    def __update_scrollbar(self):
        self.__scrollbar.setMaximum(len(self.__x_vals) - 1)
        if not self.__scrolling:
            self.__scrollbar.setValue(self.__scrollbar.maximum())

    @staticmethod
    def __get_range_on_x_val(x):
        return [x - timedelta(seconds=5), x + timedelta(seconds=5)]

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

        def __reset_plot(self, title, xlabel, ylabel):
            self.axes.clear()
            self.axes.set_title(title)
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylabel(ylabel)
