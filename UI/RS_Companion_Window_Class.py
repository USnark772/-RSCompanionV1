# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific

# from PyQt5 import QtCore, QtGui, QtWidgets
from PySide2 import QtCore, QtGui, QtWidgets


class CompanionWindow(object):
    # Class level globals to keep track of the different devices for Device Box and Device SubWindow purposes
    __list_of_devices__ = {}
    __list_of_subwindows__ = {}
    __num_subwindows__ = 0

    ################################################################################################################
    # Begin auto-generated code
    ################################################################################################################

    # Auto generated code slightly altered for readability
    def __init__(self, main_window):
        # Begin MainWindow generation code
        main_window.setObjectName("main_window")
        main_window.resize(840, 705)
        main_window.setMinimumSize(QtCore.QSize(840, 468))
        font = QtGui.QFont()
        font.setPointSize(10)
        main_window.setFont(font)
        # End MainWindow generation code
        ################################################################################################################
        # Begin Central_Widget generation code
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.central_widget_vert_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.central_widget_vert_layout.setObjectName("central_widget_vert_layout")
        self.central_widget_separator_line = QtWidgets.QFrame(self.central_widget)
        self.central_widget_separator_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.central_widget_separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.central_widget_separator_line.setObjectName("central_widget_separator_line")
        self.central_widget_vert_layout.addWidget(self.central_widget_separator_line)
        main_window.setCentralWidget(self.central_widget)
        # End Central Widget generation code
        ################################################################################################################
        # Begin MDI Dock generation code
        self.mdi_dock_frame = QtWidgets.QFrame(self.central_widget)
        self.mdi_dock_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mdi_dock_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mdi_dock_frame.setObjectName("mdi_dock_frame")
        self.mdi_dock_frame_horiz_layout = QtWidgets.QHBoxLayout(self.mdi_dock_frame)
        self.mdi_dock_frame_horiz_layout.setContentsMargins(0, 0, 0, 0)
        self.mdi_dock_frame_horiz_layout.setObjectName("mdi_dock_frame_horiz_layout")
        self.mdi_dock_area = QtWidgets.QMdiArea(self.mdi_dock_frame)
        self.mdi_dock_area.setObjectName("mdi_dock_area")
        self.mdi_dock_frame_horiz_layout.addWidget(self.mdi_dock_area)
        self.central_widget_vert_layout.addWidget(self.mdi_dock_frame)
        # End MDI Dock generation code
        ################################################################################################################
        # Begin MDI SubWindow Generation Code
        '''
        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("subwindow")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.subwindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.subwindow)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.frame_4 = QtWidgets.QFrame(self.subwindow)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 265))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout.addWidget(self.frame_4)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.subwindow)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.scrollArea_2.size_policy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(size_policy)
        self.scrollArea_2.setMinimumSize(QtCore.QSize(150, 0))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 148, 296))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.groupBox_5 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 175))
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_8.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_8.setSpacing(9)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_16 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_16.setObjectName("pushButton_16")
        self.verticalLayout_8.addWidget(self.pushButton_16)
        self.pushButton_17 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_17.setObjectName("pushButton_17")
        self.verticalLayout_8.addWidget(self.pushButton_17)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_8.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_8.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_8.addWidget(self.checkBox_4)
        self.verticalLayout_11.addWidget(self.groupBox_5)
        spacerItem = QtWidgets.QSpacerItem(20, 97, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem)
        self.groupBox_6 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_6.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_15 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_15.setObjectName("pushButton_15")
        self.verticalLayout_7.addWidget(self.pushButton_15)
        self.pushButton_14 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_14.setObjectName("pushButton_14")
        self.verticalLayout_7.addWidget(self.pushButton_14)
        self.verticalLayout_11.addWidget(self.groupBox_6)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout.addWidget(self.scrollArea_2)
        '''
        # End MDI SubWindow generation Code
        ################################################################################################################
        # Begin Menu Bar generation code
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 840, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.file_menu = QtWidgets.QMenu(self.menu_bar)
        self.file_menu.setObjectName("file_menu")
        self.window_menu = QtWidgets.QMenu(self.menu_bar)
        self.window_menu.setObjectName("window_menu")
        self.help_menu = QtWidgets.QMenu(self.menu_bar)
        self.help_menu.setObjectName("help_menu")
        self.settings_menu = QtWidgets.QMenu(self.menu_bar)
        self.settings_menu.setObjectName("settings_menu")
        self.udp_controls_menu = QtWidgets.QMenu(self.settings_menu)
        self.udp_controls_menu.setObjectName("udp_controls_menu")
        main_window.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(main_window)
        self.status_bar.setObjectName("status_bar")
        main_window.setStatusBar(self.status_bar)
        # End MenuBar generation code
        ################################################################################################################
        # Begin Control Widget generation code
        self.control_widget_dock = QtWidgets.QDockWidget(main_window)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.control_widget_dock.sizePolicy().hasHeightForWidth())
        self.control_widget_dock.setSizePolicy(size_policy)
        self.control_widget_dock.setMinimumSize(QtCore.QSize(500, 150))
        self.control_widget_dock.setMaximumSize(QtCore.QSize(650, 150))
        self.control_widget_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.control_widget_dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.control_widget_dock.setObjectName("control_widget_dock")
        self.control_widget_dock_contents = QtWidgets.QWidget()
        self.control_widget_dock_contents.setObjectName("control_widget_dock_contents")
        self.control_widget_horiz_layout = QtWidgets.QHBoxLayout(self.control_widget_dock_contents)
        self.control_widget_horiz_layout.setObjectName("control_widget_horiz_layout")
        self.control_widget_dock.setWidget(self.control_widget_dock_contents)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.control_widget_dock)
        # End Control Widget generation code
        ################################################################################################################
        # Begin Control Widget Run/New group box generation code
        self.run_new_group_box = QtWidgets.QGroupBox(self.control_widget_dock_contents)
        self.run_new_group_box.setTitle("")
        self.run_new_group_box.setObjectName("run_new_group_box")
        self.run_new_group_box_vert_layout = QtWidgets.QVBoxLayout(self.run_new_group_box)
        self.run_new_group_box_vert_layout.setObjectName("run_new_group_box_vert_layout")
        self.run_trial_push_button = QtWidgets.QPushButton(self.run_new_group_box)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.run_trial_push_button.sizePolicy().hasHeightForWidth())
        self.run_trial_push_button.setSizePolicy(size_policy)
        self.run_trial_push_button.setMinimumSize(QtCore.QSize(0, 0))
        self.run_trial_push_button.setObjectName("run_trial_push_button")
        self.run_new_group_box_vert_layout.addWidget(self.run_trial_push_button)
        self.new_block_push_button = QtWidgets.QPushButton(self.run_new_group_box)
        self.new_block_push_button.setObjectName("new_block_push_button")
        self.run_new_group_box_vert_layout.addWidget(self.new_block_push_button)
        self.control_widget_horiz_layout.addWidget(self.run_new_group_box)
        # End Control Widget Run/New group box generation code
        ################################################################################################################
        # Begin KeyFlag group box generation code
        self.key_flag_group_box = QtWidgets.QGroupBox(self.control_widget_dock_contents)
        self.key_flag_group_box.setObjectName("key_flag_group_box")
        self.key_flag_vert_layout = QtWidgets.QVBoxLayout(self.key_flag_group_box)
        self.key_flag_vert_layout.setObjectName("key_flag_vert_layout")
        self.key_flag_label = QtWidgets.QLabel(self.key_flag_group_box)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.key_flag_label.setFont(font)
        self.key_flag_label.setObjectName("key_flag_label")
        self.key_flag_vert_layout.addWidget(self.key_flag_label, 0, QtCore.Qt.AlignHCenter)
        self.control_widget_horiz_layout.addWidget(self.key_flag_group_box)
        # End KeyFlag group box generation code
        ################################################################################################################
        # Begin Block Note group box generation code
        self.block_note_group_box = QtWidgets.QGroupBox(self.control_widget_dock_contents)
        self.block_note_group_box.setObjectName("block_note_group_box")
        self.block_note_group_box_grid_layout = QtWidgets.QGridLayout(self.block_note_group_box)
        self.block_note_group_box_grid_layout.setObjectName("block_note_group_box_grid_layout")
        self.block_note_text_box = QtWidgets.QTextEdit(self.block_note_group_box)
        self.block_note_text_box.setObjectName("block_note_text_box")
        self.block_note_group_box_grid_layout.addWidget(self.block_note_text_box, 0, 1, 1, 1)
        self.post_push_button = QtWidgets.QPushButton(self.block_note_group_box)
        self.post_push_button.setObjectName("post_push_button")
        self.block_note_group_box_grid_layout.addWidget(self.post_push_button, 1, 1, 1, 1)
        self.control_widget_horiz_layout.addWidget(self.block_note_group_box)
        # End Block Note group box generation code
        ################################################################################################################
        # Begin Trial/Block information generation code
        self.trial_block_frame = QtWidgets.QFrame(self.control_widget_dock_contents)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.trial_block_frame.sizePolicy().hasHeightForWidth())
        self.trial_block_frame.setSizePolicy(size_policy)
        self.trial_block_frame.setMinimumSize(QtCore.QSize(130, 0))
        self.trial_block_frame.setObjectName("trial_block_frame")
        self.trial_block_frame_grid_layout = QtWidgets.QGridLayout(self.trial_block_frame)
        self.trial_block_frame_grid_layout.setContentsMargins(2, 2, 2, 2)
        self.trial_block_frame_grid_layout.setObjectName("trial_block_frame_grid_layout")
        self.trial_block_labels_frame = QtWidgets.QFrame(self.trial_block_frame)
        self.trial_block_labels_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trial_block_labels_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trial_block_labels_frame.setObjectName("trial_block_labels_frame")
        self.trial_block_labels_frame_vert_layout = QtWidgets.QVBoxLayout(self.trial_block_labels_frame)
        self.trial_block_labels_frame_vert_layout.setContentsMargins(2, 2, 2, 2)
        self.trial_block_labels_frame_vert_layout.setSpacing(6)
        self.trial_block_labels_frame_vert_layout.setObjectName("trial_block_labels_frame_vert_layout")
        self.trial_labels = QtWidgets.QLabel(self.trial_block_labels_frame)
        self.trial_labels.setObjectName("trial_labels")
        self.trial_block_labels_frame_vert_layout.addWidget(self.trial_labels)
        self.trial_num_label = QtWidgets.QLabel(self.trial_block_labels_frame)
        self.trial_num_label.setObjectName("trial_num_label")
        self.trial_block_labels_frame_vert_layout.addWidget(self.trial_num_label)
        self.trial_time_label = QtWidgets.QLabel(self.trial_block_labels_frame)
        self.trial_time_label.setObjectName("trial_time_label")
        self.trial_block_labels_frame_vert_layout.addWidget(self.trial_time_label)
        self.block_label = QtWidgets.QLabel(self.trial_block_labels_frame)
        self.block_label.setObjectName("block_label")
        self.trial_block_labels_frame_vert_layout.addWidget(self.block_label)
        self.block_num_label = QtWidgets.QLabel(self.trial_block_labels_frame)
        self.block_num_label.setObjectName("block_num_label")
        self.trial_block_labels_frame_vert_layout.addWidget(self.block_num_label)
        self.block_time_label = QtWidgets.QLabel(self.trial_block_labels_frame)
        self.block_time_label.setObjectName("block_time_label")
        self.trial_block_labels_frame_vert_layout.addWidget(self.block_time_label)
        self.trial_block_frame_grid_layout.addWidget(self.trial_block_labels_frame, 0, 0, 1, 1)
        self.trial_block_values_frame = QtWidgets.QFrame(self.trial_block_frame)
        self.trial_block_values_frame.setMinimumSize(QtCore.QSize(50, 0))
        self.trial_block_values_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trial_block_values_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.trial_block_values_frame.setObjectName("trial_block_values_frame")
        self.trial_block_values_frame_vert_layout = QtWidgets.QVBoxLayout(self.trial_block_values_frame)
        self.trial_block_values_frame_vert_layout.setContentsMargins(2, 2, 2, 2)
        self.trial_block_values_frame_vert_layout.setObjectName("trial_block_values_frame_vert_layout")
        self.trial_block_spacer_1 = QtWidgets.QLabel(self.trial_block_values_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.trial_block_spacer_1.setFont(font)
        self.trial_block_spacer_1.setText("")
        self.trial_block_spacer_1.setObjectName("trial_block_spacer_1")
        self.trial_block_values_frame_vert_layout.addWidget(self.trial_block_spacer_1)
        self.trial_num_val_label = QtWidgets.QLabel(self.trial_block_values_frame)
        self.trial_num_val_label.setObjectName("trial_num_val_label")
        self.trial_block_values_frame_vert_layout.addWidget(self.trial_num_val_label, 0, QtCore.Qt.AlignRight)
        self.trial_time_val_label = QtWidgets.QLabel(self.trial_block_values_frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.trial_time_val_label.setFont(font)
        self.trial_time_val_label.setObjectName("trial_time_val_label")
        self.trial_block_values_frame_vert_layout.addWidget(self.trial_time_val_label, 0, QtCore.Qt.AlignRight)
        self.trial_block_spacer_2 = QtWidgets.QLabel(self.trial_block_values_frame)
        self.trial_block_spacer_2.setText("")
        self.trial_block_spacer_2.setObjectName("trial_block_spacer_2")
        self.trial_block_values_frame_vert_layout.addWidget(self.trial_block_spacer_2)
        self.block_num_val_label = QtWidgets.QLabel(self.trial_block_values_frame)
        self.block_num_val_label.setObjectName("block_num_val_label")
        self.trial_block_values_frame_vert_layout.addWidget(self.block_num_val_label, 0, QtCore.Qt.AlignRight)
        self.block_time_val_label = QtWidgets.QLabel(self.trial_block_values_frame)
        self.block_time_val_label.setObjectName("block_time_val_label")
        self.trial_block_values_frame_vert_layout.addWidget(self.block_time_val_label, 0, QtCore.Qt.AlignRight)
        self.trial_block_frame_grid_layout.addWidget(self.trial_block_values_frame, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        self.control_widget_horiz_layout.addWidget(self.trial_block_frame)
        # End Trial/Block information generation code
        ################################################################################################################
        # Begin COM Widget generation code
        self.com_widget_dock = QtWidgets.QDockWidget(main_window)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.com_widget_dock.sizePolicy().hasHeightForWidth())
        self.com_widget_dock.setSizePolicy(size_policy)
        self.com_widget_dock.setMinimumSize(QtCore.QSize(374, 130))
        self.com_widget_dock.setMaximumSize(QtCore.QSize(524287, 130))
        self.com_widget_dock.setBaseSize(QtCore.QSize(0, 0))
        self.com_widget_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.com_widget_dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.com_widget_dock.setObjectName("com_widget_dock")
        self.com_widget_contents = QtWidgets.QWidget()
        self.com_widget_contents.setObjectName("com_widget_contents")
        self.com_widget_dock.setWidget(self.com_widget_contents)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.com_widget_dock)
        self.com_widget_contents_grid_layout = QtWidgets.QGridLayout(self.com_widget_contents)
        self.com_widget_contents_grid_layout.setObjectName("com_widget_contents_grid_layout")
        self.record_push_button = QtWidgets.QPushButton(self.com_widget_contents)
        self.record_push_button.setObjectName("record_push_button")
        self.com_widget_contents_grid_layout.addWidget(self.record_push_button, 1, 0, 1, 1)
        self.freeze_push_button = QtWidgets.QPushButton(self.com_widget_contents)
        self.freeze_push_button.setObjectName("freeze_push_button")
        self.com_widget_contents_grid_layout.addWidget(self.freeze_push_button, 1, 2, 1, 1)
        self.clear_push_button = QtWidgets.QPushButton(self.com_widget_contents)
        self.clear_push_button.setObjectName("clear_push_button")
        self.com_widget_contents_grid_layout.addWidget(self.clear_push_button, 1, 4, 1, 1)
        spacer_item_1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.com_widget_contents_grid_layout.addItem(spacer_item_1, 1, 1, 1, 1)
        self.CHANGEME_check_box = QtWidgets.QCheckBox(self.com_widget_contents)
        self.CHANGEME_check_box.setObjectName("CHANGEME_check_box")
        self.com_widget_contents_grid_layout.addWidget(self.CHANGEME_check_box, 1, 5, 1, 1)
        self.com_text_box = QtWidgets.QPlainTextEdit(self.com_widget_contents)
        self.com_text_box.setMinimumSize(QtCore.QSize(0, 0))
        self.com_text_box.setSizeIncrement(QtCore.QSize(0, 0))
        self.com_text_box.setBaseSize(QtCore.QSize(0, 0))
        self.com_text_box.setObjectName("com_text_box")
        self.com_widget_contents_grid_layout.addWidget(self.com_text_box, 0, 0, 1, 6)
        # End COM Widget generation code
        ################################################################################################################
        # Begin Configure Widget generation code
        self.configure_widget_dock = QtWidgets.QDockWidget(main_window)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.configure_widget_dock.sizePolicy().hasHeightForWidth())
        self.configure_widget_dock.setSizePolicy(size_policy)
        self.configure_widget_dock.setMinimumSize(QtCore.QSize(350, 150))
        self.configure_widget_dock.setMaximumSize(QtCore.QSize(450, 150))
        self.configure_widget_dock.setFeatures(
            QtWidgets.QDockWidget.DockWidgetFloatable |
            QtWidgets.QDockWidget.DockWidgetMovable |
            QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.configure_widget_dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.configure_widget_dock.setObjectName("configure_widget_dock")
        self.configure_widget_contents = QtWidgets.QWidget()
        self.configure_widget_contents.setObjectName("configure_widget_contents")
        self.configure_widget_contents_horiz_layout = QtWidgets.QHBoxLayout(self.configure_widget_contents)
        self.configure_widget_contents_horiz_layout.setObjectName("configure_widget_contents_horiz_layout")
        self.rs_devices_group_box = QtWidgets.QGroupBox(self.configure_widget_contents)
        self.rs_devices_group_box.setObjectName("rs_devices_group_box")
        self.rs_devices_group_box_horiz_layout = QtWidgets.QHBoxLayout(self.rs_devices_group_box)
        self.rs_devices_group_box_horiz_layout.setObjectName("rs_devices_group_box_horiz_layout")
        self.rs_devices_scroll_area = QtWidgets.QScrollArea(self.rs_devices_group_box)
        self.configure_widget_contents_horiz_layout.addWidget(self.rs_devices_group_box)
        self.rs_devices_scroll_area.setWidgetResizable(True)
        self.rs_devices_scroll_area.setObjectName("rs_devices_scroll_area")
        self.rs_devices_scroll_area_contents = QtWidgets.QWidget()
        self.rs_devices_scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 179, 94))
        self.rs_devices_scroll_area_contents.setObjectName("RS_Devices_ScrollArea_Contents")
        self.rs_devices_scroll_area.setWidget(self.rs_devices_scroll_area_contents)
        self.rs_devices_group_box_horiz_layout.addWidget(self.rs_devices_scroll_area)
        self.rs_devices_scroll_area_contents_vert_layout = QtWidgets.QVBoxLayout(self.rs_devices_scroll_area_contents)
        self.rs_devices_scroll_area_contents_vert_layout.setObjectName("RS_Devices_ScrollArea_Contents_Vert_Layout")
        # End Configure Widget generation code
        ################################################################################################################
        # Begin RS Device box generation code
        """
        self.Device_GroupBox = QtWidgets.QGroupBox(self.RS_Devices_ScrollArea_Contents)
        self.Device_GroupBox.setObjectName("Device_GroupBox")
        self.Device_GroupBox_Horiz_Layout = QtWidgets.QHBoxLayout(self.Device_GroupBox)
        self.Device_GroupBox_Horiz_Layout.setObjectName("Device_GroupBox_Horiz_Layout")
        self.Setup_PushButton = QtWidgets.QPushButton(self.Device_GroupBox)
        self.Setup_PushButton.setObjectName("Setup_PushButton")
        self.Device_GroupBox_Horiz_Layout.addWidget(self.Setup_PushButton)
        self.Device_ToolButton = QtWidgets.QToolButton(self.Device_GroupBox)
        self.Device_ToolButton.setObjectName("Device_ToolButton")
        self.Device_GroupBox_Horiz_Layout.addWidget(self.Device_ToolButton)
        self.RS_Devices_ScrollArea_Contents_Vert_Layout.addWidget(self.Device_GroupBox)
        """
        # End RS Device box generation code
        ################################################################################################################
        # Begin MDI View option generation code
        self.mdi_view_group_box = QtWidgets.QGroupBox(self.configure_widget_contents)
        self.mdi_view_group_box.setObjectName("mdi_view_group_box")
        self.mdi_view_group_box_vert_layout = QtWidgets.QVBoxLayout(self.mdi_view_group_box)
        self.mdi_view_group_box_vert_layout.setObjectName("mdi_view_group_box_vert_layout")
        self.mdi_view_main_radio_button = QtWidgets.QRadioButton(self.mdi_view_group_box)
        self.mdi_view_main_radio_button.setObjectName("mdi_view_main_radio_button")
        self.mdi_view_group_box_vert_layout.addWidget(self.mdi_view_main_radio_button)
        self.mdi_view_tiled_radio_button = QtWidgets.QRadioButton(self.mdi_view_group_box)
        self.mdi_view_tiled_radio_button.setObjectName("mdi_view_tiled_radio_button")
        self.mdi_view_group_box_vert_layout.addWidget(self.mdi_view_tiled_radio_button)
        self.mdi_view_cascade_radio_button = QtWidgets.QRadioButton(self.mdi_view_group_box)
        self.mdi_view_cascade_radio_button.setObjectName("mdi_view_cascade_radio_button")
        self.mdi_view_group_box_vert_layout.addWidget(self.mdi_view_cascade_radio_button)
        self.mdi_view_vert_radio_button = QtWidgets.QRadioButton(self.mdi_view_group_box)
        self.mdi_view_vert_radio_button.setObjectName("mdi_view_vert_radio_button")
        self.mdi_view_group_box_vert_layout.addWidget(self.mdi_view_vert_radio_button)
        self.mdi_view_horiz_radio_button = QtWidgets.QRadioButton(self.mdi_view_group_box)
        self.mdi_view_horiz_radio_button.setObjectName("mdi_view_horiz_radio_button")
        self.mdi_view_group_box_vert_layout.addWidget(self.mdi_view_horiz_radio_button)
        self.configure_widget_contents_horiz_layout.addWidget(self.mdi_view_group_box)
        self.configure_widget_dock.setWidget(self.configure_widget_contents)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.configure_widget_dock)
        # End MDI View option generation code
        ################################################################################################################
        # Begin MenuBar item generation code
        self.begin_exp_action = QtWidgets.QAction(main_window)
        self.begin_exp_action.setObjectName("begin_exp_action")
        self.com_messages_action = QtWidgets.QAction(main_window)
        self.com_messages_action.setCheckable(True)
        self.com_messages_action.setObjectName("com_messages_action")
        # TODO: Figure out what these are for
        '''
        #self.actionExit_2 = QtWidgets.QAction(main_window)
        #self.actionExit_2.setObjectName("actionExit_2")
        self.actionParameters = QtWidgets.QAction(MainWindow)
        self.actionParameters.setCheckable(True)
        self.actionParameters.setObjectName("actionParameters")
        self.actionLive_Data = QtWidgets.QAction(MainWindow)
        self.actionLive_Data.setCheckable(True)
        self.actionLive_Data.setObjectName("actionLive_Data")
        self.actionConfigure_Data_Buddy = QtWidgets.QAction(MainWindow)
        self.actionConfigure_Data_Buddy.setObjectName("actionConfigure_Data_Buddy")
        '''
        self.about_rs_companion_action = QtWidgets.QAction(main_window)
        self.about_rs_companion_action.setObjectName("about_rs_companion_action")
        self.about_rs_action = QtWidgets.QAction(main_window)
        self.about_rs_action.setObjectName("about_rs_action")
        self.end_exp_action = QtWidgets.QAction(main_window)
        self.end_exp_action.setObjectName("end_exp_action")
        self.trial_controls_action = QtWidgets.QAction(main_window)
        self.trial_controls_action.setObjectName("trial_controls_action")
        self.display_tool_tips_action = QtWidgets.QAction(main_window)
        self.display_tool_tips_action.setObjectName("display_tool_tips_action")
        self.configure_action = QtWidgets.QAction(main_window)
        self.configure_action.setObjectName("configure_action")
        self.com_port_action = QtWidgets.QAction(main_window)
        self.com_port_action.setObjectName("com_port_action")
        self.output_action = QtWidgets.QAction(main_window)
        self.output_action.setObjectName("output_action")
        self.input_action = QtWidgets.QAction(main_window)
        self.input_action.setObjectName("input_action")
        self.append_exp_action = QtWidgets.QAction(main_window)
        self.append_exp_action.setObjectName("append_exp_action")
        self.open_file_action = QtWidgets.QAction(main_window)
        self.open_file_action.setObjectName("open_file_action")
        self.file_menu.addAction(self.begin_exp_action)
        self.file_menu.addAction(self.end_exp_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.append_exp_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.open_file_action)
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
        self.set_texts(main_window)
        self.setup_button_handlers()
        self.clear_push_button.clicked.connect(self.com_text_box.clear)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    # Auto generated code slightly altered for readability
    def set_texts(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        ################################################################################################################
        # Main Window SetTitle code
        main_window.setWindowTitle(_translate("MainWindow", "RS Device Companion"))
        ################################################################################################################
        # Begin SubWindow SetTitle code
        '''
        self.subwindow.setWindowTitle(_translate("MainWindow", "Subwindow"))
        self.groupBox_5.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_16.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_17.setText(_translate("MainWindow", "PushButton"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_3.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_4.setText(_translate("MainWindow", "CheckBox"))
        self.groupBox_6.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_15.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_14.setText(_translate("MainWindow", "PushButton"))
        '''
        # End SubWindow SetTitle code
        ################################################################################################################
        # Begin MenuBar SetTitle code
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.window_menu.setTitle(_translate("MainWindow", "Window"))
        self.help_menu.setTitle(_translate("MainWindow", "Help"))
        self.settings_menu.setTitle(_translate("MainWindow", "Settings"))
        self.udp_controls_menu.setTitle(_translate("MainWindow", "UDP Controls"))
        self.begin_exp_action.setText(_translate("MainWindow", "Begin Experiment"))
        self.begin_exp_action.setToolTip(_translate("MainWindow", "Begin Experiment"))
        self.com_messages_action.setText(_translate("MainWindow", "COM Messages"))
        # TODO: Figure out what these are for
        '''
        self.actionParameters.setText(_translate("MainWindow", "Parameters"))
        self.actionLive_Data.setText(_translate("MainWindow", "Live Data"))
        self.actionConfigure_Data_Buddy.setText(_translate("MainWindow", "Configure Data Buddy"))
        #self.actionExit_2.setText(_translate("MainWindow", "Exit"))
        '''
        self.about_rs_companion_action.setText(_translate("MainWindow", "About RS Companion"))
        self.about_rs_action.setText(_translate("MainWindow", "About Red Scientific"))
        self.end_exp_action.setText(_translate("MainWindow", "End Experiment"))
        self.trial_controls_action.setText(_translate("MainWindow", "Trial Controls"))
        self.display_tool_tips_action.setText(_translate("MainWindow", "Display Tooltips"))
        self.configure_action.setText(_translate("MainWindow", "Configure"))
        self.com_port_action.setText(_translate("MainWindow", "COM Port"))
        self.output_action.setText(_translate("MainWindow", "Output"))
        self.input_action.setText(_translate("MainWindow", "Input"))
        self.append_exp_action.setText(_translate("MainWindow", "Append Experiment"))
        self.open_file_action.setText(_translate("MainWindow", "Open File  Folder"))
        # End MenuBar SetTitle code
        ################################################################################################################
        # Begin Control Widget SetTitle code
        self.control_widget_dock.setWindowTitle(_translate("MainWindow", "Control"))
        self.run_trial_push_button.setText(_translate("MainWindow", "Run\nTrial"))
        self.new_block_push_button.setText(_translate("MainWindow", "New Block"))
        self.key_flag_group_box.setTitle(_translate("MainWindow", "Key Flag"))
        self.key_flag_label.setText(_translate("MainWindow", "NA"))
        self.block_note_group_box.setTitle(_translate("MainWindow", "Block Note"))
        self.post_push_button.setText(_translate("MainWindow", "Post"))
        self.trial_labels.setText(_translate("MainWindow", "Trial"))
        self.trial_num_label.setText(_translate("MainWindow", "    Number:"))
        self.trial_time_label.setText(_translate("MainWindow", "    Time:"))
        self.block_label.setText(_translate("MainWindow", "Block"))
        self.block_num_label.setText(_translate("MainWindow", "    Number:"))
        self.block_time_label.setText(_translate("MainWindow", "    Time:"))
        self.trial_num_val_label.setText(_translate("MainWindow", "NA"))
        self.trial_time_val_label.setText(_translate("MainWindow", "NA"))
        self.block_num_val_label.setText(_translate("MainWindow", "NA"))
        self.block_time_val_label.setText(_translate("MainWindow", "NA"))
        # End Control Widget SetTitle code
        ################################################################################################################
        # Begin COM Widget SetTitle code
        self.com_widget_dock.setToolTip(_translate("MainWindow", "<html><head/><body><p>Displays all communications"
                                                                 " with Red Scientific Hardware. These can be saved for"
                                                                 " later browsing and debugging.</p></body></html>"))
        self.com_widget_dock.setWindowTitle(_translate("MainWindow", "COM"))
        self.record_push_button.setToolTip(_translate("MainWindow", "<html><head/><body><p>Saves all raw COM messages"
                                                                    " to your data folder.</p></body></html>"))
        self.record_push_button.setText(_translate("MainWindow", "Record"))
        self.freeze_push_button.setToolTip(_translate("MainWindow", "<html><head/><body><p>Freezes the auto scrolling"
                                                                    " of COM messages.</p></body></html>"))
        self.freeze_push_button.setText(_translate("MainWindow", "Freeze"))
        self.clear_push_button.setToolTip(_translate("MainWindow", "<html><head/><body><p>Clears all COM messages in"
                                                                   " the pane above.</p></body></html>"))
        self.clear_push_button.setText(_translate("MainWindow", "Clear"))
        self.CHANGEME_check_box.setText(_translate("MainWindow", "CHANGEME_CheckBox"))
        # End COM Widget SetTitle code
        ################################################################################################################
        # Begin Configure Widget SetTitle code
        self.configure_widget_dock.setWindowTitle(_translate("MainWindow", "Configure"))
        self.rs_devices_group_box.setTitle(_translate("MainWindow", "Red Scientific Devices"))
        '''
        self.Device_GroupBox.setTitle(_translate("MainWindow", "DRT - Wireless 1"))
        self.Setup_PushButton.setText(_translate("MainWindow", "Setup"))
        self.Device_ToolButton.setText(_translate("MainWindow", "..."))
        '''
        self.mdi_view_group_box.setTitle(_translate("MainWindow", "MDI View"))
        self.mdi_view_main_radio_button.setText(_translate("MainWindow", "Main"))
        self.mdi_view_tiled_radio_button.setText(_translate("MainWindow", "Tiled"))
        self.mdi_view_cascade_radio_button.setText(_translate("MainWindow", "Cascade"))
        self.mdi_view_vert_radio_button.setText(_translate("MainWindow", "Vertical"))
        self.mdi_view_horiz_radio_button.setText(_translate("MainWindow", "Horizontal"))
        # End Configure Widget SetTitle code

    ################################################################################################################
    # End auto-generated code
    ################################################################################################################

    # TODO: Get buttons working (need to know what they should each do)
    # TODO: Make handlers for menu items
    # Assign buttons to functions
    def setup_button_handlers(self):
        self.trial_controls_action.triggered.connect(self.trial_controls_action_handler)
        self.input_action.triggered.connect(self.input_action_handler)
        self.output_action.triggered.connect(self.output_action_handler)
        self.open_file_action.triggered.connect(self.open_action_handler)
        self.end_exp_action.triggered.connect(self.end_experiment_cction_handler)
        self.display_tool_tips_action.triggered.connect(self.display_tooltips_action_handler)
        self.configure_action.triggered.connect(self.configure_action_handler)
        self.com_port_action.triggered.connect(self.com_port_action_handler)
        self.com_messages_action.triggered.connect(self.com_messages_action_handler)
        self.begin_exp_action.triggered.connect(self.begin_experiment_action_handler)
        self.append_exp_action.triggered.connect(self.append_experiment_action_handler)
        self.about_rs_action.triggered.connect(self.about_rs_action_handler)
        self.about_rs_companion_action.triggered.connect(self.about_rs_companion_action_handler)
        self.mdi_view_main_radio_button.clicked.connect(self.mdi_main_handler)
        self.mdi_view_tiled_radio_button.clicked.connect(self.mdi_tile_handler)
        self.mdi_view_cascade_radio_button.clicked.connect(self.mdi_cascade_handler)
        self.mdi_view_vert_radio_button.clicked.connect(self.mdi_vert_handler)
        self.mdi_view_horiz_radio_button.clicked.connect(self.mdi_horiz_handler)
        self.run_trial_push_button.clicked.connect(self.run_trial_button_handler)
        self.new_block_push_button.clicked.connect(self.new_block_button_handler)
        self.post_push_button.clicked.connect(self.post_button_handler)
        self.record_push_button.clicked.connect(self.record_button_handler)
        self.freeze_push_button.clicked.connect(self.freeze_button_handler)
        self.clear_push_button.clicked.connect(self.clear_button_handler)
        self.CHANGEME_check_box.toggled.connect(self.CHANGEME_checkbox_handler)

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def trial_controls_action_handler(self):
        print("Trial Controls Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def input_action_handler(self):
        print("Input Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def output_action_handler(self):
        print("Output Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    # Allows user to select a file through file explorer and opens it
    def open_action_handler(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file',
                                                      'c:\\')
        print("Open Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def end_experiment_cction_handler(self):
        print("End Experiment Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def display_tooltips_action_handler(self):
        print("Display Tooltips Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def configure_action_handler(self):
        print("Configure Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def com_port_action_handler(self):
        print("COM Port Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def com_messages_action_handler(self):
        print("COM Messages Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def begin_experiment_action_handler(self):
        print("Begin Experiment Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def append_experiment_action_handler(self):
        print("Append Experiment Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def about_rs_companion_action_handler(self):
        print("About RS Companion Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def about_rs_action_handler(self):
        print("About RS Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def CHANGEME_checkbox_handler(self):
        print("CHANGEME CheckBox toggled")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def run_trial_button_handler(self):
        print("Run Trial Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def record_button_handler(self):
        print("Record Button Pressed, connected to Add_RS_Device handler")
        self.add_rs_device_handler()

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def freeze_button_handler(self):
        print("Freeze Button Pressed, connected to Remove_RS_Device handler")
        self.remove_rs_device_handler()

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def new_block_button_handler(self):
        print("New Block Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def clear_button_handler(self):
        print("Clear Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def post_button_handler(self):
        print("Post Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: After finishing this, figure out how to fix resizing a subwindow when moving it after cascading
    # Cascades the SubWindows in the MDI Dock
    def mdi_cascade_handler(self):
        print("cascade called")
        position = QtCore.QPoint(0, 0)
        max_width = self.mdi_dock_area.width()
        max_height = self.mdi_dock_area.height()
        for window in self.mdi_dock_area.subWindowList():
            rect = QtCore.QRect(0, 0, int(max(max_width/self.__num_subwindows__, 250)),
                                int(max(max_width/self.__num_subwindows__, 250)))
            window.setGeometry(rect)
            window.move(position)
            if self.__num_subwindows__ > 1:
                temp_x = position.x() + int(max(max_width / window.width(), max_width/20))
                temp_y = position.y() + int(max(max_height/window.height(), max_height/20))
                new_x = temp_x % (max_width - window.width()/2)
                new_y = temp_y % (max_height - window.height()/2)
                position.setX(new_x)
                position.setY(new_y)
        #self.mdi_dock_area.cascadeSubWindows()

    # TODO: Remove prints in this function after debugging
    # TODO: Model this after mdi_cascade_handler
    # Tiles the SubWindows in the MDI Dock
    def mdi_tile_handler(self):
        print("mdi tile handler called")
        #self.mdi_dock_area.tileSubWindows()

    # TODO: Remove prints in this function after debugging
    # TODO: Model this after mdi_cascade_handler
    # Vertically lays out the SubWindows in the MDI Dock
    def mdi_vert_handler(self):
        print("MDI_Vert_Handler called")
        if self.__num_subwindows__ < 2:
            print("MDI_Vert_Handler called MDI_Tile_Handler")
            self.mdi_tile_handler()
        else:
            print("MDI_Vert_Handler passed")

    # TODO: Remove prints in this function after debugging
    # TODO: Model this after mdi_cascade_handler
    # Horizontally lays out the SubWindows in the MDI Dock
    def mdi_horiz_handler(self):
        print("MDI_Horiz_Handler called")

    # TODO: Remove prints in this function after debugging
    # TODO: Model this after mdi_cascade_handler
    # Sets SubWindows to a default layout in the MDI Dock?
    def mdi_main_handler(self):
        print("MDI_Main_Handler called")

    # TODO: invariant must be unique device names. Figure out how to enforce this constraint
    # Adds a new unique pair of RS Device box and RS SubWindow to the UI
    def add_rs_device_handler(self):
        self.add_rs_device_box()
        self.add_rs_device_subwindow()

    # Removes an existing specific pair of RS Device box and RS Subwindow from the UI
    def remove_rs_device_handler(self):
        self.remove_rs_device_box()
        self.remove_rs_device_subwindow()

    # Generates a new RS Device box, adds it to a collection and then displays it.
    def add_rs_device_box(self):
        name = self.block_note_text_box.toPlainText()
        if name:
            self.__list_of_devices__[name] = DeviceBox(name, self.rs_devices_scroll_area_contents)
            self.rs_devices_scroll_area_contents_vert_layout.addWidget(self.__list_of_devices__[name])

    # Removes a specific RS Device box from the UI
    def remove_rs_device_box(self):
        name = self.block_note_text_box.toPlainText()
        if name in self.__list_of_devices__ and self.__list_of_devices__[name]:
            self.rs_devices_scroll_area_contents_vert_layout.removeWidget(self.__list_of_devices__[name])
            self.__list_of_devices__[name].deleteLater()
            del self.__list_of_devices__[name]

    # Generates a new RS SubWindow, adds it to a collection and then displays it.
    def add_rs_device_subwindow(self):
        # TODO: Remove prints in this function after debugging
        print("SubWindow Add called")
        name = self.block_note_text_box.toPlainText()
        if name:
            self.__num_subwindows__ += 1
            print("Num subs =", self.__num_subwindows__)
            sub = SubWindow(name, None)
            self.mdi_dock_area.addSubWindow(sub)
            self.__list_of_subwindows__[name] = sub
            sub.show()


    # TODO: Remove prints in this function after debugging
    def remove_rs_device_subwindow(self):
        print("SubWindow Remove called")
        name = self.block_note_text_box.toPlainText()
        if name in self.__list_of_subwindows__ and self.__list_of_subwindows__[name]:
            self.__num_subwindows__ -= 1
            print("Num subs =", self.__num_subwindows__)
            self.mdi_dock_area.removeSubWindow(self.__list_of_subwindows__[name])
            self.__list_of_subwindows__[name].deleteLater()
            del self.__list_of_subwindows__[name]


class DeviceBox(QtWidgets.QGroupBox):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.setObjectName(name)
        self.device_group_box_horiz_layout = QtWidgets.QHBoxLayout(self)
        self.device_group_box_horiz_layout.setObjectName("device_group_box_horiz_layout")
        self.setup_push_button = QtWidgets.QPushButton(self)
        self.setup_push_button.setObjectName("setup_push_button")
        self.device_group_box_horiz_layout.addWidget(self.setup_push_button)
        self.device_tool_button = QtWidgets.QToolButton(self)
        self.device_tool_button.setObjectName("device_tool_button")
        self.device_group_box_horiz_layout.addWidget(self.device_tool_button)
        self.set_texts(name)
        self.setup_button_handlers()

    def set_texts(self, name):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", name))
        self.setup_push_button.setText(_translate("MainWindow", "Setup"))
        self.device_tool_button.setText(_translate("MainWindow", "..."))

    def setup_button_handlers(self):
        self.device_tool_button.clicked.connect(self.device_tool_button_handler)
        self.setup_push_button.clicked.connect(self.setup_push_button_handler)

    # TODO: Figure out how to pass useful information from this handler and make it do useful things
    def device_tool_button_handler(self):
        print("Device Button Handler pressed for", self.objectName())

    # TODO: Figure out how to pass useful information from this handler and make it do useful things
    def setup_push_button_handler(self):
        print("Setup Button Handler pressed for", self.objectName())


# TODO: Create other subwindow versions based on device?
class SubWindow(QtWidgets.QMdiSubWindow):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.setObjectName(name)
        self.setWindowTitle(name)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget_horiz_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.central_widget_horiz_layout.setObjectName("central_widget_horiz_layout")
        self.central_widget_graphics_view = QtWidgets.QGraphicsView(self.central_widget)
        self.central_widget_graphics_view.setObjectName("central_widget_graphics_view")
        self.central_widget_horiz_layout.addWidget(self.central_widget_graphics_view)
        self.central_widget_frame = QtWidgets.QFrame(self.central_widget)
        self.central_widget_frame.setMinimumSize(QtCore.QSize(0, 265))
        self.central_widget_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.central_widget_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.central_widget_frame.setObjectName("central_widget_frame")
        self.central_widget_vert_layout = QtWidgets.QVBoxLayout(self.central_widget_frame)
        self.central_widget_vert_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget_vert_layout.setObjectName("central_widget_vert_layout")
        self.central_widget_horiz_layout.addWidget(self.central_widget_frame)
        self.central_widget_scroll_area = QtWidgets.QScrollArea(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.central_widget_scroll_area.sizePolicy().hasHeightForWidth())
        self.central_widget_scroll_area.setSizePolicy(size_policy)
        self.central_widget_scroll_area.setMinimumSize(QtCore.QSize(150, 0))
        self.central_widget_scroll_area.setWidgetResizable(True)
        self.central_widget_scroll_area.setObjectName("central_widget_scroll_area")
        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 148, 296))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.scroll_area_contents_vert_layout = QtWidgets.QVBoxLayout(self.scroll_area_contents)
        self.scroll_area_contents_vert_layout.setObjectName("scroll_area_contents_vert_layout")
        self.scroll_area_contents_group_box_1 = QtWidgets.QGroupBox(self.scroll_area_contents)
        self.scroll_area_contents_group_box_1.setMinimumSize(QtCore.QSize(0, 175))
        self.scroll_area_contents_group_box_1.setObjectName("scroll_area_contents_group_box")
        self.group_box_1_vert_layout = QtWidgets.QVBoxLayout(self.scroll_area_contents_group_box_1)
        self.group_box_1_vert_layout.setContentsMargins(9, 9, 9, 9)
        self.group_box_1_vert_layout.setSpacing(9)
        self.group_box_1_vert_layout.setObjectName("group_box_1_vert_layout")
        self.group_box_1_push_button_1 = QtWidgets.QPushButton(self.scroll_area_contents_group_box_1)
        self.group_box_1_push_button_1.setObjectName("group_box_1_push_button_1")
        self.group_box_1_vert_layout.addWidget(self.group_box_1_push_button_1)
        self.group_box_1_push_button_2 = QtWidgets.QPushButton(self.scroll_area_contents_group_box_1)
        self.group_box_1_push_button_2.setObjectName("group_box_1_push_button_2")
        self.group_box_1_vert_layout.addWidget(self.group_box_1_push_button_2)
        self.group_box_1_check_box_1 = QtWidgets.QCheckBox(self.scroll_area_contents_group_box_1)
        self.group_box_1_check_box_1.setObjectName("group_box_1_check_box_1")
        self.group_box_1_vert_layout.addWidget(self.group_box_1_check_box_1)
        self.group_box_1_check_box_2 = QtWidgets.QCheckBox(self.scroll_area_contents_group_box_1)
        self.group_box_1_check_box_2.setObjectName("group_box_1_check_box_2")
        self.group_box_1_vert_layout.addWidget(self.group_box_1_check_box_2)
        self.group_box_1_check_box_3 = QtWidgets.QCheckBox(self.scroll_area_contents_group_box_1)
        self.group_box_1_check_box_3.setObjectName("group_box_1_check_box_3")
        self.group_box_1_vert_layout.addWidget(self.group_box_1_check_box_3)
        self.scroll_area_contents_vert_layout.addWidget(self.scroll_area_contents_group_box_1)
        spacer_item = QtWidgets.QSpacerItem(20, 97, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scroll_area_contents_vert_layout.addItem(spacer_item)
        self.group_box_2 = QtWidgets.QGroupBox(self.scroll_area_contents)
        self.group_box_2.setMinimumSize(QtCore.QSize(100, 0))
        self.group_box_2.setObjectName("group_box_2")
        self.group_box_2_vert_layout = QtWidgets.QVBoxLayout(self.group_box_2)
        self.group_box_2_vert_layout.setObjectName("group_box_2_vert_layout")
        self.group_box_2_push_button_1 = QtWidgets.QPushButton(self.group_box_2)
        self.group_box_2_push_button_1.setObjectName("group_box_2_push_button_1")
        self.group_box_2_vert_layout.addWidget(self.group_box_2_push_button_1)
        self.group_box_2_push_button_2 = QtWidgets.QPushButton(self.group_box_2)
        self.group_box_2_push_button_2.setObjectName("group_box_2_push_button_2")
        self.group_box_2_vert_layout.addWidget(self.group_box_2_push_button_2)
        self.scroll_area_contents_vert_layout.addWidget(self.group_box_2)
        self.central_widget_scroll_area.setWidget(self.scroll_area_contents)
        self.central_widget_horiz_layout.addWidget(self.central_widget_scroll_area)
        self.setWidget(self.central_widget)
        self.set_texts(name)

    def set_texts(self, name):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", name))
        self.scroll_area_contents_group_box_1.setTitle(_translate("MainWindow", "CHANGEME_group_box_1"))
        self.group_box_1_push_button_1.setText(_translate("MainWindow", "CHANGEME_push_button_1"))
        self.group_box_1_push_button_2.setText(_translate("MainWindow", "CHANGEME_push_button_2"))
        self.group_box_1_check_box_1.setText(_translate("MainWindow", "CHANGEME_check_box_1"))
        self.group_box_1_check_box_2.setText(_translate("MainWindow", "CHANGEME_check_box_2"))
        self.group_box_1_check_box_3.setText(_translate("MainWindow", "CHANGEME_check_box_3"))
        self.group_box_2.setTitle(_translate("MainWindow", "CHANGEME_group_box_2"))
        self.group_box_2_push_button_1.setText(_translate("MainWindow", "CHANGEME_push_button_1"))
        self.group_box_2_push_button_2.setText(_translate("MainWindow", "CHANGEME_push_button_2"))