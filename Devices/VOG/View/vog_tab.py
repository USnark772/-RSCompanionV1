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
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QHBoxLayout, QVBoxLayout,\
    QCheckBox, QFrame, QLineEdit
from PySide2.QtCore import Qt, QRect
from Devices.VOG.Model.vog_defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min
from Model.general_defs import tab_line_edit_error_style, tab_line_edit_compliant_style
from CompanionLib.view_helpers import MyFrame


class VOGTab(QWidget):
    """ This code is for helping the user interact with the configurations of the VOG device. """
    def __init__(self, parent, device, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        try:
            super().__init__(parent)
        except Exception as e:
            self.logger.exception("Error making VOGTab, passed parent is invalid")
            return
        self.setLayout(QVBoxLayout(self))
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(500)

        self.layout().addWidget(MyFrame(line=True))

        """ Set configuration value display area"""
        self.__config_frame = MyFrame()
        self.__config_horiz_layout = QHBoxLayout(self.__config_frame)
        self.__config_label = QLabel(self.__config_frame)
        self.__config_label.setAlignment(Qt.AlignCenter)
        self.__config_horiz_layout.addWidget(self.__config_label)
        self.__config_val = QLabel(self.__config_frame)
        self.__config_val.setAlignment(Qt.AlignCenter)
        self.__config_horiz_layout.addWidget(self.__config_val)
        self.layout().addWidget(self.__config_frame)

        self.layout().addWidget(MyFrame(line=True))

        """ Set preset button selection area. """
        self.__presets_frame = MyFrame()
        self.__presets_vert_layout = QVBoxLayout(self.__presets_frame)
        self.__nhtsa_button = QPushButton(self.__presets_frame)
        self.__presets_vert_layout.addWidget(self.__nhtsa_button)
        self.__eblindfold_button = QPushButton(self.__presets_frame)
        self.__presets_vert_layout.addWidget(self.__eblindfold_button)
        self.__direct_control_button = QPushButton(self.__presets_frame)
        self.__presets_vert_layout.addWidget(self.__direct_control_button)
        self.layout().addWidget(self.__presets_frame)

        self.layout().addWidget(MyFrame(line=True))

        """ Set open duration, close duration, and debounce time settings display area. """
        self.__input_box_frame = MyFrame()
        self.__input_box_grid_layout = QGridLayout(self.__input_box_frame)
        self.__input_box_grid_layout.setContentsMargins(0, 6, 0, 6)
        self.__open_dur_label = QLabel(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__open_dur_label, 0, 0, 1, 1)
        self.__open_dur_line_edit = QLineEdit(self.__input_box_frame)
        self.__open_dur_line_edit.setFixedWidth(80)
        self.__input_box_grid_layout.addWidget(self.__open_dur_line_edit, 0, 1, 1, 1)
        self.__open_inf_check_box = QCheckBox(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__open_inf_check_box, 0, 2, 1, 1)
        self.__close_dur_label = QLabel(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__close_dur_label, 1, 0, 1, 1)
        self.__close_dur_line_edit = QLineEdit(self.__input_box_frame)
        self.__close_dur_line_edit.setFixedWidth(80)
        self.__input_box_grid_layout.addWidget(self.__close_dur_line_edit, 1, 1, 1, 1)
        self.__close_inf_check_box = QCheckBox(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__close_inf_check_box, 1, 2, 1, 1)
        self.__debounce_label = QLabel(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__debounce_label, 2, 0, 1, 1)
        self.__debounce_time_line_edit = QLineEdit(self.__input_box_frame)
        self.__debounce_time_line_edit.setFixedWidth(80)
        self.__input_box_grid_layout.addWidget(self.__debounce_time_line_edit, 2, 1, 1, 1)
        self.layout().addWidget(self.__input_box_frame)

        self.layout().addWidget(MyFrame(line=True))

        """ Set button mode setting display area. """
        self.__button_mode_frame = MyFrame()
        self.__button_mode_horiz_layout = QHBoxLayout(self.__button_mode_frame)
        self.__button_mode_label = QLabel(self.__button_mode_frame)
        self.__button_mode_horiz_layout.addWidget(self.__button_mode_label)
        self.__button_mode_selector = QComboBox(self.__button_mode_frame)
        self.__button_mode_selector.addItem("")
        self.__button_mode_selector.addItem("")
        self.__button_mode_horiz_layout.addWidget(self.__button_mode_selector)
        self.layout().addWidget(self.__button_mode_frame)

        self.layout().addWidget(MyFrame(line=True))

        """ Set upload button selection area. """
        self.__upload_settings_button = QPushButton()
        self.layout().addWidget(self.__upload_settings_button)

        self.layout().addWidget(MyFrame(line=True))

        """ Set manual control selection area. """
        self.__manual_control_button = QPushButton()
        self.layout().addWidget(self.__manual_control_button)

        self.layout().addWidget(MyFrame(line=True))

        self.__graph_buttons = []
        self.device_info = device
        self.__index = 0
        self.__set_texts()
        self.__set_tooltips()
        self.logger.debug("Initialized")

    def add_manual_control_handler(self, func):
        self.logger.debug("running")
        self.__manual_control_button.clicked.connect(func)
        self.logger.debug("done")

    def add_nhtsa_button_handler(self, func):
        self.logger.debug("running")
        self.__nhtsa_button.clicked.connect(func)
        self.logger.debug("done")

    def add_eblind_button_handler(self, func):
        self.logger.debug("running")
        self.__eblindfold_button.clicked.connect(func)
        self.logger.debug("done")

    def add_direct_control_button_handler(self, func):
        self.logger.debug("running")
        self.__direct_control_button.clicked.connect(func)
        self.logger.debug("done")

    def add_upload_button_handler(self, func):
        self.logger.debug("running")
        self.__upload_settings_button.clicked.connect(func)
        self.logger.debug("done")

    def add_open_inf_handler(self, func):
        self.logger.debug("running")
        self.__open_inf_check_box.toggled.connect(func)
        self.logger.debug("done")

    def add_close_inf_handler(self, func):
        self.logger.debug("running")
        self.__close_inf_check_box.toggled.connect(func)
        self.logger.debug("done")

    def add_open_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.__open_dur_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def add_close_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.__close_dur_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def add_debounce_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.__debounce_time_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def add_button_mode_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.__button_mode_selector.currentIndexChanged.connect(func)
        self.logger.debug("done")

    def set_upload_button_activity(self, is_active):
        """ Set upload button to enabled or disabled depending on is_active bool. """
        self.logger.debug("running")
        self.__upload_settings_button.setEnabled(is_active)
        self.logger.debug("done")

    def set_config_value(self, value):
        """ Set display value of config.txt. """
        self.logger.debug("running")
        self.__config_val.setText(value)
        self.logger.debug("done")

    def get_open_val(self):
        return self.__open_dur_line_edit.text()

    def set_open_val(self, val):
        """ Set display value of open duration. """
        self.logger.debug("running")
        self.__open_dur_line_edit.setText(str(val))
        self.logger.debug("done")

    def set_open_val_error(self, is_error):
        """ Set display of error in open duration line edit. """
        self.logger.debug("running")
        if is_error:
            self.__open_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.__open_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def set_close_val_error(self, is_error):
        """ Set display of error in close duration line edit. """
        self.logger.debug("running")
        if is_error:
            self.__close_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.__close_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def set_debounce_val_error(self, is_error):
        """ Set display of error in debounce line edit. """
        self.logger.debug("running")
        if is_error:
            self.__debounce_time_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.__debounce_time_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def set_open_val_entry_activity(self, is_active):
        """ Set open value line edit to enabled or disabled depending on is_active bool. """
        self.logger.debug("running")
        self.__open_dur_line_edit.setEnabled(is_active)
        self.logger.debug("done")

    def get_open_inf(self):
        return self.__open_inf_check_box.isChecked()

    def set_open_inf(self, is_checked):
        """ Set open infinity checkbox state to is_checked. """
        self.logger.debug("running")
        self.__open_inf_check_box.setChecked(is_checked)
        self.logger.debug("done")

    def get_close_val(self):
        return self.__close_dur_line_edit.text()

    def set_close_val(self, val):
        """ Set display value of close duration. """
        self.logger.debug("running")
        self.__close_dur_line_edit.setText(str(val))
        self.logger.debug("done")

    def set_close_val_entry_activity(self, is_active):
        """ Set close value line edit to enabled or disabled depending on is_active bool. """
        self.logger.debug("running")
        self.__close_dur_line_edit.setEnabled(is_active)
        self.logger.debug("done")

    def get_close_inf(self):
        return self.__close_inf_check_box.isChecked()

    def set_close_inf(self, is_checked):
        """ Set close infinity checkbox state to is_checked. """
        self.logger.debug("running")
        self.__close_inf_check_box.setChecked(is_checked)
        self.logger.debug("done")

    def get_debounce_val(self):
        return self.__debounce_time_line_edit.text()

    def set_debounce_val(self, val):
        """ Set debounce display value. """
        self.logger.debug("running")
        self.__debounce_time_line_edit.setText(str(val))
        self.logger.debug("done")

    def get_button_mode(self):
        return self.__button_mode_selector.currentIndex()

    def set_button_mode(self, val):
        """ Set display value of button mode. """
        self.logger.debug("running")
        self.__button_mode_selector.setCurrentIndex(int(val))
        self.logger.debug("done")

    def get_name(self):
        return self.device_info

    def __set_texts(self):
        self.logger.debug("running")
        self.__config_label.setText("Current configuration:")
        self.__config_val.setText("DIRECT CONTROL")
        self.__nhtsa_button.setText("NHTSA")
        self.__eblindfold_button.setText("eBlindfold")
        self.__direct_control_button.setText("Direct Control")
        self.__open_dur_label.setText("Open Duration")
        self.__open_inf_check_box.setText("INF")
        self.__close_dur_label.setText("Close Duration")
        self.__close_inf_check_box.setText("INF")
        self.__debounce_label.setText("Debounce Time")
        self.__button_mode_label.setText("Button Mode")
        self.__button_mode_selector.setItemText(0, "Hold")
        self.__button_mode_selector.setItemText(1, "Click")
        self.__upload_settings_button.setText("Upload settings")
        self.__manual_control_button.setText("Toggle Lens")
        self.logger.debug("done")

    def __set_tooltips(self):
        self.logger.debug("running")
        self.__config_label.setToolTip("Current device configuration")
        self.__nhtsa_button.setToolTip("Set Device to NHTSA standard")
        self.__eblindfold_button.setToolTip("Set Device to eBlindfold mode")
        self.__direct_control_button.setToolTip("Set Device to Direct Control mode")
        self.__button_mode_label.setToolTip("CHANGEME")
        self.__open_dur_label.setToolTip("Range: "
                                         + str(vog_min_open_close)
                                         + "-" + str(vog_max_open_close))
        self.__close_dur_label.setToolTip("Range: "
                                          + str(vog_min_open_close)
                                          + "-" + str(vog_max_open_close))
        self.__debounce_label.setToolTip("Range: "
                                         + str(vog_debounce_min)
                                         + "-" + str(vog_debounce_max))
        self.__open_inf_check_box.setToolTip("Set to manual switching")
        self.__close_inf_check_box.setToolTip("Set to manual switching")
        self.__upload_settings_button.setToolTip("Upload current configuration to device")
        self.__manual_control_button.setToolTip("Manually open or close the lens")
        self.logger.debug("done")
