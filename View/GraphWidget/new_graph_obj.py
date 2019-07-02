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
        self.__min_height = 200
        self.__height_increment = 200
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout(self))

        self.__canvases = {}
        self.__data = {}

    def add_device(self, device, data_names):
        if device not in self.__data:
            self.__data[device] = {}
            for name in data_names:
                print("Making new data array for:", name)
                self.__data[device][name] = [[], []]
        if device[0] not in self.__canvases:
            self.__add_canvas(device[0])
        self.__canvases[device[0]][1] += 1

    def remove_device(self, device):
        if device in self.__data:
            del self.__data[device]
        if device[0] in self.__canvases:
            self.__canvases[device[0]][1] -= 1
            if self.__canvases[device[0]][1] < 1:
                self.__remove_canvas(device[0])

    def add_data(self, device, data_name, x, y):
        if device in self.__data:
            print(self.__data[device])
            self.__data[device][data_name][0].append(x)
            self.__data[device][data_name][1].append(y)
            self.__plot_graph(device)

    def __plot_graph(self, device):
        if device[0] in self.__canvases:
            self.__plot(device)

    def __add_canvas(self, canvas_type):
        print("Adding canvas")
        if canvas_type == "drt" or canvas_type == "vog":
            axis_names = ("Timestamp", "Milliseconds")
        else:
            axis_names = ("Unknown device", "Unknown device")
        canvas = Canvas(Figure(figsize=(5, 5)))
        self.__canvases[canvas_type] = [canvas, 0, axis_names]
        self.layout().addWidget(canvas)
        self.layout().addWidget(NavBar(canvas, self))
        self.__plot((canvas_type, ""))
        self.__min_height += self.__height_increment
        self.setMinimumHeight(self.__min_height)

    # TODO: Figure out why graph won't disappear
    def __remove_canvas(self, canvas_type):
        if canvas_type in self.__canvases:
            del self.__canvases[canvas_type]
        new_layout = QVBoxLayout(self)
        for canvas in self.__canvases:
            new_layout.addWidget(self.__canvases[canvas][0])
            new_layout.addWidget(NavBar(self.__canvases[canvas][0], self))
        self.setLayout(new_layout)
        self.__min_height -= self.__height_increment
        self.setMinimumHeight(self.__min_height)

    def __plot(self, device):
        title = device[0]
        the_tuple = self.__canvases[title]
        figure = the_tuple[0].figure
        axes = figure.subplots()
        xlabel = the_tuple[2][0]
        ylabel = the_tuple[2][1]
        if device in self.__data:
            data = self.__data[device]
        else:
            data = {}
        axes.clear()
        axes.set_title(title)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        figure.set_tight_layout(True)
        print(data.keys())
        for name in data.keys():
            axes.plot(data[name][0], data[name][1], label=name)
        figure.autofmt_xdate()
        if len(data.keys()) > 0:
            figure.legend(loc='upper left')
        figure.canvas.draw()
