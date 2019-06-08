# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea
from PySide2.QtCore import Qt, QRect


class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.__scroll_area = QScrollArea(self)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.__scroll_area.hasHeightForWidth())
        self.__scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.__scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.__scroll_area.setSizePolicy(size_policy)
        self.__scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.__scroll_area)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setGeometry(QRect(0, 0, 199, 519))
        self.__scroll_area.setWidget(self.scroll_area_contents)
