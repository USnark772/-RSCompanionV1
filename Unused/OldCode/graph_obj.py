# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from datetime import datetime
from numpy import mean
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
from matplotlib.dates import num2date, DateFormatter


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
        self.__canvases = {}  # {device_type: [canvas, nav_bar, activity_button, is_active]}

    def add_device(self, device, data_types):
        device_type = device[0]
        device_port = device[1]
        if device_type not in self.__canvases:
            self.__add_canvas(device_type, data_types)
        self.__canvases[device_type].add_device(device_port)

    def remove_device(self, device):
        device_type = device[0]
        device_port = device[1]
        if device_type in self.__canvases:
            self.__canvases[device_type].remove_device(device_port)
        if self.__canvases[device_type].check_removal():
            self.__remove_canvas(device_type)

    def add_data(self, device, data_type, x, y):
        device_type = device[0]
        device_port = device[1]
        print("Adding data to self.__canvases")
        if device_type in self.__canvases:
            self.__canvases[device_type].add_data(data_type, device_port, x, y)

    def set_device_data_type_activity(self, device, data_type, is_active):
        device_type = device[0]
        device_port = device[1]
        if device_type in self.__canvases:
            self.__canvases[device_type].set_line_activity(data_type, device_port, is_active)

    def resize_layout(self, bigger=False):
        if bigger:
            self.__min_height += self.__height_increment
            self.setMinimumHeight(self.__min_height)
        else:
            self.__min_height -= self.__height_increment
            self.setMinimumHeight(self.__min_height)

    def __add_canvas(self, device_type, data_types):
        canvas = CanvasObj(self, device_type, data_types)
        self.__canvases[device_type] = canvas
        self.layout().addWidget(canvas)
        self.layout().addWidget(canvas.nav_bar)
        self.resize_layout(True)

    def __remove_canvas(self, canvas_type):
        if canvas_type in self.__canvases:
            self.layout().removeWidget(self.__canvases[canvas_type])
            self.layout().removeWidget(self.__canvases[canvas_type].nav_bar)
            self.__canvases[canvas_type].nav_bar.deleteLater()
            self.__canvases[canvas_type].deleteLater()
            del self.__canvases[canvas_type]
            self.resize_layout()
            for device_type in self.__canvases:
                self.__canvases[device_type].refresh()


