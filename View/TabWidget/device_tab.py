# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QTabWidget
from PySide2.QtCore import Qt


class TabContainer(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMaximumWidth(250)
        self.setMaximumHeight(500)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(250)

    def add_tab(self, contents):
        new_tab = self.__Tab()
        new_tab.add_contents(contents)
        self.setUpdatesEnabled(False)
        index = self.addTab(new_tab, "")
        self.setTabText(index, contents.get_name())
        self.setUpdatesEnabled(True)
        return index

    def remove_tab(self, index):
        self.removeTab(index)

    class __Tab(QWidget):
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

        def add_contents(self, contents):
            self.__scroll_area.setWidget(contents)
