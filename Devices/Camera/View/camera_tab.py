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

from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QFrame
from PySide2.QtCore import QRect, Qt
from CompanionLib.companion_helpers import EasyFrame, ClickAnimationButton


class CameraTab(QWidget):
    def __init__(self, name=""):
        super().__init__()
        self.name = name
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(200)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(EasyFrame(line=True))

        self.__use_cam_button = ClickAnimationButton()
        self.layout().addWidget(self.__use_cam_button)

        self.next_button = ClickAnimationButton()
        self.next_button.setText("Next resolution")
        self.layout().addWidget(self.next_button)

        self.layout().addWidget(EasyFrame(line=True))

        self.fps_selector_frame = EasyFrame()
        self.fps_selector_layout = QHBoxLayout(self.fps_selector_frame)
        self.fps_selector_label = QLabel(self.fps_selector_frame)
        self.fps_selector_label.setAlignment(Qt.AlignCenter)
        self.fps_selector_layout.addWidget(self.fps_selector_label)
        self.fps_selector_layout.addWidget(EasyFrame(vert=True))
        self.fps_selector = QComboBox(self.fps_selector_frame)
        self.fps_selector_layout.addWidget(self.fps_selector)

        self.layout().addWidget(self.fps_selector_frame)

        self.frame_size_selector_frame = EasyFrame()
        self.frame_size_selector_layout = QHBoxLayout(self.frame_size_selector_frame)
        self.frame_size_selector_label = QLabel(self.frame_size_selector_frame)
        self.frame_size_selector_label.setAlignment(Qt.AlignCenter)
        self.frame_size_selector_layout.addWidget(self.frame_size_selector_label)
        self.frame_size_selector_layout.addWidget(EasyFrame(vert=True))
        self.frame_size_selector = QComboBox(self.frame_size_selector_frame)
        self.frame_size_selector_layout.addWidget(self.frame_size_selector)

        self.layout().addWidget(self.frame_size_selector_frame)

        self.layout().addWidget(EasyFrame(line=True))

        self.__set_texts()

    def get_name(self):
        return self.name

    def add_use_cam_button_handler(self, func):
        self.__use_cam_button.clicked.connect(func)

    def add_fps_selector_handler(self, func):
        self.fps_selector.activated.connect(func)

    def add_frame_size_selector_handler(self, func):
        self.frame_size_selector.activated.connect(func)

    def get_fps(self):
        return self.fps_selector.currentText()

    def set_fps_selector(self, index):
        self.fps_selector.setCurrentIndex(index)

    def get_frame_size(self):
        return self.frame_size_selector.currentText()

    def set_frame_size_selector(self, index):
        self.frame_size_selector.setCurrentIndex(index)

    def populate_fps_selector(self, values):
        for i in range(len(values)):
            self.fps_selector.insertItem(i, values[i])

    def populate_frame_size_selector(self, values):
        for i in range(len(values)):
            self.frame_size_selector.insertItem(i, values[i])

    def __set_texts(self):
        self.__use_cam_button.setText("Toggle Camera")
        self.fps_selector_label.setText("FPS")
        self.frame_size_selector_label.setText("Frame size")
