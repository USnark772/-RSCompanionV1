# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QLineEdit
from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QFont
from Model.defs import drt_intensity_max, drt_intensity_min, drt_ISI_max, drt_ISI_min, drt_stim_dur_max, \
    drt_stim_dur_min, drt_iso_standards, drt_max_val


class TabContents(QWidget):
    def __init__(self, parent, msg_callback, device):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 520))

        self.config_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(12)
        self.config_label = QLabel()
        self.config_label.setFont(font)
        self.config_label.setAlignment(Qt.AlignCenter)
        self.config_horizontal_layout.addWidget(self.config_label)

        self.config_label_val_sep_line = QFrame()
        self.config_label_val_sep_line.setFrameShape(QFrame.VLine)
        self.config_label_val_sep_line.setFrameShadow(QFrame.Sunken)
        self.config_horizontal_layout.addWidget(self.config_label_val_sep_line)

        font = QFont()
        font.setPointSize(12)
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
        font.setPointSize(12)
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
        font.setPointSize(12)
        self.stim_intens_label = QLabel()
        self.stim_intens_label.setFont(font)
        self.stim_intens_horizontal_layout.addWidget(self.stim_intens_label)

        self.stim_intens_text_edit = QLineEdit()
        self.stim_intens_text_edit.setFixedWidth(100)
        self.stim_dur_horizontal_layout.addWidget(self.stim_intens_text_edit)
        self.stim_intens_horizontal_layout.addWidget(self.stim_intens_text_edit)
        self.layout().addLayout(self.stim_intens_horizontal_layout)

        self.stim_intens_upper_isi_sep_line = QFrame()
        self.stim_intens_upper_isi_sep_line.setFrameShape(QFrame.HLine)
        self.stim_intens_upper_isi_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.stim_intens_upper_isi_sep_line)

        self.upper_isi_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(12)
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
        font.setPointSize(12)
        self.lower_isi_label = QLabel()
        self.lower_isi_label.setFont(font)
        self.lower_isi_horizontal_layout.addWidget(self.lower_isi_label)

        self.lower_isi_text_edit = QLineEdit()
        self.lower_isi_text_edit.setFixedWidth(100)
        self.lower_isi_horizontal_layout.addWidget(self.lower_isi_text_edit)
        self.layout().addLayout(self.lower_isi_horizontal_layout)

        self.iso = False
        self.current_dur = drt_iso_standards['stimDur']
        self.current_intens = drt_iso_standards['intensity']
        self.current_upper = drt_iso_standards['upperISI']
        self.current_lower = drt_iso_standards['lowerISI']
        self.msg_callback = msg_callback
        self.device_info = device
        self.__index = 0
        self.text_edits = {'intensity': self.stim_intens_text_edit,
                           'upperISI': self.upper_isi_text_edit,
                           'lowerISI': self.lower_isi_text_edit,
                           'stimDur': self.stim_dur_text_edit}
        self.__set_texts()
        self.__set_handlers()
        self.__get_vals()

    def handle_msg(self, msg_dict):
        for item in msg_dict:
            self.__set_val(item, msg_dict[item])

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
        self.stim_dur_label.setText("Stim Duration\n(msecs)")
        self.stim_intens_label.setText("Stim Intensity")
        self.upper_isi_label.setText("Upper ISI")
        self.lower_isi_label.setText("Lower ISI")

    def __set_handlers(self):
        self.iso_default_push_button.clicked.connect(self.__iso_button_handler)
        self.stim_dur_text_edit.editingFinished.connect(self.__stim_dur_changed_handler)
        self.stim_intens_text_edit.editingFinished.connect(self.__stim_intens_changed_handler)
        self.upper_isi_text_edit.editingFinished.connect(self.__upper_isi_changed_handler)
        self.lower_isi_text_edit.editingFinished.connect(self.__lower_isi_changed_handler)

    def __get_vals(self):
        self.__callback({'cmd': "get_config"})

    def __set_val(self, var, val):
        self.text_edits[var].setText(str(val))

    def __push_upper_isi_slider(self):
        if self.lower_isi_slider.value() >= self.upper_isi_slider.value():
            self.upper_isi_slider.setValue(self.lower_isi_slider.value())
        self.lower_isi_lcd_number.display(self.lower_isi_slider.value())
        self.config_val_label.setText("Custom")

    def __push_lower_isi_slider(self):
        if self.upper_isi_slider.value() <= self.lower_isi_slider.value():
            self.lower_isi_slider.setValue(self.upper_isi_slider.value())
        self.upper_isi_lcd_number.display(self.upper_isi_slider.value())
        self.config_val_label.setText("Custom")

    def __stim_dur_changed_handler(self):
        new_dur = self.stim_dur_text_edit.text()
        new_dur_int = int(new_dur)
        if new_dur.isdigit() and drt_max_val >= new_dur_int > 0 and new_dur_int != self.current_dur:
            self.current_dur = new_dur_int
            if self.current_dur != drt_iso_standards['stimDur']:
                self.config_val_label.setText("Custom")
            self.__set_stim_duration()
        else:
            self.stim_dur_text_edit.setText(str(self.current_dur))

    def __stim_intens_changed_handler(self):
        new_intens = self.stim_intens_text_edit.text()
        new_intens_int = int(new_intens)
        if new_intens.isdigit() and 255 >= new_intens_int > 0 and new_intens_int != self.current_dur:
            self.current_intens = new_intens_int
            if self.current_intens != drt_iso_standards['intensity']:
                self.config_val_label.setText("Custom")
            self.__set_intensity()
        else:
            self.stim_intens_text_edit.setText(str(self.current_intens))

    def __upper_isi_changed_handler(self):
        new_upper = self.upper_isi_text_edit.text()
        new_upper_int = int(new_upper)
        if new_upper.isdigit() and drt_max_val >= new_upper_int > 0 and new_upper_int != self.current_upper:
            self.current_upper = new_upper_int
            if self.current_upper != drt_iso_standards['upperISI']:
                self.config_val_label.setText("Custom")
            self.__set_upper_isi()
        else:
            self.upper_isi_text_edit.setText(str(self.current_upper))

    def __lower_isi_changed_handler(self):
        new_lower = self.lower_isi_text_edit.text()
        new_lower_int = int(new_lower)
        if new_lower.isdigit() and drt_max_val >= new_lower_int > 0 and new_lower_int != self.current_lower:
            self.current_lower = new_lower_int
            if self.current_lower != drt_iso_standards['lowerISI']:
                self.config_val_label.setText("Custom")
            self.__set_lower_isi()
        else:
            self.lower_isi_text_edit.setText(str(self.current_lower))

    def __iso_button_handler(self):

        self.config_val_label.setText("ISO Standard")
        self.__set_val('upperISI', drt_iso_standards['upperISI'])
        self.__set_val('lowerISI', drt_iso_standards['lowerISI'])
        self.__set_val('intensity', drt_iso_standards['intensity'])
        self.__set_val('stimDur', drt_iso_standards['stimDur'])
        self.__set_upper_isi()
        self.__set_lower_isi()
        self.__set_intensity()
        self.__set_stim_duration()

    def __set_intensity(self):
        self.__callback({'cmd': "set_intensity", 'arg': self.stim_intens_text_edit.text()})

    def __set_upper_isi(self):
        self.__callback({'cmd': "set_upperISI", 'arg': self.upper_isi_text_edit.text()})

    def __set_lower_isi(self):
        self.__callback({'cmd': "set_lowerISI", 'arg': self.lower_isi_text_edit.text()})

    def __set_stim_duration(self):
        self.__callback({'cmd': "set_stimDur", 'arg': self.stim_dur_text_edit.text()})

    def __callback(self, msg):
        self.msg_callback(self.device_info, msg)
