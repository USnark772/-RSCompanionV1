from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QPoint, Qt
from PySide2.QtCharts import QtCharts
import sys


def main():
    a = QApplication(sys.argv)
    set0 = QtCharts.QBarSet("Jane")
    set1 = QtCharts.QBarSet("John")
    set2 = QtCharts.QBarSet("Axel")
    set3 = QtCharts.QBarSet("Mary")
    set4 = QtCharts.QBarSet("Sam")

    set0 << 1 << 2 << 3 << 4 << 5 << 6
    set1 << 5 << 0 << 0 << 4 << 0 << 7
    set2 << 3 << 5 << 8 << 13 << 8 << 5
    set3 << 5 << 6 << 7 << 3 << 4 << 5
    set4 << 9 << 7 << 5 << 3 << 1 << 2

    barseries1 = QtCharts.QBarSeries()
    barseries1.append(set0)
    barseries1.append(set1)
    barseries1.append(set2)
    barseries1.append(set3)
    barseries1.append(set4)

    lineseries1 = QtCharts.QLineSeries()
    lineseries1.setName("trend")
    lineseries1.append(QPoint(0, 4))
    lineseries1.append(QPoint(1, 15))
    lineseries1.append(QPoint(2, 20))
    lineseries1.append(QPoint(3, 4))
    lineseries1.append(QPoint(4, 12))
    lineseries1.append(QPoint(5, 17))

    chart1 = QtCharts.QChart()
    chart1.addSeries(barseries1)
    chart1.addSeries(lineseries1)
    chart1.setTitle("Line and barchart example")

    categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    axisX = QtCharts.QBarCategoryAxis()
    axisX.append(categories)
    chart1.addAxis(axisX, Qt.AlignBottom)
    lineseries1.attachAxis(axisX)
    barseries1.attachAxis(axisX)
    axisX.setRange("Jan", "Jun")

    axisY = QtCharts.QValueAxis()
    chart1.addAxis(axisY, Qt.AlignLeft)
    lineseries1.attachAxis(axisY)
    barseries1.attachAxis(axisY)
    axisY.setRange(0, 20)

    chart1.legend().setVisible(True)
    chart1.legend().setAlignment(Qt.AlignBottom)

    chartview = QtCharts.QChartView(chart1)

    window = QMainWindow()
    window.setCentralWidget(chartview)
    window.resize(440, 300)
    window.show()

    sys.exit(a.exec_())


if __name__ == '__main__':
    main()
