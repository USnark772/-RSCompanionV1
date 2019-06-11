# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from math import trunc
from PySide2.QtWidgets import QWidget, QGridLayout, QSlider, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame,\
    QLineEdit
from PySide2.QtCore import Qt, QRect, QSize
from Model.defs import drtv1_0_intensity_max, drtv1_0_intensity_min, drtv1_0_ISI_max, drtv1_0_ISI_min,\
    drtv1_0_stim_dur_max, drtv1_0_stim_dur_min, drtv1_0_iso_standards, drtv1_0_max_val,\
    tab_line_edit_compliant_style, tab_line_edit_error_style


class DRTTab(QWidget):
    def __init__(self, parent, device):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setFixedHeight(350)

        self.config_horizontal_layout = QHBoxLayout()

        self.layout().addWidget(self.__MyFrame(True))

        self.config_frame = self.__MyFrame()
        self.config_layout = QHBoxLayout(self.config_frame)
        self.config_label = QLabel(self.config_frame)
        self.config_label.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_label)
        self.config_layout.addWidget(self.__MyFrame(True, True))
        self.config_val = QLabel(self.config_frame)
        self.config_val.setAlignment(Qt.AlignCenter)
        self.config_layout.addWidget(self.config_val)
        self.layout().addWidget(self.config_frame)

        self.layout().addWidget(self.__MyFrame(True))

        self.presets_frame = self.__MyFrame()
        self.presets_layout = QVBoxLayout(self.presets_frame)
        self.iso_button = QPushButton(self.presets_frame)
        self.presets_layout.addWidget(self.iso_button)
        self.layout().addWidget(self.presets_frame)

        self.layout().addWidget(self.__MyFrame(True))

        self.slider_frame = self.__MyFrame()
        self.slider_layout = QVBoxLayout(self.slider_frame)
        self.STIMINTENSLAYOUT = QHBoxLayout(self.slider_frame)
        self.stim_intens_label = QLabel(self.slider_frame)
        self.stim_intens_label.setAlignment(Qt.AlignLeft)
        self.STIMINTENSLAYOUT.addWidget(self.stim_intens_label)
        self.stim_intens_val = QLabel(self.slider_frame)
        self.stim_intens_val.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.STIMINTENSLAYOUT.addWidget(self.stim_intens_val)
        self.slider_layout.addLayout(self.STIMINTENSLAYOUT)
#        self.slider_layout.addWidget(self.stim_intens_label)
        self.stim_intens_slider = QSlider(self.slider_frame)
        self.stim_intens_slider.setMinimum(1)
        self.stim_intens_slider.setMaximum(100)
        self.stim_intens_slider.setSliderPosition(100)
        self.stim_intens_slider.setOrientation(Qt.Horizontal)
        self.stim_intens_slider.setTickPosition(QSlider.TicksBelow)
        self.stim_intens_slider.setTickInterval(10)
        self.slider_layout.addWidget(self.stim_intens_slider)
        self.layout().addWidget(self.slider_frame)

        self.layout().addWidget(self.__MyFrame(True))

        self.input_box_frame = self.__MyFrame()
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

        self.layout().addWidget(self.__MyFrame(True))

        self.upload_settings_button = QPushButton()
        self.layout().addWidget(self.upload_settings_button)

        self.layout().addWidget(self.__MyFrame(True))

        self.device_info = device
        self.__index = 0
        self.__set_texts()
        self.__set_tooltips()

    def add_iso_button_handler(self, func):
        self.iso_button.clicked.connect(func)

    def add_upload_button_handler(self, func):
        self.upload_settings_button.clicked.connect(func)

    def add_stim_dur_entry_changed_handler(self, func):
        self.stim_dur_line_edit.textChanged.connect(func)

    def add_stim_intens_entry_changed_handler(self, func):
        self.stim_intens_slider.valueChanged.connect(func)

    def add_upper_isi_entry_changed_handler(self, func):
        self.upper_isi_line_edit.textChanged.connect(func)

    def add_lower_isi_entry_changed_handler(self, func):
        self.lower_isi_line_edit.textChanged.connect(func)

    def set_upload_button_activity(self, is_active):
        self.upload_settings_button.setEnabled(is_active)

    def set_config_val(self, val):
        self.config_val.setText(str(val))

    def get_stim_dur_val(self):
        return self.stim_dur_line_edit.text()

    def set_stim_dur_val(self, val):
        self.stim_dur_line_edit.setText(str(val))

    def set_stim_dur_val_error(self, is_error):
        if is_error:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.stim_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)

    def set_upper_isi_val_error(self, is_error):
        if is_error:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.upper_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)

    def set_lower_isi_val_error(self, is_error):
        if is_error:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.lower_isi_line_edit.setStyleSheet(tab_line_edit_compliant_style)

    def get_stim_intens_val(self):
        return self.stim_intens_slider.value()

    def set_stim_intens_val(self, val):
        self.stim_intens_slider.setValue(int(val))
        self.set_stim_intens_val_label(val)

    def set_stim_intens_val_label(self, val):
        self.stim_intens_val.setText(str(val) + "%")

    def get_upper_isi_val(self):
        return self.upper_isi_line_edit.text()

    def set_upper_isi_val(self, val):
        self.upper_isi_line_edit.setText(str(val))

    def get_lower_isi_val(self):
        return self.lower_isi_line_edit.text()

    def set_lower_isi_val(self, val):
        self.lower_isi_line_edit.setText(str(val))

    def get_name(self):
        return self.device_info

    def get_index(self):
        return self.__index

    def set_index(self, new_index):
        self.__index = new_index

    def __set_texts(self):
        self.config_label.setText("Config")
        self.config_val.setText("ISO")
        self.iso_button.setText("ISO")
        self.stim_dur_label.setText("Stim Duration")
        self.stim_intens_label.setText("Stim Intensity")
        self.upper_isi_label.setText("Upper ISI")
        self.lower_isi_label.setText("Lower ISI")
        self.upload_settings_button.setText("Upload settings")

    def __set_tooltips(self):
        self.config_label.setToolTip("Current device configuration")
        self.iso_button.setToolTip("Set device to ISO standard")
        self.upper_isi_label.setToolTip("Milliseconds. Range: Lower ISI-" + str(drtv1_0_max_val))
        self.lower_isi_label.setToolTip("Milliseconds. Range: " + str(drtv1_0_ISI_min) + "-Upper ISI")
        self.stim_dur_label.setToolTip("Milliseconds. Range: " + str(drtv1_0_stim_dur_min) + "-" + str(drtv1_0_max_val))
        self.stim_intens_label.setToolTip("Intensity of the stimulus")
        self.upload_settings_button.setToolTip("Upload current configuration to device")
        self.stim_intens_slider.setToolTip(str(self.stim_intens_slider.value()) + "%")

    class __MyFrame(QFrame):
        def __init__(self, line=False, vert=False):
            super().__init__()
            if line:
                if vert:
                    self.setFrameShape(QFrame.VLine)
                else:
                    self.setFrameShape(QFrame.HLine)
                self.setFrameShadow(QFrame.Sunken)
            else:
                self.setFrameShape(QFrame.StyledPanel)
                self.setFrameShadow(QFrame.Raised)



    '''

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

    '''