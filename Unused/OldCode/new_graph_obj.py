
from datetime import datetime
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QScrollBar
from PySide2.QtCore import QDate, QTime, QDateTime, Qt
from PySide2.QtGui import QPainter
from PySide2.QtCharts import QtCharts


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
        self.setFixedHeight(400)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.setLayout(QVBoxLayout())

        self.__chart = QtCharts.QChart()
        self.__chart.legend().setVisible(True)
        self.__chart.legend().setAlignment(Qt.AlignBottom)
        self.set_title(self.__name)

        self.__cur_date = QDate(datetime.now().date())
        self.__start_date = QDate(1970, 1, 1)  # Because of stupid Qt designers
        time = QTime(datetime.now().time())
        self.__x_start = QDateTime(self.__start_date, time)

        self.__range_x = [self.__x_start, self.__x_start.addSecs(120)]
        self.__x_axis = QtCharts.QDateTimeAxis()
        self.__x_axis.setFormat("d:h:m:s")
        self.__x_axis.setRange(self.__range_x[0], self.__range_x[1])
        self.__x_axis.setTickCount(6)
        self.__chart.addAxis(self.__x_axis, Qt.AlignBottom)

        self.__range_y = [-1, 500]
        self.__y_axis = QtCharts.QValueAxis()
        self.__y_axis.setRange(self.__range_y[0], self.__range_y[1])
        self.__y_axis.setTickCount(5)
        self.__chart.addAxis(self.__y_axis, Qt.AlignLeft)

        self.__chart_view = QtCharts.QChartView(self.__chart)
        self.__chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout().addWidget(self.__chart_view)

        self.__scroll_bar = self.__create_scroll_bar(self.__move_graph)
        self.layout().addWidget(self.__scroll_bar)

        self.set_axis_names("Timestamp", "Milliseconds")

        self.__min_msecs = self.__range_x[1].toMSecsSinceEpoch()
        self.__last_timestamp = self.__range_x[1]
        self.__biggest_y = 0
        self.__scrolling = False
        self.__x_axis_changed = False

        self.__test_adding_points()

    def add_point(self, name, x, y):
        for series in self.__chart.series():
            if series.name() == name:
                series.append(self.__get_modified_msecs(x), y)
                self.__check_x_axis()
                self.__check_y_axis(y)

    def set_title(self, title):
        self.__chart.setTitle(title)

    def set_axis_names(self, x_name="", y_name=""):
        self.__x_axis.setTitleText(x_name)
        self.__y_axis.setTitleText(y_name)

    def add_line_series(self, name):
        series = QtCharts.QLineSeries()
        series.setName(name)
        series.setPointsVisible(True)
        self.__chart.addSeries(series)
        series.attachAxis(self.__x_axis)
        series.attachAxis(self.__y_axis)

    def reset_graph(self):
        for series in self.__chart.series():
            del series

    def __check_x_axis(self):
        if self.__last_timestamp > self.__range_x[1]:
            self.__x_axis_changed = True
            self.__range_x = [self.__last_timestamp.addSecs(-120), self.__last_timestamp]
        if not self.__scrolling:
            self.__x_axis.setRange(self.__range_x[0], self.__range_x[1])

    def __check_y_axis(self, new_y):
        if new_y > self.__biggest_y:
            self.__biggest_y = new_y + new_y * 0.5
            self.__range_y[1] = self.__biggest_y
            self.__chart.axisY().setRange(self.__range_y[0], self.__range_y[1])

    def __get_modified_msecs(self, timestamp):
        input_to_mod = QDateTime(timestamp.date(), timestamp.time())
        if input_to_mod.date() > self.__cur_date:
            new_date = QDate(input_to_mod.date().year() - self.__cur_date.year() + self.__start_date.year(),
                             input_to_mod.date().month() - self.__cur_date.month() + self.__start_date.month(),
                             input_to_mod.date().day() - self.__cur_date.day() + self.__start_date.day())
            temp_timestamp = QDateTime(new_date, input_to_mod.time())
        else:
            temp_timestamp = QDateTime(self.__start_date, input_to_mod.time())
        if temp_timestamp > self.__last_timestamp:
            self.__last_timestamp = temp_timestamp
        return temp_timestamp.toMSecsSinceEpoch()

    def __move_graph(self):
        if self.__x_axis_changed:
            self.__scrolling = True
            temp_x_start = self.__get_new_x_start_val()
            x_range = (temp_x_start.addSecs(-120), temp_x_start)
            self.__x_axis.setRange(x_range[0], x_range[1])
            if self.__scroll_bar.value() == self.__scroll_bar.maximum():
                self.__scrolling = False

    def __get_new_x_start_val(self):
        scroll_msecs = self.__last_timestamp.toMSecsSinceEpoch() * (self.__scroll_bar.value() / 100)
        ret = QDateTime(1970, 1, 1, 0, 0, 0)
        ret.setMSecsSinceEpoch(max(scroll_msecs, self.__min_msecs))
        return ret

    def __test_adding_points(self):
        self.add_line_series("test_series")
        self.add_line_series("test_series_2")

        time_one = QDateTime(self.__cur_date, datetime.now().time())
        time_two = time_one.addSecs(10)
        time_three = time_two.addDays(6)

        self.add_point("test_series", time_one, 300)
        self.add_point("test_series", time_two, 800)
        self.add_point("test_series", time_three, 0)

        self.add_point("test_series_2", time_one, 600)
        self.add_point("test_series_2", time_two, 200)

        self.reset_graph()

    @staticmethod
    def __create_scroll_bar(func=None):
        scroll_bar = QScrollBar()
        scroll_bar.setOrientation(Qt.Horizontal)
        scroll_bar.setRange(0, 100)
        scroll_bar.setValue(100)
        if func:
            scroll_bar.valueChanged.connect(func)
        return scroll_bar
