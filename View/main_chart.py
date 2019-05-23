# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QScrollBar, QWidget
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt
from Model.device_graph_rep import DeviceGraphData
import Model.defs as defs


class MainChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())

        self.chart = self.__create_chart("Data Overview")
        self.chart_view = QtCharts.QChartView(self.chart)
        self.layout().addWidget(self.chart_view)

        self.scroll_bar = self.__create_scroll_bar()
        self.scroll_bar.valueChanged.connect(self.__move_graph)
        self.layout().addWidget(self.scroll_bar)

        self.data_reps = []  # To keep track of data for each device for creation of bars or lines

        self.num_points = 0
        self.range_y = [-1, 200]
        self.range_x = [0, 7]
        self.__set_chart_axes()
        self.scrolling = False

    def __add_data_point(self, device, data):
        start_index = 0
        for rep in self.data_reps:  # Save data point
            if rep.name() == device:
                rep.add_point(data)
                start_index = rep.get_start_index()
        for item in self.chart.series():  # Update graph with point
            if item.objectName() == "line_series":
                if item.name() == device:
                    item.append(item.count(), data)
                    self.__update_axes(data, item.count())
                    return True
            elif item.objectName() == "scatter_series":
                if item.name() == device:
                    item.append(item.count() + start_index, data)
                    self.__update_axes(data, item.count())
                    return True
            elif item.objectName() == "stacked_bar_series":
                for item2 in item.barSets():
                    if item2.label() == device:
                        item2.append(data)
                        self.__update_axes(data, item2.count())
                        return True
        return False

    def __update_axes(self, data, num_points):
        if num_points > self.range_x[1]:
            self.range_x[0] += 1
            self.range_x[1] += 1
            self.__set_chart_axes()
            self.num_points = num_points
        if data > self.range_y[1]:  # Update y axis if new data exceeds range
            self.range_y[1] = data + self.range_y[1] * 0.2
            self.__set_chart_axes()

    def __create_rep_as_stacked_bar_series(self, rep):
        bar_series = self.__create_stacked_bar_series()
        bar_set = [self.__create_bar_set(rep.name() + " open", rep.get_points(), rep.get_start_index()),
                   self.__create_bar_set(rep.name() + " closed", rep.get_points(), rep.get_start_index())]
        bar_series.append(bar_set)
        self.chart.addSeries(bar_series)
        self.__set_chart_axes()

    def __create_rep_as_scatter_series(self, rep, shape=0):
        the_series = self.__create_scatter_series(rep.name(), rep.get_points(), rep.get_start_index(), shape)
        self.chart.addSeries(the_series)
        self.__set_chart_axes()

    def handle_msg(self, msg_dict):
        name = self.__get_device_name(msg_dict['device'])
        if msg_dict['device'][0] == "drt":
            self.__add_data_point(name, int(msg_dict['rt']))
        elif msg_dict['device'][0] == "vog":
            mil_opened = msg_dict[defs.vog_block_field[1]]
            mil_closed = msg_dict[defs.vog_block_field[2]]
            self.__add_data_point(name + " open", int(mil_opened))
            self.__add_data_point(name + " closed", int(mil_closed))

    def add_device(self, device):
        name = self.__get_device_name(device)
        if device[0] == "drt":
            rep = DeviceGraphData(name, self.num_points)
            self.data_reps.append(rep)
            self.__create_rep_as_scatter_series(rep, 0)
        elif device[0] == "vog":
            rep = DeviceGraphData(name + " open", self.num_points)
            self.data_reps.append(rep)
            rep2 = DeviceGraphData(name + " closed", self.num_points)
            self.data_reps.append(rep2)
            self.__create_rep_as_scatter_series(rep, 1)
            self.__create_rep_as_scatter_series(rep2, 1)

    def __move_graph(self):
        if self.num_points > 7:
            temp_range_val = (self.num_points - 7) * (self.scroll_bar.value() / 100)
            x_range = (temp_range_val - 1, temp_range_val + 7)
            self.chart.axisX().setRange(x_range[0], x_range[1])

    def __set_chart_axes(self):
        x_axis = QtCharts.QValueAxis()
        x_axis.setTitleText("Trial Number")
        x_axis.setRange(self.range_x[0] - 1, self.range_x[1])
        x_axis.setTickInterval(1)
        x_axis.setTickCount(9)
        y_axis = QtCharts.QValueAxis()
        y_axis.setTitleText("Milliseconds Elapsed")
        y_axis.setRange(self.range_y[0], self.range_y[1])
        for axis in self.chart.axes():
            self.chart.removeAxis(axis)
            for series in self.chart.series():
                series.detachAxis(axis)
        self.chart.addAxis(x_axis, Qt.AlignBottom)
        self.chart.addAxis(y_axis, Qt.AlignLeft)
        for series in self.chart.series():
            series.attachAxis(x_axis)
            series.attachAxis(y_axis)

    @staticmethod
    def __create_bar_set(name, vals, i):
        prev_vals = []
        the_set = QtCharts.QBarSet(name)
        the_set.setObjectName("bar_set")
        for b in range(i):
            prev_vals.append(0)
        the_set.append(prev_vals)
        the_set.append(vals)
        return the_set

    @staticmethod
    def __create_bar_series(sets=()):
        the_series = QtCharts.QBarSeries()
        the_series.setObjectName("bar_series")
        for item in sets:
            the_series.append(item)
        return the_series

    @staticmethod
    def __create_stacked_bar_series(sets=()):
        the_series = QtCharts.QStackedBarSeries()
        the_series.setObjectName("stacked_bar_series")
        for item in sets:
            the_series.append(item)
        return the_series

    @staticmethod
    def __create_line_series(name, points, i):
        the_series = QtCharts.QLineSeries()
        the_series.setObjectName("line_series")
        the_series.setName(name)
        for point in points:
            the_series.append(the_series.count() + i, point)
        return the_series

    @staticmethod
    def __create_scatter_series(name, points, i, shape):
        the_series = QtCharts.QScatterSeries()
        the_series.setObjectName("scatter_series")
        the_series.setName(name)
        if shape == 1:
            the_series.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeRectangle)
        for point in points:
            the_series.append(the_series.count() + i, point)
        return the_series

    @staticmethod
    def __create_chart(title, set_of_series=()):
        the_chart = QtCharts.QChart()
        the_chart.setTitle(title)
        the_chart.legend().setVisible(True)
        the_chart.legend().setAlignment(Qt.AlignBottom)
        for series in set_of_series:
            the_chart.addSeries(series)
        return the_chart

    @staticmethod
    def __create_scroll_bar():
        scroll_bar = QScrollBar()
        scroll_bar.setOrientation(Qt.Horizontal)
        scroll_bar.setRange(0, 100)
        scroll_bar.setValue(100)
        return scroll_bar

    @staticmethod
    def __get_device_name(item):
        ret = str(item[0] + " on " + item[1])
        return ret
