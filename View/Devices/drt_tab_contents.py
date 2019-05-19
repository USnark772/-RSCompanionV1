# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QLabel, QPushButton, QSlider, QHBoxLayout, QVBoxLayout, QFrame, QLCDNumber
from PySide2.QtCore import QCoreApplication, QSize, Qt
from PySide2.QtGui import QFont
import Model.defs as defs


class TabContents(QVBoxLayout):
    def __init__(self, parent, device_name, msg_callback):
        super().__init__(parent)

        self.device_name = device_name
        self.msg_callback = msg_callback
        self.setObjectName(self.device_name)

        self.iso_default = False

        self.config_horizontal_layout = QHBoxLayout()
        self.config_horizontal_layout.setObjectName("config_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.config_label = QLabel()
        self.config_label.setFont(font)
        self.config_label.setObjectName("config_label")
        self.config_horizontal_layout.addWidget(self.config_label)

        self.config_label_val_sep_line = QFrame()
        self.config_label_val_sep_line.setFrameShape(QFrame.VLine)
        self.config_label_val_sep_line.setFrameShadow(QFrame.Sunken)
        self.config_label_val_sep_line.setObjectName("config_label_val_sep_line")
        self.config_horizontal_layout.addWidget(self.config_label_val_sep_line)

        font = QFont()
        font.setPointSize(12)
        self.config_val_label = QLabel()
        self.config_val_label.setFont(font)
        self.config_val_label.setObjectName("config_val_label")
        self.config_horizontal_layout.addWidget(self.config_val_label)
        self.addLayout(self.config_horizontal_layout)

        self.iso_default_push_button = QPushButton()
        self.iso_default_push_button.setObjectName("iso_default_push_button")
        self.addWidget(self.iso_default_push_button)

        self.config_stim_dur_sep_line = QFrame()
        self.config_stim_dur_sep_line.setFrameShape(QFrame.HLine)
        self.config_stim_dur_sep_line.setFrameShadow(QFrame.Sunken)
        self.config_stim_dur_sep_line.setObjectName("config_stim_dur_sep_line")
        self.addWidget(self.config_stim_dur_sep_line)

        self.stim_dur_horizontal_layout = QHBoxLayout()
        self.stim_dur_horizontal_layout.setObjectName("stim_dur_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.stim_dur_label = QLabel()
        self.stim_dur_label.setFont(font)
        self.stim_dur_label.setObjectName("stim_dur_label")
        self.stim_dur_horizontal_layout.addWidget(self.stim_dur_label)

        self.stim_dur_lcd_number = QLCDNumber()
        self.stim_dur_lcd_number.setMinimumSize(QSize(80, 40))
        self.stim_dur_lcd_number.setObjectName("stim_dur_lcd_number")
        self.stim_dur_horizontal_layout.addWidget(self.stim_dur_lcd_number)
        self.addLayout(self.stim_dur_horizontal_layout)

        self.stim_dur_slider = QSlider()
        self.stim_dur_slider.setMinimumSize(QSize(175, 0))
        self.stim_dur_slider.setOrientation(Qt.Horizontal)
        self.stim_dur_slider.setObjectName("stim_dur_slider")
        self.addWidget(self.stim_dur_slider)

        self.stim_dur_intens_sep_line = QFrame()
        self.stim_dur_intens_sep_line.setFrameShape(QFrame.HLine)
        self.stim_dur_intens_sep_line.setFrameShadow(QFrame.Sunken)
        self.stim_dur_intens_sep_line.setObjectName("stim_dur_intens_sep_line")
        self.addWidget(self.stim_dur_intens_sep_line)

        self.stim_intens_horizontal_layout = QHBoxLayout()
        self.stim_intens_horizontal_layout.setObjectName("stim_intens_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.stim_intens_label = QLabel()
        self.stim_intens_label.setFont(font)
        self.stim_intens_label.setObjectName("stim_intens_label")
        self.stim_intens_horizontal_layout.addWidget(self.stim_intens_label)

        self.stim_intens_lcd_number = QLCDNumber()
        self.stim_intens_lcd_number.setMinimumSize(QSize(80, 40))
        self.stim_intens_lcd_number.setObjectName("stim_intens_lcd_number")
        self.stim_intens_horizontal_layout.addWidget(self.stim_intens_lcd_number)
        self.addLayout(self.stim_intens_horizontal_layout)

        self.stim_intens_slider = QSlider()
        self.stim_intens_slider.setMinimumSize(QSize(175, 0))
        self.stim_intens_slider.setOrientation(Qt.Horizontal)
        self.stim_intens_slider.setObjectName("stim_intens_slider")
        self.addWidget(self.stim_intens_slider)

        self.stim_intens_upper_isi_sep_line = QFrame()
        self.stim_intens_upper_isi_sep_line.setFrameShape(QFrame.HLine)
        self.stim_intens_upper_isi_sep_line.setFrameShadow(QFrame.Sunken)
        self.stim_intens_upper_isi_sep_line.setObjectName("stim_intens_upper_isi_sep_line")
        self.addWidget(self.stim_intens_upper_isi_sep_line)

        self.upper_isi_horizontal_layout = QHBoxLayout()
        self.upper_isi_horizontal_layout.setObjectName("upper_isi_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.upper_isi_label = QLabel()
        self.upper_isi_label.setFont(font)
        self.upper_isi_label.setObjectName("upper_isi_label")
        self.upper_isi_horizontal_layout.addWidget(self.upper_isi_label)

        self.upper_isi_lcd_number = QLCDNumber()
        self.upper_isi_lcd_number.setMinimumSize(QSize(80, 40))
        self.upper_isi_lcd_number.setObjectName("upper_isi_lcd_number")
        self.upper_isi_horizontal_layout.addWidget(self.upper_isi_lcd_number)
        self.addLayout(self.upper_isi_horizontal_layout)

        self.upper_isi_slider = QSlider()
        self.upper_isi_slider.setMinimumSize(QSize(175, 0))
        self.upper_isi_slider.setOrientation(Qt.Horizontal)
        self.upper_isi_slider.setObjectName("upper_isi_slider")
        self.addWidget(self.upper_isi_slider)

        self.upper_lower_isi_sep_line = QFrame()
        self.upper_lower_isi_sep_line.setFrameShape(QFrame.HLine)
        self.upper_lower_isi_sep_line.setFrameShadow(QFrame.Sunken)
        self.upper_lower_isi_sep_line.setObjectName("upper_lower_isi_sep_line")
        self.addWidget(self.upper_lower_isi_sep_line)

        self.lower_isi_horizontal_layout = QHBoxLayout()
        self.lower_isi_horizontal_layout.setObjectName("lower_isi_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.lower_isi_label = QLabel()
        self.lower_isi_label.setFont(font)
        self.lower_isi_label.setObjectName("lower_isi_label")
        self.lower_isi_horizontal_layout.addWidget(self.lower_isi_label)

        self.lower_isi_lcd_number = QLCDNumber()
        self.lower_isi_lcd_number.setMinimumSize(QSize(80, 40))
        self.lower_isi_lcd_number.setObjectName("lower_isi_lcd_number")
        self.lower_isi_horizontal_layout.addWidget(self.lower_isi_lcd_number)
        self.addLayout(self.lower_isi_horizontal_layout)

        self.lower_isi_slider = QSlider()
        self.lower_isi_slider.setMinimumSize(QSize(175, 0))
        self.lower_isi_slider.setOrientation(Qt.Horizontal)
        self.lower_isi_slider.setObjectName("lower_isi_slider")
        self.addWidget(self.lower_isi_slider)

        self.__set_texts()
        # FROM CONFIG WIDGET
        self.__set_handlers()
        self.values = {'intensity': self.stim_intens_slider,
                       'upperISI': self.upper_isi_slider,
                       'lowerISI': self.lower_isi_slider,
                       'stimDur': self.stim_dur_slider}
        self.__set_slider_settings()
        # self.__set_line_edit_settings()
        self.__set_handlers()
        self.__get_vals()

    def __set_texts(self):
        _translate = QCoreApplication.translate
        self.config_label.setText(_translate("Form", "Configuration"))
        self.config_val_label.setText(_translate("Form", "ISO Standard"))
        self.iso_default_push_button.setText(_translate("Form", "ISO Standard"))
        self.stim_dur_label.setText(_translate("Form", "Stim Duration\n(msecs)"))
        self.stim_intens_label.setText(_translate("Form", "Stim Intensity"))
        self.upper_isi_label.setText(_translate("Form", "Upper ISI"))
        self.lower_isi_label.setText(_translate("Form", "Lower ISI"))

    def __set_slider_settings(self):
        self.stim_intens_slider.setRange(defs.drt_intensity_min, defs.drt_intensity_max)
        self.upper_isi_slider.setRange(defs.drt_ISI_min, defs.drt_ISI_max)
        self.lower_isi_slider.setRange(defs.drt_ISI_min, defs.drt_ISI_max)
        self.stim_dur_slider.setRange(defs.drt_stim_dur_min, defs.drt_stim_dur_max)

    def __set_handlers(self):
        self.iso_default_push_button.clicked.connect(self.__iso_button_handler)
        self.lower_isi_slider.valueChanged.connect(self.__push_upper_isi_slider)
        self.upper_isi_slider.valueChanged.connect(self.__push_lower_isi_slider)
        self.stim_dur_slider.valueChanged.connect(self.__stim_dur_changed_handler)
        self.stim_intens_slider.valueChanged.connect(self.__intensity_changed_handler)
        self.lower_isi_slider.sliderReleased.connect(self.__isi_released_handler)
        self.upper_isi_slider.sliderReleased.connect(self.__isi_released_handler)
        self.stim_dur_slider.sliderReleased.connect(self.__set_stim_duration_handler)
        self.stim_intens_slider.sliderReleased.connect(self.__set_intensity_handler)

    def __get_vals(self):
        if defs.debug_print:
            print("drt Getting vals")
        self.msg_callback({'cmd': "get_config"})

    def __set_val(self, var, val):
        self.values[var].setValue(int(val))

    def __isi_released_handler(self):
        self.__set_upper_isi_handler()
        self.__set_lower_isi_handler()

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

    def __intensity_changed_handler(self):
        self.stim_intens_lcd_number.display(self.stim_intens_slider.value())
        self.config_val_label.setText("Custom")

    def __stim_dur_changed_handler(self):
        self.stim_dur_lcd_number.display(self.stim_dur_slider.value())
        self.config_val_label.setText("Custom")

    def __iso_button_handler(self):
        self.iso_default = True
        self.config_val_label.setText("ISO Standard")
        self.__set_val('upperISI', 5000)
        self.__set_val('lowerISI', 3000)
        self.__set_val('stimDur', 1000)
        self.__set_val('intensity', 255)
        self.__set_intensity_handler()
        self.__set_upper_isi_handler()
        self.__set_lower_isi_handler()
        self.__set_stim_duration_handler()

    def __set_intensity_handler(self):
        self.msg_callback({'cmd': "set_intensity", 'arg': str(self.stim_intens_slider.value())})

    def __set_upper_isi_handler(self):
        self.msg_callback({'cmd': "set_upperISI", 'arg': str(self.upper_isi_slider.value())})

    def __set_lower_isi_handler(self):
        self.msg_callback({'cmd': "set_lowerISI", 'arg': str(self.lower_isi_slider.value())})

    def __set_stim_duration_handler(self):
        if defs.debug_print:
            print("drt Sending update to device")
        self.msg_callback({'cmd': "set_stimDur", 'arg': str(self.stim_dur_slider.value())})

    def handle_msg(self, msg_dict):
        if defs.debug_print:
            print()
            print("drt Handling message")
        for item in msg_dict:
            if defs.debug_print:
                print(item)
            self.__set_val(item, msg_dict[item])
