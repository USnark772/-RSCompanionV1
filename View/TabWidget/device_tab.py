""" Licensed under GNU GPL-3.0-or-later """
"""
This file is part of RS Companion.

RS Companion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RS Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RS Companion.  If not, see <https://www.gnu.org/licenses/>.
"""

# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QTabWidget
from PySide2.QtCore import Qt


class TabContainer(QTabWidget):
    """ This code will contain __Tab objects for display to the user. """
    def __init__(self, parent, width_range):
        super().__init__(parent)
        self.setMaximumWidth(width_range[0])
        self.setMinimumWidth(width_range[1])
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.__tabs = {}

    def add_tab(self, contents, port):
        new_tab = self.__Tab()
        new_tab.add_contents(contents)
        self.setUpdatesEnabled(False)
        index = self.addTab(new_tab, "")
        self.__tabs[port] = new_tab
        self.setTabText(index, contents.get_name())
        self.setUpdatesEnabled(True)

    def remove_tab(self, port):
        the_tab = self.__tabs[port]
        self.removeTab(QTabWidget.indexOf(self, the_tab))
        del self.__tabs[port]

    class __Tab(QWidget):
        """ This code is for showing device specific items. This is just a scrollable display area. """
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
