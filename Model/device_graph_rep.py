class DeviceGraphData:
    def __init__(self, name, index):
        self.__name = name
        self.__points = []
        self.__beginning_index = index

    def add_point(self, point):
        self.__points.append(point)

    def get_points(self):
        return self.__points

    def name(self):
        return self.__name

