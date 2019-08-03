# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from numpy import mean
from View.DisplayWidget.graph import CanvasObj


class DRTGraph(CanvasObj):
    def __init__(self, parent):
        """ Superclass requires reference to parent, title of graph, plot names (types of data) """
        self.__plot_names = ["Response Time", "Clicks"]
        super().__init__(parent, "drt", self.__plot_names, self.plot_data)
        self.__data = {}
        for name in self.__plot_names:
            self.__data[name] = {}
        # self.__add_mean()

    def plot_data(self, axes, plot_name, show_in_legend):
        """
        Plot data on given axes according to which plot_name.
        show_in_legend determines if adding a legend line for specific data set
        """
        data = self.__data[plot_name]
        # mean = self.__data[plot_name]['mean']
        lines = []
        for port in data:
            if show_in_legend:
                the_label = port
            else:
                the_label = "_nolegend_"
            line, = axes.plot(data[port][0], data[port][1], label=the_label, marker='o')
            lines.append((port, line))
        # line, = axes.plot(mean[0], mean[1], label='mean')
        # lines.append(("mean", line))
        return lines

    def add_device(self, device_port):
        """ Create slots for data associated with device_port """
        for name in self.__plot_names:
            self.__data[name][device_port] = [[], []]

    def remove_device(self, device_port):
        """ Remove data associated with device_port """
        for name in self.__plot_names:
            del self.__data[name][device_port]

    def add_data(self, port, port_data):
        """ Ensure data comes in as type, x, y """
        self.set_new(False)
        self.__data[port_data[0]][port][0].append(port_data[1])
        self.__data[port_data[0]][port][1].append(port_data[2])
        # self.__calc_mean(self.__data[port_data[0]])
        self.plot()

    def __add_mean(self):
        for name in self.__plot_names:
            self.__data[name]['mean'] = [[], []]

    def __calc_mean(self, d, level=0):  # x_range_start, x_range_end, level=0):
        result = []
        for k, v in d.items():
            if isinstance(v, dict):
                temp = self.__calc_mean(v, level + 1)  # x_range_start, x_range_end, level+1)
                if temp:
                    result += temp
            elif isinstance(v, list):  # {device_type: {data_type: {device_port: [[x], [y]]}}}
                result += v[1]
        if len(result) > 0:
            if level == 0:
                ret = mean(result)
                return ret
            else:
                return result
        return None