class CanvasObj(Canvas):
    def __init__(self, parent, device_type, data_types):
        super().__init__(Figure(figsize=(5, 5)))
        self.__parent = parent
        self.setParent(parent)
        self.__title = device_type
        self.is_active = True
        self.nav_bar = MyNavBar(self, parent)
        self.__legend_plot_links = {}
        self.__lines = {}  # {device_port: [is_active, line1, line2, ...]
        self.__data = {}
        self.__plots = {}  # sub_type: coords, xlabel, ylabel, active, legend
        self.set_subplots(data_types)
        self.__setup_data(data_types)
        #self.figure.canvas.mpl_connect('button_press_event', self.__onclick)
        #self.figure.canvas.mpl_connect('pick_event', self.__onpick)
        self.__plot(new=True)

    def set_title(self, title):
        self.__title = title

    def refresh(self):
        pass

    def add_device(self, device_port):
        self.__lines[device_port] = [True]
        for data_type in self.__data:
            self.__data[data_type][device_port] = [[], []]

    def remove_device(self, device_port):
        del self.__lines[device_port]
        for data_type in self.__data:
            del self.__data[data_type][device_port]

    def add_data(self, data_type, device_port, x, y):
        print("Adding data in CanvasObj")
        self.__data[data_type][device_port][0].append(x)
        self.__data[data_type][device_port][1].append(y)
        print("Added to self.__data")
        print("Mean of", data_type, "is:", self.__calc_mean(self.__data[data_type]))
        if self.__data[data_type][device_port][2]:
            self.__plot(self.__data)

    def set_line_activity(self, data_type, device_port, is_active):
        self.__data[data_type][device_port][2] = is_active

    '''
    -   The onclick event has attributes x and y carrying the pixel coordinates from the corner of the figure
    -   These coordinates can be converted into figure coordinates by using 
        fig.transFigure.inverted().transform((x,y))
    -   You can get the bounding box of each subplot by bb=ax.get_position()
    -   iterate through all subplots (axes) of the image
    -   you can test whether the click is within the area of this bounding box by bb.contains(fx,fy), where fx and 
        fy are the button click coordinates transformed into image position
    '''
    def __onpick(self, event):
        legend_line = event.artist
        plot_line = self.__legend_plot_links[legend_line]
        vis = not plot_line.get_visible()
        plot_line.set_visible(vis)
        if vis:
            legend_line.set_alpha(1.0)
        else:
            legend_line.set_alpha(0.2)
        self.figure.canvas.draw()

    def __onclick(self, event):
        if event.xdata and event.xdata < 1:
            return
        print(event.xdata, event.ydata)
        converted_coords = self.figure.transFigure.inverted().transform((event.x, event.y))
        the_subplot = None
        for subplot in self.figure.get_axes():
            plot_bounding_box = subplot.get_position()
            if plot_bounding_box.contains(converted_coords[0], converted_coords[1]):
                the_subplot = subplot
                break
        if the_subplot:
            print(num2date(event.xdata), event.y, the_subplot.title)

    def __match_leglines_to_plotlines(self):
        legend = self.figure.legend(loc='upper left')
        for legline, origline in zip(legend.get_lines(), self.__lines):
            legline.set_picker(5)  # 5 pts tolerance
            self.__legend_plot_links[legline] = origline

    def __plot(self, data=None, new=False):
        self.figure.clear()
        self.figure.set_tight_layout(True)
        i = 0
        for data_type in self.__plots:
            if self.__plots[data_type][3]:
                coords = self.__plots[data_type][0]
                axes = self.figure.add_subplot(coords[0], coords[1], coords[2])
                axes.tick_params(axis='x', labelrotation=30)
                axes.set_ylabel(self.__plots[data_type][2])
                if i == 0:
                    axes.set_title(self.__title)
                elif i == len(self.__plots) - 1:
                    axes.set_xlabel(self.__plots[data_type][1])
                if not new:
                    print("Plotting data")
                    if i == 0:
                        self.__plot_device_type(axes, data_type, False)
                    else:
                        self.__plot_device_type(axes, data_type)
                i += 1
        self.__match_leglines_to_plotlines()
        self.figure.canvas.draw()

    def __setup_data(self, data_types):
        for element in data_types:
            self.__data[element] = {}

    def set_subplots(self, data_types):
        r = len(data_types)
        c = 1
        ts_label = "Timestamp"
        print("set_subplots, r =:", r)
        for i in range(0, r):
            print("set_subplots loop")
            self.__plots[data_types[i]] = [(r, c, i + 1), ts_label, data_types[i], True]

    def __toggle_plot_activity(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.show()
            self.nav_bar.show()
            self.toggle_graph_button.setText("Hide " + self.__title + " graph")
            self.__parent.resize_layout(True)
        else:
            self.hide()
            self.nav_bar.hide()
            self.toggle_graph_button.setText("Show " + self.__title + " graph")
            self.__parent.resize_layout()

    def __calc_mean(self, d, level=0):  # x_range_start, x_range_end, level=0):
        result = []
        for k, v in d.items():
            if isinstance(v, dict):
                temp = self.__calc_mean(v, level + 1)  # x_range_start, x_range_end, level+1)
                if temp:
                    result += temp
            elif isinstance(v, list):  # {device_type: {data_type: {device_port: [[x], [y], is_active, artist]}}}
                result += v[1]
        if len(result) > 0:
            if level == 0:
                ret = mean(result)
                return ret
            else:
                return result
        return None

    def __plot_device_type(self, axes, data_type, draw_label=True):
        if self.__title == "drt":
            self.__plot_drt(axes, data_type, draw_label)
        elif self.__title == "vog":
            self.__plot_vog(axes, data_type, draw_label)

    def __plot_drt(self, axes, data_type, draw_label):
        for key in self.__data[data_type]:
            if not draw_label:
                self.__lines[key] = axes.plot(self.__data[key][0], self.__data[key][1], label=key,
                                              visible=self.__data[key][2], marker='o')
            else:
                self.__lines[key] = axes.plot(self.__data[key][0], self.__data[key][1], visible=self.__data[key][2],
                                              marker='o')

    def __plot_vog(self, axes, data_type, draw_label):
        for key in self.__data[data_type]:
            if not draw_label:
                self.__lines[key] = axes.plot(self.__data[key][0], self.__data[key][1], label=key,
                                              visible=self.__data[key][2], marker='o', linestyle='None')
            else:
                self.__lines[key] = axes.plot(self.__data[key][0], self.__data[key][1], visible=self.__data[key][2],
                                              marker='o', linestyle='None')


class MyNavBar(NavBar):
    def __init__(self, figure, figure_parent):
        super().__init__(figure, figure_parent)
