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
from PySide2.QtWidgets import QWidget, QGridLayout, QSlider, QLabel, QHBoxLayout, QVBoxLayout, QLineEdit
from PySide2.QtCore import Qt, QRect, QSize
from Devices.DRT.Model.drt_defs import drtv1_0_ISI_min, drtv1_0_stim_dur_min, drtv1_0_max_val
from Model.general_defs import tab_line_edit_compliant_style, tab_line_edit_error_style
from CompanionLib.companion_helpers import EasyFrame, ClickAnimationButton


class DRTTab(QWidget):
    """ This code is for helping the user interact with the configurations of the DRT device. """
    def __init__(self, parent, device, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        try:
            super().__init__(parent)
        except Exception as e:
            self.logger.exception("Error making DRTTab, passed in parent is invalid")
            return
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(400)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(EasyFrame(line=True))

        """ Set configuration value display area"""
        self.config_frame = EasyFrame()
        self.config_layout = QHBoxLayout(self.config_frame)
        self.config_label = QLabel(self.config_frame)
        self.config_label.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_label)
        self.config_val = QLabel(self.config_frame)
        self.config_val.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_val)
        self.layout().addWidget(self.config_frame)

        self.layout().addWidget(EasyFrame(line=True))

        """ Set preset button selection area. """
        self.presets_frame = EasyFrame()
        self.presets_layout = QVBoxLayout(self.presets_frame)
        self.iso_button = ClickAnimationButton(self.presets_frame)
        self.presets_layout.addWidget(self.iso_button)
        self.layout().addWidget(self.presets_frame)

        self.layout().addWidget(EasyFrame(line=True))

        """ Set stim intensity settings display area. """
        self.slider_frame = EasyFrame()
        self.slider_layout = QVBoxLayout(self.slider_frame)
        self.slider_label_layout = QHBoxLayout(self.slider_frame)
        self.stim_intens_label = QLabel(self.slider_frame)
        self.stim_intens_label.setAlignment(Qt.AlignLeft)
        self.slider_label_layout.addWidget(self.stim_intens_label)
        self.stim_intens_val = QLabel(self.slider_frame)
        self.stim_intens_val.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.slider_label_layout.addWidget(self.stim_intens_val)
        self.slider_layout.addLayout(self.slider_label_layout)
        self.stim_intens_slider = QSlider(self.slider_frame)
        self.stim_intens_slider.setMinimum(1)
        self.stim_intens_slider.setMaximum(100)
        self.stim_intens_slider.setSliderPosition(100)
        self.stim_intens_slider.setOrientation(Qt.Horizontal)
        self.stim_intens_slider.setTickPosition(QSlider.TicksBelow)
        self.stim_intens_slider.setTickInterval(10)
        self.slider_layout.addWidget(self.stim_intens_slider)
        self.layout().addWidget(self.slider_frame)

        self.layout().addWidget(EasyFrame(line=True))

        """ Set stim duration, upper isi and lower isi settings display area. """
        self.input_box_frame = EasyFrame()
        self.input_box_layout = QGridLayout(self.input_box_frame)
        self.stim_dur_line_edit = QLineEdit(self.input_box_frame)
        self.stim_dur_line_edit.setMaximumSize(QSize(100, 16777215))
        self.input_box_layout.addWidget(self.stim_dur_line_edit, 0, 1, 1, 1)
        self.upper_isi_label = QLabel(self.input_box_frame)
        self.input_box_layout.addWidget(self.upper_isi_label, 1, 0, 1, 1)
        self.upper_isi_line_edit = QLineEdit(self.input_box_frame)
        self.upper_isi_line_edit.setMaximumSize(QSize(100, 16777215))
        self.input_box_layout.addWidget(self.upper_isi_line_edit, 1, 1, 1, 1)
        self.stim_dur_label = QLabel(self.input_box_frame)
        self.input_box_layout.addWidget(self.stim_dur_label, 0, 0, 1, 1)
        self.lower_isi_line_edit = QLineEdit(self.input_box_frame)
        self.lower_isi_line_edit.setMaximumSize(QSize(100, 16777215))
        self.input_box_layout.addWidget(self.lower_isi_line_edit, 2, 1, 1, 1)
        self.lower_isi_label = QLabel(self.input_box_frame)
        self.input_box_layout.addWidget(self.lower_isi_label, 2, 0, 1, 1)
        self.layout().addWidget(self.input_box_frame)

        self.layout().addWidget(EasyFrame(line=True))

        """ Set upload button selection area. """
        self.upload_settings_button = ClickAnimationButton()
        self.layout().addWidget(self.upload_settings_button)

        self.layout().addWidget(EasyFrame(line=True))

        self.__graph_buttons = []
        self.device_info = device
        self.__index = 0
        self.__set_texts()
        self.__set_tooltips()
        self.logger.debug("Initialized")

    def add_iso_button_handler(self, func):
        self.logger.debug("running")
        self.iso_button.clicked.connect(func)
        self.logger.debug("done")

    def add_upload_button_handler(self, func):
        self.logger.debug("running")
        self.upload_settings_button.clicked.connect(func)
        self.logger.debug("done")

    def add_stim_dur_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.stim_dur_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def add_stim_intens_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.stim_intens_slider.valueChanged.connect(func)
        self.logger.debug("done")

    def add_upper_isi_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.upper_isi_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def add_lower_isi_entry_changed_handler(self, func):
        self.logger.debug("running")
        self.lower_isi_line_edit.textChanged.connect(func)
        self.logger.debug("done")

    def set_upload_button_activity(self, is_active):
        self.logger.debug("running")
        self.upload_settings_button.setEnabled(is_active)
        self.logger.debug("done")

    def set_config_val(self, val):
        """ Set display value of config.txt. """
        self.logger.debug("running")
        self.config_val.setText(str(val))
        self.logger.debug("done")

    def get_stim_dur_val(self):
        return self.stim_dur_line_edit.text()

    def set_stim_dur_val(self, val):
        """ Set display value of stim duration. """
        self.logger.debug("running")
        self.stim_dur_line_edit.setText(str(val))
        self.logger.debug("done")

    def set_stim_dur_val_error(self, is_error):
        """ Set display of error in stim duration line edit. """
        self.logger.debug("running")
        if is_error:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def set_upper_isi_val_error(self, is_error):
        """ Set display of error in upper isi line edit. """
        self.logger.debug("running")
        if is_error:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def set_lower_isi_val_error(self, is_error):
        """ Set display of error in lower isi line edit. """
        self.logger.debug("running")
        if is_error:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)
        self.logger.debug("done")

    def get_stim_intens_val(self):
        return self.stim_intens_slider.value()

    def set_stim_intens_val(self, val):
        """ Set display value of stim intensity. """
        self.logger.debug("running")
        self.stim_intens_slider.setValue(int(val))
        self.set_stim_intens_val_label(val)
        self.logger.debug("done")

    def set_stim_intens_val_label(self, val):
        """ Set display value of stim intensity label. """
        self.logger.debug("running")
        self.stim_intens_val.setText(str(val) + "%")
        self.logger.debug("done")

    def get_upper_isi_val(self):
        return self.upper_isi_line_edit.text()

    def set_upper_isi_val(self, val):
        """ Set display value of upper isi. """
        self.logger.debug("running")
        self.upper_isi_line_edit.setText(str(val))
        self.logger.debug("done")

    def get_lower_isi_val(self):
        return self.lower_isi_line_edit.text()

    def set_lower_isi_val(self, val):
        """ Set display value of lower isi. """
        self.logger.debug("running")
        self.lower_isi_line_edit.setText(str(val))
        self.logger.debug("done")

    def get_name(self):
        return self.device_info

    def __set_texts(self):
        self.logger.debug("running")
        self.config_label.setText("Current configuration:")
        self.config_val.setText("ISO")
        self.iso_button.setText("ISO")
        self.stim_dur_label.setText("Stim Duration")
        self.stim_intens_label.setText("Stim Intensity")
        self.upper_isi_label.setText("Upper ISI")
        self.lower_isi_label.setText("Lower ISI")
        self.upload_settings_button.setText("Upload settings")
        self.logger.debug("done")

    def __set_tooltips(self):
        self.logger.debug("running")
        self.config_label.setToolTip("Current device configuration")
        self.iso_button.setToolTip("Set device to ISO standard")
        self.upper_isi_label.setToolTip("Milliseconds. Range: Lower ISI-" + str(drtv1_0_max_val))
        self.lower_isi_label.setToolTip("Milliseconds. Range: " + str(drtv1_0_ISI_min) + "-Upper ISI")
        self.stim_dur_label.setToolTip("Milliseconds. Range: " + str(drtv1_0_stim_dur_min) + "-" + str(drtv1_0_max_val))
        self.stim_intens_label.setToolTip("Intensity of the stimulus")
        self.upload_settings_button.setToolTip("Upload current configuration to device")
        self.stim_intens_slider.setToolTip(str(self.stim_intens_slider.value()) + "%")
        self.logger.debug("done")
