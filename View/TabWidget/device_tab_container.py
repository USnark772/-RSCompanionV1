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
# Date: 2019 - 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from PySide2.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QAbstractScrollArea, QTabWidget
from PySide2.QtCore import Qt


class TabContainer(QTabWidget):
    """ This code will contain __Tab objects for display to the user. """
    def __init__(self, parent, width_range, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setMaximumWidth(width_range[0])
        self.setMinimumWidth(width_range[1])
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.__tabs = {}
        self.setMovable(True)
        self.logger.debug("Initialized")

    def add_tab(self, contents):
        self.logger.debug("running")
        new_tab = self.__Tab()
        new_tab.add_contents(contents)
        self.setUpdatesEnabled(False)
        self.addTab(new_tab, contents.get_name())
        self.__tabs[contents.get_name()] = new_tab
        self.setUpdatesEnabled(True)
        self.logger.debug("done")

    def remove_tab(self, name):
        self.logger.debug("running")
        if name in self.__tabs.keys():
            the_tab = self.__tabs[name]
            self.removeTab(QTabWidget.indexOf(self, the_tab))
            del self.__tabs[name]
        self.logger.debug("done")

    # TODO: Finish this?
    def set_tab_visibility(self, name: str, is_visible: bool) -> None:
        """
        Set whether or not the tab is show in the ui.
        :param name: tab name.
        :param is_visible: Whether or not to show the tab.
        :return: None
        """
        if name in self.__tabs.keys():
            the_tab = self.__tabs[name]
            the_tab.setVisibility(is_visible)

    class __Tab(QWidget):
        """ This code is for showing device specific items. This is just a scrollable display area. """
        def __init__(self):
            self.logger = logging.getLogger(__name__)
            self.logger.debug("Initializing")
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
            self.logger.debug("Initialized")

        def add_contents(self, contents):
            self.logger.debug("running")
            self.__scroll_area.setWidget(contents)
            self.logger.debug("done")
