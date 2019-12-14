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
from View.DisplayWidget.graph_nav_bar import MyNavBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class CanvasObj(Canvas):
    """ This code is for graphing data from devices. """
    def __init__(self, parent, title, plot_names, plotter):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__(Figure(figsize=(5, 5)))
        self.setToolTip("Click on legend to show/hide lines. Drag legend to move it")
        self.setToolTipDuration(3000)
        self.__parent = parent
        self.setParent(parent)
        self.__title = title
        self.__plot_names = []
        self.__set_plot_names(plot_names)
        self.__plotter = plotter
        self.__nav_bar = MyNavBar(self, parent)
        self.__nav_bar.update()
        self.__legend_plot_links = {}
        self.__plots = {}  # plot_name: coords, name, active
        self.__set_subplots()
        self.__vlines = []
        #self.figure.canvas.mpl_connect('button_press_event', self.__onclick)
        self.figure.canvas.mpl_connect('pick_event', self.__onpick)
        self.plot(new=True)
        self.__new = True
        self.logger.debug("Initialized")

    def refresh_self(self):
        """ Redraw the canvas. """
        self.logger.debug("running")
        try:
            self.figure.canvas.draw()
        except Exception as e:
            self.logger.exception("issue with drawing canvas.")
        self.logger.debug("done")

    def get_title(self):
        return self.__title

    def set_new(self, is_new):
        """ If graph is new then there is no data to display. """
        self.logger.debug("running")
        self.__new = is_new
        self.logger.debug("done")

    def get_new(self):
        return self.__new

    def __set_plot_names(self, names):
        """ Each plot name will be used to create a graph for a specific data type. """
        self.logger.debug("running")
        for name in names:
            self.__plot_names.append(name)
        self.logger.debug("done")

    def get_nav_bar(self):
        return self.__nav_bar

    def plot(self, new=False):
        """ Reset all subplots to empty then call subclass's plot function for each subplot """
        self.logger.debug("running")
        lines = {}
        self.__legend_plot_links = {}
        self.figure.clear()
        self.figure.set_tight_layout(True)
        i = 0
        for plot_name in self.__plots:  # coords, name, active
            plot = self.__plots[plot_name]
            lines[plot_name] = []
            if plot[1]:
                coords = plot[0]
                axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                axes.tick_params(axis='x', labelrotation=30)
                axes.set_ylabel(plot_name)
                if i == 0:
                    show_in_legend = True
                    axes.set_title(self.__title)
                else:
                    show_in_legend = False
                if i == len(self.__plots) - 1:
                    axes.set_xlabel("Timestamp")
                if not new:
                    lines[plot_name] = self.__plotter(axes, plot_name, show_in_legend)
            i += 1
        if not new:
            legend = self.figure.legend(loc='upper left', framealpha=0.4)
            legend.set_draggable(True)
            self.__match_legend_plot_lines(legend, lines)
            self.add_vert_lines()
        self.figure.canvas.draw()
        self.logger.debug("done")

    def add_vert_lines(self, timestamp=None):
        for axes in self.figure.get_axes():
            if timestamp:
                self.__vlines.append(timestamp)
                axes.axvline(timestamp)
                self.refresh_self()
            else:
                for line in self.__vlines:
                    axes.axvline(line)

    def __match_legend_plot_lines(self, legend, lines):
        """ Attach lines in all subplots to appropriate marker in legend """
        self.logger.debug("running")
        for legend_line in legend.get_lines():
            self.__legend_plot_links[legend_line] = []
            legend_line.set_picker(5)
            for plot in lines:
                for line in lines[plot]:
                    if line[0] == legend_line.get_label():
                        self.__legend_plot_links[legend_line].append(line[1])
        self.logger.debug("done")

    def __set_subplots(self):
        """ Set coords and names of subplots. Must be called after self.__plot_names is set to a list of strings """
        self.logger.debug("running")
        if len(self.__plot_names) < 1:
            return
        r = len(self.__plot_names)
        c = 1
        for i in range(0, r):
            self.__plots[self.__plot_names[i]] = [(r, c, i + 1), True]
        self.logger.debug("done")

    def __onpick(self, event):
        """ show or hide lines in subplots based on which marker in legend was clicked """
        self.logger.debug("running")
        legend_line = event.artist
        if legend_line in self.__legend_plot_links:
            plot_lines = self.__legend_plot_links[legend_line]
        else:
            self.logger.debug("done, no matched lines")
            return
        for line in plot_lines:
            visible = not line.get_visible()
            line.set_visible(visible)
        if visible:
            legend_line.set_alpha(1.0)
        else:
            legend_line.set_alpha(0.2)
        self.figure.canvas.draw()
        self.logger.debug("done")
