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

from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QSlider
from PySide2.QtCore import QRect, Qt
from CompanionLib.companion_helpers import EasyFrame, ClickAnimationButton


class CameraTab(QWidget):
    def __init__(self, name=""):
        super().__init__()
        self.name = name
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(300)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(EasyFrame(line=True))

        self.use_cam_button = ClickAnimationButton()
        self.layout().addWidget(self.use_cam_button)

        self.color_toggle_button = ClickAnimationButton()
        self.layout().addWidget(self.color_toggle_button)

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

        self.frame_rotation_slider_frame = EasyFrame()
        self.frame_rotation_slider_layout = QVBoxLayout(self.frame_rotation_slider_frame)
        self.frame_rotation_slider_label = QLabel(self.frame_rotation_slider_frame)
        self.frame_rotation_slider_label.setAlignment(Qt.AlignCenter)
        self.frame_rotation_slider_layout.addWidget(self.frame_rotation_slider_label)
        self.frame_rotation_slider_layout.addWidget(EasyFrame(vert=True))
        self.frame_rotation_slider = QSlider(self.frame_rotation_slider_frame)
        self.frame_rotation_slider.setOrientation(Qt.Horizontal)
        self.frame_rotation_slider.setRange(0, 360)
        self.frame_rotation_slider.setTickPosition(QSlider.TicksBelow)
        self.frame_rotation_slider.setTickInterval(90)
        self.frame_rotation_slider_layout.addWidget(self.frame_rotation_slider)

        self.layout().addWidget(self.frame_rotation_slider_frame)

        self.layout().addWidget(EasyFrame(line=True))

        self.__set_texts()
        self.__set_tooltips()

    def get_name(self):
        return self.name

    def set_controls_active(self, is_active):
        # self.frame_rotation_slider.setEnabled(is_active)
        self.frame_size_selector.setEnabled(is_active)
        self.fps_selector.setEnabled(is_active)
        self.use_cam_button.setEnabled(is_active)
        # self.color_toggle_button.setEnabled(is_active)

    def add_use_cam_button_handler(self, func):
        self.use_cam_button.clicked.connect(func)

    def add_color_toggle_button_handler(self, func):
        self.color_toggle_button.clicked.connect(func)

    def add_fps_selector_handler(self, func):
        self.fps_selector.activated.connect(func)

    def add_frame_size_selector_handler(self, func):
        self.frame_size_selector.activated.connect(func)

    def add_frame_rotation_handler(self, func):
        self.frame_rotation_slider.valueChanged.connect(func)

    def add_frame_rotation_released_handler(self, func):
        self.frame_rotation_slider.sliderReleased.connect(func)

    def get_fps(self):
        return self.fps_selector.currentData()

    def set_fps(self, index):
        self.fps_selector.setCurrentIndex(index)

    def get_frame_size(self):
        return self.frame_size_selector.currentData()

    def set_frame_size(self, index):
        self.frame_size_selector.setCurrentIndex(index)

    def set_rotation(self, value):
        self.frame_rotation_slider.setValue(value)

    def get_rotation(self):
        return self.frame_rotation_slider.value()

    def populate_fps_selector(self, values):
        for i in range(len(values)):
            self.fps_selector.insertItem(i, values[i][0], values[i][1])

    def populate_frame_size_selector(self, values):
        for i in range(len(values)):
            self.frame_size_selector.insertItem(i, values[i][0], values[i][1])

    def __set_texts(self):
        self.use_cam_button.setText("Toggle Camera")
        self.fps_selector_label.setText("FPS")
        self.frame_size_selector_label.setText("Frame size")
        self.color_toggle_button.setText("Toggle color")
        self.frame_rotation_slider_label.setText("Rotate")

    def __set_tooltips(self):
        fps_selector_tooltip = "Select frame rate for the saved footage"
        frame_size_tooltip = "Select resolution for this camera. Higher resolutions may cause issues."
        use_cam_tooltip = "Toggle whether this camera is being used."
        use_color_tooltip = "Toggle between color or black and white video."
        rotation_tooltip = "Set rotation angle for video feed."
        self.use_cam_button.setToolTip(use_cam_tooltip)
        self.color_toggle_button.setToolTip(use_color_tooltip)
        self.fps_selector_frame.setToolTip(fps_selector_tooltip)
        self.frame_size_selector_frame.setToolTip(frame_size_tooltip)
        self.frame_rotation_slider_frame.setToolTip(rotation_tooltip)
