# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QSlider, QComboBox, QHBoxLayout, QVBoxLayout, QCheckBox, \
    QFrame, QLCDNumber
from PySide2.QtCore import Qt, QSize, QRect
from PySide2.QtGui import QFont
from Model.general_defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min, vog_button_mode


class TabContents(QWidget):
    def __init__(self, parent, msg_callback, device):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setGeometry(QRect(0, 0, 200, 520))

        self.config_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(14)
        self.config_label = QLabel()
        self.config_label.setFont(font)
        self.config_horizontal_layout.addWidget(self.config_label)

        self.config_label_val_line = QFrame()
        self.config_label_val_line.setFrameShape(QFrame.VLine)
        self.config_label_val_line.setFrameShadow(QFrame.Sunken)
        self.config_horizontal_layout.addWidget(self.config_label_val_line)

        font = QFont()
        font.setPointSize(12)
        self.config_val_label = QLabel()
        self.config_val_label.setFont(font)
        self.config_horizontal_layout.addWidget(self.config_val_label)
        self.layout().addLayout(self.config_horizontal_layout)

        self.config_opened_sep_line = QFrame()
        self.config_opened_sep_line.setFrameShape(QFrame.HLine)
        self.config_opened_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.config_opened_sep_line)

        font = QFont()
        font.setPointSize(14)
        self.opened_state_dur_label_horizontal_layout = QHBoxLayout()
        self.opened_state_dur_label = QLabel()
        self.opened_state_dur_label.setFont(font)
        self.opened_state_dur_label_horizontal_layout.addWidget(self.opened_state_dur_label)

        self.opened_state_dur_lcd_number = QLCDNumber()
        self.opened_state_dur_lcd_number.setMinimumSize(QSize(0, 40))
        self.opened_state_dur_label_horizontal_layout.addWidget(self.opened_state_dur_lcd_number)
        self.layout().addLayout(self.opened_state_dur_label_horizontal_layout)

        self.opened_state_dur_slider_horizontal_layout = QHBoxLayout()
        self.opened_state_inf_check_box = QCheckBox()
        self.opened_state_dur_slider_horizontal_layout.addWidget(self.opened_state_inf_check_box)

        self.max_opened_slider = QSlider()
        self.max_opened_slider.setOrientation(Qt.Horizontal)
        self.opened_state_dur_slider_horizontal_layout.addWidget(self.max_opened_slider)
        self.layout().addLayout(self.opened_state_dur_slider_horizontal_layout)

        self.opened_mode_sep_line = QFrame()
        self.opened_mode_sep_line.setFrameShape(QFrame.HLine)
        self.opened_mode_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.opened_mode_sep_line)

        font = QFont()
        font.setPointSize(14)
        self.debounce_label = QLabel()
        self.debounce_label.setFont(font)
        self.debounce_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.debounce_label)

        self.button_mode_combo_box = QComboBox()
        self.button_mode_combo_box.setEditable(False)
        self.button_mode_combo_box.addItem("")
        self.button_mode_combo_box.addItem("")
        self.layout().addWidget(self.button_mode_combo_box)

        self.mode_closed_sep_line = QFrame()
        self.mode_closed_sep_line.setFrameShape(QFrame.HLine)
        self.mode_closed_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.mode_closed_sep_line)

        self.closed_state_dur_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(14)
        self.closed_state_dur_label = QLabel()
        self.closed_state_dur_label.setFont(font)
        self.closed_state_dur_horizontal_layout.addWidget(self.closed_state_dur_label)

        self.closed_state_dur_lcd_number = QLCDNumber()
        self.closed_state_dur_lcd_number.setMinimumSize(QSize(0, 40))
        self.closed_state_dur_horizontal_layout.addWidget(self.closed_state_dur_lcd_number)
        self.layout().addLayout(self.closed_state_dur_horizontal_layout)

        self.closed_state_dur_slider_horizontal_layout = QHBoxLayout()
        self.closed_state_inf_check_box = QCheckBox()
        self.closed_state_dur_slider_horizontal_layout.addWidget(self.closed_state_inf_check_box)

        self.max_closed_slider = QSlider()
        self.max_closed_slider.setOrientation(Qt.Horizontal)
        self.closed_state_dur_slider_horizontal_layout.addWidget(self.max_closed_slider)
        self.layout().addLayout(self.closed_state_dur_slider_horizontal_layout)

        self.closed_debounce_sep_line = QFrame()
        self.closed_debounce_sep_line.setFrameShape(QFrame.HLine)
        self.closed_debounce_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.closed_debounce_sep_line)

        self.debounce_horizontal_layout = QHBoxLayout()

        font = QFont()
        font.setPointSize(14)
        self.debounce_label = QLabel()
        self.debounce_label.setFont(font)
        self.debounce_horizontal_layout.addWidget(self.debounce_label)

        self.debounce_lcd_number = QLCDNumber()
        self.debounce_lcd_number.setMinimumSize(QSize(0, 40))
        self.debounce_horizontal_layout.addWidget(self.debounce_lcd_number)
        self.layout().addLayout(self.debounce_horizontal_layout)

        self.debounce_time_slider = QSlider()
        self.debounce_time_slider.setOrientation(Qt.Horizontal)
        self.layout().addWidget(self.debounce_time_slider)

        self.debounce_presets_sep_line = QFrame()
        self.debounce_presets_sep_line.setFrameShape(QFrame.HLine)
        self.debounce_presets_sep_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.debounce_presets_sep_line)

        self.nhtsa_standard_push_button = QPushButton()
        self.layout().addWidget(self.nhtsa_standard_push_button)

        self.eblind_push_button = QPushButton()
        self.layout().addWidget(self.eblind_push_button)

        self.dir_control_default_push_button = QPushButton()
        self.layout().addWidget(self.dir_control_default_push_button)

        self.msg_callback = msg_callback
        self.device_info = device
        self.__index = 0
        self.max_val = str(2147483647)
        self.values = {'MaxOpen': self.max_opened_slider,
                       'MaxClose': self.max_closed_slider,
                       'Debounce': self.debounce_time_slider,
                       'ClickMode': self.button_mode_combo_box,
                       'Name': self.config_val_label,
                       'ButtonControl': 0}  # For direct control mode
        self.__set_texts()
        self.__set_slider_ranges()
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
        self.config_label.setText("Configuration")
        self.config_val_label.setText("--DIRECT CONTROL--")
        self.opened_state_dur_label.setText("Opened State\nDuration")
        self.opened_state_inf_check_box.setText("INF")
        self.debounce_label.setText("Button Mode")
        self.button_mode_combo_box.setItemText(0, "Click")
        self.button_mode_combo_box.setItemText(1, "Hold")
        self.closed_state_dur_label.setText("Closed State\nDuration")
        self.closed_state_inf_check_box.setText("INF")
        self.debounce_label.setText("Debounce Time")
        self.nhtsa_standard_push_button.setText("NHTSA Standard")
        self.eblind_push_button.setText("eBlindfold")
        self.dir_control_default_push_button.setText("Direct Control")

    def __set_slider_ranges(self):
        self.max_opened_slider.setRange(vog_min_open_close, vog_max_open_close)
        self.max_closed_slider.setRange(vog_min_open_close, vog_max_open_close)
        self.debounce_time_slider.setRange(vog_debounce_min, vog_debounce_max)
        self.button_mode_combo_box.setCurrentIndex(vog_button_mode)

    def __set_handlers(self):
        self.eblind_push_button.clicked.connect(self.__eblind_handler)
        self.nhtsa_standard_push_button.clicked.connect(self.__nhtsa_default_handler)
        self.dir_control_default_push_button.clicked.connect(self.__direct_control_handler)
        self.max_opened_slider.sliderReleased.connect(self.__max_open_slider_handler)
        self.max_closed_slider.sliderReleased.connect(self.__max_closed_slider_handler)
        self.debounce_time_slider.sliderReleased.connect(self.__debounce_slider_handler)
        self.max_opened_slider.valueChanged.connect(self.__max_opened_slider_lcd_monitor)
        self.max_closed_slider.valueChanged.connect(self.__max_closed_slider_lcd_monitor)
        self.debounce_time_slider.valueChanged.connect(self.__debounce_slider_lcd_monitor)
        self.opened_state_inf_check_box.clicked.connect(self.__opened_inf_handler)
        self.closed_state_inf_check_box.clicked.connect(self.__closed_inf_handler)
        self.button_mode_combo_box.currentIndexChanged.connect(self.__change_event)

    def __change_event(self):
        self.__callback({'cmd': 'set_configClickMode', 'arg': self.button_mode_combo_box.currentIndex()})

    def __get_vals(self):
        self.__callback({'cmd': 'get_configName'})
        self.__callback({'cmd': 'get_configMaxOpen'})
        self.__callback({'cmd': 'get_configMaxClose'})
        self.__callback({'cmd': 'get_configDebounce'})
        self.__callback({'cmd': 'get_configClickMode'})
        self.__callback({'cmd': 'get_configButtonControl'})

    def __set_val(self, item, val):
        if item == "ButtonControl":
            self.values[item] = int(val)
        elif item == "Name":
            font = QFont()
            font.setPointSize(12)
            self.values[item].setText(val)
            self.values[item].setFont(font)
        elif self.values[item].isEnabled():
            self.values[item].setValue(int(val))

    def __max_opened_slider_lcd_monitor(self):
        self.opened_state_dur_lcd_number.display(self.max_opened_slider.value())

    def __max_closed_slider_lcd_monitor(self):
        self.closed_state_dur_lcd_number.display(self.max_closed_slider.value())

    def __debounce_slider_lcd_monitor(self):
        self.debounce_lcd_number.display(self.debounce_time_slider.value())

    def __opened_inf_handler(self):
        if self.opened_state_inf_check_box.checkState() == Qt.Checked:
            self.max_opened_slider.setDisabled(True)
            self.__callback({'cmd': "set_configMaxOpen", 'arg': self.max_val})
        else:
            self.max_opened_slider.setDisabled(False)
            self.__callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_opened_slider.value())})

    def __closed_inf_handler(self):
        if self.closed_state_inf_check_box.checkState() == Qt.Checked:
            self.max_closed_slider.setDisabled(True)
            self.__callback({'cmd': "set_configMaxClose", 'arg': self.max_val})
        else:
            self.max_closed_slider.setDisabled(False)
            self.__callback({'cmd': "set_configMaxClose", 'arg': str(self.max_closed_slider.value())})

    def __nhtsa_default_handler(self):
        self.opened_state_inf_check_box.setChecked(False)
        self.closed_state_inf_check_box.setChecked(False)
        self.max_opened_slider.setDisabled(False)
        self.max_closed_slider.setDisabled(False)
        self.__callback({'cmd': "set_configName", 'arg': "NHTSA"})
        self.__callback({'cmd': "set_configMaxOpen", 'arg': "1500"})
        self.__callback({'cmd': "set_configMaxClose", 'arg': "1500"})
        self.__callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.__callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.__callback({'cmd': "set_configButtonControl", 'arg': "0"})

    def __eblind_handler(self):
        self.opened_state_inf_check_box.setChecked(False)
        self.closed_state_inf_check_box.setChecked(False)
        self.max_opened_slider.setDisabled(False)
        self.max_closed_slider.setDisabled(False)
        self.__callback({'cmd': "set_configName", 'arg': "eBlindfold"})
        self.__callback({'cmd': "set_configMaxOpen", 'arg': self.max_val})
        self.__callback({'cmd': "set_configMaxClose", 'arg': "0"})
        self.__callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.__callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.__callback({'cmd': "set_configButtonControl", 'arg': "0"})

    def __direct_control_handler(self):
        self.opened_state_inf_check_box.setChecked(True)
        self.closed_state_inf_check_box.setChecked(True)
        self.max_opened_slider.setDisabled(True)
        self.max_closed_slider.setDisabled(True)
        self.__callback({'cmd': "set_configName", 'arg': "--DIRECT CONTROL--"})
        self.__callback({'cmd': "set_configMaxOpen", 'arg': self.max_val})
        self.__callback({'cmd': "set_configMaxClose", 'arg': "0"})
        self.__callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.__callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.__callback({'cmd': "set_configButtonControl", 'arg': "1"})

    def __max_open_slider_handler(self):
        self.__callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_opened_slider.value())})

    def __max_closed_slider_handler(self):
        self.__callback({'cmd': "set_configMaxClose", 'arg': str(self.max_closed_slider.value())})

    def __debounce_slider_handler(self):
        self.__callback({'cmd': "set_configDebounce", 'arg': str(self.debounce_time_slider.value())})

    def __callback(self, msg):
        self.msg_callback(self.device_info, msg)
