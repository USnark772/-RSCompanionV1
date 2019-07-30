# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from View.DisplayWidget.graph import CanvasObj


class VOGGraph(CanvasObj):
    def __init__(self, parent):
        """ Superclass requires reference to parent, title of graph, plot names (types of data) """
        super().__init__(parent, "vog", ["Time Open/Closed"], self.plot_data)
        self.__data = {}

    def plot_data(self, axes, plot_name, show_in_legend):
        """
        Plot data on given axes according to which plot_name.
        show_in_legend determines if adding a label for specific data set.
        """
        lines = []
        for port in self.__data:
            the_label_open = port + " open"
            the_label_closed = port + " closed"
            line1, = axes.plot(self.__data[port][0], self.__data[port][1], label=the_label_open, marker='o',
                               linestyle='None')
            line2, = axes.plot(self.__data[port][0], self.__data[port][2], color=line1.get_color(),
                               label=the_label_closed, marker='s', linestyle='None')  # color=line1.get_color()
            lines.append((the_label_open, line1))
            lines.append((the_label_closed, line2))
        return lines

    def add_device(self, device_port):
        """ Create slots for data associated with device_port """
        self.__data[device_port] = [[], [], []]  # x, y1, y2

    def remove_device(self, device_port):
        """ Remove data associated with device_port """
        del self.__data[device_port]

    def add_data(self, port, data):
        """ Ensure data comes in as x, y1, y2 """
        self.__data[port][0].append(data[0])
        self.__data[port][1].append(data[1])
        self.__data[port][2].append(data[2])
        self.plot()
