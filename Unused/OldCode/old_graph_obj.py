# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from datetime import timedelta
from CompanionLib.time_funcs import round_time, get_current_time


class GraphObj(QFrame):
    def __init__(self, name, x_label, y_label, graph_type=111):
        super().__init__()
        self.name = name
        self.__graph_type = graph_type
        self.__x_label = x_label
        self.__y_label = y_label
        self.__data = {}
        self.__line_names = []
        time = get_current_time(graph=True)
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

        self.__graph = self.__PlotCanvas(self, self.__graph_type)
        self.layout().addWidget(self.__graph)

        self.__nav_bar = NavBar(self.__graph, self)
        self.layout().addWidget(self.__nav_bar)

        self.__refresh_plot()

    def add_line(self, name):
        self.__data[name] = [[], []]
        self.__line_names.append(name)

    def add_data(self, name, x, y):
        self.__adding_point = True
        if type(x) == list:
            for e in x:
                self.__append_x(name, e)
        else:
            self.__append_x(name, x)
        if type(y) == list:
            for a in y:
                self.__append_y(name, a)
        else:
            self.__append_y(name, y)
        self.__refresh_plot()
        self.__adding_point = False

    def reset_data(self):
        self.__clear_data()
        self.__refresh_plot()

    def __append_x(self, name, x):
        self.__data[name][0].append(x)
        new_e = round_time(x, 1)
        if new_e not in self.__x_vals:
            self.__x_vals.append(new_e)

    def __append_y(self, name, y):
        self.__data[name][1].append(y)

    def __clear_data(self):
        for line in self.__data:
            self.__data[line] = []
        self.__x_vals = []
        self.__scrollbar.setRange(0, 0)

    def __refresh_plot(self):
        self.__graph.plot(self.__data, self.name, self.__x_label, self.__y_label, self.__line_names)
        self.__graph.draw()

    def __remake_graph_obj(self):
        self.__graph = self.__PlotCanvas(self, self.__graph_type)

    @staticmethod
    def __get_range_on_x_val(x):
        return [x - timedelta(minutes=3), x + timedelta(minutes=1)]

    class __PlotCanvas(Canvas):
        def __init__(self, parent=None, width=5, height=4, dpi=100, graph_type=111):
            self.canvas = Canvas.__init__(self, Figure(figsize=(width, height), dpi=dpi))
            self.setParent(parent)
            Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.axes = self.figure.add_subplot(graph_type)

        def add_plot(self, name, type):
            self.__axes[name] = self.figure.add_subplot(type)

        def plot(self, data, title, xlabel, ylabel, line_names):
            self.__reset_plot(title, xlabel, ylabel)
            for name in line_names:
                arr = data[name]
                if len(arr) == 2:  # Has x and y coordinates
                    self.axes.plot(arr[0], arr[1], label=name)
            self.figure.autofmt_xdate()
            if len(line_names) > 0:
                self.figure.legend(loc='upper left')

        def __reset_plot(self, title, xlabel, ylabel):
            self.axes.clear()
            self.axes.set_title(title)
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylabel(ylabel)
