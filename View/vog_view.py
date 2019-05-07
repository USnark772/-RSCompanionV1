# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QLabel, QPushButton, QSlider, QGraphicsView, QWidget, QComboBox, QScrollArea, QGroupBox,\
    QHBoxLayout, QVBoxLayout, QToolButton, QCheckBox
from PySide2.QtCore import QRect, QCoreApplication, Qt
from PySide2.QtCharts import QtCharts
import Model.defs as defs


class Tab(QWidget):
    def __init__(self, device_id, msg_callback, settings_widget_button):
        super().__init__()
        self.device_id = device_id
        self.msg_callback = msg_callback
        self.configure_widget_button = settings_widget_button
        self.device_name = self.device_id[0] + " on " + self.device_id[1]
        self.setObjectName(self.device_name)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(QRect(0, 0, 201, 521))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setGeometry(QRect(0, 0, 199, 519))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.group_box_1 = QGroupBox(self.scroll_area_contents)
        self.group_box_1.setGeometry(QRect(0, 0, 191, 101))
        self.group_box_1.setObjectName("group_box_1")
        self.group_box_1_horiz_layout_1 = QHBoxLayout(self.group_box_1)
        self.group_box_1_horiz_layout_1.setObjectName("group_box_1_horiz_layout")
        self.vert_layout = QVBoxLayout()
        self.vert_layout.setObjectName("vert_layout")
        # TODO: add more buttons?
        '''
        self.push_button_1 = QPushButton(self.group_box_1)
        self.push_button_1.setObjectName("push_button_1")
        self.vert_layout.addWidget(self.push_button_1)
        '''
        self.peek_button = QPushButton(self.scroll_area_contents)
        self.peek_button.setObjectName("peek_button")
        self.peek_button.setGeometry(50, 300, 100, 20)

        # self.vert_layout.addWidget(self.push_button_2)

        self.group_box_1_horiz_layout_2 = QHBoxLayout()
        self.group_box_1_horiz_layout_2.setObjectName("group_box_1_horiz_layout_2")
        self.tool_button = QToolButton(self.group_box_1)
        self.tool_button.setObjectName("tool_button")
        self.group_box_1_horiz_layout_2.addWidget(self.tool_button)

        self.vert_layout.addLayout(self.group_box_1_horiz_layout_2)
        self.group_box_1_horiz_layout_1.addLayout(self.vert_layout)
        self.scroll_area.setWidget(self.scroll_area_contents)
        self.__set_texts()
        self.__setup_button_handlers()

    def __set_texts(self):
        _translate = QCoreApplication.translate
        '''
        self.push_button_1.setText(_translate("MainWindow", "CHANGEME PushButton"))
        '''
        self.peek_button.setText(_translate("MainWindow", "Open"))

        self.tool_button.setText(_translate("MainWindow", "Configure device"))

    def __setup_button_handlers(self):
        self.tool_button.clicked.connect(self.__setup_push_button_handler)
        self.peek_button.clicked.connect(self.__peek_handler)
        '''
        self.push_button_1.clicked.connect()
        '''

    # TODO: Change button text depending on if lenses are open or closed
    def __peek_handler(self):
        print("peek button clicked")
        # if

    def __setup_push_button_handler(self):
        self.configure_widget_button()


