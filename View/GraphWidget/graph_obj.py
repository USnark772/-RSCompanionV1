# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
from datetime import datetime, timedelta


class GraphObj(QFrame):
    def __init__(self):
        super().__init__()

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.__min_height = 400
        self.__height_increment = 400
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout(self))

        self.__canvases = {}
        self.__data = {}  # {device_type: {data_type: {device_port: [[x], [y]]}}}

    def add_device(self, device, data_types):
        device_type = device[0]
        device_port = device[1]
        if device_type not in self.__data:
            self.__data[device_type] = {}
            for data_type in data_types:
                if data_type not in self.__data[device_type]:
                    self.__data[device_type][data_type] = {}
                if device_port not in self.__data[device_type][data_type]:
                    self.__data[device_type][data_type][device_port] = [[], [], True]
        if device_type not in self.__canvases:
            self.__add_canvas(device_type, data_types)
        self.__canvases[device_type][0].device_ports.append(device_port)

    def remove_device(self, device):
        device_type = device[0]
        device_port = device[1]
        if device_type in self.__data:
            for data_type in self.__data[device_type]:
                if device_port in self.__data[device_type][data_type]:
                    del self.__data[device_type][data_type][device_port]
        if device_type in self.__canvases:
            if device_port in self.__canvases[device_type][0].device_ports:
                self.__canvases[device_type][0].device_ports.remove(device_port)
            if len(self.__canvases[device_type][0].device_ports) < 1:
                self.__remove_canvas(device_type)

    def add_data(self, device, data_type, x, y):
        device_type = device[0]
        device_port = device[1]
        if device_type in self.__data:
            self.__data[device_type][data_type][device_port][0].append(x)
            self.__data[device_type][data_type][device_port][1].append(y)
            self.__plot_graph(device)

    def set_device_data_type_activity(self, device, data_type, is_active):
        device_type = device[0]
        device_port = device[1]
        self.__data[device_type][data_type][device_port][2] = is_active

    # TODO: Implement this
    def set_plot_activity(self):
        pass

    def __plot_graph(self, device):
        device_type = device[0]
        if device_type in self.__canvases:
            self.__canvases[device_type][0].plot(self.__data[device_type])

    # TODO: check that this initialization works
    def __add_canvas(self, canvas_type, sub_types):
        canvas = self.__CanvasObj(canvas_type)
        self.__canvases[canvas_type] = [canvas]
        self.__set_subplots(canvas_type, sub_types)
        self.layout().addWidget(canvas)
        nav_bar = NavBar(canvas, self)
        self.__canvases[canvas_type].append(nav_bar)
        self.layout().addWidget(nav_bar)
        canvas.plot(new=True)
        self.__min_height += self.__height_increment
        self.setMinimumHeight(self.__min_height)

    def __set_subplots(self, device_type, data_types):
        r = len(data_types)
        c = 1
        ts_label = "Timestamp"
        for i in range(0, r):
            self.__canvases[device_type][0].plots[data_types[i]]\
                = [(r, c, i + 1), ts_label, data_types[i], True]

    # TODO: Figure out why graph won't disappear
    def __remove_canvas(self, canvas_type):
        self.layout().removeWidget(self.__canvases[canvas_type][0])
        self.__canvases[canvas_type][0].deleteLater()
        self.__canvases[canvas_type][1].deleteLater()
        del self.__canvases[canvas_type]
        self.__min_height -= self.__height_increment
        self.setMinimumHeight(self.__min_height)
        for device_type in self.__canvases:
            device = (device_type, "")
            self.__plot_graph(device)

    class __CanvasObj(Canvas):
        def __init__(self, device_type):
            Canvas.__init__(self, Figure(figsize=(5, 5)))
            self.device_ports = []
            self.title = device_type
            self.plots = {}  # sub_type: coords, xlabel, ylabel, active

        # TODO: Fix subplot layout issues
        def plot(self, data=None, new=False):
            self.figure.clear()
            # self.figure.suptitle(self.title)
            # self.figure.tight_layout(rect=[1, .1, .7, 0.8])  # (left, bottom, right, top)
            self.figure.set_tight_layout(True)
            # self.figure.subplots_adjust(left=0.15, right=0.98, top=0.93, bottom=0.2, hspace=0.8, wspace=0.8)
            i = 0
            for data_type in self.plots:
                if self.plots[data_type][3]:
                    coords = self.plots[data_type][0]
                    axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                    axes.tick_params(axis='x', labelrotation=30)
                    axes.set_ylabel(self.plots[data_type][2])
                    if i == 0:
                        axes.set_title(self.title)
                    elif i == len(self.plots) - 1:
                        axes.set_xlabel(self.plots[data_type][1])
                    i += 1
                    if not new:
                        self.__plot_device_type(self.title, axes, data[data_type])
            # self.figure.legend(loc='upper left')
            self.figure.canvas.draw()

        # TODO: NEW DEVICE ADDITION. Add reference to new device plot function in this if else statement
        def __plot_device_type(self, device_type, axes, data):
            if device_type == "drt":
                self.__plot_drt(axes, data)
            elif device_type == "vog":
                self.__plot_vog(axes, data)

        ###########################################################################
        # TODO: NEW DEVICE ADDITION. Add new device plot function below this line
        ###########################################################################

        @staticmethod
        def __plot_drt(axes, data):
            for key in data:
                if data[key][2]:
                    axes.plot(data[key][0], data[key][1], label=key)

        @staticmethod
        def __plot_vog(axes, data):
            highest = datetime.now() + timedelta(seconds=5)
            lowest = datetime.now() + timedelta(seconds=-5)
            for key in data:
                if data[key][2]:
                    temp_x = data[key][0]
                    temp_y = data[key][1]
                    if len(temp_x) > 0:
                        if highest < max(temp_x):
                            highest = max(temp_x)
                        if lowest > min(temp_x):
                            lowest = min(temp_x)
                    axes.scatter(temp_x, temp_y, label=key)
            axes.set_xlim(lowest + timedelta(seconds=-5), highest + timedelta(seconds=5))

