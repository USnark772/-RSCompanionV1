# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'companion_main_window_take2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1009, 753)
        MainWindow.setMinimumSize(QtCore.QSize(840, 468))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.Central_Widget = QtWidgets.QWidget(MainWindow)
        self.Central_Widget.setObjectName("Central_Widget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.Central_Widget)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.Central_Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.tabWidget = QtWidgets.QTabWidget(self.Central_Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_3)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 111, 521))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 109, 519))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.Device_GroupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.Device_GroupBox_2.setGeometry(QtCore.QRect(0, 0, 101, 101))
        self.Device_GroupBox_2.setObjectName("Device_GroupBox_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.Device_GroupBox_2)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.Setup_PushButton_2 = QtWidgets.QPushButton(self.Device_GroupBox_2)
        self.Setup_PushButton_2.setObjectName("Setup_PushButton_2")
        self.verticalLayout_5.addWidget(self.Setup_PushButton_2)
        self.Setup_PushButton_3 = QtWidgets.QPushButton(self.Device_GroupBox_2)
        self.Setup_PushButton_3.setObjectName("Setup_PushButton_3")
        self.verticalLayout_5.addWidget(self.Setup_PushButton_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Device_ToolButton_2 = QtWidgets.QToolButton(self.Device_GroupBox_2)
        self.Device_ToolButton_2.setObjectName("Device_ToolButton_2")
        self.horizontalLayout_3.addWidget(self.Device_ToolButton_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_9.addLayout(self.verticalLayout_5)
        self.Device_GroupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.Device_GroupBox_3.setGeometry(QtCore.QRect(0, 100, 101, 101))
        self.Device_GroupBox_3.setObjectName("Device_GroupBox_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.Device_GroupBox_3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.Setup_PushButton_4 = QtWidgets.QPushButton(self.Device_GroupBox_3)
        self.Setup_PushButton_4.setObjectName("Setup_PushButton_4")
        self.verticalLayout_7.addWidget(self.Setup_PushButton_4)
        self.Setup_PushButton_5 = QtWidgets.QPushButton(self.Device_GroupBox_3)
        self.Setup_PushButton_5.setObjectName("Setup_PushButton_5")
        self.verticalLayout_7.addWidget(self.Setup_PushButton_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.Device_ToolButton_3 = QtWidgets.QToolButton(self.Device_GroupBox_3)
        self.Device_ToolButton_3.setObjectName("Device_ToolButton_3")
        self.horizontalLayout_6.addWidget(self.Device_ToolButton_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_10.addLayout(self.verticalLayout_7)
        self.Device_GroupBox_4 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.Device_GroupBox_4.setGeometry(QtCore.QRect(0, 200, 101, 101))
        self.Device_GroupBox_4.setObjectName("Device_GroupBox_4")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.Device_GroupBox_4)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.Setup_PushButton_6 = QtWidgets.QPushButton(self.Device_GroupBox_4)
        self.Setup_PushButton_6.setObjectName("Setup_PushButton_6")
        self.verticalLayout_8.addWidget(self.Setup_PushButton_6)
        self.Setup_PushButton_7 = QtWidgets.QPushButton(self.Device_GroupBox_4)
        self.Setup_PushButton_7.setObjectName("Setup_PushButton_7")
        self.verticalLayout_8.addWidget(self.Setup_PushButton_7)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.Device_ToolButton_4 = QtWidgets.QToolButton(self.Device_GroupBox_4)
        self.Device_ToolButton_4.setObjectName("Device_ToolButton_4")
        self.horizontalLayout_7.addWidget(self.Device_ToolButton_4)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_11.addLayout(self.verticalLayout_8)
        self.ThisIsMyPushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.ThisIsMyPushButton.setGeometry(QtCore.QRect(20, 310, 56, 17))
        self.ThisIsMyPushButton.setObjectName("ThisIsMyPushButton")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout_9.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.Central_Widget)
        self.MenuBar = QtWidgets.QMenuBar(MainWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 1009, 18))
        self.MenuBar.setObjectName("MenuBar")
        self.File_Menu = QtWidgets.QMenu(self.MenuBar)
        self.File_Menu.setObjectName("File_Menu")
        self.Window_Menu = QtWidgets.QMenu(self.MenuBar)
        self.Window_Menu.setObjectName("Window_Menu")
        self.Help_Menu = QtWidgets.QMenu(self.MenuBar)
        self.Help_Menu.setObjectName("Help_Menu")
        self.Settings_Menu = QtWidgets.QMenu(self.MenuBar)
        self.Settings_Menu.setObjectName("Settings_Menu")
        self.menuUDP_Controls = QtWidgets.QMenu(self.Settings_Menu)
        self.menuUDP_Controls.setObjectName("menuUDP_Controls")
        MainWindow.setMenuBar(self.MenuBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Control_Window_Dock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Control_Window_Dock.sizePolicy().hasHeightForWidth())
        self.Control_Window_Dock.setSizePolicy(sizePolicy)
        self.Control_Window_Dock.setMinimumSize(QtCore.QSize(500, 150))
        self.Control_Window_Dock.setMaximumSize(QtCore.QSize(150000, 150))
        self.Control_Window_Dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable|QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.Control_Window_Dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.Control_Window_Dock.setObjectName("Control_Window_Dock")
        self.Control_Window_Dock_Contents = QtWidgets.QWidget()
        self.Control_Window_Dock_Contents.setObjectName("Control_Window_Dock_Contents")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.Control_Window_Dock_Contents)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Run_New_GroupBox = QtWidgets.QGroupBox(self.Control_Window_Dock_Contents)
        self.Run_New_GroupBox.setTitle("")
        self.Run_New_GroupBox.setObjectName("Run_New_GroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Run_New_GroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Run_Trial_PushButton = QtWidgets.QPushButton(self.Run_New_GroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Run_Trial_PushButton.sizePolicy().hasHeightForWidth())
        self.Run_Trial_PushButton.setSizePolicy(sizePolicy)
        self.Run_Trial_PushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.Run_Trial_PushButton.setObjectName("Run_Trial_PushButton")
        self.verticalLayout.addWidget(self.Run_Trial_PushButton)
        self.New_Block_PushButton = QtWidgets.QPushButton(self.Run_New_GroupBox)
        self.New_Block_PushButton.setObjectName("New_Block_PushButton")
        self.verticalLayout.addWidget(self.New_Block_PushButton)
        self.horizontalLayout_4.addWidget(self.Run_New_GroupBox)
        self.Key_Flag_GroupBox = QtWidgets.QGroupBox(self.Control_Window_Dock_Contents)
        self.Key_Flag_GroupBox.setObjectName("Key_Flag_GroupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.Key_Flag_GroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Key_Flag_Label = QtWidgets.QLabel(self.Key_Flag_GroupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Key_Flag_Label.setFont(font)
        self.Key_Flag_Label.setObjectName("Key_Flag_Label")
        self.verticalLayout_6.addWidget(self.Key_Flag_Label, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_4.addWidget(self.Key_Flag_GroupBox)
        self.Block_Note_GroupBox = QtWidgets.QGroupBox(self.Control_Window_Dock_Contents)
        self.Block_Note_GroupBox.setObjectName("Block_Note_GroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Block_Note_GroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Block_Note_TextBox = QtWidgets.QTextEdit(self.Block_Note_GroupBox)
        self.Block_Note_TextBox.setObjectName("Block_Note_TextBox")
        self.gridLayout_2.addWidget(self.Block_Note_TextBox, 0, 1, 1, 1)
        self.Post_PushButton = QtWidgets.QPushButton(self.Block_Note_GroupBox)
        self.Post_PushButton.setObjectName("Post_PushButton")
        self.gridLayout_2.addWidget(self.Post_PushButton, 1, 1, 1, 1)
        self.horizontalLayout_4.addWidget(self.Block_Note_GroupBox)
        self.Trial_Block_Frame = QtWidgets.QFrame(self.Control_Window_Dock_Contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Trial_Block_Frame.sizePolicy().hasHeightForWidth())
        self.Trial_Block_Frame.setSizePolicy(sizePolicy)
        self.Trial_Block_Frame.setMinimumSize(QtCore.QSize(130, 0))
        self.Trial_Block_Frame.setObjectName("Trial_Block_Frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Trial_Block_Frame)
        self.gridLayout_3.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Trial_Block_Labels_Frame = QtWidgets.QFrame(self.Trial_Block_Frame)
        self.Trial_Block_Labels_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Trial_Block_Labels_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Trial_Block_Labels_Frame.setObjectName("Trial_Block_Labels_Frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Trial_Block_Labels_Frame)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Trial_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Trial_Label.setObjectName("Trial_Label")
        self.verticalLayout_2.addWidget(self.Trial_Label)
        self.Trial_Num_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Trial_Num_Label.setObjectName("Trial_Num_Label")
        self.verticalLayout_2.addWidget(self.Trial_Num_Label)
        self.Trial_Time_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Trial_Time_Label.setObjectName("Trial_Time_Label")
        self.verticalLayout_2.addWidget(self.Trial_Time_Label)
        self.Block_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Block_Label.setObjectName("Block_Label")
        self.verticalLayout_2.addWidget(self.Block_Label)
        self.Block_Num_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Block_Num_Label.setObjectName("Block_Num_Label")
        self.verticalLayout_2.addWidget(self.Block_Num_Label)
        self.Block_Time_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Block_Time_Label.setObjectName("Block_Time_Label")
        self.verticalLayout_2.addWidget(self.Block_Time_Label)
        self.gridLayout_3.addWidget(self.Trial_Block_Labels_Frame, 0, 0, 1, 1)
        self.Trial_Block_Values_Frame = QtWidgets.QFrame(self.Trial_Block_Frame)
        self.Trial_Block_Values_Frame.setMinimumSize(QtCore.QSize(50, 0))
        self.Trial_Block_Values_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Trial_Block_Values_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Trial_Block_Values_Frame.setObjectName("Trial_Block_Values_Frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Trial_Block_Values_Frame)
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Trial_Block_Spacer_1 = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Trial_Block_Spacer_1.setFont(font)
        self.Trial_Block_Spacer_1.setText("")
        self.Trial_Block_Spacer_1.setObjectName("Trial_Block_Spacer_1")
        self.verticalLayout_4.addWidget(self.Trial_Block_Spacer_1)
        self.Trial_Num_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Trial_Num_Val_Label.setObjectName("Trial_Num_Val_Label")
        self.verticalLayout_4.addWidget(self.Trial_Num_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Trial_Time_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Trial_Time_Val_Label.setFont(font)
        self.Trial_Time_Val_Label.setObjectName("Trial_Time_Val_Label")
        self.verticalLayout_4.addWidget(self.Trial_Time_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Trial_Block_Spacer_2 = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Trial_Block_Spacer_2.setText("")
        self.Trial_Block_Spacer_2.setObjectName("Trial_Block_Spacer_2")
        self.verticalLayout_4.addWidget(self.Trial_Block_Spacer_2)
        self.Block_Num_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Block_Num_Val_Label.setObjectName("Block_Num_Val_Label")
        self.verticalLayout_4.addWidget(self.Block_Num_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Block_Time_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Block_Time_Val_Label.setObjectName("Block_Time_Val_Label")
        self.verticalLayout_4.addWidget(self.Block_Time_Val_Label, 0, QtCore.Qt.AlignRight)
        self.gridLayout_3.addWidget(self.Trial_Block_Values_Frame, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        self.horizontalLayout_4.addWidget(self.Trial_Block_Frame)
        self.Control_Window_Dock.setWidget(self.Control_Window_Dock_Contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.Control_Window_Dock)
        self.Begin_Experiment_Action = QtWidgets.QAction(MainWindow)
        self.Begin_Experiment_Action.setObjectName("Begin_Experiment_Action")
        self.COM_Messages_Action = QtWidgets.QAction(MainWindow)
        self.COM_Messages_Action.setCheckable(True)
        self.COM_Messages_Action.setObjectName("COM_Messages_Action")
        self.actionParameters = QtWidgets.QAction(MainWindow)
        self.actionParameters.setCheckable(True)
        self.actionParameters.setObjectName("actionParameters")
        self.actionLive_Data = QtWidgets.QAction(MainWindow)
        self.actionLive_Data.setCheckable(True)
        self.actionLive_Data.setObjectName("actionLive_Data")
        self.actionConfigure_Data_Buddy = QtWidgets.QAction(MainWindow)
        self.actionConfigure_Data_Buddy.setObjectName("actionConfigure_Data_Buddy")
        self.About_RS_Companion_Action = QtWidgets.QAction(MainWindow)
        self.About_RS_Companion_Action.setObjectName("About_RS_Companion_Action")
        self.About_Red_Scientific_Action = QtWidgets.QAction(MainWindow)
        self.About_Red_Scientific_Action.setObjectName("About_Red_Scientific_Action")
        self.End_Experiment_Action = QtWidgets.QAction(MainWindow)
        self.End_Experiment_Action.setObjectName("End_Experiment_Action")
        self.Trial_Controls_Action = QtWidgets.QAction(MainWindow)
        self.Trial_Controls_Action.setObjectName("Trial_Controls_Action")
        self.actionExit_2 = QtWidgets.QAction(MainWindow)
        self.actionExit_2.setObjectName("actionExit_2")
        self.Display_Tooltips_Action = QtWidgets.QAction(MainWindow)
        self.Display_Tooltips_Action.setObjectName("Display_Tooltips_Action")
        self.Configure_Action = QtWidgets.QAction(MainWindow)
        self.Configure_Action.setObjectName("Configure_Action")
        self.COM_Port_Action = QtWidgets.QAction(MainWindow)
        self.COM_Port_Action.setObjectName("COM_Port_Action")
        self.Output_Action = QtWidgets.QAction(MainWindow)
        self.Output_Action.setObjectName("Output_Action")
        self.Input_Aciton = QtWidgets.QAction(MainWindow)
        self.Input_Aciton.setObjectName("Input_Aciton")
        self.Append_Experiment_Action = QtWidgets.QAction(MainWindow)
        self.Append_Experiment_Action.setObjectName("Append_Experiment_Action")
        self.Open_Action = QtWidgets.QAction(MainWindow)
        self.Open_Action.setObjectName("Open_Action")
        self.File_Menu.addAction(self.Begin_Experiment_Action)
        self.File_Menu.addAction(self.End_Experiment_Action)
        self.File_Menu.addSeparator()
        self.File_Menu.addAction(self.Append_Experiment_Action)
        self.File_Menu.addSeparator()
        self.File_Menu.addAction(self.Open_Action)
        self.Window_Menu.addAction(self.Trial_Controls_Action)
        self.Window_Menu.addAction(self.COM_Messages_Action)
        self.Window_Menu.addAction(self.Configure_Action)
        self.Window_Menu.addSeparator()
        self.Window_Menu.addAction(self.Display_Tooltips_Action)
        self.Window_Menu.addSeparator()
        self.Help_Menu.addAction(self.About_RS_Companion_Action)
        self.Help_Menu.addAction(self.About_Red_Scientific_Action)
        self.menuUDP_Controls.addAction(self.Output_Action)
        self.menuUDP_Controls.addAction(self.Input_Aciton)
        self.Settings_Menu.addAction(self.COM_Port_Action)
        self.Settings_Menu.addAction(self.menuUDP_Controls.menuAction())
        self.MenuBar.addAction(self.File_Menu.menuAction())
        self.MenuBar.addAction(self.Settings_Menu.menuAction())
        self.MenuBar.addAction(self.Window_Menu.menuAction())
        self.MenuBar.addAction(self.Help_Menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RS Device Companion"))
        self.Device_GroupBox_2.setTitle(_translate("MainWindow", "DRT - Wireless 1"))
        self.Setup_PushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.Setup_PushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.Device_ToolButton_2.setText(_translate("MainWindow", "..."))
        self.Device_GroupBox_3.setTitle(_translate("MainWindow", "DRT - Wireless 1"))
        self.Setup_PushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.Setup_PushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.Device_ToolButton_3.setText(_translate("MainWindow", "..."))
        self.Device_GroupBox_4.setTitle(_translate("MainWindow", "DRT - Wireless 1"))
        self.Setup_PushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.Setup_PushButton_7.setText(_translate("MainWindow", "PushButton"))
        self.Device_ToolButton_4.setText(_translate("MainWindow", "..."))
        self.ThisIsMyPushButton.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Tab 2"))
        self.File_Menu.setTitle(_translate("MainWindow", "File"))
        self.Window_Menu.setTitle(_translate("MainWindow", "Window"))
        self.Help_Menu.setTitle(_translate("MainWindow", "Help"))
        self.Settings_Menu.setTitle(_translate("MainWindow", "Settings"))
        self.menuUDP_Controls.setTitle(_translate("MainWindow", "UDP Controls"))
        self.Control_Window_Dock.setWindowTitle(_translate("MainWindow", "Control"))
        self.Run_Trial_PushButton.setText(_translate("MainWindow", "Run\n"
"Trial"))
        self.New_Block_PushButton.setText(_translate("MainWindow", "New Block"))
        self.Key_Flag_GroupBox.setTitle(_translate("MainWindow", "Key Flag"))
        self.Key_Flag_Label.setText(_translate("MainWindow", "NA"))
        self.Block_Note_GroupBox.setTitle(_translate("MainWindow", "Block Note"))
        self.Post_PushButton.setText(_translate("MainWindow", "Post"))
        self.Trial_Label.setText(_translate("MainWindow", "Trial"))
        self.Trial_Num_Label.setText(_translate("MainWindow", "    Number:"))
        self.Trial_Time_Label.setText(_translate("MainWindow", "    Time:"))
        self.Block_Label.setText(_translate("MainWindow", "Block"))
        self.Block_Num_Label.setText(_translate("MainWindow", "    Number:"))
        self.Block_Time_Label.setText(_translate("MainWindow", "    Time:"))
        self.Trial_Num_Val_Label.setText(_translate("MainWindow", "NA"))
        self.Trial_Time_Val_Label.setText(_translate("MainWindow", "NA"))
        self.Block_Num_Val_Label.setText(_translate("MainWindow", "NA"))
        self.Block_Time_Val_Label.setText(_translate("MainWindow", "NA"))
        self.Begin_Experiment_Action.setText(_translate("MainWindow", "Begin Experiment"))
        self.Begin_Experiment_Action.setToolTip(_translate("MainWindow", "Begin Experiment"))
        self.COM_Messages_Action.setText(_translate("MainWindow", "COM Messages"))
        self.actionParameters.setText(_translate("MainWindow", "Parameters"))
        self.actionLive_Data.setText(_translate("MainWindow", "Live Data"))
        self.actionConfigure_Data_Buddy.setText(_translate("MainWindow", "Configure Data Buddy"))
        self.About_RS_Companion_Action.setText(_translate("MainWindow", "About RS Companion"))
        self.About_Red_Scientific_Action.setText(_translate("MainWindow", "About Red Scientific"))
        self.End_Experiment_Action.setText(_translate("MainWindow", "End Experiment"))
        self.Trial_Controls_Action.setText(_translate("MainWindow", "Trial Controls"))
        self.actionExit_2.setText(_translate("MainWindow", "Exit"))
        self.Display_Tooltips_Action.setText(_translate("MainWindow", "Display Tooltips"))
        self.Configure_Action.setText(_translate("MainWindow", "Configure"))
        self.COM_Port_Action.setText(_translate("MainWindow", "COM Port"))
        self.Output_Action.setText(_translate("MainWindow", "Output"))
        self.Input_Aciton.setText(_translate("MainWindow", "Input"))
        self.Append_Experiment_Action.setText(_translate("MainWindow", "Append Experiment"))
        self.Open_Action.setText(_translate("MainWindow", "Open File  Folder"))

