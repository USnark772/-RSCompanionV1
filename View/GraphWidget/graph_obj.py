# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure


class GraphObj(QFrame):
    def __init__(self):
        super().__init__()

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.__min_height = 300
        self.__height_increment = 300
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
                    self.__data[device_type][data_type][device_port] = [[], []]
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

    def add_data(self, device, data_type, x, y):  # {device_type: {data_type: {device_port: [[x], [y]]}}}
        device_type = device[0]
        device_port = device[1]
        if device_type in self.__data:
            self.__data[device_type][data_type][device_port][0].append(x)
            self.__data[device_type][data_type][device_port][1].append(y)
            self.__plot_graph(device)

    def __plot_graph(self, device):
        device_type = device[0]
        if device_type in self.__canvases:
            self.__canvases[device_type][0].plot(self.__data[device_type])

    # TODO: check that this initialization works
    def __add_canvas(self, canvas_type, sub_types):  # {device_type: {data_type: {device_port: [[x], [y]]}}}
        canvas = self.__CanvasObj(canvas_type)
        self.__canvases[canvas_type] = [canvas]
        self.__set_subplots(canvas_type, sub_types)
        self.layout().addWidget(canvas)
        nav_bar = NavBar(canvas, self)
        self.__canvases[canvas_type].append(nav_bar)
        self.layout().addWidget(nav_bar)
        temp = (canvas_type, "")
        self.__data[temp] = {}
        self.__plot_graph(temp)
        del self.__data[temp]
        self.__min_height += self.__height_increment
        self.setMinimumHeight(self.__min_height)

    def __set_subplots(self, device_type, data_types):
        r = len(data_types)
        c = 1
        ts_label = ""
        for i in range(0, r):
            if i == r - 1:
                ts_label = "Timestamp"
            self.__canvases[device_type][0].plots[data_types[i]]\
                = [(r, c, i + 1), ts_label, data_types[i]]

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
        '''
        if canvas_type in self.__canvases:
            del self.__canvases[canvas_type]
        new_layout = QVBoxLayout(self)
        for canvas in self.__canvases:
            new_layout.addWidget(self.__canvases[canvas])
            new_layout.addWidget(NavBar(self.__canvases[canvas], self))
        old_layout = self.layout()
        del old_layout
        self.setLayout(new_layout)
        self.__min_height -= self.__height_increment
        self.setMinimumHeight(self.__min_height)
        '''

    class __CanvasObj(Canvas):
        def __init__(self, device_type):
            Canvas.__init__(self, Figure(figsize=(5, 5)))
            self.device_ports = []
            self.title = device_type
            self.plots = {}  # sub_type: coords, xlabel, ylabel

        # TODO: Fix subplot layout issues
        def plot(self, data):  # {data_type: {device_port: [[x], [y]]}}}
            self.figure.clear()
            self.figure.suptitle(self.title)
            # self.figure.tight_layout(rect=[1, .1, .7, 0.8])  # (left, bottom, right, top)
            self.figure.set_tight_layout(True)
            # self.figure.subplots_adjust(left=0.15, right=0.98, top=0.93, bottom=0.2, hspace=0.8, wspace=0.8)
            for data_type in self.plots:
                coords = self.plots[data_type][0]
                axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                axes.set_xlabel(self.plots[data_type][1])
                axes.tick_params(axis='x', labelrotation=30)
                axes.set_ylabel(self.plots[data_type][2])
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
                axes.plot(data[key][0], data[key][1], label=key)

        @staticmethod
        def __plot_vog(axes, data):
            for key in data:
                axes.scatter(data[key][0], data[key][1], label=key)
