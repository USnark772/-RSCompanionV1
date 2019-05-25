# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide2.QtCore import QRect
import Model.defs as defs
import View.chart_obj as chart


class GraphContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.scroll_area)
        self.contents = QWidget()
        self.contents.setGeometry(QRect(0, 0, 335, 499))
        self.contents_layout = QVBoxLayout(self.contents)
        self.scroll_area.setWidget(self.contents)
        self.list_of_graphs = {}

    def __add_data_point(self, device, data):
        self.list_of_graphs[device].add_point(data)

    def handle_msg(self, msg_dict):
        device = msg_dict['device']
        if device[0] == "drt":
            self.__add_data_point(device, int(msg_dict['rt']))
        elif device[0] == "vog":
            self.__add_data_point(device, (int(msg_dict[defs.vog_block_field[1]]), int(msg_dict[defs.vog_block_field[2]])))

    def add_device(self, device):
        graph_obj = chart.GraphObj(device)
        self.list_of_graphs[device] = graph_obj
        self.contents_layout.addWidget(graph_obj)

    def remove_device(self, device):
        self.list_of_graphs[device].deleteLater()
