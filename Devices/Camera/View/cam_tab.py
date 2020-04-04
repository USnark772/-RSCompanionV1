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
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QLabel, QLineEdit, QProgressBar, QCheckBox,\
    QSpacerItem, QSizePolicy
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QRect, Qt
from Model.app_helpers import EasyFrame
from Model.app_defs import tab_line_edit_error_style, tab_line_edit_compliant_style


max_height = 500
combo_box_height = 22


class CameraTab(QWidget):
    def __init__(self, ch, name=""):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.name = name
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(max_height)

        self.config_horizontal_layout = QHBoxLayout()

        self.initialization_bar_frame = EasyFrame()
        self.initialization_bar_layout = QVBoxLayout(self.initialization_bar_frame)
        self.initialization_bar_label = QLabel(self.initialization_bar_frame)
        self.initialization_bar_layout.addWidget(self.initialization_bar_label)
        self.initialization_bar = QProgressBar(self.initialization_bar_frame)
        self.initialization_bar.setTextVisible(True)
        self.initialization_bar.setAlignment(Qt.AlignHCenter)
        self.initialization_bar.setMaximumHeight(15)
        self.initialization_bar_layout.addWidget(self.initialization_bar)
        self.initialization_bar_frame.setMaximumHeight(70)

        self.show_cam_checkbox_frame = EasyFrame()
        self.show_cam_checkbox_layout = QHBoxLayout(self.show_cam_checkbox_frame)
        self.show_cam_checkbox_label = QLabel(self.show_cam_checkbox_frame)
        self.show_cam_checkbox_label.setAlignment(Qt.AlignLeft)
        self.show_cam_checkbox_layout.addWidget(self.show_cam_checkbox_label)
        self.show_cam_checkbox_layout.addWidget(EasyFrame(vert=True))
        self.show_cam_checkbox = QCheckBox()
        self.show_cam_checkbox.setChecked(True)
        self.show_cam_checkbox.setLayoutDirection(Qt.RightToLeft)
        self.show_cam_checkbox_layout.addWidget(self.show_cam_checkbox)
        self.show_cam_checkbox_frame.setMaximumHeight(50)

        self.frame_size_selector_frame = EasyFrame()
        self.frame_size_selector_layout = QHBoxLayout(self.frame_size_selector_frame)
        self.frame_size_selector_label = QLabel(self.frame_size_selector_frame)
        self.frame_size_selector_label.setAlignment(Qt.AlignLeft)
        self.frame_size_selector_layout.addWidget(self.frame_size_selector_label)
        self.frame_size_selector_layout.addWidget(EasyFrame(vert=True))
        self.frame_size_selector = QComboBox(self.frame_size_selector_frame)
        self.frame_size_selector.setMaximumHeight(combo_box_height)
        self.frame_size_selector_layout.addWidget(self.frame_size_selector)
        self.frame_size_selector_frame.setMaximumHeight(50)

        self.frame_rotation_setting_frame = EasyFrame()
        self.frame_rotation_setting_layout = QHBoxLayout(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_label = QLabel(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_label.setAlignment(Qt.AlignLeft)
        self.frame_rotation_setting_layout.addWidget(self.frame_rotation_setting_label)
        self.frame_rotation_setting_layout.addWidget(EasyFrame(vert=True))
        self.frame_rotation_setting_entry_box = QLineEdit(self.frame_rotation_setting_frame)
        self.frame_rotation_setting_entry_box.setMaximumSize(90, 20)
        self.frame_rotation_setting_entry_box.setAlignment(Qt.AlignRight)
        self.frame_rotation_setting_layout.addWidget(self.frame_rotation_setting_entry_box)
        self.frame_rotation_setting_frame.setMaximumHeight(50)

        self.image_display_frame = EasyFrame()
        self.image_display_layout = QVBoxLayout(self.image_display_frame)
        self.image_display_label = QLabel(self.image_display_frame)
        self.image_display_label.setAlignment(Qt.AlignHCenter)
        self.image_display_layout.addWidget(self.image_display_label)
        self.image_display = QLabel(self.image_display_frame)
        self.image_display.setAlignment(Qt.AlignHCenter)
        self.image_display_layout.addWidget(self.image_display)

        self.fps_display_frame = EasyFrame()
        self.fps_display_layout = QHBoxLayout(self.fps_display_frame)
        self.fps_display_label = QLabel(self.fps_display_frame)
        self.fps_display_label.setAlignment(Qt.AlignRight)
        self.fps_display_layout.addWidget(self.fps_display_label)
        self.fps_display_value = QLabel(self.fps_display_frame)
        self.fps_display_value.setAlignment(Qt.AlignLeft)
        self.fps_display_layout.addWidget(self.fps_display_value)

        spacer = QSpacerItem(1, 1, vData=QSizePolicy.Expanding)

        self.layout().addWidget(self.initialization_bar_frame)
        self.layout().addWidget(EasyFrame(line=True))
        self.layout().addWidget(self.frame_size_selector_frame)
        self.layout().addWidget(self.frame_rotation_setting_frame)
        self.layout().addWidget(EasyFrame(line=True))
        self.layout().addWidget(self.show_cam_checkbox_frame)
        self.layout().addWidget(self.image_display_frame)
        self.layout().addWidget(self.fps_display_frame)
        self.layout().addWidget(EasyFrame(line=True))
        self.layout().addItem(spacer)

        self.__set_texts()
        self.__set_tooltips()
        self.set_tab_active(False)
        self.logger.debug("Initialized")

    def get_name(self):
        return self.name

    def set_tab_active(self, is_active, feed=False):
        self.logger.debug("running")
        self.__set_controls_active(is_active)
        if feed:
            self.show_feed(is_active)
        self.logger.debug("done")

    def add_use_cam_button_handler(self, func):
        self.logger.debug("running")
        self.use_cam_button.clicked.connect(func)
        self.logger.debug("done")

    def add_show_cam_button_handler(self, func):
        self.logger.debug("running")
        self.show_cam_checkbox.toggled.connect(func)
        self.logger.debug("done")

    def add_bw_button_handler(self, func):
        self.logger.debug("running")
        self.bw_button.clicked.connect(func)
        self.logger.debug("done")

    def add_settings_toggle_button_handler(self, func):
        self.logger.debug("running")
        self.settings_toggle_button.clicked.connect(func)
        self.logger.debug("done")

    def add_frame_size_selector_handler(self, func):
        self.logger.debug("running")
        self.frame_size_selector.activated.connect(func)
        self.logger.debug("done")

    def add_frame_rotation_handler(self, func):
        self.logger.debug("running")
        self.frame_rotation_setting_entry_box.textChanged.connect(func)
        self.logger.debug("done")

    def update_feed(self, image: QPixmap):
        self.image_display.setPixmap(image)

    def show_feed(self, is_active: bool):
        if not is_active:
            self.image_display_label.setText('Preview unavailable')
        else:
            self.image_display_label.setText('Preview')
        self.image_display.setVisible(is_active)

    def get_frame_size(self):
        return self.frame_size_selector.currentData()

    def set_frame_size(self, index):
        self.logger.debug("running")
        self.frame_size_selector.setCurrentIndex(index)
        self.logger.debug("done")

    def get_rotation(self):
        return self.frame_rotation_setting_entry_box.text()

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

    def populate_frame_size_selector(self, values):
        self.logger.debug("running")
        for i in range(len(values)):
            self.frame_size_selector.insertItem(i, values[i][0], values[i][1])
        self.logger.debug("done")

    def add_item_to_size_selector(self, item):
        self.logger.debug("running")
        self.frame_size_selector.insertItem(self.frame_size_selector.count(), item)
        self.logger.debug("done")

    def empty_size_selector(self):
        self.logger.debug("running")
        for i in range(self.frame_size_selector.count()):
            self.frame_size_selector.removeItem(i)
        self.logger.debug("done")

    def set_init_progress_bar_val(self, value):
        self.initialization_bar.setValue(value)

    def remove_init_prog_bar(self):
        self.initialization_bar_frame.hide()

    def update_fps_value(self, value: int):
        self.fps_display_value.setText(str(value))

    def __set_controls_active(self, is_active):
        self.logger.debug("running")
        self.frame_size_selector.setEnabled(is_active)
        self.frame_rotation_setting_entry_box.setEnabled(is_active)
        self.show_cam_checkbox.setEnabled(is_active)
        self.logger.debug("done")

    def __set_texts(self):
        self.logger.debug("running")
        self.initialization_bar_label.setText('Initialization progress')
        self.initialization_bar.setValue(0)
        self.image_display_label.setText("Preview")
        self.image_display.setText("Initializing")
        self.show_cam_checkbox_label.setText("Show feed")
        self.frame_size_selector_label.setText("Frame size")
        self.frame_rotation_setting_label.setText("Rotate image")
        self.fps_display_label.setText("FPS:")
        self.fps_display_value.setText("0")
        self.logger.debug("done")

    def __set_tooltips(self):
        self.logger.debug("running")
        frame_size_tooltip = "Select resolution for this camera."
        show_cam_tooltip = "Show or hide camera feed preview. (Does not disable camera)"
        fps_display_tooltip = "The approximate fps this cam is performing at. This value can be affected by the load "\
                              "your computer is currently under."
        rotation_tooltip = "Set degree of rotation for video feed. -360 < value < 360."
        image_display_tooltip = "Preview of camera feed."
        self.show_cam_checkbox_frame.setToolTip(show_cam_tooltip)
        self.frame_size_selector_frame.setToolTip(frame_size_tooltip)
        self.frame_rotation_setting_frame.setToolTip(rotation_tooltip)
        self.image_display_frame.setToolTip(image_display_tooltip)
        self.fps_display_frame.setToolTip(fps_display_tooltip)
        self.logger.debug("done")
