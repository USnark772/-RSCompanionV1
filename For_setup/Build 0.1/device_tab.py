# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea
from PySide2.QtCore import Qt, QRect


class Tab(QWidget):
    def __init__(self, device_id, msg_callback):
        super().__init__()
        self.device_id = device_id
        self.msg_callback = msg_callback
        self.device_name = self.device_id[0] + " on " + self.device_id[1]
        self.setObjectName(self.device_name)
        self.tab_vert_layout = QVBoxLayout(self)
        self.tab_vert_layout.setObjectName("vert_layout_1")
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
        self.scroll_area.setObjectName("scroll_area")
        self.tab_vert_layout.addWidget(self.scroll_area)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setGeometry(QRect(0, 0, 199, 519))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.scroll_area.setWidget(self.scroll_area_contents)
