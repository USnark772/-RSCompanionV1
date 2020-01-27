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

from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import QRect
from CompanionLib.companion_helpers import EasyFrame, ClickAnimationButton


class CameraTab(QWidget):
    def __init__(self, parent=None, name=""):
        super().__init__(parent)
        self.name = name
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(400)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(EasyFrame(line=True))

        self.__use_cam_button = ClickAnimationButton()
        self.layout().addWidget(self.__use_cam_button)

        self.layout().addWidget(EasyFrame(line=True))

        self.__set_texts()

    def get_name(self):
        return self.name

    def add_use_cam_button_handler(self, func):
        self.__use_cam_button.clicked.connect(func)

    def __set_texts(self):
        self.__use_cam_button.setText("Toggle Camera")
