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
from PySide2.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QPushButton


class GraphFrame(QFrame):
    """ This code is to contain and properly size graph widgets. """
    def __init__(self, parent, canvas):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__(parent)
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumWidth(500)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLayout(QVBoxLayout(self))
        self.__visible = True
        self.__canvas = canvas
        self.__show_hide_button = QPushButton(self)
        self.__show_hide_button.setFixedSize(150, 30)
        self.__show_hide_button.clicked.connect(self.__set_graph_visibility)
        self.layout().addWidget(self.__show_hide_button)
        self.__navbar_height = 100
        self.__canvas_height = 400
        self.__show_hide_button.setText("Hide " + self.__canvas.get_title() + " graph")
        self.layout().addWidget(self.__canvas)
        self.layout().addWidget(self.__canvas.get_nav_bar())
        self.setFixedHeight(self.__navbar_height + self.__canvas_height)
        self.logger.debug("Initialized")

    def set_graph_height(self, height):
        """ Each display type will be a different size. """
        self.logger.debug("running")
        self.__canvas_height = height
        self.logger.debug("done")

    def __set_graph_visibility(self):
        """ Show or hide the graph in the display area. """
        self.logger.debug("running")
        self.__visible = not self.__visible
        if self.__visible:
            self.layout().removeWidget(self.__canvas.get_nav_bar())
            self.layout().addWidget(self.__canvas)
            self.layout().addWidget(self.__canvas.get_nav_bar())
            self.setFixedHeight(40 + self.__navbar_height + self.__canvas_height)
            self.__show_hide_button.setText("Hide " + self.__canvas.get_title() + " graph")
        else:
            self.layout().removeWidget(self.__canvas)
            self.layout().removeWidget(self.__canvas.get_nav_bar())
            self.setFixedHeight(40)
            self.__show_hide_button.setText("Show " + self.__canvas.get_title() + " graph")
        self.logger.debug("done")

    def get_graph(self):
        return self.__canvas
