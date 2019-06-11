# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from math import trunc
from PySide2.QtWidgets import QWidget, QSlider, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLineEdit
from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QFont
from Model.defs import drtv1_0_intensity_max, drtv1_0_intensity_min, drtv1_0_ISI_max, drtv1_0_ISI_min, \
    drtv1_0_stim_dur_max, drtv1_0_stim_dur_min, drtv1_0_iso_standards, drtv1_0_max_val


class DRTTab(QWidget):
    def __init__(self, parent, msg_callback, device):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setFixedHeight(400)

        self.config_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)
        self.config_label = QLabel()
        self.config_label.setFont(font)
        self.config_label.setAlignment(Qt.AlignCenter)
        self.config_horizontal_layout.addWidget(self.config_label)

        self.config_label_val_sep_line = QFrame()
        self.config_label_val_sep_line.setFrameShape(QFrame.VLine)
        self.config_label_val_sep_line.setFrameShadow(QFrame.Sunken)
        self.config_horizontal_layout.addWidget(self.config_label_val_sep_line)

        font = QFont()
        font.setPointSize(10)
        self.config_val_label = QLabel()
        self.config_val_label.setFont(font)
        self.config_val_label.setAlignment(Qt.AlignCenter)
        self.config_horizontal_layout.addWidget(self.config_val_label)
        self.layout().addLayout(self.config_horizontal_layout)

        self.iso_default_push_button = QPushButton()
        self.layout().addWidget(self.iso_default_push_button)

        self.config_stim_dur_sep_line = QFrame()
        self.config_stim_dur_sep_line.setFrameShape(QFrame.HLine)
        self.config_stim_dur_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.config_stim_dur_sep_line)

        self.stim_dur_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)
        self.stim_dur_label = QLabel()
        self.stim_dur_label.setFont(font)
        self.stim_dur_horizontal_layout.addWidget(self.stim_dur_label)

        self.stim_dur_text_edit = QLineEdit()
        self.stim_dur_text_edit.setFixedWidth(100)
        self.stim_dur_horizontal_layout.addWidget(self.stim_dur_text_edit)
        self.layout().addLayout(self.stim_dur_horizontal_layout)

        self.stim_dur_intens_sep_line = QFrame()
        self.stim_dur_intens_sep_line.setFrameShape(QFrame.HLine)
        self.stim_dur_intens_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.stim_dur_intens_sep_line)

        self.stim_intens_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)
        self.stim_intens_label = QLabel()
        self.stim_intens_label.setFont(font)
        self.stim_intens_horizontal_layout.addWidget(self.stim_intens_label)

        self.stim_intens_val = QLabel()
        self.stim_intens_val.setAlignment(Qt.AlignCenter)
        self.stim_dur_horizontal_layout.addWidget(self.stim_intens_val)
        self.stim_intens_horizontal_layout.addWidget(self.stim_intens_val)
        self.layout().addLayout(self.stim_intens_horizontal_layout)

        self.stim_intens_slider = QSlider()
        self.stim_intens_slider.setOrientation(Qt.Horizontal)
        self.stim_intens_slider.setRange(drtv1_0_intensity_min, drtv1_0_intensity_max)
        self.layout().addWidget(self.stim_intens_slider)

        self.stim_intens_upper_isi_sep_line = QFrame()
        self.stim_intens_upper_isi_sep_line.setFrameShape(QFrame.HLine)
        self.stim_intens_upper_isi_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.stim_intens_upper_isi_sep_line)

        self.upper_isi_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)
        self.upper_isi_label = QLabel()
        self.upper_isi_label.setFont(font)
        self.upper_isi_horizontal_layout.addWidget(self.upper_isi_label)

        self.upper_isi_text_edit = QLineEdit()
        self.upper_isi_text_edit.setFixedWidth(100)
        self.upper_isi_horizontal_layout.addWidget(self.upper_isi_text_edit)
        self.layout().addLayout(self.upper_isi_horizontal_layout)

        self.upper_lower_isi_sep_line = QFrame()
        self.upper_lower_isi_sep_line.setFrameShape(QFrame.HLine)
        self.upper_lower_isi_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.upper_lower_isi_sep_line)

        self.lower_isi_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(10)
        self.lower_isi_label = QLabel()
        self.lower_isi_label.setFont(font)
        self.lower_isi_horizontal_layout.addWidget(self.lower_isi_label)

        self.lower_isi_text_edit = QLineEdit()
        self.lower_isi_text_edit.setFixedWidth(100)
        self.lower_isi_horizontal_layout.addWidget(self.lower_isi_text_edit)
        self.layout().addLayout(self.lower_isi_horizontal_layout)

        self.upload_settings_button = QPushButton()
        self.layout().addWidget(self.upload_settings_button)

        self.compliant_text_color = "rgb(0, 0, 0)"
        self.error_text_color = "rgb(255, 0, 0)"
        self.selection_color = "rgb(0, 150, 255)"
        self.font_size = "13px"
        self.error_style = "QLineEdit { color: "\
                           + self.error_text_color\
                           + "; selection-background-color: "\
                           + self.selection_color \
                           + "; font: " \
                           + self.font_size + "; }"
        self.compliant_style = "QLineEdit { color: "\
                               + self.compliant_text_color\
                               + "; selection-background-color: "\
                               + self.selection_color \
                               + "; font: " \
                               + self.font_size + "; }"
        self.handling_msg = False
        self.errors = [False, False, False]  # upper, lower, dur
        self.current_vals = {'intensity': drtv1_0_iso_standards['intensity'],
                             'upperISI': drtv1_0_iso_standards['upperISI'],
                             'lowerISI': drtv1_0_iso_standards['lowerISI'],
                             'stimDur': drtv1_0_iso_standards['stimDur']}
        self.msg_callback = msg_callback
        self.device_info = device
        self.__index = 0
        self.text_edits = {'intensity': self.stim_intens_val,
                           'upperISI': self.upper_isi_text_edit,
                           'lowerISI': self.lower_isi_text_edit,
                           'stimDur': self.stim_dur_text_edit}
        self.sliders = {'intensity': self.stim_intens_slider}
        self.__set_texts()
        self.__set_tooltips()
        self.__set_handlers()
        self.__get_vals()

    def handle_msg(self, msg_dict):
        self.handling_msg = True
        for item in msg_dict:
            self.__set_val(item, msg_dict[item])
        self.__check_vals()
        self.handling_msg = False

    def get_name(self):
        return self.device_info[0]

    def set_index(self, new_index):
        self.__index = new_index

    def get_index(self):
        return self.__index

    def __set_texts(self):
        self.config_label.setText("Config")
        self.config_val_label.setText("ISO Standard")
        self.iso_default_push_button.setText("ISO Standard")
        self.stim_dur_label.setText("Stim Duration")
        self.stim_intens_label.setText("Stim Intensity")
        self.upper_isi_label.setText("Upper ISI")
        self.lower_isi_label.setText("Lower ISI")
        self.upload_settings_button.setText("Upload settings")

    def __set_tooltips(self):
        self.config_label.setToolTip("Current device configuration")
        self.iso_default_push_button.setToolTip("Set device to ISO standard")
        self.upper_isi_label.setToolTip("Milliseconds. Range: Lower ISI-" + str(drtv1_0_max_val))
        self.lower_isi_label.setToolTip("Milliseconds. Range: 0-Upper ISI")
        self.stim_dur_label.setToolTip("Milliseconds. Range: 0-" + str(drtv1_0_max_val))
        self.upload_settings_button.setToolTip("Upload current configuration to device")

    def __set_handlers(self):
        self.iso_default_push_button.clicked.connect(self.__iso_button_handler)
        self.stim_dur_text_edit.editingFinished.connect(self.__stim_dur_changed_handler)
        self.upper_isi_text_edit.editingFinished.connect(self.__upper_isi_changed_handler)
        self.lower_isi_text_edit.editingFinished.connect(self.__lower_isi_changed_handler)
        self.stim_intens_slider.valueChanged.connect(self.__stim_intens_changed_handler)
        self.upload_settings_button.clicked.connect(self.__upload_button_handler)

    def __stim_dur_changed_handler(self):
        print("stim dur changed")
        self.__check_stim_dur_val()
        self.__check_error_colors()
        self.__set_upload_button(True)

    def __stim_intens_changed_handler(self):
        print("slider changed")
        new_intens = self.stim_intens_slider.value()
        self.stim_intens_val.setText(self.__calc_intens_percentage(new_intens))
        self.__set_upload_button(True)

    def __upper_isi_changed_handler(self):
        print("upper isi changed")
        self.__check_upper_isi_val()
        self.__check_error_colors()
        self.__set_upload_button(True)

    def __lower_isi_changed_handler(self):
        print("lower isi changed")
        self.__check_lower_isi_val()
        self.__check_error_colors()
        self.__set_upload_button(True)

    def __iso_button_handler(self):
        self.config_val_label.setText("ISO Standard")
        self.__set_upper_isi(drtv1_0_iso_standards['upperISI'])
        self.__set_lower_isi(drtv1_0_iso_standards['lowerISI'])
        self.__set_intens(drtv1_0_iso_standards['intensity'])
        self.__set_stim_duration(drtv1_0_iso_standards['stimDur'])
        self.__reset_errors()
        self.__set_upload_button(False)

    def __upload_button_handler(self):
        # Only send uploads if needed, then set as custom and disable upload button
        stim_dur = int(self.stim_dur_text_edit.text())
        stim_intens = self.stim_intens_slider.value()
        upper = int(self.upper_isi_text_edit.text())
        lower = int(self.lower_isi_text_edit.text())
        if stim_dur != self.current_vals['stimDur']:
            self.__set_stim_duration(stim_dur)
        if stim_intens != self.current_vals['intensity']:
            self.__set_intens(stim_intens)
        if upper != self.current_vals['upperISI']:
            self.__set_upper_isi(upper)
        if lower != self.current_vals['lowerISI']:
            self.__set_lower_isi(lower)
        self.config_val_label.setText("Custom")
        self.__set_upload_button(False)

    def __check_stim_dur_val(self):
        self.errors[2] = True
        new_dur = self.stim_dur_text_edit.text()
        if new_dur.isdigit():
            new_dur_int = int(new_dur)
            if drtv1_0_stim_dur_max >= new_dur_int >= drtv1_0_stim_dur_min:
                self.errors[2] = False

    def __check_upper_isi_val(self):
        self.errors[0] = True
        new_upper = self.upper_isi_text_edit.text()
        if new_upper.isdigit():
            new_upper_int = int(new_upper)
            if drtv1_0_ISI_max >= new_upper_int >= int(self.lower_isi_text_edit.text()):
                self.errors[0] = False

    def __check_lower_isi_val(self):
        self.errors[1] = True
        new_lower = self.lower_isi_text_edit.text()
        if new_lower.isdigit():
            new_lower_int = int(new_lower)
            if int(self.upper_isi_text_edit.text()) >= new_lower_int >= drtv1_0_ISI_min:
                self.errors[1] = False

    def __set_upload_button(self, is_active):
        if self.errors[0] or self.errors[1] or self.errors[2] or self.handling_msg:
            self.upload_settings_button.setEnabled(False)
        else:
            self.upload_settings_button.setEnabled(is_active)

    def __get_vals(self):
        self.__callback({'cmd': "get_config"})

    def __set_val(self, var, val):
        self.current_vals[var] = val

    def __check_vals(self):
        for key in self.current_vals:
            if key in self.sliders.keys():
                self.sliders[key].setValue(self.current_vals[key])
            if key in self.text_edits.keys():
                if key == "intensity":
                    value = self.__calc_intens_percentage(self.current_vals[key])
                else:
                    value = str(self.current_vals[key])
                self.text_edits[key].setText(value)

    def __check_error_colors(self):
        if self.errors[0]:
            self.upper_isi_text_edit.setStyleSheet(self.error_style)
        else:
            self.upper_isi_text_edit.setStyleSheet(self.compliant_style)
        if self.errors[1]:
            self.lower_isi_text_edit.setStyleSheet(self.error_style)
        else:
            self.lower_isi_text_edit.setStyleSheet(self.compliant_style)
        if self.errors[2]:
            self.stim_dur_text_edit.setStyleSheet(self.error_style)
        else:
            self.stim_dur_text_edit.setStyleSheet(self.compliant_style)

    def __reset_errors(self):
        for i in range(len(self.errors)):
            self.errors[i] = False
        self.__check_error_colors()

    def __set_intens(self, val):
        self.__callback({'cmd': "set_intensity", 'arg': str(val)})

    def __set_upper_isi(self, val):
        self.__callback({'cmd': "set_upperISI", 'arg': str(val)})

    def __set_lower_isi(self, val):
        self.__callback({'cmd': "set_lowerISI", 'arg': str(val)})

    def __set_stim_duration(self, val):
        self.__callback({'cmd': "set_stimDur", 'arg': str(val)})

    def __callback(self, msg):
        self.msg_callback(self.device_info, msg)

    @staticmethod
    def __calc_intens_percentage(val):
        return str(trunc(val / drtv1_0_intensity_max * 100)) + "%"