class ConfigureWidget(QWidget):
    def __init__(self, device_name, msg_callback):
        super().__init__()
        self.device_name = device_name
        self.msg_callback = msg_callback
        self.setObjectName(self.device_name)
        self.button_control = 0
        self.max_val = 2147483647
        self.resize(400, 300)
        self.settings_graphics_view_2 = QGraphicsView(self)
        self.settings_graphics_view_2.setGeometry(QRect(75, 20, 301, 151))
        self.settings_graphics_view_2.setObjectName("settings_graphics_view_2")
        # self.set_current_push_button = QPushButton(self)
        # self.set_current_push_button.setGeometry(QRect(30, 230, 71, 41))
        # self.set_current_push_button.setObjectName("set_current_push_button")
        self.debounce_time_slider = QSlider(self)
        self.debounce_time_slider.setGeometry(QRect(30, 30, 16, 160))
        self.debounce_time_slider.setMinimum(1)
        self.debounce_time_slider.setMaximum(100)
        self.debounce_time_slider.setOrientation(Qt.Vertical)
        self.debounce_time_slider.setObjectName("debounce_time_slider")
        self.debounce_label = QLabel(self)
        self.debounce_label.setGeometry(QRect(10, 10, 61, 16))
        self.debounce_label.setObjectName("debounce_label")
        self.opened_state_duration_label = QLabel(self)
        self.opened_state_duration_label.setGeometry(QRect(304, 227, 81, 20))
        self.opened_state_duration_label.setObjectName("upper_isi_label_2")
        self.max_open_slider = QSlider(self)
        self.max_open_slider.setGeometry(QRect(130, 230, 160, 16))
        self.max_open_slider.setOrientation(Qt.Horizontal)
        self.max_open_slider.setObjectName("max_open_slider")
        self.closed_state_duration_label = QLabel(self)
        self.closed_state_duration_label.setGeometry(QRect(304, 257, 81, 20))
        self.closed_state_duration_label.setObjectName("upper_isi_label_3")
        self.max_closed_slider = QSlider(self)
        self.max_closed_slider.setGeometry(QRect(130, 260, 160, 16))
        self.max_closed_slider.setOrientation(Qt.Horizontal)
        self.max_closed_slider.setObjectName("max_closed_slider")
        self.nhtsa_default_push_button = QPushButton(self)
        self.nhtsa_default_push_button.setGeometry(QRect(10, 200, 61, 20))
        self.nhtsa_default_push_button.setObjectName("eblind_default_push_button")
        self.eblindfold_push_button = QPushButton(self)
        self.eblindfold_push_button.setGeometry(QRect(10, 230, 61, 20))
        self.eblindfold_push_button.setObjectName("nhtsa_default_push_button")
        self.dir_control_default_push_button = QPushButton(self)
        self.dir_control_default_push_button.setGeometry(QRect(10, 260, 61, 20))
        self.dir_control_default_push_button.setObjectName("dir_control_default_push_button")
        self.config_label = QLabel(self)
        self.config_label.setGeometry(QRect(240, 190, 61, 16))
        self.config_label.setObjectName("config_label")
        self.config_val_label = QLabel(self)
        self.config_val_label.setGeometry(QRect(300, 190, 75, 16))
        self.config_val_label.setObjectName("config_val_label")
        self.button_mode_combo_box = QComboBox(self)
        self.button_mode_combo_box.setGeometry(QRect(150, 188, 53, 22))
        self.button_mode_combo_box.setEditable(False)
        self.button_mode_combo_box.setObjectName("button_mode_combo_box")
        self.button_mode_combo_box.addItem("")
        self.button_mode_combo_box.addItem("")
        self.button_mode_label = QLabel(self)
        self.button_mode_label.setGeometry(QRect(90, 190, 51, 16))
        self.button_mode_label.setObjectName("button_mode_label")

        self.opened_state_dur_inf_check_box = QCheckBox(self)
        self.opened_state_dur_inf_check_box.setGeometry(QRect(90, 230, 31, 16))
        self.opened_state_dur_inf_check_box.setObjectName("opened_state_dur_inf_check_box")
        self.closed_state_dur_inf_check_box = QCheckBox(self)
        self.closed_state_dur_inf_check_box.setGeometry(QRect(90, 260, 31, 16))
        self.closed_state_dur_inf_check_box.setObjectName("closed_state_dur_inf_check_box")

        self.__set_texts()
        self.values = {'MaxOpen': self.max_open_slider,
                       'MaxClose': self.max_closed_slider,
                       'Debounce': self.debounce_time_slider,
                       'ClickMode': self.button_mode_combo_box,
                       'Name': self.config_val_label,
                       'ButtonControl': self.button_control}  # For direct control mode
        self.__set_slider_ranges()
        self.__set_handlers()
        self.__get_vals()

    def __set_texts(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "VOG Config"))
        #self.set_current_push_button.setText(_translate("Form", "Upload settings"))
        self.debounce_label.setText(_translate("Form", "Debounce Time"))
        self.opened_state_duration_label.setText(_translate("Form", "Opened State Duration"))
        self.closed_state_duration_label.setText(_translate("Form", "Closed State Duration"))
        self.nhtsa_default_push_button.setText(_translate("Form", "NHTSA Default"))
        self.eblindfold_push_button.setText(_translate("Form", "eBlindfold"))
        self.dir_control_default_push_button.setText(_translate("Form", "Direct Control"))
        self.config_label.setText(_translate("Form", "Configuration:"))
        self.config_val_label.setText(_translate("Form", "--DIRECT CONTROL--"))
        self.button_mode_combo_box.setItemText(0, _translate("Form", "Click"))
        self.button_mode_combo_box.setItemText(1, _translate("Form", "Hold"))
        self.button_mode_label.setText(_translate("Form", "Button Mode:"))
        self.opened_state_dur_inf_check_box.setText(_translate("Form", "INF"))
        self.closed_state_dur_inf_check_box.setText(_translate("Form", "INF"))

    def __set_slider_ranges(self):
        self.max_open_slider.setRange(defs.vog_min_open_close, defs.vog_max_open_close)
        self.max_closed_slider.setRange(defs.vog_min_open_close, defs.vog_max_open_close)
        self.debounce_time_slider.setRange(defs.vog_debounce_min, defs.vog_debounce_max)
        self.button_mode_combo_box.setCurrentIndex(0)

    def __set_handlers(self):
        # self.set_current_push_button.clicked.connect(self.__update_button_handler)
        self.eblindfold_push_button.clicked.connect(self.__eblind_handler)
        self.nhtsa_default_push_button.clicked.connect(self.__nhtsa_default_handler)
        self.dir_control_default_push_button.clicked.connect(self.__direct_control_handler)
        # self.button_mode_combo_box.currentIndexChanged.connect(self.__button_combo_box_handler)
        self.max_open_slider.sliderReleased.connect(self.__max_open_slider_handler)
        self.max_closed_slider.sliderReleased.connect(self.__max_closed_slider_handler)
        self.debounce_time_slider.sliderReleased.connect(self.__debounce_slider_handler)
        self.opened_state_dur_inf_check_box.clicked.connect(self.__opened_inf_handler)
        self.closed_state_dur_inf_check_box.clicked.connect(self.__closed_inf_handler)

    def __get_vals(self):
        self.msg_callback({'cmd': 'get_configName'})
        self.msg_callback({'cmd': 'get_configMaxOpen'})
        self.msg_callback({'cmd': 'get_configMaxClose'})
        self.msg_callback({'cmd': 'get_configDebounce'})
        self.msg_callback({'cmd': 'get_configClickMode'})
        self.msg_callback({'cmd': 'get_configButtonControl'})

    def __set_val(self, item, val):
        if self.values[item].isEnabled():
            self.values[item].setValue(int(val))

    def __update_button_handler(self):
        print("__update_button_handler")

    def __opened_inf_handler(self):
        print("__opened_inf changed")
        if self.opened_state_dur_inf_check_box.checkState() == Qt.Checked:
            print("went form unchecked to checked")
            self.max_open_slider.setDisabled(True)
            self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_val)})
        else:
            print("went from checked to unchecked")
            self.max_open_slider.setDisabled(False)
            self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_open_slider.value())})

    def __closed_inf_handler(self):
        print("__closed_inf changed")
        if self.closed_state_dur_inf_check_box.checkState() == Qt.Checked:
            print("went form unchecked to checked")
            self.max_closed_slider.setDisabled(True)
            self.msg_callback({'cmd': "set_configMaxClose", 'arg': str(self.max_val)})
        else:
            print("went from checked to unchecked")
            self.max_closed_slider.setDisabled(False)
            self.msg_callback({'cmd': "set_configMaxClose", 'arg': str(self.max_closed_slider.value())})

    def __nhtsa_default_handler(self):
        # print("__nhtsa_default_handler")
        self.msg_callback({'cmd': "set_configName", 'arg': "NHTSA"})
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': "1500"})
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': "1500"})
        self.msg_callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.msg_callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.msg_callback({'cmd': "set_configButtonControl", 'arg': "0"})

    def __eblind_handler(self):
        # print("__eblind_handler")
        self.msg_callback({'cmd': "set_configName", 'arg': "eBlindfold"})
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_val)})
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': "0"})
        self.msg_callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.msg_callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.msg_callback({'cmd': "set_configButtonControl", 'arg': "0"})

    def __direct_control_handler(self):
        # print("__direct_control_handler")
        self.msg_callback({'cmd': "set_configName", 'arg': "--DIRECT CONTROL--"})
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_val)})
        self.msg_callback({'cmd': "set_configMaxClose", 'arg': "0"})
        self.msg_callback({'cmd': "set_configDebounce", 'arg': "100"})
        self.msg_callback({'cmd': "set_configClickMode", 'arg': "1"})
        self.msg_callback({'cmd': "set_configButtonControl", 'arg': "1"})

    def __max_open_slider_handler(self):
        # print("max_open_slider changed")
        self.msg_callback({'cmd': "set_configMaxOpen", 'arg': str(self.max_open_slider.value())})

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

