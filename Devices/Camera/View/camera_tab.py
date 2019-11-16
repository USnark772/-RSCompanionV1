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

from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QComboBox
from PySide2.QtCore import QRect
from CompanionLib.companion_helpers import EasyFrame, ClickAnimationButton


class CameraTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(400)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(EasyFrame(True))

        self.__cam_selector_frame = EasyFrame()
        self.__cam_selector_horiz_layout = QHBoxLayout(self.__cam_selector_frame)
        self.__cam_selector_label = QLabel(self.__cam_selector_frame)
        self.__cam_selector_horiz_layout.addWidget(self.__cam_selector_label)
        self.__cam_selector = QComboBox(self.__cam_selector_frame)
        self.__cam_selector_horiz_layout.addWidget(self.__cam_selector)
        self.layout().addWidget(self.__cam_selector_frame)

        self.layout().addWidget(EasyFrame(line=True))

        """ Set upload button selection area. """
        # TODO: Replace cam_selector_button with this.
        self.__upload_settings_button = ClickAnimationButton()
        self.layout().addWidget(self.__upload_settings_button)

        self.layout().addWidget(EasyFrame(True))

        self.__set_texts()

    def add_cam_selector_button_handler(self, func):
        self.__upload_settings_button.clicked.connect(func)

    def get_name(self):
        return "Cameras"

    def add_cam(self, cam_index):
        self.__cam_selector.addItem("")
        self.__cam_selector.setItemText(cam_index, str(cam_index))

    def get_cam_index(self):
        return self.__cam_selector.currentIndex()

    def __set_texts(self):
        self.__cam_selector_label.setText("Select Camera")
        self.__upload_settings_button.setText("Upload Settings")
