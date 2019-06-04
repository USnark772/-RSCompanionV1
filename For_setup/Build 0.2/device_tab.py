# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea
from PySide2.QtCore import Qt, QRect


class Tab(QWidget):
    def __init__(self, msg_callback):
        super().__init__()
        self.msg_callback = msg_callback
        self.setLayout(QVBoxLayout())
        self.scroll_area = QScrollArea(self)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.scroll_area.hasHeightForWidth())
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setSizePolicy(size_policy)
        self.scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.scroll_area)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setGeometry(QRect(0, 0, 199, 519))
        self.scroll_area.setWidget(self.scroll_area_contents)
