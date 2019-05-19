# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QLabel, QPushButton, QSlider, QComboBox, QHBoxLayout, QVBoxLayout, QCheckBox, QFrame, \
    QLCDNumber
from PySide2.QtCore import QCoreApplication, Qt, QSize
from PySide2.QtGui import QFont
import Model.defs as defs


class TabContents(QVBoxLayout):
    def __init__(self, parent, device_name, msg_callback):
        super().__init__(parent)

        self.device_name = device_name
        self.msg_callback = msg_callback

        self.max_val = 2147483647

        self.setObjectName(self.device_name)

        self.config_horizontal_layout = QHBoxLayout()
        self.config_horizontal_layout.setObjectName("config_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.config_label = QLabel()
        self.config_label.setFont(font)
        self.config_label.setObjectName("config_label")
        self.config_horizontal_layout.addWidget(self.config_label)

        self.config_label_val_line = QFrame()
        self.config_label_val_line.setFrameShape(QFrame.VLine)
        self.config_label_val_line.setFrameShadow(QFrame.Sunken)
        self.config_label_val_line.setObjectName("config_label_val_line")
        self.config_horizontal_layout.addWidget(self.config_label_val_line)

        font = QFont()
        font.setPointSize(12)
        self.config_val_label = QLabel()
        self.config_val_label.setFont(font)
        self.config_val_label.setObjectName("config_val_label")
        self.config_horizontal_layout.addWidget(self.config_val_label)
        self.addLayout(self.config_horizontal_layout)

        self.config_opened_sep_line = QFrame()
        self.config_opened_sep_line.setFrameShape(QFrame.HLine)
        self.config_opened_sep_line.setFrameShadow(QFrame.Sunken)
        self.config_opened_sep_line.setObjectName("config_opened_sep_line")
        self.addWidget(self.config_opened_sep_line)

        font = QFont()
        font.setPointSize(14)
        self.opened_state_dur_label_horizontal_layout = QHBoxLayout()
        self.opened_state_dur_label_horizontal_layout.setObjectName("opened_state_dur_label_horizontal_layout")
        self.opened_state_dur_label = QLabel()
        self.opened_state_dur_label.setFont(font)
        self.opened_state_dur_label.setObjectName("opened_state_dur_label")
        self.opened_state_dur_label_horizontal_layout.addWidget(self.opened_state_dur_label)

        self.opened_state_dur_lcd_number = QLCDNumber()
        self.opened_state_dur_lcd_number.setMinimumSize(QSize(0, 40))
        self.opened_state_dur_lcd_number.setObjectName("opened_state_dur_lcd_number")
        self.opened_state_dur_label_horizontal_layout.addWidget(self.opened_state_dur_lcd_number)
        self.addLayout(self.opened_state_dur_label_horizontal_layout)

        self.opened_state_dur_slider_horizontal_layout = QHBoxLayout()
        self.opened_state_dur_slider_horizontal_layout.setObjectName("opened_state_dur_slider_horizontal_layout")
        self.opened_state_inf_check_box = QCheckBox()
        self.opened_state_inf_check_box.setObjectName("opened_state_dur_inf_check_box")
        self.opened_state_dur_slider_horizontal_layout.addWidget(self.opened_state_inf_check_box)

        self.max_opened_slider = QSlider()
        self.max_opened_slider.setOrientation(Qt.Horizontal)
        self.max_opened_slider.setObjectName("max_opened_slider")
        self.opened_state_dur_slider_horizontal_layout.addWidget(self.max_opened_slider)
        self.addLayout(self.opened_state_dur_slider_horizontal_layout)

        self.opened_mode_sep_line = QFrame()
        self.opened_mode_sep_line.setFrameShape(QFrame.HLine)
        self.opened_mode_sep_line.setFrameShadow(QFrame.Sunken)
        self.opened_mode_sep_line.setObjectName("opened_mode_sep_line")
        self.addWidget(self.opened_mode_sep_line)

        font = QFont()
        font.setPointSize(14)
        self.debounce_label = QLabel()
        self.debounce_label.setFont(font)
        self.debounce_label.setAlignment(Qt.AlignCenter)
        self.debounce_label.setObjectName("debounce_label")
        self.addWidget(self.debounce_label)

        self.button_mode_combo_box = QComboBox()
        self.button_mode_combo_box.setEditable(False)
        self.button_mode_combo_box.setObjectName("button_mode_combo_box")
        self.button_mode_combo_box.addItem("")
        self.button_mode_combo_box.addItem("")
        self.addWidget(self.button_mode_combo_box)

        self.mode_closed_sep_line = QFrame()
        self.mode_closed_sep_line.setFrameShape(QFrame.HLine)
        self.mode_closed_sep_line.setFrameShadow(QFrame.Sunken)
        self.mode_closed_sep_line.setObjectName("mode_closed_sep_line")
        self.addWidget(self.mode_closed_sep_line)

        self.closed_state_dur_horizontal_layout = QHBoxLayout()
        self.closed_state_dur_horizontal_layout.setObjectName("closed_state_dur_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.closed_state_dur_label = QLabel()
        self.closed_state_dur_label.setFont(font)
        self.closed_state_dur_label.setObjectName("closed_state_dur_label")
        self.closed_state_dur_horizontal_layout.addWidget(self.closed_state_dur_label)

        self.closed_state_dur_lcd_number = QLCDNumber()
        self.closed_state_dur_lcd_number.setMinimumSize(QSize(0, 40))
        self.closed_state_dur_lcd_number.setObjectName("closed_state_dur_lcd_number")
        self.closed_state_dur_horizontal_layout.addWidget(self.closed_state_dur_lcd_number)
        self.addLayout(self.closed_state_dur_horizontal_layout)

        self.closed_state_dur_slider_horizontal_layout = QHBoxLayout()
        self.closed_state_dur_slider_horizontal_layout.setObjectName("closed_state_dur_slider_horizontal_layout")
        self.closed_state_inf_check_box = QCheckBox()
        self.closed_state_inf_check_box.setObjectName("closed_state_inf_check_box")
        self.closed_state_dur_slider_horizontal_layout.addWidget(self.closed_state_inf_check_box)

        self.max_closed_slider = QSlider()
        self.max_closed_slider.setOrientation(Qt.Horizontal)
        self.max_closed_slider.setObjectName("max_closed_slider")
        self.closed_state_dur_slider_horizontal_layout.addWidget(self.max_closed_slider)
        self.addLayout(self.closed_state_dur_slider_horizontal_layout)

        self.closed_debounce_sep_line = QFrame()
        self.closed_debounce_sep_line.setFrameShape(QFrame.HLine)
        self.closed_debounce_sep_line.setFrameShadow(QFrame.Sunken)
        self.closed_debounce_sep_line.setObjectName("closed_debounce_sep_line")
        self.addWidget(self.closed_debounce_sep_line)

        self.debounce_horizontal_layout = QHBoxLayout()
        self.debounce_horizontal_layout.setObjectName("debounce_horizontal_layout")

        font = QFont()
        font.setPointSize(14)
        self.debounce_label = QLabel()
        self.debounce_label.setFont(font)
        self.debounce_label.setObjectName("debounce_label")
        self.debounce_horizontal_layout.addWidget(self.debounce_label)

        self.debounce_lcd_number = QLCDNumber()
        self.debounce_lcd_number.setMinimumSize(QSize(0, 40))
        self.debounce_lcd_number.setObjectName("debounce_lcd_number")
        self.debounce_horizontal_layout.addWidget(self.debounce_lcd_number)
        self.addLayout(self.debounce_horizontal_layout)

        self.debounce_time_slider = QSlider()
        self.debounce_time_slider.setOrientation(Qt.Horizontal)
        self.debounce_time_slider.setObjectName("debounce_time_slider")
        self.addWidget(self.debounce_time_slider)

        self.debounce_presets_sep_line = QFrame()
        self.debounce_presets_sep_line.setFrameShape(QFrame.HLine)
        self.debounce_presets_sep_line.setFrameShadow(QFrame.Sunken)
        self.debounce_presets_sep_line.setObjectName("debounce_presets_sep_line")
        self.addWidget(self.debounce_presets_sep_line)

        self.nhtsa_standard_push_button = QPushButton()
        self.nhtsa_standard_push_button.setObjectName("nhtsa_standard_push_button")
        self.addWidget(self.nhtsa_standard_push_button)

        self.eblind_push_button = QPushButton()
        self.eblind_push_button.setObjectName("eblind_push_button")
        self.addWidget(self.eblind_push_button)

        self.dir_control_default_push_button = QPushButton()
        self.dir_control_default_push_button.setObjectName("dir_control_default_push_button")
        self.addWidget(self.dir_control_default_push_button)

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

    def __set_texts(self):
        _translate = QCoreApplication.translate
        self.config_label.setText(_translate("Form", "Configuration"))
        self.config_val_label.setText(_translate("Form", "--DIRECT CONTROL--"))
        self.opened_state_dur_label.setText(_translate("Form", "Opened State\nDuration"))
        self.opened_state_inf_check_box.setText(_translate("Form", "INF"))
        self.debounce_label.setText(_translate("Form", "Button Mode"))
        self.button_mode_combo_box.setItemText(0, _translate("Form", "Click"))
        self.button_mode_combo_box.setItemText(1, _translate("Form", "Hold"))
        self.closed_state_dur_label.setText(_translate("Form", "Closed State\nDuration"))
        self.closed_state_inf_check_box.setText(_translate("Form", "INF"))
        self.debounce_label.setText(_translate("Form", "Debounce Time"))
        self.nhtsa_standard_push_button.setText(_translate("Form", "NHTSA Standard"))
        self.eblind_push_button.setText(_translate("Form", "eBlindfold"))
        self.dir_control_default_push_button.setText(_translate("Form", "Direct Control"))

    def __set_slider_ranges(self):
        self.max_opened_slider.setRange(defs.vog_min_open_close, defs.vog_max_open_close)
        self.max_closed_slider.setRange(defs.vog_min_open_close, defs.vog_max_open_close)
        self.debounce_time_slider.setRange(defs.vog_debounce_min, defs.vog_debounce_max)
        self.button_mode_combo_box.setCurrentIndex(defs.vog_button_mode)

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

    def __get_vals(self):
        self.msg_callback({'cmd': 'get_configName'})
        self.msg_callback({'cmd': 'get_configMaxOpen'})
        self.msg_callback({'cmd': 'get_configMaxClose'})
        self.msg_callback({'cmd': 'get_configDebounce'})
        self.msg_callback({'cmd': 'get_configClickMode'})
        self.msg_callback({'cmd': 'get_configButtonControl'})

    def __set_val(self, item, val):
        if defs.debug_print:
            print("item", item)
        if item == "ButtonControl":
            self.values[item] = int(val)
        elif item == "Name":
            font = QFont()
            font.setPointSize(12)
            _translate = QCoreApplication.translate
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
        print("__opened_inf changed")
        if self.opened_state_inf_check_box.checkState() == Qt.Checked:
            print("went form unchecked to checked")
            self.max_opened_slider.setDisabled(True)
            self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_val)})
        else:
            print("went from checked to unchecked")
            self.max_opened_slider.setDisabled(False)
            self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_opened_slider.value())})

    def __closed_inf_handler(self):
        if defs.debug_print:
            print("__closed_inf changed")
        if self.closed_state_inf_check_box.checkState() == Qt.Checked:
            if defs.debug_print:
                print("went form unchecked to checked")
            self.max_closed_slider.setDisabled(True)
            self.msg_callback({'cmd': "set_configMaxClose", 'arg': str(self.max_val)})
        else:
            if defs.debug_print:
                print("went from checked to unchecked")
            self.max_closed_slider.setDisabled(False)
            self.msg_callback({'cmd': "set_configMaxClose", 'arg': str(self.max_closed_slider.value())})

    def __nhtsa_default_handler(self):
        if defs.debug_print:
            print("__nhtsa_default_handler")
        self.opened_state_inf_check_box.setChecked(False)
        self.closed_state_inf_check_box.setChecked(False)
        self.max_opened_slider.setDisabled(False)
        self.max_closed_slider.setDisabled(False)
        self.msg_callback({'cmd': "set_configName", 'arg': "NHTSA"})
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': "1500"})
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': "1500"})
        self.msg_callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.msg_callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.msg_callback({'cmd': "set_configButtonControl", 'arg': "0"})


    def __eblind_handler(self):
        if defs.debug_print:
            print("__eblind_handler")
        self.opened_state_inf_check_box.setChecked(False)
        self.closed_state_inf_check_box.setChecked(False)
        self.max_opened_slider.setDisabled(False)
        self.max_closed_slider.setDisabled(False)
        self.msg_callback({'cmd': "set_configName", 'arg': "eBlindfold"})
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_val)})
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': "0"})
        self.msg_callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.msg_callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.msg_callback({'cmd': "set_configButtonControl", 'arg': "0"})

    def __direct_control_handler(self):
        if defs.debug_print:
            print("__direct_control_handler")
        self.opened_state_inf_check_box.setChecked(True)
        self.closed_state_inf_check_box.setChecked(True)
        self.max_opened_slider.setDisabled(True)
        self.max_closed_slider.setDisabled(True)
        self.msg_callback({'cmd': "set_configName", 'arg': "--DIRECT CONTROL--"})
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_val)})
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': "0"})
        self.msg_callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.msg_callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.msg_callback({'cmd': "set_configButtonControl", 'arg': "1"})

    def __max_open_slider_handler(self):
        # print("max_open_slider changed")
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_opened_slider.value())})

    def __max_closed_slider_handler(self):
        # print("max_closed_slider changed")
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': str(self.max_closed_slider.value())})

    def __debounce_slider_handler(self):
        # print("debounce_slider changed")
        self.msg_callback({'cmd': "set_configDebounce", 'arg': str(self.debounce_time_slider.value())})

    def handle_msg(self, msg_dict):
        # print("vog_device_view.ConfigureWidget.handle_msg()", msg_dict)
        for item in msg_dict:
            # print(item, msg_dict[item])
            self.__set_val(item, msg_dict[item])
