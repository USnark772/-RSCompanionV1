# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFrame, QHBoxLayout, QTabWidget, QSizePolicy, \
    QMenuBar, QMenu, QStatusBar, QDockWidget, QGroupBox, QPushButton, QLineEdit, QLabel, QGridLayout, QTextEdit, \
    QAction
from PySide2.QtCore import QSize, QRect, Qt, QMetaObject, QCoreApplication
from PySide2.QtGui import QFont, QKeyEvent
import device as device_container
import chart_container as main_chart
from help_window import HelpWindow
from device_tab import Tab
from saved_file_tab_contents import TabContents as SavedFileTabContents


class CompanionWindow(QMainWindow):
    # To keep track of which device is which for data display purposes
    __list_of_devices__ = {}

    # Auto generated code slightly altered for readability
    def __init__(self, msg_handler):
        super().__init__()
        # Begin MainWindow generation code
        self.setMinimumSize(QSize(450, 550))
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        # End MainWindow generation code
        ################################################################################################################
        # Begin Central_Widget generation code
        self.central_widget = QWidget(self)
        self.central_widget_vert_layout = QVBoxLayout(self.central_widget)
        self.central_widget_separator_line = QFrame(self.central_widget)
        self.central_widget_separator_line.setFrameShape(QFrame.HLine)
        self.central_widget_separator_line.setFrameShadow(QFrame.Sunken)
        self.central_widget_vert_layout.addWidget(self.central_widget_separator_line)
        self.setCentralWidget(self.central_widget)
        # End Central Widget generation code
        ################################################################################################################
        # Begin Experiment View Area generation code
        self.exp_data_view_horiz_layout = QHBoxLayout()
        self.main_chart_area = main_chart.GraphContainer()
        self.exp_data_view_horiz_layout.addWidget(self.main_chart_area)
        # End Experiment View Area generation code
        ################################################################################################################
        # Begin RS Device Tab generation code
        self.rs_devices_tab_widget = QTabWidget(self.central_widget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.rs_devices_tab_widget.sizePolicy().hasHeightForWidth())
        self.rs_devices_tab_widget.setSizePolicy(size_policy)
        self.rs_devices_tab_widget.setMinimumWidth(250)
        self.exp_data_view_horiz_layout.addWidget(self.rs_devices_tab_widget)
        self.central_widget_vert_layout.addLayout(self.exp_data_view_horiz_layout)
        # End RS Device Tab generation code
        ################################################################################################################
        # Begin Menu Bar generation code
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setGeometry(QRect(0, 0, 840, 22))
        self.file_menu = QMenu(self.menu_bar)
        # self.window_menu = QMenu(self.menu_bar)
        self.help_menu = QMenu(self.menu_bar)
        # self.settings_menu = QMenu(self.menu_bar)
        # self.udp_controls_menu = QMenu(self.settings_menu)
        self.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        # End MenuBar generation code
        ################################################################################################################
        # Begin Control Widget generation code
        self.control_widget_dock = QDockWidget(self)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.control_widget_dock.sizePolicy().hasHeightForWidth())
        self.control_widget_dock.setSizePolicy(size_policy)
        self.control_widget_dock.setMinimumSize(QSize(500, 150))
        self.control_widget_dock.setMaximumSize(QSize(16777215, 150))
        self.control_widget_dock.setFeatures(
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetVerticalTitleBar)
        self.control_widget_dock.setAllowedAreas(Qt.TopDockWidgetArea)
        self.control_widget_dock_contents = QWidget()
        self.control_widget_horiz_layout = QHBoxLayout(self.control_widget_dock_contents)
        self.control_widget_dock.setWidget(self.control_widget_dock_contents)
        self.addDockWidget(Qt.DockWidgetArea(4), self.control_widget_dock)
        # End Control Widget generation code
        ################################################################################################################
        # Begin Control Widget Run/New group box generation code
        self.exp_control_group_box = QGroupBox(self.control_widget_dock_contents)
        self.exp_control_group_box.setTitle("")
        self.exp_control_group_box_vert_layout = QVBoxLayout(self.exp_control_group_box)
        self.run_new_exp_push_button = QPushButton(self.exp_control_group_box)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.run_new_exp_push_button.sizePolicy().hasHeightForWidth())
        self.run_new_exp_push_button.setSizePolicy(size_policy)
        self.run_new_exp_push_button.setMinimumSize(QSize(0, 0))
        self.exp_control_group_box_vert_layout.addWidget(self.run_new_exp_push_button)
        self.end_exp_push_button = QPushButton(self.exp_control_group_box)
        self.exp_control_group_box_vert_layout.addWidget(self.end_exp_push_button)
        self.exp_name_input_box = QLineEdit(self.exp_control_group_box)
        self.exp_name_input_box.setPlaceholderText("Enter experiment name here")
        self.exp_control_group_box_vert_layout.addWidget(self.exp_name_input_box)
        self.control_widget_horiz_layout.addWidget(self.exp_control_group_box)
        self.block_control_group_box = QGroupBox(self.control_widget_dock_contents)
        self.block_control_group_box.setTitle("")
        self.block_control_group_box_vert_layout = QVBoxLayout(self.block_control_group_box)
        self.run_new_block_push_button = QPushButton(self.block_control_group_box)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.run_new_block_push_button.sizePolicy().hasHeightForWidth())
        self.run_new_block_push_button.setSizePolicy(size_policy)
        self.run_new_block_push_button.setMinimumSize(QSize(0, 0))
        self.block_control_group_box_vert_layout.addWidget(self.run_new_block_push_button)
        self.end_block_push_button = QPushButton(self.block_control_group_box)
        self.block_control_group_box_vert_layout.addWidget(self.end_block_push_button)
        self.block_name_input_box = QLineEdit(self.block_control_group_box)
        self.block_name_input_box.setPlaceholderText("Enter block name here")
        self.block_control_group_box_vert_layout.addWidget(self.block_name_input_box)
        self.control_widget_horiz_layout.addWidget(self.block_control_group_box)
        # End Control Widget Run/New group box generation code
        ################################################################################################################
        # Begin KeyFlag group box generation code
        self.key_flag_group_box = QGroupBox(self.control_widget_dock_contents)
        self.key_flag_vert_layout = QVBoxLayout(self.key_flag_group_box)
        self.key_flag_label = QLabel(self.key_flag_group_box)
        font = QFont()
        font.setPointSize(16)
        self.key_flag_label.setFont(font)
        self.key_flag_vert_layout.addWidget(self.key_flag_label, 0, Qt.AlignHCenter)
        self.control_widget_horiz_layout.addWidget(self.key_flag_group_box)
        # End KeyFlag group box generation code
        ################################################################################################################
        # Begin Block Note group box generation code
        self.block_note_group_box = QGroupBox(self.control_widget_dock_contents)
        self.block_note_group_box_grid_layout = QGridLayout(self.block_note_group_box)
        self.block_note_text_box = QTextEdit(self.block_note_group_box)
        self.block_note_text_box.setPlaceholderText("Enter block note text here")
        self.block_note_group_box_grid_layout.addWidget(self.block_note_text_box, 0, 1, 1, 1)
        self.save_block_note_push_button = QPushButton(self.block_note_group_box)
        self.block_note_group_box_grid_layout.addWidget(self.save_block_note_push_button, 1, 1, 1, 1)
        self.control_widget_horiz_layout.addWidget(self.block_note_group_box)
        # End Block Note group box generation code
        ################################################################################################################
        # Begin Trial/Block information generation code
        self.exp_block_frame = QFrame(self.control_widget_dock_contents)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.exp_block_frame.sizePolicy().hasHeightForWidth())
        self.exp_block_frame.setSizePolicy(size_policy)
        self.exp_block_frame.setMinimumSize(QSize(130, 0))
        self.exp_block_frame_grid_layout = QGridLayout(self.exp_block_frame)
        self.exp_block_frame_grid_layout.setContentsMargins(2, 2, 2, 2)
        self.exp_block_labels_frame = QFrame(self.exp_block_frame)
        self.exp_block_labels_frame.setFrameShape(QFrame.StyledPanel)
        self.exp_block_labels_frame.setFrameShadow(QFrame.Raised)
        self.exp_block_labels_frame.setFixedWidth(150)
        self.exp_block_labels_frame_vert_layout = QVBoxLayout(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.setContentsMargins(2, 2, 2, 2)
        self.exp_block_labels_frame_vert_layout.setSpacing(6)
        self.exp_label = QLabel(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.addWidget(self.exp_label)
        self.exp_num_label = QLabel(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.addWidget(self.exp_num_label)
        self.exp_time_label = QLabel(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.addWidget(self.exp_time_label)
        self.block_label = QLabel(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.addWidget(self.block_label)
        self.block_num_label = QLabel(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.addWidget(self.block_num_label)
        self.block_time_label = QLabel(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.addWidget(self.block_time_label)
        self.exp_block_frame_grid_layout.addWidget(self.exp_block_labels_frame, 0, 0, 1, 1)
        self.exp_block_values_frame = QFrame(self.exp_block_frame)
        self.exp_block_values_frame.setMinimumSize(QSize(60, 0))
        self.exp_block_values_frame.setFrameShape(QFrame.StyledPanel)
        self.exp_block_values_frame.setFrameShadow(QFrame.Raised)
        self.exp_block_values_frame_vert_layout = QVBoxLayout(self.exp_block_values_frame)
        self.exp_block_values_frame_vert_layout.setContentsMargins(2, 2, 2, 2)
        self.exp_block_spacer_1 = QLabel(self.exp_block_values_frame)
        font = QFont()
        font.setPointSize(10)
        self.exp_block_spacer_1.setFont(font)
        self.exp_block_spacer_1.setText("")
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_block_spacer_1)
        self.exp_num_val_label = QLabel(self.exp_block_values_frame)
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_num_val_label, 0, Qt.AlignRight)
        self.exp_time_val_label = QLabel(self.exp_block_values_frame)
        font = QFont()
        font.setPointSize(10)
        self.exp_time_val_label.setFont(font)
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_time_val_label, 0, Qt.AlignRight)
        self.exp_block_spacer_2 = QLabel(self.exp_block_values_frame)
        self.exp_block_spacer_2.setText("")
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_block_spacer_2)
        self.block_num_val_label = QLabel(self.exp_block_values_frame)
        self.exp_block_values_frame_vert_layout.addWidget(self.block_num_val_label, 0, Qt.AlignRight)
        self.block_time_val_label = QLabel(self.exp_block_values_frame)
        self.exp_block_values_frame_vert_layout.addWidget(self.block_time_val_label, 0, Qt.AlignRight)
        self.exp_block_frame_grid_layout.addWidget(self.exp_block_values_frame, 0, 1, 1, 1, Qt.AlignRight)
        self.control_widget_horiz_layout.addWidget(self.exp_block_frame)
        # End Trial/Block information generation code
        ################################################################################################################
        # Begin MenuBar item generation code
        #self.begin_exp_action = QAction(main_window)
        # self.save_action = QAction(self)
        # self.save_as_action = QAction(self)
        # self.com_messages_action = QAction(self)
        # self.com_messages_action.setCheckable(True)
        self.about_rs_companion_action = QAction(self)
        self.about_rs_action = QAction(self)
        self.check_for_updates_action = QAction(self)
        # self.end_exp_action = QAction(main_window)
        # self.trial_controls_action = QAction(self)
        # self.display_tool_tips_action = QAction(self)
        # self.configure_action = QAction(self)
        # self.com_port_action = QAction(self)
        # self.output_action = QAction(self)
        # self.input_action = QAction(self)
        # self.append_exp_action = QAction(self)
        self.open_file_action = QAction(self)
        #self.file_menu.addAction(self.begin_exp_action)
        #self.file_menu.addAction(self.end_exp_action)
        #self.file_menu.addSeparator()
        # self.file_menu.addAction(self.save_action)
        # self.file_menu.addAction(self.save_as_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addSeparator()
        # self.file_menu.addAction(self.append_exp_action)
        # self.window_menu.addAction(self.trial_controls_action)
        # self.window_menu.addAction(self.com_messages_action)
        # self.window_menu.addAction(self.configure_action)
        # self.window_menu.addSeparator()
        # self.window_menu.addAction(self.display_tool_tips_action)
        # self.window_menu.addSeparator()
        self.help_menu.addAction(self.about_rs_companion_action)
        self.help_menu.addAction(self.about_rs_action)
        self.help_menu.addAction(self.check_for_updates_action)

        # self.udp_controls_menu.addAction(self.output_action)
        # self.udp_controls_menu.addAction(self.input_action)
        # self.settings_menu.addAction(self.com_port_action)
        # self.settings_menu.addAction(self.udp_controls_menu.menuAction())
        self.menu_bar.addAction(self.file_menu.menuAction())
        # self.menu_bar.addAction(self.settings_menu.menuAction())
        # self.menu_bar.addAction(self.window_menu.menuAction())
        self.menu_bar.addAction(self.help_menu.menuAction())
        # End MenuBar item generation code
        ################################################################################################################
        # Begin final initialization
        self.saved_file_tab = None
        self.tab_contents = None
        self.num_tab_buttons = 0
        self.__set_texts(self)
        # self.__set_colors()
        self.__setup_handlers(msg_handler)
        self.__set_tool_tips()
        self.__initialize_button_states()
        QMetaObject.connectSlotsByName(self)

    # Auto generated code slightly altered for readability
    def __set_texts(self, main_window):
        _translate = QCoreApplication.translate
        ################################################################################################################
        # Main Window SetTitle code
        main_window.setWindowTitle(_translate("MainWindow", "RS Device Companion App"))
        ################################################################################################################
        # Begin MenuBar SetTitle code
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        # self.window_menu.setTitle(_translate("MainWindow", "Window"))
        self.help_menu.setTitle(_translate("MainWindow", "Help"))
        # self.settings_menu.setTitle(_translate("MainWindow", "Settings"))
        # self.udp_controls_menu.setTitle(_translate("MainWindow", "UDP Controls"))
        #self.begin_exp_action.setText(_translate("MainWindow", "Begin Experiment"))
        #self.begin_exp_action.setToolTip(_translate("MainWindow", "Begin Experiment"))
        # self.com_messages_action.setText(_translate("MainWindow", "COM Messages"))
        self.about_rs_companion_action.setText(_translate("MainWindow", "About RS Companion"))
        self.about_rs_action.setText(_translate("MainWindow", "About Red Scientific"))
        self.check_for_updates_action.setText(_translate("MainWindow", "Check For Updates"))
        # self.trial_controls_action.setText(_translate("MainWindow", "Trial Controls"))
        # self.display_tool_tips_action.setText(_translate("MainWindow", "Display Tooltips"))
        # self.configure_action.setText(_translate("MainWindow", "Configure"))
        # self.com_port_action.setText(_translate("MainWindow", "COM Port"))
        # self.output_action.setText(_translate("MainWindow", "Output"))
        # self.input_action.setText(_translate("MainWindow", "Input"))
        # self.append_exp_action.setText(_translate("MainWindow", "Append Experiment"))
        self.open_file_action.setText(_translate("MainWindow", "Open"))
        # self.save_action.setText(_translate("MainWindow", "Save"))
        # self.save_as_action.setText(_translate("MainWindow", "Save As"))
        # End MenuBar SetTitle code
        ################################################################################################################
        # Begin Control Widget SetTitle code
        self.control_widget_dock.setWindowTitle(_translate("MainWindow", "Control"))
        self.run_new_exp_push_button.setText(_translate("MainWindow", "Begin New Experiment"))
        self.end_exp_push_button.setText(_translate("MainWindow", "End Experiment"))
        self.run_new_block_push_button.setText(_translate("MainWindow", "Begin New Block"))
        self.end_block_push_button.setText(_translate("MainWindow", "End Block"))
        self.key_flag_group_box.setTitle(_translate("MainWindow", "Key Flag"))
        self.key_flag_label.setText(_translate("MainWindow", "N/A"))
        self.block_note_group_box.setTitle(_translate("MainWindow", "Block Note"))
        self.save_block_note_push_button.setText(_translate("MainWindow", "Save Block Note"))
        self.exp_label.setText(_translate("MainWindow", "Experiment"))
        self.exp_num_label.setText(_translate("MainWindow", "    Number:"))
        self.exp_time_label.setText(_translate("MainWindow", "    Time:"))
        self.block_label.setText(_translate("MainWindow", "Block"))
        self.block_num_label.setText(_translate("MainWindow", "    Number:"))
        self.block_time_label.setText(_translate("MainWindow", "    Time:"))
        self.exp_num_val_label.setText(_translate("MainWindow", "0"))
        self.exp_time_val_label.setText(_translate("MainWindow", "00:00:00"))
        self.block_num_val_label.setText(_translate("MainWindow", "0"))
        self.block_time_val_label.setText(_translate("MainWindow", "00:00:00"))
        # End Control Widget SetTitle code

    def __set_tool_tips(self):
        self.run_new_exp_push_button.setToolTip("Begin a new experiment")
        self.end_exp_push_button.setToolTip("End a currently running experiment")
        self.run_new_block_push_button.setToolTip("Begin a new block")
        self.end_block_push_button.setToolTip("End a currently running block")
        self.save_block_note_push_button.setToolTip("Save the block note to the save file")
        self.key_flag_group_box.setToolTip("The most recent key pressed for reference in save file")
        self.exp_label.setToolTip("Information about the current experiment")
        self.exp_num_label.setToolTip("The number of the current experiment")
        self.exp_time_label.setToolTip("The start time of the current experiment")
        self.block_label.setToolTip("Information about the current block within the current experiment")
        self.block_num_label.setToolTip("The number of the current block")
        self.block_time_label.setToolTip("The start time of the current block")

    def __setup_handlers(self, msg_handler):
        self.about_rs_action.triggered.connect(self.__about_rs_action_handler)
        self.about_rs_companion_action.triggered.connect(self.__about_rs_companion_action_handler)
        self.msg_callback = msg_handler

    def __initialize_button_states(self):
        self.end_exp_push_button.setEnabled(False)
        self.run_new_block_push_button.setEnabled(False)
        self.end_block_push_button.setEnabled(False)
        self.save_block_note_push_button.setEnabled(False)

    def __about_rs_companion_action_handler(self):
        print("About RS Companion Action triggered")
        self.help_window = HelpWindow("About Red Scientific Companion App", "CHANGEME The RS Companion App was "
                                                           "designed by "
                                                           "Joel Cooper and brought to life by Phillip Riskin. "
                                                           "It has many functionalities that you might not be "
                                                           "aware of so play around with it and see what's "
                                                           "going on! Have fun :)")
        self.help_window.show()

    def __about_rs_action_handler(self):
        print("About RS Action triggered")
        self.help_window = HelpWindow("About Red Scientific", "CHANGEME Red Scientific is an awesome company that will do "
                                                              "great things in the years to come and keep Phillip "
                                                              "really happy by paying him lots of money because "
                                                              "RS is rich from selling all those awesome devices "
                                                              "which are made even awesomer by the View that Phillip "
                                                              "was instrumental in making work. boom.")
        self.help_window.show()

    def __move_main_graph(self):
        self.main_chart_area.scroll_graph(self.chart_scroll_bar.value())

    def set_open_handler(self, handler):
        self.open_file_action.triggered.connect(handler)

    def set_new_exp_handler(self, handler):
        self.run_new_exp_push_button.clicked.connect(handler)

    def set_end_exp_handler(self, handler):
        self.end_exp_push_button.clicked.connect(handler)

    def set_new_block_handler(self, handler):
        self.run_new_block_push_button.clicked.connect(handler)

    def set_end_block_handler(self, handler):
        self.end_block_push_button.clicked.connect(handler)

    def set_save_note_handler(self, handler):
        self.save_block_note_push_button.clicked.connect(handler)

    def set_update_handler(self, handler):
        self.check_for_updates_action.triggered.connect(handler)

    def set_note_box_event_handler(self, handler):
        self.block_note_text_box.textChanged.connect(handler)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.key_flag_label.setText(chr(event.key()))
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        event.accept()

    def closeEvent(self, event):
        self.msg_callback({'action': "close"})
        for device in self.__list_of_devices__:
            self.__list_of_devices__[device].remove_self()

    def set_current_exp_time(self, time):
        self.exp_time_val_label.setText(time)

    def set_current_exp_number(self, num):
        self.exp_num_val_label.setText(str(num))

    def set_current_block_time(self, time):
        self.block_time_val_label.setText(time)

    def set_current_block_number(self, num):
        self.block_num_val_label.setText(str(num))

    def get_key_flag(self):
        return self.key_flag_label.text()

    def get_block_note(self):
        return self.block_note_text_box.toPlainText()

    def get_exp_name(self):
        return self.exp_name_input_box.text()

    def get_block_name(self):
        return self.block_name_input_box.text()

    def toggle_exp_buttons(self):
        if self.end_exp_push_button.isEnabled():
            self.end_exp_push_button.setEnabled(False)
        else:
            self.end_exp_push_button.setEnabled(True)
        if self.run_new_block_push_button.isEnabled():
            self.run_new_block_push_button.setEnabled(False)
        else:
            self.run_new_block_push_button.setEnabled(True)
        pass

    def toggle_blk_buttons(self):
        if self.end_block_push_button.isEnabled():
            self.end_block_push_button.setEnabled(False)
        else:
            self.end_block_push_button.setEnabled(True)

    def activate_save_button(self):
        self.save_block_note_push_button.setEnabled(True)

    def deactivate_save_button(self):
        self.save_block_note_push_button.setEnabled(False)

    def add_saved_file_tab(self):
        self.saved_file_tab = Tab(self.remove_saved_file_from_tab)
        self.rs_devices_tab_widget.setUpdatesEnabled(False)
        index = self.rs_devices_tab_widget.addTab(self.saved_file_tab, "")
        self.rs_devices_tab_widget.setUpdatesEnabled(True)
        self.rs_devices_tab_widget.setTabText(index, "Saved Files")
        self.tab_contents = SavedFileTabContents(self.saved_file_tab.scroll_area_contents,
                                                 self.remove_saved_file_from_tab)

    def remove_saved_file_tab(self):
        self.rs_devices_tab_widget.removeTab(self.rs_devices_tab_widget.indexOf(self.saved_file_tab))
        self.saved_file_tab.deleteLater()
        self.saved_file_tab = None

    def add_saved_file_to_tab(self, filename, controller_callback):
        if not self.saved_file_tab:
            self.add_saved_file_tab()
        self.num_tab_buttons += 1
        self.tab_contents.add_close_button(filename, controller_callback)

    def remove_saved_file_from_tab(self, filename):
        self.main_chart_area.remove_device(filename)
        self.num_tab_buttons -= 1
        if self.num_tab_buttons == 0:
            self.remove_saved_file_tab()

    # Passes message received to proper device display object
    def handle_msg(self, msg_dict):
        if msg_dict['type'] == "add":
            del msg_dict['type']
            self.add_rs_device_handler(msg_dict['device'])
        elif msg_dict['type'] == "remove":
            del msg_dict['type']
            self.remove_rs_device_handler(msg_dict['device'])
        elif msg_dict['type'] == "settings":
            del msg_dict['type']
            for device in self.__list_of_devices__:
                if device == msg_dict['device']:
                    del msg_dict['device']
                    self.__list_of_devices__[device].handle_msg(msg_dict)
                    pass
        elif msg_dict['type'] == "data":
            del msg_dict['type']
            self.main_chart_area.handle_msg(msg_dict)

    # Creates an RSDevice and adds it to the list of devices
    def add_rs_device_handler(self, device):
        if device not in self.__list_of_devices__:
            self.__list_of_devices__[device] = device_container.RSDevice(device, self.msg_callback,
                                                                         self.rs_devices_tab_widget)
            self.main_chart_area.add_device(device)

    # Deletes an RSDevice and removes it from the list of devices
    def remove_rs_device_handler(self, device):
        if device in self.__list_of_devices__:
            self.__list_of_devices__[device].remove_self()
            del self.__list_of_devices__[device]
            self.main_chart_area.remove_device(device)
