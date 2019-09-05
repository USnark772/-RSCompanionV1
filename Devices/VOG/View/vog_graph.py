""" Licensed under GNU GPL-3.0-or-later """
"""
This file is part of RS Companion.

RS Companion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RS Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RS Companion.  If not, see <https://www.gnu.org/licenses/>.
"""

# Author: Phillip Riskin
# Date: 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from numpy import mean
from View.DisplayWidget.graph import CanvasObj


class VOGGraph(CanvasObj):
    """
    This code is for helping the user visualize the data given by the VOG device.
    Parent class is CanvasObj which handles the basic graphing utility.
    This class handles how to store and interpret data for the graph
    """
    def __init__(self, parent):
        """ Superclass requires reference to parent, title of graph, plot names (types of data) """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__(parent, "vog", ["Time Open/Closed"], self.plot_data)
        self.__data = {}
        # self.__add_mean()
        self.logger.debug("Initialized")

    def plot_data(self, axes, plot_name, show_in_legend):
        """
        Plot data on given axes according to which plot_name.
        show_in_legend determines if adding a label for specific data set.
        """
        self.logger.debug("running")
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
        # line, = axes.plot(self.__data['mean'][0], self.__data['mean'][1], label="mean")
        # lines.append(("mean", line))
        self.logger.debug("done")
        return lines

    def add_device(self, device_port):
        """ Create slots for data associated with device_port """
        self.logger.debug("running")
        self.__data[device_port] = [[], [], []]  # x, y1, y2
        self.logger.debug("done")

    def remove_device(self, device_port):
        """ Remove data associated with device_port """
        self.logger.debug("running")
        del self.__data[device_port]
        self.logger.debug("done")

    def add_data(self, port, data):
        """ Ensure data comes in as x, y1, y2 """
        self.logger.debug("running")
        self.set_new(False)
        self.__data[port][0].append(data[0])
        self.__data[port][1].append(data[1])
        self.__data[port][2].append(data[2])
        # self.__data['mean'] = self.__calc_mean(self.__data)
        self.plot()
        self.logger.debug("done")

    def __add_mean(self):
        """ Add new line to represent mean of data. """
        self.logger.debug("running")
        self.__data['mean'] = [[], []]
        self.logger.debug("done")

    def __calc_mean(self, d, level=0):  # x_range_start, x_range_end, level=0):
        """ Calculate the mean of all data points in data storage. """
        result = [[], []]
        for k, v in d.items():
            if isinstance(v, dict):
                temp = self.__calc_mean(v, level + 1)  # x_range_start, x_range_end, level+1)
                if temp:
                    result += temp
            elif isinstance(v, list):  # {device_type: {data_type: {device_port: [[x], [y]]}}}
                result[0] += v[1]
                result[1] += v[2]
        if len(result) > 0:
            if level == 0:
                ret1 = mean(result[0])
                ret2 = mean(result[1])
                return [ret1, ret2]
            else:
                return result
        return None
