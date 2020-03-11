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
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QLineEdit, QCheckBox
from PySide2.QtCore import QRect, Qt
from CompanionLib.companion_helpers import EasyFrame, ClickAnimationButton
from Model.general_defs import tab_line_edit_error_style, tab_line_edit_compliant_style


class CameraTab(QWidget):
    def __init__(self, ch, name=""):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.name = name
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(300)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(EasyFrame(line=True))

        self.use_cam_button = ClickAnimationButton()
        self.layout().addWidget(self.use_cam_button)

        self.show_cam_button = ClickAnimationButton()
        self.layout().addWidget(self.show_cam_button)

        self.settings_toggle_button = ClickAnimationButton()
        self.layout().addWidget(self.settings_toggle_button)

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

        self.frame_rotation_setting_frame = EasyFrame()
        self.frame_rotation_setting_layout = QHBoxLayout(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_label = QLabel(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_layout.addWidget(self.frame_rotation_setting_label)
        self.frame_rotation_setting_layout.addWidget(EasyFrame(vert=True))
        self.frame_rotation_setting_entry_box = QLineEdit(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_entry_box.setMaximumSize(90, 20)
        self.frame_rotation_setting_entry_box.setAlignment(Qt.AlignRight)
        self.frame_rotation_setting_layout.addWidget(self.frame_rotation_setting_entry_box)

        self.layout().addWidget(self.frame_rotation_setting_frame)

        self.layout().addWidget(EasyFrame(line=True))

        self.__set_texts()
        self.__set_tooltips()
        self.set_tab_active(False)
        self.logger.debug("Initialized")

    def get_name(self):
        return self.name

    def set_tab_active(self, is_active):
        self.logger.debug("running")
        self.set_controls_active(is_active)
        self.frame_rotation_setting_entry_box.setEnabled(is_active)
        self.settings_toggle_button.setEnabled(is_active)
        self.use_cam_button.setEnabled(is_active)
        self.show_cam_button.setEnabled(is_active)
        self.logger.debug("done")

    def set_controls_active(self, is_active):
        self.logger.debug("running")
        self.frame_size_selector.setEnabled(is_active)
        self.fps_selector.setEnabled(is_active)
        self.use_cam_button.setEnabled(is_active)
        self.logger.debug("done")

    def add_use_cam_button_handler(self, func):
        self.logger.debug("running")
        self.use_cam_button.clicked.connect(func)
        self.logger.debug("done")

    def add_show_cam_button_handler(self, func):
        self.logger.debug("running")
        self.show_cam_button.clicked.connect(func)
        self.logger.debug("done")

    def add_settings_toggle_button_handler(self, func):
        self.logger.debug("running")
        self.settings_toggle_button.clicked.connect(func)
        self.logger.debug("done")

    def add_fps_selector_handler(self, func):
        self.logger.debug("running")
        self.fps_selector.activated.connect(func)
        self.logger.debug("done")

    def add_frame_size_selector_handler(self, func):
        self.logger.debug("running")
        self.frame_size_selector.activated.connect(func)
        self.logger.debug("done")

    def add_frame_rotation_handler(self, func):
        self.logger.debug("running")
        self.frame_rotation_setting_entry_box.textChanged.connect(func)
        self.logger.debug("done")

    def get_fps(self):
        return self.fps_selector.currentData()

    def set_fps(self, index):
        self.logger.debug("running")
        self.fps_selector.setCurrentIndex(index)
        self.logger.debug("done")

    def get_frame_size(self):
        return self.frame_size_selector.currentData()

    def set_frame_size(self, index):
        self.logger.debug("running")
        self.frame_size_selector.setCurrentIndex(index)
        self.logger.debug("done")

    def set_rotation(self, value: str):
        self.logger.debug("running")
        self.frame_rotation_setting_entry_box.setText(value)
        self.logger.debug("done")

    def set_rotation_error(self, is_error: bool):
        """ Set display of error in frame rotation line edit. """
        self.logger.debug("running")
        if is_error:
            self.frame_rotation_setting_entry_box.setStyleSheet(tab_line_edit_error_style)
        else:
            self.frame_rotation_setting_entry_box.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def get_rotation(self):
        return self.frame_rotation_setting_entry_box.text()

    def populate_fps_selector(self, values):
        self.logger.debug("running")
        for i in range(len(values)):
            self.fps_selector.insertItem(i, values[i][0], values[i][1])
        self.logger.debug("done")

    def populate_frame_size_selector(self, values):
        self.logger.debug("running")
        for i in range(len(values)):
            self.frame_size_selector.insertItem(i, values[i][0], values[i][1])
        self.logger.debug("done")

    def add_item_to_size_selector(self, item):
        self.logger.debug("running")
        self.frame_size_selector.insertItem(self.frame_size_selector.count(), item)
        self.logger.debug("done")

    def add_item_to_fps_selector(self, item):
        self.logger.debug("running")
        self.fps_selector.insertItem(self.fps_selector.count(), item)
        self.logger.debug("done")

    def empty_size_selector(self):
        self.logger.debug("running")
        for i in range(self.frame_size_selector.count()):
            self.frame_size_selector.removeItem(i)
        self.logger.debug("done")

    def empty_fps_selector(self):
        self.logger.debug("running")
        for i in range(self.fps_selector.count()):
            self.fps_selector.removeItem(i)
        self.logger.debug("done")

    def __set_texts(self):
        self.logger.debug("running")
        self.use_cam_button.setText("Toggle Camera Usage")
        self.show_cam_button.setText("Toggle Camera Display")
        self.fps_selector_label.setText("FPS")
        self.frame_size_selector_label.setText("Frame size")
        self.settings_toggle_button.setText("Camera Settings")
        self.frame_rotation_setting_label.setText("Image rotation degrees")
        self.logger.debug("done")

    def __set_tooltips(self):
        self.logger.debug("running")
        fps_selector_tooltip = "Select frame rate for the saved footage"
        frame_size_tooltip = "Select resolution for this camera. Higher resolutions may cause issues."
        use_cam_tooltip = "Toggle whether this camera is being used."
        show_cam_tooltip = "Toggle whether this camera feed is added to the UI. (Does not disable camera)"
        settings_window_tooltip = "Open a window with extra camera settings."
        rotation_tooltip = "Set rotation angle for video feed. -360 < value < 360."
        self.use_cam_button.setToolTip(use_cam_tooltip)
        self.show_cam_button.setToolTip(show_cam_tooltip)
        self.settings_toggle_button.setToolTip(settings_window_tooltip)
        self.fps_selector_frame.setToolTip(fps_selector_tooltip)
        self.frame_size_selector_frame.setToolTip(frame_size_tooltip)
        self.frame_rotation_setting_frame.setToolTip(rotation_tooltip)
        self.logger.debug("done")
