# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QHBoxLayout, QVBoxLayout,\
    QCheckBox, QFrame, QLineEdit
from PySide2.QtCore import Qt, QRect
from Devices.VOG.Model.vog_defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min
from Model.general_defs import tab_line_edit_error_style, tab_line_edit_compliant_style


class VOGTab(QWidget):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setLayout(QVBoxLayout(self))
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(450)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__config_frame = self.__MyFrame(self)
        self.__config_horiz_layout = QHBoxLayout(self.__config_frame)
        self.__config_label = QLabel(self.__config_frame)
        self.__config_label.setAlignment(Qt.AlignCenter)
        self.__config_horiz_layout.addWidget(self.__config_label)
        self.__config_val = QLabel(self.__config_frame)
        self.__config_val.setAlignment(Qt.AlignCenter)
        self.__config_horiz_layout.addWidget(self.__config_val)
        self.layout().addWidget(self.__config_frame)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__presets_frame = self.__MyFrame(self)
        self.__presets_vert_layout = QVBoxLayout(self.__presets_frame)
        self.__nhtsa_button = QPushButton(self.__presets_frame)
        self.__presets_vert_layout.addWidget(self.__nhtsa_button)
        self.__eblindfold_button = QPushButton(self.__presets_frame)
        self.__presets_vert_layout.addWidget(self.__eblindfold_button)
        self.__direct_control_button = QPushButton(self.__presets_frame)
        self.__presets_vert_layout.addWidget(self.__direct_control_button)
        self.layout().addWidget(self.__presets_frame)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__input_box_frame = self.__MyFrame(self)
        self.__input_box_grid_layout = QGridLayout(self.__input_box_frame)
        self.__input_box_grid_layout.setContentsMargins(0, 6, 0, 6)
        self.__open_dur_label = QLabel(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__open_dur_label, 0, 0, 1, 1)
        self.__open_dur_line_edit = QLineEdit(self.__input_box_frame)
        self.__open_dur_line_edit.setFixedWidth(80)
        self.__input_box_grid_layout.addWidget(self.__open_dur_line_edit, 0, 1, 1, 1)
        self.__open_inf_check_box = QCheckBox(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__open_inf_check_box, 0, 2, 1, 1)
        self.__close_dur_label = QLabel(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__close_dur_label, 1, 0, 1, 1)
        self.__close_dur_line_edit = QLineEdit(self.__input_box_frame)
        self.__close_dur_line_edit.setFixedWidth(80)
        self.__input_box_grid_layout.addWidget(self.__close_dur_line_edit, 1, 1, 1, 1)
        self.__close_inf_check_box = QCheckBox(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__close_inf_check_box, 1, 2, 1, 1)
        self.__debounce_label = QLabel(self.__input_box_frame)
        self.__input_box_grid_layout.addWidget(self.__debounce_label, 2, 0, 1, 1)
        self.__debounce_time_line_edit = QLineEdit(self.__input_box_frame)
        self.__debounce_time_line_edit.setFixedWidth(80)
        self.__input_box_grid_layout.addWidget(self.__debounce_time_line_edit, 2, 1, 1, 1)
        self.layout().addWidget(self.__input_box_frame)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__button_mode_frame = self.__MyFrame()
        self.__button_mode_horiz_layout = QHBoxLayout(self.__button_mode_frame)
        self.__button_mode_label = QLabel(self.__button_mode_frame)
        self.__button_mode_horiz_layout.addWidget(self.__button_mode_label)
        self.__button_mode_selector = QComboBox(self.__button_mode_frame)
        self.__button_mode_selector.addItem("")
        self.__button_mode_selector.addItem("")
        self.__button_mode_horiz_layout.addWidget(self.__button_mode_selector)
        self.layout().addWidget(self.__button_mode_frame)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__upload_settings_button = QPushButton()
        self.layout().addWidget(self.__upload_settings_button)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__manual_control_button = QPushButton()
        self.layout().addWidget(self.__manual_control_button)

        self.layout().addWidget(self.__MyFrame(self, line=True))

        self.__name = name
        self.__index = 0
        self.__set_texts()
        self.__set_tooltips()

    def add_manual_control_handler(self, func):
        self.__manual_control_button.clicked.connect(func)

    def add_nhtsa_button_handler(self, func):
        self.__nhtsa_button.clicked.connect(func)

    def add_eblind_button_handler(self, func):
        self.__eblindfold_button.clicked.connect(func)

    def add_direct_control_button_handler(self, func):
        self.__direct_control_button.clicked.connect(func)

    def add_upload_button_handler(self, func):
        self.__upload_settings_button.clicked.connect(func)

    def add_open_inf_handler(self, func):
        self.__open_inf_check_box.toggled.connect(func)

    def add_close_inf_handler(self, func):
        self.__close_inf_check_box.toggled.connect(func)

    def add_open_entry_changed_handler(self, func):
        self.__open_dur_line_edit.textChanged.connect(func)

    def add_close_entry_changed_handler(self, func):
        self.__close_dur_line_edit.textChanged.connect(func)

    def add_debounce_entry_changed_handler(self, func):
        self.__debounce_time_line_edit.textChanged.connect(func)

    def add_button_mode_entry_changed_handler(self, func):
        self.__button_mode_selector.currentIndexChanged.connect(func)

    def set_upload_button_activity(self, is_active):
        self.__upload_settings_button.setEnabled(is_active)

    def set_config_value(self, value):
        self.__config_val.setText(value)

    def get_open_val(self):
        return self.__open_dur_line_edit.text()

    def set_open_val(self, val):
        self.__open_dur_line_edit.setText(str(val))

    def set_open_val_error(self, is_error):
        if is_error:
            self.__open_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.__open_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)

    def set_close_val_error(self, is_error):
        if is_error:
            self.__close_dur_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.__close_dur_line_edit.setStyleSheet(tab_line_edit_compliant_style)

    def set_debounce_val_error(self, is_error):
        if is_error:
            self.__debounce_time_line_edit.setStyleSheet(tab_line_edit_error_style)
        else:
            self.__debounce_time_line_edit.setStyleSheet(tab_line_edit_compliant_style)

    def set_open_val_entry_activity(self, is_active):
        self.__open_dur_line_edit.setEnabled(is_active)

    def get_open_inf(self):
        return self.__open_inf_check_box.isChecked()

    def set_open_inf(self, is_checked):
        self.__open_inf_check_box.setChecked(is_checked)

    def get_close_val(self):
        return self.__close_dur_line_edit.text()

    def set_close_val(self, val):
        self.__close_dur_line_edit.setText(str(val))

    def set_close_val_entry_activity(self, is_active):
        self.__close_dur_line_edit.setEnabled(is_active)

    def get_close_inf(self):
        return self.__close_inf_check_box.isChecked()

    def set_close_inf(self, is_checked):
        self.__close_inf_check_box.setChecked(is_checked)

    def get_debounce_val(self):
        return self.__debounce_time_line_edit.text()

    def set_debounce_val(self, val):
        self.__debounce_time_line_edit.setText(str(val))

    def get_button_mode(self):
        return self.__button_mode_selector.currentIndex()

    def set_button_mode(self, val):
        self.__button_mode_selector.setCurrentIndex(int(val))

    def get_name(self):
        return self.__name

    def get_index(self):
        return self.__index

    def set_index(self, new_index):
        self.__index = new_index

    def __set_texts(self):
        self.__config_label.setText("Current configuration:")
        self.__config_val.setText("DIRECT CONTROL")
        self.__nhtsa_button.setText("NHTSA")
        self.__eblindfold_button.setText("eBlindfold")
        self.__direct_control_button.setText("Direct Control")
        self.__open_dur_label.setText("Open Duration")
        self.__open_inf_check_box.setText("INF")
        self.__close_dur_label.setText("Close Duration")
        self.__close_inf_check_box.setText("INF")
        self.__debounce_label.setText("Debounce Time")
        self.__button_mode_label.setText("Button Mode")
        self.__button_mode_selector.setItemText(0, "Hold")
        self.__button_mode_selector.setItemText(1, "Click")
        self.__upload_settings_button.setText("Upload settings")
        self.__manual_control_button.setText("Toggle Lens")

    def __set_tooltips(self):
        self.__config_label.setToolTip("Current device configuration")
        self.__nhtsa_button.setToolTip("Set Device to NHTSA standard")
        self.__eblindfold_button.setToolTip("Set Device to eBlindfold mode")
        self.__direct_control_button.setToolTip("Set Device to Direct Control mode")
        self.__button_mode_label.setToolTip("CHANGEME")
        self.__open_dur_label.setToolTip("Range: "
                                         + str(vog_min_open_close)
                                         + "-" + str(vog_max_open_close))
        self.__close_dur_label.setToolTip("Range: "
                                          + str(vog_min_open_close)
                                          + "-" + str(vog_max_open_close))
        self.__debounce_label.setToolTip("Range: "
                                         + str(vog_debounce_min)
                                         + "-" + str(vog_debounce_max))
        self.__open_inf_check_box.setToolTip("Set to manual switching")
        self.__close_inf_check_box.setToolTip("Set to manual switching")
        self.__upload_settings_button.setToolTip("Upload current configuration to device")
        self.__manual_control_button.setToolTip("Manually open or close the lens")

    class __MyFrame(QFrame):
        def __init__(self, parent=None, line=False, vert=False):
            super().__init__(parent)
            if line:
                if vert:
                    self.setFrameShape(QFrame.VLine)
                else:
                    self.setFrameShape(QFrame.HLine)
                self.setFrameShadow(QFrame.Sunken)
            else:
                self.setFrameShape(QFrame.StyledPanel)
                self.setFrameShadow(QFrame.Raised)
