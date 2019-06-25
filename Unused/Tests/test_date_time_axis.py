import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QScrollBar, QFrame, QVBoxLayout
from PySide2.QtCore import QDateTime, Qt, QDate, QTime
from PySide2.QtGui import QPainter
from PySide2.QtCharts import QtCharts
from datetime import datetime


def __create_scroll_bar(func=None):
    scroll_bar = QScrollBar()
    scroll_bar.setOrientation(Qt.Horizontal)
    scroll_bar.setRange(0, 100)
    scroll_bar.setValue(100)
    if func:
        scroll_bar.valueChanged.connect(func)
    return scroll_bar


def main():
    def move_graph():
        nonlocal x_axis
        nonlocal x_start
        nonlocal x_end
        x_axis.setRange(x_start, x_end)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    frame = QFrame()
    frame.setLayout(QVBoxLayout())

    series = QtCharts.QLineSeries()
    series.setPointsVisible(True)

    chart = QtCharts.QChart()
    chart.addSeries(series)
    chart.setTitle("date time x axis test")
    chart.legend().setVisible(False)

    x_axis = QtCharts.QDateTimeAxis()
    x_axis.setFormat("h:m:s")
    date = QDate(1970, 1, 1)  # Because of stupid Qt designers
    time = QTime(datetime.now().time())

    x_start = QDateTime(date, time)
    x_end = QDateTime(date, time.addSecs(120))

    x_axis.setRange(x_start, x_end)
    x_axis.setTitleText("date time")
    x_axis.setTickCount(6)
    chart.addAxis(x_axis, Qt.AlignBottom)
    series.attachAxis(x_axis)

    y_axis = QtCharts.QValueAxis()
    y_axis.setRange(0, 4)
    y_axis.setTickCount(5)
    chart.addAxis(y_axis, Qt.AlignLeft)
    series.attachAxis(y_axis)

    chart_view = QtCharts.QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)

    frame.layout().addWidget(chart_view)
    frame.layout().addWidget(__create_scroll_bar(move_graph))

    time_one = QDateTime(date, time.addSecs(10))
    time_two = time_one.addSecs(10)
    time_three = time_two.addSecs(10)
    time_four = time_three.addSecs(10)
    time_five = time_four.addSecs(10)
    time_six = time_five.addSecs(130)

    print(x_start.toMSecsSinceEpoch())
    print(time_one.toMSecsSinceEpoch())
    print(time_two.toMSecsSinceEpoch())
    print(time_three.toMSecsSinceEpoch())
    print(time_four.toMSecsSinceEpoch())
    print(time_five.toMSecsSinceEpoch())
    print(time_six.toMSecsSinceEpoch())
    series.append(time_one.toMSecsSinceEpoch(), 3)
    series.append(time_two.toMSecsSinceEpoch(), 1)
    series.append(time_three.toMSecsSinceEpoch(), 2)
    series.append(time_four.toMSecsSinceEpoch(), 2)
    series.append(time_five.toMSecsSinceEpoch(), 4)
    series.append(time_six.toMSecsSinceEpoch(), 3)

    if time_six > x_end:
        x_axis.setRange(time_six.addSecs(-120), time_six)

    main_window = QMainWindow()
    main_window.setCentralWidget(frame)
    main_window.resize(820, 600)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()