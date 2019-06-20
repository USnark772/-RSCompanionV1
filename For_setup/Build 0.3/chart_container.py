# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide2.QtCore import QRect
import defs as defs
import chart_obj as chart


class GraphContainer(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.__scroll_area = QScrollArea(self)
        self.__scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.__scroll_area)
        self.__contents = QWidget()
        self.__contents.setGeometry(QRect(0, 0, 335, 499))
        self.__contents.setLayout(QVBoxLayout())
        self.__scroll_area.setWidget(self.__contents)
        self.__list_of_graphs = {}
        self.__num_devices = 0

    def add_data_point(self, device, data):
        self.__list_of_graphs[device].add_data_point(data)

    def handle_msg(self, msg_dict):
        device = msg_dict['device']
        if device[0] == "drt":
            self.add_data_point(device, int(msg_dict[defs.drtv1_0_trial_fields[3]]))
        elif device[0] == "vog":
            self.add_data_point(device, (int(msg_dict[defs.vog_block_field[1]]), int(msg_dict[defs.vog_block_field[2]])))

    def add_device(self, device):
        graph_obj = chart.GraphObj(device)
        self.__list_of_graphs[device] = graph_obj
        self.__contents.layout().addWidget(graph_obj)

    def remove_device(self, device):
        self.__list_of_graphs[device].deleteLater()
