from PySide2.QtCharts import QtCharts


class DeviceRep:
    points = []

    def __init__(self, name):
        self.name = name

    def make_as_bar_set(self):
        self.set = QtCharts.QBarSet(self.name)
        for point in self.points:
            self.set.append(point)

    def make_as_line_series(self):
        self.set = QtCharts.QLineSeries(self.name)
        for point in self.points:
            self.set.append(point)

    def add_point(self, point):
        i = self.points.count()
        self.points[i] = point
        self.set.append(self.points[i])

    def get_points(self):
        return self.points
