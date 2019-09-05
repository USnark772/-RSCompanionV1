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
# Date: 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from PySide2.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide2.QtCore import QRect


class DisplayContainer(QWidget):
    """ This code is to create an area for display widgets such as graphs to be shown to the user. """
    def __init__(self, parent, callback):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.__callback = callback
        self.setLayout(QVBoxLayout())
        self.__scroll_area = QScrollArea(self)
        self.__scroll_area.verticalScrollBar().valueChanged.connect(self.__slider_changed_notifier)
        self.__scroll_area.setWidgetResizable(True)
        self.layout().addWidget(self.__scroll_area)
        contents = QWidget(self)
        contents.setGeometry(QRect(0, 0, 335, 499))
        contents.setLayout(QVBoxLayout())
        self.__scroll_area.setWidget(contents)
        self.__list_of_displays = []
        self.logger.debug("Initialized")

    def add_display(self, display):
        """ Add a display, typically a graph, to the set of displays to be displayed in the display area. """
        self.logger.debug("running")
        self.__list_of_displays.append(display)
        self.__refresh()
        self.logger.debug("done")

    def remove_display(self, display):
        """ Remove a display, typically a graph, from the set of displays if it exists. """
        self.logger.debug("running")
        if display in self.__list_of_displays:
            self.__list_of_displays.remove(display)
        self.__refresh()
        self.logger.debug("done")

    def __refresh(self):
        """ Rebuild display area to refresh the view. """
        self.logger.debug("running")
        new_contents = QWidget(self)
        new_contents.setGeometry(QRect(0, 0, 335, 499))
        new_contents.setLayout(QVBoxLayout())
        for display in self.__list_of_displays:
            new_contents.layout().addWidget(display)
        self.__scroll_area.setWidget(new_contents)
        self.logger.debug("done")

    def __slider_changed_notifier(self):
        """ Notify controller that the user scrolled the display area. """
        self.logger.debug("running")
        self.__callback()
        self.logger.debug("done")
