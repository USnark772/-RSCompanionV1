# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from View.DisplayWidget.graph_nav_bar import MyNavBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class CanvasObj(Canvas):
    def __init__(self, parent, title, plot_names, plotter):
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
        #self.figure.canvas.mpl_connect('button_press_event', self.__onclick)
        self.figure.canvas.mpl_connect('pick_event', self.__onpick)
        self.plot(new=True)
        self.__new = True

    def refresh_self(self):
        self.figure.canvas.draw()

    def get_title(self):
        return self.__title

    def set_new(self, is_new):
        self.__new = is_new

    def __set_plot_names(self, names):
        for name in names:
            self.__plot_names.append(name)

    def get_nav_bar(self):
        return self.__nav_bar

    def plot(self, new=False):
        """ Reset all subplots to empty then call subclass's plot function for each subplot """
        lines = {}
        self.__legend_plot_links = {}
        self.figure.clear()
        self.figure.set_tight_layout(True)
        i = 0
        for key in self.__plots:  # coords, name, active
            plot = self.__plots[key]
            lines[plot[1]] = []
            if plot[2]:
                coords = plot[0]
                axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                axes.tick_params(axis='x', labelrotation=30)
                axes.set_ylabel(plot[1])
                if i == 0:
                    show_in_legend = True
                    axes.set_title(self.__title)
                else:
                    show_in_legend = False
                if i == len(self.__plots) - 1:
                    axes.set_xlabel("Timestamp")
                if not new:
                    lines[plot[1]] = self.__plotter(axes, plot[1], show_in_legend)
            i += 1
        if not new:
            legend = self.figure.legend(loc='upper left', framealpha=0.4)
            legend.set_draggable(True)
            self.__match_legend_plot_lines(legend, lines)
        self.figure.canvas.draw()

    def __match_legend_plot_lines(self, legend, lines):
        """ Attach lines in all subplots to appropriate marker in legend """
        for legend_line in legend.get_lines():
            self.__legend_plot_links[legend_line] = []
            legend_line.set_picker(5)
            for plot in lines:
                for line in lines[plot]:
                    if line[0] == legend_line.get_label():
                        self.__legend_plot_links[legend_line].append(line[1])

    def __set_subplots(self):
        """ Set coords and names of subplots. Must be called after self.__plot_names is set to a list of strings """
        if len(self.__plot_names) < 1:
            return
        r = len(self.__plot_names)
        c = 1
        for i in range(0, r):
            self.__plots[self.__plot_names[i]] = [(r, c, i + 1), self.__plot_names[i], True]

    def __onpick(self, event):
        """ show or hide lines in subplots based on which marker in legend was clicked """
        legend_line = event.artist
        plot_lines = self.__legend_plot_links[legend_line]
        for line in plot_lines:
            visible = not line.get_visible()
            line.set_visible(visible)
        if visible:
            legend_line.set_alpha(1.0)
        else:
            legend_line.set_alpha(0.2)
        self.figure.canvas.draw()
