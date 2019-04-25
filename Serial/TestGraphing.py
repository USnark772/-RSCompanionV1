# from: https://doc.qt.io/qt-5/qtcharts-percentbarchart-example.html
from PySide2.QtCharts import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

a = QApplication([])

set0 = QtCharts.QBarSet("Jane")
set1 = QtCharts.QBarSet("John")
set2 = QtCharts.QBarSet("Axel")
set3 = QtCharts.QBarSet("Mary")
set4 = QtCharts.QBarSet("Samantha")

set0 << 1 << 2 << 3 << 4 << 5 << 6
set1 << 5 << 0 << 0 << 4 << 0 << 7
set2 << 3 << 5 << 8 << 13 << 8 << 5
set3 << 5 << 6 << 7 << 3 << 4 << 5
set4 << 9 << 7 << 5 << 3 << 1 << 2

series = QtCharts.QPercentBarSeries()
series.append(set0)
series.append(set1)
series.append(set2)
series.append(set3)
series.append(set4)

chart = QtCharts.QChart()
chart.addSeries(series)
chart.setTitle("Simple percentbarchart example")
chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
axis = QtCharts.QBarCategoryAxis()
axis.append(categories)
chart.createDefaultAxes()
chart.setAxisX(axis, series)

chart.legend().setVisible(True)
chart.legend().setAlignment(Qt.AlignBottom)

chartView = QtCharts.QChartView(chart)
chartView.setRenderHint(QPainter.Antialiasing)

window = QMainWindow()
window.setCentralWidget(chartView)
window.resize(420, 300)
window.show()

a.exec_()