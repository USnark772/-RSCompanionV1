# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import *
from PySide2.QtCore import QSize, QRect, Qt, QMetaObject, QCoreApplication
from PySide2.QtGui import QFont, QPainter, QPalette
from PySide2.QtCharts import QtCharts

import View.device as device_container
import View.main_chart as main_chart
from View.help_window import HelpWindow


# TODO: handle closing all windows when main window is closed
class CompanionWindow(object):
    # To keep track of which device is which for data display purposes
    __list_of_devices__ = {}

    # Auto generated code slightly altered for readability
    def __init__(self, main_window, msg_handler):
        # Begin MainWindow generation code
        main_window.setObjectName("main_window")
        main_window.resize(840, 705)
        main_window.setMinimumSize(QSize(840, 468))
        font = QFont()
        font.setPointSize(10)
        main_window.setFont(font)
        # End MainWindow generation code
        ################################################################################################################
        # Begin Central_Widget generation code
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.central_widget_vert_layout = QVBoxLayout(self.central_widget)
        self.central_widget_vert_layout.setObjectName("central_widget_vert_layout")
        self.central_widget_separator_line = QFrame(self.central_widget)
        self.central_widget_separator_line.setFrameShape(QFrame.HLine)
        self.central_widget_separator_line.setFrameShadow(QFrame.Sunken)
        self.central_widget_separator_line.setObjectName("central_widget_separator_line")
        self.central_widget_vert_layout.addWidget(self.central_widget_separator_line)
        main_window.setCentralWidget(self.central_widget)
        # End Central Widget generation code
        ################################################################################################################
        # Begin Experiment View Area generation code
        self.exp_data_view_horiz_layout = QHBoxLayout()
        self.exp_data_view_horiz_layout.setObjectName("exp_data_view_horiz_layout")
        self.exp_data_view_vert_layout = QVBoxLayout()
        self.exp_data_view_vert_layout.setObjectName("exp_data_view_vert_layout")
        self.main_chart = main_chart.MainChartWidget()
        self.main_chart_view = QtCharts.QChartView(self.central_widget)
        self.main_chart_view.setChart(self.main_chart)
        self.main_chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_scroll_bar = QScrollBar()
        self.chart_scroll_bar.setOrientation(Qt.Horizontal)
        self.chart_scroll_bar.setMaximum(100)
        self.chart_scroll_bar.setMinimum(0)
        self.chart_scroll_bar.setValue(100)
        self.exp_data_view_vert_layout.addWidget(self.main_chart_view)
        self.exp_data_view_vert_layout.addWidget(self.chart_scroll_bar)
        # End Experiment View Area generation code
        ################################################################################################################
        # Begin RS Device Tab generation code
        self.rs_devices_tab_widget = QTabWidget(self.central_widget)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.rs_devices_tab_widget.sizePolicy().hasHeightForWidth())
        self.rs_devices_tab_widget.setSizePolicy(size_policy)
        self.rs_devices_tab_widget.setMinimumWidth(200)
        self.rs_devices_tab_widget.setObjectName("rs_devices_tab_widget")
        self.exp_data_view_horiz_layout.addLayout(self.exp_data_view_vert_layout)
        self.exp_data_view_horiz_layout.addWidget(self.rs_devices_tab_widget)
        self.central_widget_vert_layout.addLayout(self.exp_data_view_horiz_layout)
        # End RS Device Tab generation code
        ################################################################################################################
        # Begin Menu Bar generation code
        self.menu_bar = QMenuBar(main_window)
        self.menu_bar.setGeometry(QRect(0, 0, 840, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.file_menu = QMenu(self.menu_bar)
        self.file_menu.setObjectName("file_menu")
        self.window_menu = QMenu(self.menu_bar)
        self.window_menu.setObjectName("window_menu")
        self.help_menu = QMenu(self.menu_bar)
        self.help_menu.setObjectName("help_menu")
        self.settings_menu = QMenu(self.menu_bar)
        self.settings_menu.setObjectName("settings_menu")
        self.udp_controls_menu = QMenu(self.settings_menu)
        self.udp_controls_menu.setObjectName("udp_controls_menu")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)
        # End MenuBar generation code
        ################################################################################################################
        # Begin Control Widget generation code
        self.control_widget_dock = QDockWidget(main_window)
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
        self.control_widget_dock.setObjectName("control_widget_dock")
        self.control_widget_dock_contents = QWidget()
        self.control_widget_dock_contents.setObjectName("control_widget_dock_contents")
        self.control_widget_horiz_layout = QHBoxLayout(self.control_widget_dock_contents)
        self.control_widget_horiz_layout.setObjectName("control_widget_horiz_layout")
        self.control_widget_dock.setWidget(self.control_widget_dock_contents)
        main_window.addDockWidget(Qt.DockWidgetArea(4), self.control_widget_dock)
        # End Control Widget generation code
        ################################################################################################################
        # Begin Control Widget Run/New group box generation code
        self.exp_control_group_box = QGroupBox(self.control_widget_dock_contents)
        self.exp_control_group_box.setTitle("")
        self.exp_control_group_box.setObjectName("exp_control_group_box")
        self.exp_control_group_box_vert_layout = QVBoxLayout(self.exp_control_group_box)
        self.exp_control_group_box_vert_layout.setObjectName("exp_control_group_box_vert_layout")
        self.run_new_exp_push_button = QPushButton(self.exp_control_group_box)
        self.run_new_exp_push_button.setObjectName("run_new_exp_push_button")
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.run_new_exp_push_button.sizePolicy().hasHeightForWidth())
        self.run_new_exp_push_button.setSizePolicy(size_policy)
        self.run_new_exp_push_button.setMinimumSize(QSize(0, 0))
        self.exp_control_group_box_vert_layout.addWidget(self.run_new_exp_push_button)
        self.end_exp_push_button = QPushButton(self.exp_control_group_box)
        self.end_exp_push_button.setObjectName("end_block_push_button")
        self.exp_control_group_box_vert_layout.addWidget(self.end_exp_push_button)
        self.exp_name_label = QLineEdit(self.exp_control_group_box)
        self.exp_name_label.setPlaceholderText("Enter experiment name here")
        self.exp_control_group_box_vert_layout.addWidget(self.exp_name_label)
        self.control_widget_horiz_layout.addWidget(self.exp_control_group_box)
        self.block_control_group_box = QGroupBox(self.control_widget_dock_contents)
        self.block_control_group_box.setTitle("")
        self.block_control_group_box.setObjectName("run_new_group_box")
        self.block_control_group_box_vert_layout = QVBoxLayout(self.block_control_group_box)
        self.block_control_group_box_vert_layout.setObjectName("block_control_group_box_vert_layout")
        self.run_new_block_push_button = QPushButton(self.block_control_group_box)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.run_new_block_push_button.sizePolicy().hasHeightForWidth())
        self.run_new_block_push_button.setSizePolicy(size_policy)
        self.run_new_block_push_button.setMinimumSize(QSize(0, 0))
        self.run_new_block_push_button.setObjectName("run_new_block_push_button")
        self.block_control_group_box_vert_layout.addWidget(self.run_new_block_push_button)
        self.end_block_push_button = QPushButton(self.block_control_group_box)
        self.end_block_push_button.setObjectName("end_block_push_button")
        self.block_control_group_box_vert_layout.addWidget(self.end_block_push_button)
        self.block_name_label = QLineEdit(self.block_control_group_box)
        self.block_name_label.setPlaceholderText("Enter block name here")
        self.block_control_group_box_vert_layout.addWidget(self.block_name_label)
        self.control_widget_horiz_layout.addWidget(self.block_control_group_box)
        # End Control Widget Run/New group box generation code
        ################################################################################################################
        # Begin KeyFlag group box generation code
        self.key_flag_group_box = QGroupBox(self.control_widget_dock_contents)
        self.key_flag_group_box.setObjectName("key_flag_group_box")
        self.key_flag_vert_layout = QVBoxLayout(self.key_flag_group_box)
        self.key_flag_vert_layout.setObjectName("key_flag_vert_layout")
        self.key_flag_label = QLabel(self.key_flag_group_box)
        font = QFont()
        font.setPointSize(16)
        self.key_flag_label.setFont(font)
        self.key_flag_label.setObjectName("key_flag_label")
        self.key_flag_vert_layout.addWidget(self.key_flag_label, 0, Qt.AlignHCenter)
        self.control_widget_horiz_layout.addWidget(self.key_flag_group_box)
        # End KeyFlag group box generation code
        ################################################################################################################
        # Begin Block Note group box generation code
        self.block_note_group_box = QGroupBox(self.control_widget_dock_contents)
        self.block_note_group_box.setObjectName("block_note_group_box")
        self.block_note_group_box_grid_layout = QGridLayout(self.block_note_group_box)
        self.block_note_group_box_grid_layout.setObjectName("block_note_group_box_grid_layout")
        self.block_note_text_box = QTextEdit(self.block_note_group_box)
        self.block_note_text_box.setObjectName("block_note_text_box")
        self.block_note_group_box_grid_layout.addWidget(self.block_note_text_box, 0, 1, 1, 1)
        self.post_push_button = QPushButton(self.block_note_group_box)
        self.post_push_button.setObjectName("post_push_button")
        self.block_note_group_box_grid_layout.addWidget(self.post_push_button, 1, 1, 1, 1)
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
        self.exp_block_frame.setObjectName("exp_block_frame")
        self.exp_block_frame_grid_layout = QGridLayout(self.exp_block_frame)
        self.exp_block_frame_grid_layout.setContentsMargins(2, 2, 2, 2)
        self.exp_block_frame_grid_layout.setObjectName("exp_block_frame_grid_layout")
        self.exp_block_labels_frame = QFrame(self.exp_block_frame)
        self.exp_block_labels_frame.setFrameShape(QFrame.StyledPanel)
        self.exp_block_labels_frame.setFrameShadow(QFrame.Raised)
        self.exp_block_labels_frame.setObjectName("exp_block_labels_frame")
        self.exp_block_labels_frame_vert_layout = QVBoxLayout(self.exp_block_labels_frame)
        self.exp_block_labels_frame_vert_layout.setContentsMargins(2, 2, 2, 2)
        self.exp_block_labels_frame_vert_layout.setSpacing(6)
        self.exp_block_labels_frame_vert_layout.setObjectName("exp_block_labels_frame_vert_layout")
        self.exp_labels = QLabel(self.exp_block_labels_frame)
        self.exp_labels.setObjectName("exp_labels")
        self.exp_block_labels_frame_vert_layout.addWidget(self.exp_labels)
        self.exp_num_label = QLabel(self.exp_block_labels_frame)
        self.exp_num_label.setObjectName("exp_num_label")
        self.exp_block_labels_frame_vert_layout.addWidget(self.exp_num_label)
        self.exp_time_label = QLabel(self.exp_block_labels_frame)
        self.exp_time_label.setObjectName("exp_time_label")
        self.exp_block_labels_frame_vert_layout.addWidget(self.exp_time_label)
        self.block_label = QLabel(self.exp_block_labels_frame)
        self.block_label.setObjectName("block_label")
        self.exp_block_labels_frame_vert_layout.addWidget(self.block_label)
        self.block_num_label = QLabel(self.exp_block_labels_frame)
        self.block_num_label.setObjectName("block_num_label")
        self.exp_block_labels_frame_vert_layout.addWidget(self.block_num_label)
        self.block_time_label = QLabel(self.exp_block_labels_frame)
        self.block_time_label.setObjectName("block_time_label")
        self.exp_block_labels_frame_vert_layout.addWidget(self.block_time_label)
        self.exp_block_frame_grid_layout.addWidget(self.exp_block_labels_frame, 0, 0, 1, 1)
        self.exp_block_values_frame = QFrame(self.exp_block_frame)
        self.exp_block_values_frame.setMinimumSize(QSize(50, 0))
        self.exp_block_values_frame.setFrameShape(QFrame.StyledPanel)
        self.exp_block_values_frame.setFrameShadow(QFrame.Raised)
        self.exp_block_values_frame.setObjectName("exp_block_values_frame")
        self.exp_block_values_frame_vert_layout = QVBoxLayout(self.exp_block_values_frame)
        self.exp_block_values_frame_vert_layout.setContentsMargins(2, 2, 2, 2)
        self.exp_block_values_frame_vert_layout.setObjectName("exp_block_values_frame_vert_layout")
        self.exp_block_spacer_1 = QLabel(self.exp_block_values_frame)
        font = QFont()
        font.setPointSize(10)
        self.exp_block_spacer_1.setFont(font)
        self.exp_block_spacer_1.setText("")
        self.exp_block_spacer_1.setObjectName("exp_block_spacer_1")
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_block_spacer_1)
        self.exp_num_val_label = QLabel(self.exp_block_values_frame)
        self.exp_num_val_label.setObjectName("exp_num_val_label")
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_num_val_label, 0, Qt.AlignRight)
        self.exp_time_val_label = QLabel(self.exp_block_values_frame)
        font = QFont()
        font.setPointSize(10)
        self.exp_time_val_label.setFont(font)
        self.exp_time_val_label.setObjectName("exp_time_val_label")
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_time_val_label, 0, Qt.AlignRight)
        self.exp_block_spacer_2 = QLabel(self.exp_block_values_frame)
        self.exp_block_spacer_2.setText("")
        self.exp_block_spacer_2.setObjectName("exp_block_spacer_2")
        self.exp_block_values_frame_vert_layout.addWidget(self.exp_block_spacer_2)
        self.block_num_val_label = QLabel(self.exp_block_values_frame)
        self.block_num_val_label.setObjectName("block_num_val_label")
        self.exp_block_values_frame_vert_layout.addWidget(self.block_num_val_label, 0, Qt.AlignRight)
        self.block_time_val_label = QLabel(self.exp_block_values_frame)
        self.block_time_val_label.setObjectName("block_time_val_label")
        self.exp_block_values_frame_vert_layout.addWidget(self.block_time_val_label, 0, Qt.AlignRight)
        self.exp_block_frame_grid_layout.addWidget(self.exp_block_values_frame, 0, 1, 1, 1, Qt.AlignRight)
        self.control_widget_horiz_layout.addWidget(self.exp_block_frame)
        # End Trial/Block information generation code
        ################################################################################################################
        # Begin MenuBar item generation code
        #self.begin_exp_action = QAction(main_window)
        #self.begin_exp_action.setObjectName("begin_exp_action")
        self.save_action = QAction(main_window)
        self.save_action.setObjectName("save_action")
        self.save_as_action = QAction(main_window)
        self.save_as_action.setObjectName("save_as_action")
        self.com_messages_action = QAction(main_window)
        self.com_messages_action.setCheckable(True)
        self.com_messages_action.setObjectName("com_messages_action")
        self.about_rs_companion_action = QAction(main_window)
        self.about_rs_companion_action.setObjectName("about_rs_companion_action")
        self.about_rs_action = QAction(main_window)
        self.about_rs_action.setObjectName("about_rs_action")
        #self.end_exp_action = QAction(main_window)
        #self.end_exp_action.setObjectName("end_exp_action")
        self.trial_controls_action = QAction(main_window)
        self.trial_controls_action.setObjectName("trial_controls_action")
        self.display_tool_tips_action = QAction(main_window)
        self.display_tool_tips_action.setObjectName("display_tool_tips_action")
        self.configure_action = QAction(main_window)
        self.configure_action.setObjectName("configure_action")
        self.com_port_action = QAction(main_window)
        self.com_port_action.setObjectName("com_port_action")
        self.output_action = QAction(main_window)
        self.output_action.setObjectName("output_action")
        self.input_action = QAction(main_window)
        self.input_action.setObjectName("input_action")
        self.append_exp_action = QAction(main_window)
        self.append_exp_action.setObjectName("append_exp_action")
        self.open_file_action = QAction(main_window)
        self.open_file_action.setObjectName("open_file_action")
        #self.file_menu.addAction(self.begin_exp_action)
        #self.file_menu.addAction(self.end_exp_action)
        #self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addAction(self.open_file_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.append_exp_action)
        self.window_menu.addAction(self.trial_controls_action)
        self.window_menu.addAction(self.com_messages_action)
        self.window_menu.addAction(self.configure_action)
        self.window_menu.addSeparator()
        self.window_menu.addAction(self.display_tool_tips_action)
        self.window_menu.addSeparator()
        self.help_menu.addAction(self.about_rs_companion_action)
        self.help_menu.addAction(self.about_rs_action)
        self.udp_controls_menu.addAction(self.output_action)
        self.udp_controls_menu.addAction(self.input_action)
        self.settings_menu.addAction(self.com_port_action)
        self.settings_menu.addAction(self.udp_controls_menu.menuAction())
        self.menu_bar.addAction(self.file_menu.menuAction())
        self.menu_bar.addAction(self.settings_menu.menuAction())
        self.menu_bar.addAction(self.window_menu.menuAction())
        self.menu_bar.addAction(self.help_menu.menuAction())
        # End MenuBar item generation code
        ################################################################################################################
        # Begin final initialization
        self.__set_texts(main_window)
        # self.__set_colors()
        self.__setup_handlers(msg_handler)
        QMetaObject.connectSlotsByName(main_window)

    # Auto generated code slightly altered for readability
    def __set_texts(self, main_window):
        _translate = QCoreApplication.translate
        ################################################################################################################
        # Main Window SetTitle code
        main_window.setWindowTitle(_translate("MainWindow", "RS Device Companion"))
        ################################################################################################################
        # Begin MenuBar SetTitle code
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.window_menu.setTitle(_translate("MainWindow", "Window"))
        self.help_menu.setTitle(_translate("MainWindow", "Help"))
        self.settings_menu.setTitle(_translate("MainWindow", "Settings"))
        self.udp_controls_menu.setTitle(_translate("MainWindow", "UDP Controls"))
        #self.begin_exp_action.setText(_translate("MainWindow", "Begin Experiment"))
        #self.begin_exp_action.setToolTip(_translate("MainWindow", "Begin Experiment"))
        self.com_messages_action.setText(_translate("MainWindow", "COM Messages"))
        self.about_rs_companion_action.setText(_translate("MainWindow", "About RS Companion"))
        self.about_rs_action.setText(_translate("MainWindow", "About Red Scientific"))
        #self.end_exp_action.setText(_translate("MainWindow", "End Experiment"))
        self.trial_controls_action.setText(_translate("MainWindow", "Trial Controls"))
        self.display_tool_tips_action.setText(_translate("MainWindow", "Display Tooltips"))
        self.configure_action.setText(_translate("MainWindow", "Configure"))
        self.com_port_action.setText(_translate("MainWindow", "COM Port"))
        self.output_action.setText(_translate("MainWindow", "Output"))
        self.input_action.setText(_translate("MainWindow", "Input"))
        self.append_exp_action.setText(_translate("MainWindow", "Append Experiment"))
        self.open_file_action.setText(_translate("MainWindow", "Open"))
        self.save_action.setText(_translate("MainWindow", "Save"))
        self.save_as_action.setText(_translate("MainWindow", "Save As"))
        # End MenuBar SetTitle code
        ################################################################################################################
        # Begin Control Widget SetTitle code
        self.control_widget_dock.setWindowTitle(_translate("MainWindow", "Control"))
        self.run_new_exp_push_button.setText(_translate("MainWindow", "Begin New Experiment"))
        self.end_exp_push_button.setText(_translate("MainWindow", "End Experiment"))
        self.run_new_block_push_button.setText(_translate("MainWindow", "Begin New Block"))
        self.end_block_push_button.setText(_translate("MainWindow", "End Block"))
        self.key_flag_group_box.setTitle(_translate("MainWindow", "Key Flag"))
        self.key_flag_label.setText(_translate("MainWindow", "NA"))
        self.block_note_group_box.setTitle(_translate("MainWindow", "Block Note"))
        self.post_push_button.setText(_translate("MainWindow", "Post"))
        self.exp_labels.setText(_translate("MainWindow", "Experiment"))
        self.exp_num_label.setText(_translate("MainWindow", "    Number:"))
        self.exp_time_label.setText(_translate("MainWindow", "    Time:"))
        self.block_label.setText(_translate("MainWindow", "Block"))
        self.block_num_label.setText(_translate("MainWindow", "    Number:"))
        self.block_time_label.setText(_translate("MainWindow", "    Time:"))
        self.exp_num_val_label.setText(_translate("MainWindow", "NA"))
        self.exp_time_val_label.setText(_translate("MainWindow", "NA"))
        self.block_num_val_label.setText(_translate("MainWindow", "NA"))
        self.block_time_val_label.setText(_translate("MainWindow", "NA"))
        # End Control Widget SetTitle code

    # TODO: Decide to use this or not.
    def __set_colors(self):
        pal = self.run_new_block_push_button.palette()
        pal.setColor(QPalette.Button, Qt.cyan)
        self.run_new_block_push_button.setAutoFillBackground(True)
        self.run_new_block_push_button.setFlat(True)
        self.run_new_block_push_button.setPalette(pal)
        self.run_new_block_push_button.update()
        pal2 = self.run_new_exp_push_button.palette()
        pal2.setColor(QPalette.Button, Qt.yellow)
        self.run_new_exp_push_button.setAutoFillBackground(True)
        self.run_new_exp_push_button.setFlat(True)
        self.run_new_exp_push_button.setPalette(pal2)
        self.run_new_exp_push_button.update()

    def __setup_handlers(self, msg_handler):
        self.chart_scroll_bar.valueChanged.connect(self.__move_main_graph)
        self.about_rs_action.triggered.connect(self.__about_rs_action_handler)
        self.about_rs_companion_action.triggered.connect(self.__about_rs_companion_action_handler)
        self.msg_callback = msg_handler

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
        self.main_chart.scroll_graph(self.chart_scroll_bar.value())

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
            self.main_chart.handle_msg(msg_dict)

    # Creates an RSDevice and adds it to the list of devices
    def add_rs_device_handler(self, device):
        if device not in self.__list_of_devices__:
            self.__list_of_devices__[device] = device_container.RSDevice(device, self.msg_callback,
                                                                         self.rs_devices_tab_widget)
            self.main_chart.add_device(device)

    # Deletes an RSDevice and removes it from the list of devices
    def remove_rs_device_handler(self, device):
        if device in self.__list_of_devices__:
            self.__list_of_devices__[device].remove_self()
            del self.__list_of_devices__[device]
