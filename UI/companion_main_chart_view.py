from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt


class MainChartWidget(QtCharts.QChart):
    def __init__(self):
        super().__init__()
        self.setTitle("Overview")
        self.bar_sets = {}

        # TODO: Replace these with dynamic device addition
        device_1 = "drt on COM5"
        device_2 = "vog on COM6"
        self.__make_bar_set(device_1, (1, 2, 3, 4, 5, 6))
        self.__make_bar_set(device_2, (5, 0, 0, 4, 0, 7))
        self.num_points = 6

        self.num_visible = 10
        self.range_y = (0, 10)
        self.range_x = (0, 10)
        self.offset = 0
        self.scrolling = False
        self.series = QtCharts.QBarSeries()
        self.series.setBarWidth(1/2)
        self.series.setLabelsVisible(True)
        self.__add_bar_set(device_1)
        self.__add_bar_set(device_2)
        self.addSeries(self.series)
        self.setTitle("Test Overview")
        self.__refresh()
        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

    def __make_bar_set(self, name, values=None):
        self.bar_sets[name] = QtCharts.QBarSet(name)
        if values:
            self.bar_sets[name].append(values)

    def __add_bar_set(self, name):
        self.series.append(self.bar_sets[name])

    def __refresh(self):
        self.createDefaultAxes()
        temp_axis_x = QtCharts.QValueAxis()
        temp_axis_y = QtCharts.QValueAxis()
        temp_axis_x.setTickCount(10)
        if self.range_x[0] <= self.num_points:
            self.range_x = (self.num_points - 10.5, self.num_points)
        temp_axis_x.setRange(self.range_x[0], self.range_x[1])
        temp_axis_y.setRange(self.range_y[0], self.range_y[1])
        self.setAxisX(temp_axis_x, self.series)
        self.setAxisY(temp_axis_y, self.series)

    def __append_point(self, device, point):
        self.bar_sets[device].append(point)
        self.num_points += 1
        if point > self.range_y[1]:
            self.range_y = (0, point)
        if not self.scrolling:
            self.__refresh()

    def handle_msg(self, device, value):
        self.__append_point(device, value)

    def scroll_graph(self, value):
        self.scrolling = True
        if self.num_points > 10:
            temp_range_val = (self.num_points - 10) * (value/100)
            self.createDefaultAxes()
            axis_x = QtCharts.QValueAxis()
            axis_y = QtCharts.QValueAxis()
            axis_x.setRange(temp_range_val - .5, temp_range_val + 10)
            axis_y.setRange(self.range_y[0], self.range_y[1])
            self.setAxisX(axis_x, self.series)
            self.setAxisY(axis_y, self.series)
            if temp_range_val >= self.num_points - 10:
                self.scrolling = False
