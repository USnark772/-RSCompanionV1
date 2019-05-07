
class OldDRTConfigureWidget(QWidget):
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
        self.lower_isi_label.setGeometry(QRect(350, 260, 35, 10))
        self.lower_isi_label.setObjectName("lower_isi_label")

        self.lower_isi_line_edit = QLineEdit(self)
        self.lower_isi_line_edit.setGeometry(QRect(130, 260, 30, 15))
        self.lower_isi_line_edit.setObjectName("lower_isi_line_edit")

        self.upper_isi_line_edit = QLineEdit(self)
        self.upper_isi_line_edit.setGeometry(QRect(130, 240, 30, 15))
        self.upper_isi_line_edit.setObjectName("upper_isi_line_edit")

        self.stim_dur_line_edit = QLineEdit(self)
        self.stim_dur_line_edit.setGeometry(QRect(18, 210, 30, 15))
        self.stim_dur_line_edit.setObjectName("stim_dur_line_edit")

        self.intensity_line_edit = QLineEdit(self)
        self.intensity_line_edit.setGeometry(QRect(78, 210, 30, 15))
        self.intensity_line_edit.setObjectName("intensity_line_edit")

        self.stim_dur_label = QLabel(self)
        self.stim_dur_label.setGeometry(QRect(10, 20, 51, 16))
        self.stim_dur_label.setObjectName("stim_dur_label")

        self.upper_isi_label = QLabel(self)
        self.upper_isi_label.setGeometry(QRect(350, 240, 35, 10))
        self.upper_isi_label.setObjectName("upper_isi_label")

        self.iso_default_push_button = QPushButton(self)
        self.iso_default_push_button.setGeometry(QRect(35, 270, 61, 20))
        self.iso_default_push_button.setObjectName("iso_default_push_button")
        # self.upload_settings_push_button = QPushButton(self)
        # self.upload_settings_push_button.setGeometry(QRect(30, 230, 71, 41))
        # self.upload_settings_push_button.setObjectName("upload_settings_push_button")

        # Sliders
        self.intensity_slider = QSlider(self)
        self.intensity_slider.setGeometry(QRect(85, 40, 16, 160))
        self.intensity_slider.setOrientation(Qt.Vertical)
        self.intensity_slider.setObjectName("intensity_slider")

        self.upper_isi_slider = QSlider(self)
        self.upper_isi_slider.setGeometry(QRect(180, 240, 160, 16))
        self.upper_isi_slider.setOrientation(Qt.Horizontal)
        self.upper_isi_slider.setObjectName("upper_isi_slider")

        self.lower_isi_slider = QSlider(self)
        self.lower_isi_slider.setGeometry(QRect(180, 260, 160, 16))
        self.lower_isi_slider.setOrientation(Qt.Horizontal)
        self.lower_isi_slider.setObjectName("lower_isi_slider")

        self.stim_dur_slider = QSlider(self)
        self.stim_dur_slider.setGeometry(QRect(25, 40, 16, 160))
        self.stim_dur_slider.setOrientation(Qt.Vertical)
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
        self.__set_slider_settings()
        self.__set_line_edit_settings()
        self.__get_vals()

    def __set_texts(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("self", "DRT Config"))
        self.lower_isi_label.setText(_translate("self", "Lower ISI"))
        self.stim_dur_label.setText(_translate("self", "Stim Duration"))
        self.upper_isi_label.setText(_translate("self", "Upper ISI"))
        self.iso_default_push_button.setText(_translate("self", "ISO default"))
        # self.upload_settings_push_button.setText(_translate("self", "Upload settings"))
        self.stim_intensity_label.setText(_translate("self", "Stim Intensity"))

    def __set_slider_settings(self):
        self.intensity_slider.setRange(defs.drt_intensity_min, defs.drt_intensity_max)
        self.upper_isi_slider.setRange(defs.drt_ISI_min, defs.drt_ISI_max)
        self.lower_isi_slider.setRange(defs.drt_ISI_min, defs.drt_ISI_max)
        self.stim_dur_slider.setRange(defs.drt_stim_dur_min, defs.drt_stim_dur_max)

    def __set_line_edit_settings(self):
        self.stim_dur_line_edit.setReadOnly(True)
        self.lower_isi_line_edit.setReadOnly(True)
        self.upper_isi_line_edit.setReadOnly(True)
        self.intensity_line_edit.setReadOnly(True)

    def __set_handlers(self):
        # self.upload_settings_push_button.clicked.connect(self.__update_button_handler)
        self.iso_default_push_button.clicked.connect(self.__iso_button_handler)
        self.lower_isi_slider.valueChanged.connect(self.__push_upper_isi_slider)
        self.upper_isi_slider.valueChanged.connect(self.__push_lower_isi_slider)
        self.stim_dur_slider.valueChanged.connect(self.__stim_dur_changed_handler)
        self.intensity_slider.valueChanged.connect(self.__intensity_changed_handler)
        self.lower_isi_slider.sliderReleased.connect(self.__isi_released_handler)
        self.upper_isi_slider.sliderReleased.connect(self.__isi_released_handler)
        self.stim_dur_slider.sliderReleased.connect(self.__set_stim_duration_handler)
        self.intensity_slider.sliderReleased.connect(self.__set_intensity_handler)
        self.stim_dur_line_edit.textEdited.connect(self.__stim_dur_line_edit_changed)

    def __get_vals(self):
        self.msg_callback({'cmd': "get_config"})

    def __set_val(self, var, val):
        self.values[var].setValue(int(val))

    def __lower_isi_tooltip_handler(self):
        self.lower_isi_slider.setToolTip(str(self.lower_isi_slider.value()))

    def __isi_released_handler(self):
        self.__set_upper_isi_handler()
        self.__set_lower_isi_handler()

    def __push_upper_isi_slider(self):
        if self.lower_isi_slider.value() >= self.upper_isi_slider.value():
            self.upper_isi_slider.setValue(self.lower_isi_slider.value())
        self.lower_isi_line_edit.setText(str(self.lower_isi_slider.value()))

    def __push_lower_isi_slider(self):
        self.__lower_isi_tooltip_handler()
        if self.upper_isi_slider.value() <= self.lower_isi_slider.value():
            self.lower_isi_slider.setValue(self.upper_isi_slider.value())
        self.upper_isi_line_edit.setText(str(self.upper_isi_slider.value()))

    def __intensity_changed_handler(self):
        self.intensity_line_edit.setText(str(self.intensity_slider.value()))

    def __stim_dur_changed_handler(self):
        self.stim_dur_line_edit.setText(str(self.stim_dur_slider.value()))

    # TODO: Fix this or toss it
    def __stim_dur_line_edit_changed(self, text):
        try:
            value = int(text)
            self.stim_dur_slider.setValue(value)
            self.__set_stim_duration_handler()
        except:
            self.message = HelpWindow("Error", "Must be a valid integer")

    def __iso_button_handler(self):
        self.__set_val('upperISI', 5000)
        self.__set_val('lowerISI', 3000)
        self.__set_val('stimDur', 1000)
        self.__set_val('intensity', 255)
        self.__set_intensity_handler()
        self.__set_upper_isi_handler()
        self.__set_lower_isi_handler()
        self.__set_stim_duration_handler()

    def __set_intensity_handler(self):
        self.msg_callback({'cmd': "set_intensity", 'arg': str(self.intensity_slider.value())})

    def __set_upper_isi_handler(self):
        self.msg_callback({'cmd': "set_upperISI", 'arg': str(self.upper_isi_slider.value())})

    def __set_lower_isi_handler(self):
        self.msg_callback({'cmd': "set_lowerISI", 'arg': str(self.lower_isi_slider.value())})

    def __set_stim_duration_handler(self):
        self.msg_callback({'cmd': "set_stimDur", 'arg': str(self.stim_dur_slider.value())})

    def handle_msg(self, msg_dict):
        for item in msg_dict:
            self.__set_val(item, msg_dict[item])

class OldVOGConfigureWidget(QWidget):
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

    '''
    def __update_button_handler(self):
        print("__update_button_handler")
    '''

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

