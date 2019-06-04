# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html


class DeviceGraphData:
    def __init__(self, name, index):
        self.__name = name
        self.__points = []
        self.__beginning_index = index

    def add_point(self, point):
        #print("device_graph_rep.DeviceGraphData.add_point()")
        #print("Trying to add point")
        self.__points.append(point)
        #print("Added point")

    def get_points(self):
        return self.__points

    def name(self):
        return self.__name

    def get_start_index(self):
        return self.__beginning_index
