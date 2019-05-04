# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import *
from PySide2.QtCore import QRect, QCoreApplication, QSize, Qt
from PySide2.QtCharts import QtCharts
import Model.defs as defs


class Tab(QWidget):
    def __init__(self, device_id, msg_callback, settings_widget_button):
        super().__init__()
        self.device_id = device_id
        self.msg_callback = msg_callback
        self.configure_widget_button = settings_widget_button
        self.device_name = self.device_id[0] + " on " + self.device_id[1]
        self.zero_line = QtCharts.QLineSeries
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
        self.push_button_2 = QPushButton(self.group_box_1)
        self.push_button_2.setObjectName("push_button_2")
        self.vert_layout.addWidget(self.push_button_2)

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
        self.push_button_2.setText(_translate("MainWindow", "CHANGEME PushButton"))

        self.tool_button.setText(_translate("MainWindow", "Configure device"))


    def __setup_button_handlers(self):
        self.tool_button.clicked.connect(self.__setup_push_button_handler)
        self.push_button_2.clicked.connect(self.__button_2_handler)
        '''
        self.push_button_1.clicked.connect()
        '''

    def __button_2_handler(self):
        print("Button 2 clicked")

    def __setup_push_button_handler(self):
        self.configure_widget_button()


class ConfigureWidget(QWidget):
    def __init__(self, device_name, msg_callback):
        super().__init__()
        self.device_name = device_name
        self.msg_callback = msg_callback
        self.setObjectName(self.device_name)
        self.resize(400, 300)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(400, 300))
        self.config_chart = ConfigChart()
        self.config_chart_view = QtCharts.QChartView(self)
        self.config_chart_view.setGeometry(QRect(120, 20, 256, 192))
        self.config_chart_view.setObjectName("settings_graphics_view")
        self.config_chart_view.setChart(self.config_chart)
        self.lower_isi_label = QLabel(self)
        self.lower_isi_label.setGeometry(QRect(350, 240, 35, 10))
        self.lower_isi_label.setObjectName("lower_isi_label")
        self.stim_dur_label = QLabel(self)
        self.stim_dur_label.setGeometry(QRect(10, 20, 51, 16))
        self.stim_dur_label.setObjectName("stim_dur_label")
        self.upper_isi_label = QLabel(self)
        self.upper_isi_label.setGeometry(QRect(350, 220, 35, 10))
        self.upper_isi_label.setObjectName("upper_isi_label")
        self.iso_default_push_button = QPushButton(self)
        self.iso_default_push_button.setGeometry(QRect(330, 270, 61, 20))
        self.iso_default_push_button.setObjectName("iso_default_push_button")
        self.upload_settings_push_button = QPushButton(self)
        self.upload_settings_push_button.setGeometry(QRect(30, 230, 71, 41))
        self.upload_settings_push_button.setObjectName("upload_settings_push_button")

        # Sliders
        self.intensity_slider = QSlider(self)
        self.intensity_slider.setGeometry(QRect(85, 40, 16, 160))
        self.intensity_slider.setOrientation(Qt.Vertical)
        #self.intensity_slider.setPageStep(1)
        self.intensity_slider.setObjectName("intensity_slider")
        self.upper_isi_slider = QSlider(self)
        self.upper_isi_slider.setGeometry(QRect(180, 220, 160, 16))
        self.upper_isi_slider.setOrientation(Qt.Horizontal)
        #self.upper_isi_slider.setPageStep(1)
        self.upper_isi_slider.setObjectName("upper_isi_slider")
        self.lower_isi_slider = QSlider(self)
        self.lower_isi_slider.setGeometry(QRect(180, 240, 160, 16))
        self.lower_isi_slider.setOrientation(Qt.Horizontal)
        #self.lower_isi_slider.setPageStep(1)
        self.lower_isi_slider.setObjectName("lower_isi_slider")
        self.stim_dur_slider = QSlider(self)
        self.stim_dur_slider.setGeometry(QRect(25, 40, 16, 160))
        self.stim_dur_slider.setOrientation(Qt.Vertical)
        #self.stim_dur_slider.setPageStep(1)
        self.stim_dur_slider.setObjectName("stim_dur_slider")


        self.stim_intensity_label = QLabel(self)
        self.stim_intensity_label.setGeometry(QRect(65, 20, 51, 16))
        self.stim_intensity_label.setObjectName("stim_intensity_label")
        self.close_me_bool = False
        self.__set_texts()
        self.__set_handlers()
        self.values = {'intensity': self.intensity_slider,
                       'upperISI': self.upper_isi_slider,
                       'lowerISI': self.lower_isi_slider,
                       'stimDur': self.stim_dur_slider}
        self.__set_slider_ranges()
        self.__get_vals()

    def __set_slider_ranges(self):
        self.intensity_slider.setMinimum(defs.drt_intensity_min)
        self.intensity_slider.setMaximum(defs.drt_intensity_max)
        self.upper_isi_slider.setMinimum(defs.drt_ISI_min)
        self.upper_isi_slider.setMaximum(defs.drt_ISI_max)
        self.lower_isi_slider.setMinimum(defs.drt_ISI_min)
        self.lower_isi_slider.setMaximum(defs.drt_ISI_max)
        self.stim_dur_slider.setMaximum(defs.drt_stim_dur_max)
        self.stim_dur_slider.setMinimum(defs.drt_stim_dur_min)

    def __set_texts(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("self", "DRT Config"))
        self.lower_isi_label.setText(_translate("self", "Lower ISI"))
        self.stim_dur_label.setText(_translate("self", "Stim Duration"))
        self.upper_isi_label.setText(_translate("self", "Upper ISI"))
        self.iso_default_push_button.setText(_translate("self", "ISO default"))
        self.upload_settings_push_button.setText(_translate("self", "Upload settings"))
        self.stim_intensity_label.setText(_translate("self", "Stim Intensity"))

    def __set_handlers(self):
        self.upload_settings_push_button.clicked.connect(self.__update_button_handler)
        self.iso_default_push_button.clicked.connect(self.__iso_button_handler)
        self.lower_isi_slider.valueChanged.connect(self.__lower_isi_slider_handler)
        self.upper_isi_slider.valueChanged.connect(self.__upper_isi_slider_handler)
        self.stim_dur_slider.valueChanged.connect(self.__stim_dur_slider_handler)
        self.intensity_slider.valueChanged.connect(self.__intensity_slider_handler)

    def __get_vals(self):
        msg_dict = {'cmd': "get_config"}
        self.msg_callback(msg_dict)

    def __set_val(self, var, val):
        print("drt_device_view.ConfigureWidget.__set_val")
        self.values[var].setValue(int(val))

    def __stim_dur_slider_handler(self):
        pass

    def __intensity_slider_handler(self):
        pass

    def __lower_isi_slider_handler(self):
        self.__push_upper_isi_slider()

    def __upper_isi_slider_handler(self):
        self.__push_lower_isi_slider()

    def __push_upper_isi_slider(self):
        if self.lower_isi_slider.value() >= self.upper_isi_slider.value():
            self.upper_isi_slider.setValue(self.lower_isi_slider.value())

    def __push_lower_isi_slider(self):
        if self.upper_isi_slider.value() <= self.lower_isi_slider.value():
            self.lower_isi_slider.setValue(self.upper_isi_slider.value())

    def __update_button_handler(self):
        self.__set_intensity_handler()
        self.__set_lower_isi_handler()
        self.__set_upper_isi_handler()
        self.__set_stim_duration_handler()

    def __iso_button_handler(self):
        print("ISO default button pressed")

    def __set_intensity_handler(self):
        print("drt_device_view.ConfigureWidget.__set_intensity_handler")
        value = self.intensity_slider.value()
        msg_dict = {'cmd': "set_intensity",
                    'arg': str(value)}
        self.msg_callback(msg_dict)

    def __set_upper_isi_handler(self):
        print("drt_device_view.ConfigureWidget.__set_upper_isi_handler")
        value = self.upper_isi_slider.value()
        msg_dict = {'cmd': "set_upperISI",
                    'arg': str(value)}
        self.msg_callback(msg_dict)

    def __set_lower_isi_handler(self):
        print("drt_device_view.ConfigureWidget.__set_lower_isi_handler")
        value = self.lower_isi_slider.value()
        msg_dict = {'cmd': "set_lowerISI",
                    'arg': str(value)}
        self.msg_callback(msg_dict)

    def __set_stim_duration_handler(self):
        print("drt_device_view.ConfigureWidget.__set_stim_dur_handler")
        value = self.stim_dur_slider.value()
        msg_dict = {'cmd': "set_stimDur",
                    'arg': str(value)}
        self.msg_callback(msg_dict)

    def handle_msg(self, msg_dict):
        print("drt_device_view.ConfigureWidget.handle_msg")
        for item in msg_dict:
            print(item, msg_dict[item])
            self.__set_val(item, msg_dict[item])

# TODO: Create graphic for drt config window
class ConfigChart(QtCharts.QChart):
    def __init__(self):
        super().__init__()
        self.setTitle("Config")
