from PySide2.QtWidgets import QApplication, QMainWindow, QScrollBar, QVBoxLayout, QWidget
from PySide2.QtCore import QPoint, Qt, QTimer
from PySide2.QtCharts import QtCharts
import sys


def create_bar_set(name="default", vals=(), i=0):
    prev_vals = []
    the_set = QtCharts.QBarSet(name)
    the_set.setObjectName("bar_set")
    for b in range(i):
        prev_vals.append(0)
    the_set.append(prev_vals)
    the_set.append(vals)
    return the_set


def create_bar_series(sets=()):
    the_series = QtCharts.QBarSeries()
    the_series.setObjectName("bar_series")
    for set in sets:
        the_series.append(set)
    return the_series


def create_line_series(name, points):
    the_series = QtCharts.QLineSeries()
    the_series.setObjectName("line_series")
    the_series.setName(name)
    for point in points:
        the_series.append(the_series.count(), point)
    return the_series


def create_chart(title, set_of_series):
    the_chart = QtCharts.QChart()
    the_chart.setTitle(title)
    the_chart.legend().setVisible(True)
    the_chart.legend().setAlignment(Qt.AlignBottom)
    for series in set_of_series:
        the_chart.addSeries(series)
    return the_chart


'''
def set_chart_axis(the_chart, categories, range):
x_axis = QtCharts.QBarCategoryAxis()
x_axis.append(categories)
x_axis.setRange(range[0], range[1])
'''
def set_chart_axis(the_chart, x_range):
    x_axis = QtCharts.QValueAxis()
    x_axis.setTitleText("Trial Number")
    x_axis.setRange(x_range[0] - 1, x_range[1])
    x_axis.setTickInterval(1)
    x_axis.setTickCount(9)
    y_axis = QtCharts.QValueAxis()
    y_axis.setTitleText("Milliseconds Elapsed")
    y_axis.setRange(-1, 21)
    for axis in the_chart.axes():
        the_chart.removeAxis(axis)
        for series in the_chart.series():
            series.detachAxis(axis)
    the_chart.addAxis(x_axis, Qt.AlignBottom)
    the_chart.addAxis(y_axis, Qt.AlignLeft)
    for series in the_chart.series():
        series.attachAxis(x_axis)
        series.attachAxis(y_axis)


def add_data_point(device, data, set):
    for item in set:
        if item.objectName() == "line_series":
            if item.name() == device:
                item.append(item.count(), data)
                return True
        elif item.objectName() == "bar_series":
            for item2 in item.barSets():
                if item2.label() == device:
                    item2.append(data)
                    return True
    return False


class ChartExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        self.central_widget = QWidget(self)
        self.vert_layout = QVBoxLayout(self)
        self.central_widget.setLayout(self.vert_layout)
        self.chart_scroll_bar = QScrollBar()
        self.chart_scroll_bar.setOrientation(Qt.Horizontal)
        self.chart_scroll_bar.setRange(0, 100)
        self.chart_scroll_bar.valueChanged.connect(self.__move_graph)

        self.num_points = 0
        self.bar_sets = []
        self.set_of_series = []
        self.bar_set_data = (("Jane", (1, 2, 3, 4, 5, 6)),
                        ("John", (5, 0, 0, 4, 0, 7)),
                        ("Axel", (3, 5, 8, 13, 8, 5)),
                        ("Mary", (5, 6, 7, 3, 4, 5)))
        self.additional_bar_set = ("Sam", (9, 7, 5, 3, 1, 2))
        self.num_points = 12
        for item in self.bar_set_data:
            self.bar_sets.append(create_bar_set(item[0], item[1]))

        self.bar_series = create_bar_series(self.bar_sets)
        self.set_of_series.append(self.bar_series)
        self.line_series = create_line_series("trend", (4, 15, 20, 4, 12, 17))
        self.set_of_series.append(self.line_series)

        self.chart_obj = create_chart("Line and barchart example", self.set_of_series)

        # self.categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        x_range = (0, 7)
        # set_chart_axis(self.chart_obj, self.categories, range)
        set_chart_axis(self.chart_obj, x_range)

        self.chart_view = QtCharts.QChartView(self.chart_obj)

        self.vert_layout.addWidget(self.chart_view)
        self.vert_layout.addWidget(self.chart_scroll_bar)

        self.setCentralWidget(self.central_widget)
        self.show()

    def __move_graph(self):
        temp_range_val = (self.num_points - 7) * (self.chart_scroll_bar.value() / 100)
        x_range = (temp_range_val, temp_range_val + 7)
        set_chart_axis(self.chart_obj, x_range)

    def change(self):
        print("Change called")
        self.bar_sets = []
        self.set_of_series = []
        for item in self.bar_set_data:
            self.bar_sets.append(create_bar_set(item[0], item[1]))

        self.bar_series = create_bar_series(self.bar_sets)
        self.set_of_series.append(self.bar_series)
        self.line_series = create_line_series("trend", (4, 15, 20, 4, 12, 17))
#                                          (QPoint(0, 4), QPoint(1, 15), QPoint(2, 20), QPoint(3, 4), QPoint(4, 12),
#                                           QPoint(5, 17)))
        self.set_of_series.append(self.line_series)

        categories = ["Jan", "Feb", "Mar", "Apr", "May"]
        range = ("Jan", "May")
        self.chart_obj.deleteLater()
        self.chart_obj = create_chart("New chart", self.set_of_series)
        set_chart_axis(self.chart_obj, categories, range)
        self.vert_layout.removeWidget(self.chart_view)
        self.vert_layout.removeWidget(self.chart_scroll_bar)
        self.chart_view.setChart(self.chart_obj)
        self.vert_layout.addWidget(self.chart_view)
        self.vert_layout.addWidget(self.chart_scroll_bar)
        self.setCentralWidget(self.central_widget)
        print("Change finished")

    def change_again(self):
        add_data_point("Jane", 5, self.set_of_series)

    def change_again2(self):
        add_data_point("trend", 8, self.set_of_series)

    def change_3(self):
        self.bar_series.append(create_bar_set(self.additional_bar_set[0], self.additional_bar_set[1], 3))

    def change_4(self):
        bar_sets = self.bar_series.barSets()
        for set in bar_sets:
            if set.label() == self.additional_bar_set[0]:
                self.bar_series.remove(set)

def main():
    a = QApplication(sys.argv)

    chart_example = ChartExample()
    update_timer = QTimer()
    update_timer.setSingleShot(True)
    update_timer.timeout.connect(chart_example.change_again)
    update_timer.start(3000)
    update_timer2 = QTimer()
    update_timer2.setSingleShot(True)
    update_timer2.timeout.connect(chart_example.change_again2)
    update_timer2.start(5000)
    update_timer3 = QTimer()
    update_timer3.setSingleShot(True)
    update_timer3.timeout.connect(chart_example.change_3)
    update_timer3.start(8000)
    update_timer4 = QTimer()
    update_timer4.setSingleShot(True)
    update_timer4.timeout.connect(chart_example.change_4)
    update_timer4.start(10000)

    sys.exit(a.exec_())


if __name__ == '__main__':
    main()
