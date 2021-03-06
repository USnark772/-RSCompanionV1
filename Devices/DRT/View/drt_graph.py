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
from datetime import datetime, timedelta
from numpy import mean
from View.DisplayWidget.graph import CanvasObj


class DRTGraph(CanvasObj):
    """
    This code is for helping the user visualize the data given by the DRT device.
    Parent class is CanvasObj which handles the basic graphing utility.
    This class handles how to store and interpret data for the graph
    """
    def __init__(self, parent, ch):
        """ Superclass requires reference to parent, title of graph, plot names (types of data) """
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.__plot_names = ["Response Time", "Clicks"]
        super().__init__(parent, "DRT", self.__plot_names, self.plot_data)
        self.__data = {}
        for name in self.__plot_names:
            self.__data[name] = {}
        # self.__add_mean()
        self.logger.debug("Initialized")

    def plot_data(self, axes, plot_name, show_in_legend):
        """
        Plot data on given axes according to which plot_name.
        show_in_legend determines if adding a legend line for specific data set
        """
        self.logger.debug("running")
        data = self.__data[plot_name]
        # mean = self.__data[plot_name]['mean']
        lines = []
        left = datetime.now()
        right = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for port in data:
            if show_in_legend:
                the_label = port
            else:
                the_label = "_nolegend_"
            line, = axes.plot(data[port][0], data[port][1], label=the_label, marker='o')
            lines.append((port, line))
            if len(data[port][0]) > 0:
                if right < data[port][0][-1]:
                    right = data[port][0][-1]
                if left > data[port][0][0]:
                    left = data[port][0][0]
        if left < right - timedelta(minutes=2):
            left = right - timedelta(minutes=2)
        axes.set_xlim(left=left - timedelta(seconds=10), right=right + timedelta(seconds=10))
        # line, = axes.plot(mean[0], mean[1], label='mean')
        # lines.append(("mean", line))
        self.logger.debug("done")
        return lines

    def add_device(self, device_port):
        """ Create slots for data associated with device_port """
        self.logger.debug("running")
        for name in self.__plot_names:
            self.__data[name][device_port] = [[], []]
        self.logger.debug("done")

    def remove_device(self, device_port):
        """ Remove data associated with device_port """
        self.logger.debug("running")
        for name in self.__plot_names:
            del self.__data[name][device_port]
        self.logger.debug("done")

    def add_data(self, port, port_data):
        """ Ensure data comes in as type, x, y """
        self.logger.debug("running")
        self.set_new(False)
        self.__data[port_data[0]][port][0].append(port_data[1])
        self.__data[port_data[0]][port][1].append(port_data[2])
        # self.__calc_mean(self.__data[port_data[0]])
        self.plot()
        self.logger.debug("done")

    def add_empty_point(self, timestamp):
        if self.get_new():
            return
        for port_data in self.__data.values():
            for port in port_data.values():
                port[0].append(timestamp)
                port[1].append(None)
        self.refresh_self()

    def __add_mean(self):
        """ Add new line to represent mean of data. """
        self.logger.debug("running")
        for name in self.__plot_names:
            self.__data[name]['mean'] = [[], []]
        self.logger.debug("done")

    def __calc_mean(self, d, level=0):  # x_range_start, x_range_end, level=0):
        """ Calculate the mean of all data points in data storage. """
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
