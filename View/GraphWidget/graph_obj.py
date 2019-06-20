# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QScrollBar, QFrame, QSizePolicy
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt, QDateTime, QDate, QTime
from datetime import datetime


class GraphObj(QFrame):
    def __init__(self, name):
        super().__init__()
        self.__name = name

        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFixedHeight(300)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.setLayout(QVBoxLayout())

        self.__graph = self.__create_chart(self.__name)
        self.__chart_view = QtCharts.QChartView(self.__graph)
        self.layout().addWidget(self.__chart_view)

        self.__scroll_bar = self.__create_scroll_bar(self.__move_graph)
        self.layout().addWidget(self.__scroll_bar)

        self.__num_points = 0
        self.__x_start = QDateTime(QDate(1970, 1, 1), QTime(datetime.now().time()))
        self.__range_x = [self.__x_start, self.__x_start.addSecs(120)]
        self.__range_y = [-1, 7]
        self.__scrolling = False

    def reset_graph(self):
        self.layout().removeWidget(self.__chart_view)
        self.layout().removeWidget(self.__scroll_bar)
        self.__graph = self.__create_chart(self.__name)
        self.__chart_view = QtCharts.QChartView(self.__graph)
        self.layout().addWidget(self.__chart_view)
        self.layout().addWidget(self.__scroll_bar)

    def set_chart_axes(self, x_title, y_title):
        x_axis = QtCharts.QDateTimeAxis()
        # x_axis = QtCharts.QValueAxis()
        x_axis.setFormat("h:m:s")
        x_axis.setTitleText(x_title)
        x_axis.setRange(self.__range_x[0], self.__range_x[1])
        x_axis.setTickCount(5)
        y_axis = QtCharts.QValueAxis()
        y_axis.setTitleText(y_title)
        y_axis.setRange(self.__range_y[0], self.__range_y[1])
        for axis in self.__graph.axes():
            self.__graph.removeAxis(axis)
            for series in self.__graph.series():
                series.detachAxis(axis)
        self.__graph.addAxis(x_axis, Qt.AlignBottom)
        self.__graph.addAxis(y_axis, Qt.AlignLeft)
        for series in self.__graph.series():
            series.attachAxis(x_axis)
            series.attachAxis(y_axis)

    def add_line_series(self, name):
        self.__graph.addSeries(self.create_line_series(name))

    def add_point(self, name, x, y):
        for series in self.__graph.series():
            if series.name() == name:
                print(x, y)
                series.append(x, y)

    def __move_graph(self):
        self.__scrolling = True
        if self.__num_points > 7:
            temp_range_val = (self.__num_points - 7) * (self.__scroll_bar.value() / 100)
            x_range = (temp_range_val - 1, temp_range_val + 7)
            self.__graph.axisX().setRange(x_range[0], x_range[1])
        if self.__scroll_bar.value() == self.__scroll_bar.maximum():
            self.__scrolling = False

    def __update_axes(self, data, num_points):
        if num_points > self.__range_x[1]:
            self.__range_x[0] += 1
            self.__range_x[1] += 1
            if not self.__scrolling:
                self.__graph.axisX().setRange(self.__range_x[0], self.__range_x[1])
            self.__num_points = num_points
        if data > self.__range_y[1]:  # Update y axis if new data exceeds range
            self.__range_y[1] = data + self.__range_y[1] * 0.2
            self.__graph.axisY().setRange(self.__range_y[0], self.__range_y[1])

    @staticmethod
    def __create_chart(name):
        the_chart = QtCharts.QChart()
        the_chart.setTitle(name)
        the_chart.legend().setVisible(True)
        the_chart.legend().setAlignment(Qt.AlignBottom)
        return the_chart

    @staticmethod
    def __create_scroll_bar(func=None):
        scroll_bar = QScrollBar()
        scroll_bar.setOrientation(Qt.Horizontal)
        scroll_bar.setRange(0, 100)
        scroll_bar.setValue(100)
        scroll_bar.valueChanged.connect(func)
        return scroll_bar

    @staticmethod
    def create_line_series(name):
        the_series = QtCharts.QLineSeries()
        the_series.setName(name)
        the_series.setPointsVisible(True)
        return the_series
