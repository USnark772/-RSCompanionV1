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

from PySide2.QtWidgets import QDockWidget, QHBoxLayout, QWidget
from PySide2.QtCore import Qt


class ControlDock(QDockWidget):
    """
    A detachable area for other widgets such as frames.
    Typically this will be used for overall app control and feedback.
    """
    def __init__(self, parent, size):
        super().__init__(parent)
        self.setMaximumSize(size)
        self.setFeatures(
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetVerticalTitleBar)
        self.setAllowedAreas(Qt.TopDockWidgetArea)
        self.setWidget(QWidget())
        self.widget().setLayout(QHBoxLayout())

        self.__set_texts()

    def add_widget(self, widget):
        self.widget().layout().addWidget(widget)

    def __set_texts(self):
        self.setWindowTitle("Control")
