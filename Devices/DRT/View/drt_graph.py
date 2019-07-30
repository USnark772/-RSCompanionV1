# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from View.DisplayWidget.graph import CanvasObj


class DRTGraph(CanvasObj):
    def __init__(self, parent):
        """ Superclass requires reference to parent, title of graph, plot names (types of data) """
        self.__plot_names = ["Response Time", "Clicks"]
        super().__init__(parent, "drt", self.__plot_names, self.plot_data)
        self.__data = {}

    def plot_data(self, axes, plot_name, show_in_legend):
        """
        Plot data on given axes according to which plot_name.
        show_in_legend determines if adding a legend line for specific data set
        """
        data = self.__data[plot_name]
        lines = []
        for port in data:
            if show_in_legend:
                the_label = port
            else:
                the_label = "_nolegend_"
            line, = axes.plot(data[port][0], data[port][1], label=the_label, marker='o')
            lines.append((port, line))
        return lines

    def add_device(self, device_port):
        """ Create slots for data associated with device_port """
        for name in self.__plot_names:
            self.__data[name] = {}
            self.__data[name][device_port] = [[], []]

    def remove_device(self, device_port):
        """ Remove data associated with device_port """
        for name in self.__plot_names:
            del self.__data[name][device_port]

    def add_data(self, port, data):
        """ Ensure data comes in as type, x, y """
        self.__data[data[0]][port][0].append(data[1])
        self.__data[data[0]][port][1].append(data[2])
        self.plot()
