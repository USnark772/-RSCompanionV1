# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html



class DRTGraphController(GraphObj):
    def __init__(self, name):
        super().__init__(name)
        self.__series_name = "Response Time"
        self.reset_graph()

    def add_data_to_graph(self, timestamp, data):
        self.__graph_obj.add_data_point(self.__series_name, timestamp, data)

    def reset_graph(self):
        self.__graph_obj.reset_graph()
        self.__graph_obj.set_chart_axes("Timestamp", "Milliseconds")
        self.__graph_obj.add_line_series(self.__series_name)
