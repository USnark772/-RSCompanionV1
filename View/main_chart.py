# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt

# TODO: Each device draws lines back to start when running multiple blocks
# TODO: Make user able to choose graphing type (Bar, line, etc.)
# TODO: update graph without needing a device plugged in
class MainChartWidget(QtCharts.QChart):
    def __init__(self):
        super().__init__()
        self.setTitle("Overview")
        # self.bar_sets = {}
        self.lines = {}

        self.num_points = 0
        self.range_y = (-1, 10)
        self.range_x = (0, 10)
        self.scrolling = False
        # self.bar_series = QtCharts.QBarSeries()
        # self.bar_series.setBarWidth(1 / 2)
        # self.bar_series.setLabelsVisible(True)
        # self.__add_bar_set(device_1)
        # self.__add_bar_set(device_2)
        # self.addSeries(self.bar_series)
        self.setTitle("Test Overview")
        self.__refresh()
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

    #def __make_bar_set(self, name, values=None):
    #    self.bar_sets[name] = QtCharts.QBarSet(name)
    #    if values:
    #        self.bar_sets[name].append(values)

    def __make_line_series(self, name, values=None):
        self.lines[name] = QtCharts.QLineSeries()
        self.lines[name].setName(name)
        self.lines[name].setPointsVisible()
        if values:
            for value in values:
                self.lines[name].append(value[0], value[1])
        self.addSeries(self.lines[name])
        self.__refresh()

    #def __add_bar_set(self, name):
    #    self.bar_series.append(self.bar_sets[name])

    def __refresh(self):
        self.createDefaultAxes()
        temp_axis_x = QtCharts.QValueAxis()
        temp_axis_y = QtCharts.QValueAxis()
        temp_axis_y.setTickInterval(100)
        temp_axis_x.setTickCount(10)
        if self.range_x[0] <= self.num_points and self.num_points > 10:
            self.range_x = (self.num_points - 10.5, self.num_points)
        else:
            self.range_x = (0, 10)
        temp_axis_x.setRange(self.range_x[0], self.range_x[1])
        temp_axis_y.setRange(self.range_y[0], self.range_y[1])
        #self.setAxisX(temp_axis_x, self.bar_series)
        #self.setAxisY(temp_axis_y, self.bar_series)
        for line in self.lines:
            self.setAxisX(temp_axis_x, self.lines[line])
            self.setAxisY(temp_axis_y, self.lines[line])

    def __append_point(self, device, point):
        print("companion_main_chart_view.MainChartWidget.__append_point() point = ",
              int(point[0]), int(point[1]))
        self.lines[device].append(int(point[0]), int(point[1]))
        if int(point[1]) > self.range_y[1]:
            self.range_y = (-1, int(point[1]))
        if int(point[0]) > self.num_points:
            self.num_points = int(point[0])
        if not self.scrolling:
            self.__refresh()

    def __append_point_old(self, device, point):
        self.bar_sets[device].append(point)
        self.num_points += 1
        if point > self.range_y[1]:
            self.range_y = (-1, point)
        if not self.scrolling:
            self.__refresh()

    def handle_msg(self, msg_dict):
        # TODO: Handle msg better
        name = msg_dict['device'][0] + " on " + msg_dict['device'][1]
        self.__append_point(name, (msg_dict['trial'], msg_dict['rt']))

    def add_device(self, device):
        name = device[0] + " on " + device[1]
        self.__make_line_series(name)

    def scroll_graph(self, value):
        self.scrolling = True
        if self.num_points > 10:
            temp_range_val = (self.num_points - 10) * (value/100)
            self.createDefaultAxes()
            axis_x = QtCharts.QValueAxis()
            axis_y = QtCharts.QValueAxis()
            axis_x.setRange(temp_range_val - .5, temp_range_val + 10)
            axis_y.setRange(self.range_y[0], self.range_y[1])
            #self.setAxisX(axis_x, self.bar_series)
            #self.setAxisY(axis_y, self.bar_series)
            for line in self.lines:
                self.setAxisX(axis_x, self.lines[line])
                self.setAxisY(axis_y, self.lines[line])
            if temp_range_val >= self.num_points - 10:
                self.scrolling = False
