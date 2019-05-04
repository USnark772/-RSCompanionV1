from PySide2.QtCharts import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

a = QApplication([])

chart = QtCharts.QChart()
chart.legend().hide()

x_axis = QtCharts.QValueAxis()
x_axis.setTickCount(10)
chart.addAxis(x_axis, Qt.AlignBottom)

series = QtCharts.QSplineSeries()
series << QPointF(1, 5) << QPointF(3.5, 18) << QPointF(4.8, 7.5) << QPointF(10, 2.5)
chart.addSeries(series)

y_axis = QtCharts.QValueAxis()
y_axis.setLinePenColor(Qt.blue)

chart.addAxis(y_axis, Qt.AlignLeft)
series.attachAxis(y_axis)
series.attachAxis(x_axis)

series2 = QtCharts.QSplineSeries()
series2 << QPointF(1, 0.5) << QPointF(1.5, 4.5) << QPointF(2.4, 2.5) << QPointF(4.3, 12.5) \
        << QPointF(5.2, 3.5) << QPointF(7.4, 16.5) << QPointF(8.3, 7.5) << QPointF(10, 17)
chart.addSeries(series2)

y_axis2 = QtCharts.QCategoryAxis()
y_axis2.append("0", 1)
#y_axis2.append("Medium", 12)
#y_axis2.append("High", 17)
y_axis2.setLinePenColor(Qt.darkGreen)
y_axis2.setGridLinePen(series2.pen())

chart.addAxis(y_axis2, Qt.AlignRight)
series2.attachAxis(x_axis)
series2.attachAxis(y_axis2)

chartView = QtCharts.QChartView(chart)
chartView.setRenderHint(QPainter.Antialiasing)

window = QMainWindow()
window.setCentralWidget(chartView)
window.resize(1280, 1024)
window.show()

a.exec_()
