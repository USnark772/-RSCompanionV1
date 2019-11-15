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

from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox
from PySide2.QtCore import Qt, QRect
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *
from CompanionLib.companion_helpers import MyFrame


class WebcamViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(400)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(MyFrame(True))

        self.__button_mode_frame = MyFrame()
        self.__button_mode_horiz_layout = QHBoxLayout(self.__button_mode_frame)
        self.__button_mode_label = QLabel(self.__button_mode_frame)
        self.__button_mode_horiz_layout.addWidget(self.__button_mode_label)
        self.__button_mode_selector = QComboBox(self.__button_mode_frame)
        self.__button_mode_horiz_layout.addWidget(self.__button_mode_selector)
        self.layout().addWidget(self.__button_mode_frame)

        self.layout().addWidget(MyFrame(line=True))

        """ Set upload button selection area. """
        self.__upload_settings_button = QPushButton()
        self.layout().addWidget(self.__upload_settings_button)

        self.layout().addWidget(MyFrame(True))

        self.__set_texts()

    def __set_texts(self):
        self.__button_mode_label.setText("Select Cam")

    def get_name(self):
        return "webcam"

    def add_cam(self, cam_index):
        self.__button_mode_selector.addItem(cam_index, text=cam_index)

