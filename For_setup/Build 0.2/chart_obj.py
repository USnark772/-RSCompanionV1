# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QScrollBar, QFrame, QSizePolicy
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt


class GraphObj(QFrame):
    def __init__(self, name):
        super().__init__()
        self.device_info = name
        self.name = self.__get_device_name(name)

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFixedHeight(300)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.chart = self.__make_chart()
        self.chart_view = QtCharts.QChartView(self.chart)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.chart_view)
        self.scroll_bar = self.__create_scroll_bar(self.__move_graph)
        self.layout().addWidget(self.scroll_bar)

        self.__set_graph_type()
        self.num_points = 0
        self.range_y = [0, 200]
        self.range_x = [-1, 7]
        self.__set_chart_axes()
        self.scrolling = False

    def add_point(self, data):
        if self.device_info[0] == "vog":
            for series in self.chart.series():
                if series.name() == "open":
                    series.append(series.count(), data[0])
                    self.__update_axes(data[0], series.count())
                elif series.name() == "closed":
                    series.append(series.count(), data[1])
                    self.__update_axes(data[1], series.count())
        elif self.device_info[0] == "drt":
            for series in self.chart.series():
                series.append(series.count(), data)
                self.__update_axes(data, series.count())

    def __set_graph_type(self):
        if self.device_info[0] == "vog":
            self.chart.addSeries(self.__create_scatter_series("open"))
            self.chart.addSeries(self.__create_scatter_series("closed"))
        elif self.device_info[0] == "drt":
            self.chart.addSeries(self.__create_line_series(self.name))

    def __set_chart_axes(self):
        x_axis = QtCharts.QValueAxis()
        x_axis.setTitleText("Trial Number")
        x_axis.setRange(self.range_x[0], self.range_x[1])
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

    def __move_graph(self):
        self.scrolling = True
        if self.num_points > 7:
            temp_range_val = (self.num_points - 7) * (self.scroll_bar.value() / 100)
            x_range = (temp_range_val - 1, temp_range_val + 7)
            self.chart.axisX().setRange(x_range[0], x_range[1])
        if self.scroll_bar.value() == self.scroll_bar.maximum():
            self.scrolling = False

    def __update_axes(self, data, num_points):
        if num_points > self.range_x[1]:
            self.range_x[0] += 1
            self.range_x[1] += 1
            if not self.scrolling:
                self.chart.axisX().setRange(self.range_x[0], self.range_x[1])
            self.num_points = num_points
        if data > self.range_y[1]:  # Update y axis if new data exceeds range
            self.range_y[1] = data + self.range_y[1] * 0.2
            self.chart.axisY().setRange(self.range_y[0], self.range_y[1])

    def __make_chart(self):
        show_legend = False
        if self.device_info[0] == "vog":
            show_legend = True
        return self.__create_chart(self.name, show_legend)

    @staticmethod
    def __get_device_name(item):
        ret = str(item[0] + " on " + item[1])
        return ret

    @staticmethod
    def __create_scroll_bar(func=None):
        scroll_bar = QScrollBar()
        scroll_bar.setOrientation(Qt.Horizontal)
        scroll_bar.setRange(0, 100)
        scroll_bar.setValue(100)
        scroll_bar.valueChanged.connect(func)
        return scroll_bar

    @staticmethod
    def __create_chart(title, visible=False, set_of_series=()):
        the_chart = QtCharts.QChart()
        the_chart.setTitle(title)
        the_chart.legend().setVisible(visible)
        the_chart.legend().setAlignment(Qt.AlignBottom)
        for series in set_of_series:
            the_chart.addSeries(series)
        return the_chart

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
    def __create_line_series(name, points=(), i=0):
        the_series = QtCharts.QLineSeries()
        the_series.setObjectName("line_series")
        the_series.setName(name)
        the_series.setPointsVisible(True)
        for point in points:
            the_series.append(the_series.count() + i, point)
        return the_series

    @staticmethod
    def __create_scatter_series(name, points=(), i=0, shape=0):
        the_series = QtCharts.QScatterSeries()
        the_series.setObjectName("scatter_series")
        the_series.setName(name)
        if shape == 1:
            the_series.setMarkerShape(QtCharts.QScatterSeries.MarkerShapeRectangle)
        for point in points:
            the_series.append(the_series.count() + i, point)
        return the_series