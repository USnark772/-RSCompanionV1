# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific

from PyQt5 import QtCore, QtGui, QtWidgets

class Companion_Window(object):
    # To keep track of the different devices for Device Box and SubWindow purposes
    ListOfDevices = {}
    ListOfSubWindows = {}
    NumSubWindows = 0
    # Auto generated code slightly altered for readability
    def __init__(self, MainWindow):
        # Begin MainWindow generation code
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 705)
        MainWindow.setMinimumSize(QtCore.QSize(840, 468))
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        # End MainWindow generation code
        ################################################################################################################
        # Begin Central_Widget generation code
        self.Central_Widget = QtWidgets.QWidget(MainWindow)
        self.Central_Widget.setObjectName("Central_Widget")
        self.Central_Widget_Vert_Layout = QtWidgets.QVBoxLayout(self.Central_Widget)
        self.Central_Widget_Vert_Layout.setObjectName("Central_Widget_Vert_Layout")
        self.Central_Widget_Separator_Line = QtWidgets.QFrame(self.Central_Widget)
        self.Central_Widget_Separator_Line.setFrameShape(QtWidgets.QFrame.HLine)
        self.Central_Widget_Separator_Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Central_Widget_Separator_Line.setObjectName("Central_Widget_Separator_Line")
        self.Central_Widget_Vert_Layout.addWidget(self.Central_Widget_Separator_Line)
        MainWindow.setCentralWidget(self.Central_Widget)
        # End Central Widget generation code
        ################################################################################################################
        # Begin MDI Dock generation code
        self.MDI_Dock_Frame = QtWidgets.QFrame(self.Central_Widget)
        self.MDI_Dock_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MDI_Dock_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MDI_Dock_Frame.setObjectName("MDI_Dock_Frame")
        self.MDI_Dock_Frame_Horiz_Layout = QtWidgets.QHBoxLayout(self.MDI_Dock_Frame)
        self.MDI_Dock_Frame_Horiz_Layout.setContentsMargins(0, 0, 0, 0)
        self.MDI_Dock_Frame_Horiz_Layout.setObjectName("MDI_Dock_Frame_Horiz_Layout")
        self.MDI_Dock_Area = QtWidgets.QMdiArea(self.MDI_Dock_Frame)
        self.MDI_Dock_Area.setObjectName("MDI_Dock_Area")
        self.MDI_Dock_Frame_Horiz_Layout.addWidget(self.MDI_Dock_Area)
        self.Central_Widget_Vert_Layout.addWidget(self.MDI_Dock_Frame)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
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
        self.MenuBar = QtWidgets.QMenuBar(MainWindow)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 840, 22))
        self.MenuBar.setObjectName("MenuBar")
        self.File_Menu = QtWidgets.QMenu(self.MenuBar)
        self.File_Menu.setObjectName("File_Menu")
        self.Window_Menu = QtWidgets.QMenu(self.MenuBar)
        self.Window_Menu.setObjectName("Window_Menu")
        self.Help_Menu = QtWidgets.QMenu(self.MenuBar)
        self.Help_Menu.setObjectName("Help_Menu")
        self.Settings_Menu = QtWidgets.QMenu(self.MenuBar)
        self.Settings_Menu.setObjectName("Settings_Menu")
        self.UDP_Controls_Menu = QtWidgets.QMenu(self.Settings_Menu)
        self.UDP_Controls_Menu.setObjectName("menuUDP_Controls")
        MainWindow.setMenuBar(self.MenuBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # End MenuBar generation code
        ################################################################################################################
        # Begin Control Widget generation code
        self.Control_Widget_Dock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Control_Widget_Dock.sizePolicy().hasHeightForWidth())
        self.Control_Widget_Dock.setSizePolicy(sizePolicy)
        self.Control_Widget_Dock.setMinimumSize(QtCore.QSize(500, 150))
        self.Control_Widget_Dock.setMaximumSize(QtCore.QSize(650, 150))
        self.Control_Widget_Dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.Control_Widget_Dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.Control_Widget_Dock.setObjectName("Control_Window_Dock")
        self.Control_Widget_Dock_Contents = QtWidgets.QWidget()
        self.Control_Widget_Dock_Contents.setObjectName("Control_Window_Dock_Contents")
        self.Control_Widget_Horiz_Layout = QtWidgets.QHBoxLayout(self.Control_Widget_Dock_Contents)
        self.Control_Widget_Horiz_Layout.setObjectName("Control_Widget_Horiz_Layout")
        self.Control_Widget_Dock.setWidget(self.Control_Widget_Dock_Contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.Control_Widget_Dock)
        # End Control Widget generation code
        ################################################################################################################
        # Begin Control Widget Run/New group box generation code
        self.Run_New_GroupBox = QtWidgets.QGroupBox(self.Control_Widget_Dock_Contents)
        self.Run_New_GroupBox.setTitle("")
        self.Run_New_GroupBox.setObjectName("Run_New_GroupBox")
        self.Run_New_GroupBox_Vert_Layout = QtWidgets.QVBoxLayout(self.Run_New_GroupBox)
        self.Run_New_GroupBox_Vert_Layout.setObjectName("Run_New_GroupBox_Vert_Layout")
        self.Run_Trial_PushButton = QtWidgets.QPushButton(self.Run_New_GroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Run_Trial_PushButton.sizePolicy().hasHeightForWidth())
        self.Run_Trial_PushButton.setSizePolicy(sizePolicy)
        self.Run_Trial_PushButton.setMinimumSize(QtCore.QSize(0, 0))
        self.Run_Trial_PushButton.setObjectName("Run_Trial_PushButton")
        self.Run_New_GroupBox_Vert_Layout.addWidget(self.Run_Trial_PushButton)
        self.New_Block_PushButton = QtWidgets.QPushButton(self.Run_New_GroupBox)
        self.New_Block_PushButton.setObjectName("New_Block_PushButton")
        self.Run_New_GroupBox_Vert_Layout.addWidget(self.New_Block_PushButton)
        self.Control_Widget_Horiz_Layout.addWidget(self.Run_New_GroupBox)
        # End Control Widget Run/New group box generation code
        ################################################################################################################
        # Begin KeyFlag group box generation code
        self.Key_Flag_GroupBox = QtWidgets.QGroupBox(self.Control_Widget_Dock_Contents)
        self.Key_Flag_GroupBox.setObjectName("Key_Flag_GroupBox")
        self.Key_Flag_Vert_Layout = QtWidgets.QVBoxLayout(self.Key_Flag_GroupBox)
        self.Key_Flag_Vert_Layout.setObjectName("Key_Flag_Vert_Layout")
        self.Key_Flag_Label = QtWidgets.QLabel(self.Key_Flag_GroupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Key_Flag_Label.setFont(font)
        self.Key_Flag_Label.setObjectName("Key_Flag_Label")
        self.Key_Flag_Vert_Layout.addWidget(self.Key_Flag_Label, 0, QtCore.Qt.AlignHCenter)
        self.Control_Widget_Horiz_Layout.addWidget(self.Key_Flag_GroupBox)
        # End KeyFlag group box generation code
        ################################################################################################################
        # Begin Block Note group box generation code
        self.Block_Note_GroupBox = QtWidgets.QGroupBox(self.Control_Widget_Dock_Contents)
        self.Block_Note_GroupBox.setObjectName("Block_Note_GroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Block_Note_GroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Block_Note_TextBox = QtWidgets.QTextEdit(self.Block_Note_GroupBox)
        self.Block_Note_TextBox.setObjectName("Block_Note_TextBox")
        self.gridLayout_2.addWidget(self.Block_Note_TextBox, 0, 1, 1, 1)
        self.Post_PushButton = QtWidgets.QPushButton(self.Block_Note_GroupBox)
        self.Post_PushButton.setObjectName("Post_PushButton")
        self.gridLayout_2.addWidget(self.Post_PushButton, 1, 1, 1, 1)
        self.Control_Widget_Horiz_Layout.addWidget(self.Block_Note_GroupBox)
        # End Block Note group box generation code
        ################################################################################################################
        # Begin Trial/Block information generation code
        self.Trial_Block_Frame = QtWidgets.QFrame(self.Control_Widget_Dock_Contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Trial_Block_Frame.sizePolicy().hasHeightForWidth())
        self.Trial_Block_Frame.setSizePolicy(sizePolicy)
        self.Trial_Block_Frame.setMinimumSize(QtCore.QSize(130, 0))
        self.Trial_Block_Frame.setObjectName("Trial_Block_Frame")
        self.Trial_Block_Frame_Grid_Layout = QtWidgets.QGridLayout(self.Trial_Block_Frame)
        self.Trial_Block_Frame_Grid_Layout.setContentsMargins(2, 2, 2, 2)
        self.Trial_Block_Frame_Grid_Layout.setObjectName("Trial_Block_Frame_Grid_Layout")
        self.Trial_Block_Labels_Frame = QtWidgets.QFrame(self.Trial_Block_Frame)
        self.Trial_Block_Labels_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Trial_Block_Labels_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Trial_Block_Labels_Frame.setObjectName("Trial_Block_Labels_Frame")
        self.Trial_Block_Labels_Frame_Vert_Layout = QtWidgets.QVBoxLayout(self.Trial_Block_Labels_Frame)
        self.Trial_Block_Labels_Frame_Vert_Layout.setContentsMargins(2, 2, 2, 2)
        self.Trial_Block_Labels_Frame_Vert_Layout.setSpacing(6)
        self.Trial_Block_Labels_Frame_Vert_Layout.setObjectName("Trial_Block_Labels_Frame_Vert_Layout")
        self.Trial_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Trial_Label.setObjectName("Trial_Label")
        self.Trial_Block_Labels_Frame_Vert_Layout.addWidget(self.Trial_Label)
        self.Trial_Num_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Trial_Num_Label.setObjectName("Trial_Num_Label")
        self.Trial_Block_Labels_Frame_Vert_Layout.addWidget(self.Trial_Num_Label)
        self.Trial_Time_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Trial_Time_Label.setObjectName("Trial_Time_Label")
        self.Trial_Block_Labels_Frame_Vert_Layout.addWidget(self.Trial_Time_Label)
        self.Block_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Block_Label.setObjectName("Block_Label")
        self.Trial_Block_Labels_Frame_Vert_Layout.addWidget(self.Block_Label)
        self.Block_Num_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Block_Num_Label.setObjectName("Block_Num_Label")
        self.Trial_Block_Labels_Frame_Vert_Layout.addWidget(self.Block_Num_Label)
        self.Block_Time_Label = QtWidgets.QLabel(self.Trial_Block_Labels_Frame)
        self.Block_Time_Label.setObjectName("Block_Time_Label")
        self.Trial_Block_Labels_Frame_Vert_Layout.addWidget(self.Block_Time_Label)
        self.Trial_Block_Frame_Grid_Layout.addWidget(self.Trial_Block_Labels_Frame, 0, 0, 1, 1)
        self.Trial_Block_Values_Frame = QtWidgets.QFrame(self.Trial_Block_Frame)
        self.Trial_Block_Values_Frame.setMinimumSize(QtCore.QSize(50, 0))
        self.Trial_Block_Values_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Trial_Block_Values_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Trial_Block_Values_Frame.setObjectName("Trial_Block_Values_Frame")
        self.Trial_Block_Values_Frame_Vert_Layout = QtWidgets.QVBoxLayout(self.Trial_Block_Values_Frame)
        self.Trial_Block_Values_Frame_Vert_Layout.setContentsMargins(2, 2, 2, 2)
        self.Trial_Block_Values_Frame_Vert_Layout.setObjectName("Trial_Block_Values_Frame_Vert_Layout")
        self.Trial_Block_Spacer_1 = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Trial_Block_Spacer_1.setFont(font)
        self.Trial_Block_Spacer_1.setText("")
        self.Trial_Block_Spacer_1.setObjectName("Trial_Block_Spacer_1")
        self.Trial_Block_Values_Frame_Vert_Layout.addWidget(self.Trial_Block_Spacer_1)
        self.Trial_Num_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Trial_Num_Val_Label.setObjectName("Trial_Num_Val_Label")
        self.Trial_Block_Values_Frame_Vert_Layout.addWidget(self.Trial_Num_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Trial_Time_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Trial_Time_Val_Label.setFont(font)
        self.Trial_Time_Val_Label.setObjectName("Trial_Time_Val_Label")
        self.Trial_Block_Values_Frame_Vert_Layout.addWidget(self.Trial_Time_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Trial_Block_Spacer_2 = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Trial_Block_Spacer_2.setText("")
        self.Trial_Block_Spacer_2.setObjectName("Trial_Block_Spacer_2")
        self.Trial_Block_Values_Frame_Vert_Layout.addWidget(self.Trial_Block_Spacer_2)
        self.Block_Num_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Block_Num_Val_Label.setObjectName("Block_Num_Val_Label")
        self.Trial_Block_Values_Frame_Vert_Layout.addWidget(self.Block_Num_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Block_Time_Val_Label = QtWidgets.QLabel(self.Trial_Block_Values_Frame)
        self.Block_Time_Val_Label.setObjectName("Block_Time_Val_Label")
        self.Trial_Block_Values_Frame_Vert_Layout.addWidget(self.Block_Time_Val_Label, 0, QtCore.Qt.AlignRight)
        self.Trial_Block_Frame_Grid_Layout.addWidget(self.Trial_Block_Values_Frame, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        self.Control_Widget_Horiz_Layout.addWidget(self.Trial_Block_Frame)
        # End Trial/Block information generation code
        ################################################################################################################
        # Begin COM Widget generation code
        self.COM_Widget_Dock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.COM_Widget_Dock.sizePolicy().hasHeightForWidth())
        self.COM_Widget_Dock.setSizePolicy(sizePolicy)
        self.COM_Widget_Dock.setMinimumSize(QtCore.QSize(374, 130))
        self.COM_Widget_Dock.setMaximumSize(QtCore.QSize(524287, 130))
        self.COM_Widget_Dock.setBaseSize(QtCore.QSize(0, 0))
        self.COM_Widget_Dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.COM_Widget_Dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.COM_Widget_Dock.setObjectName("COM_Widget_Dock")
        self.COM_Wdget_Contents = QtWidgets.QWidget()
        self.COM_Wdget_Contents.setObjectName("COM_Wdget_Contents")
        self.COM_Widget_Dock.setWidget(self.COM_Wdget_Contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.COM_Widget_Dock)
        self.gridLayout = QtWidgets.QGridLayout(self.COM_Wdget_Contents)
        self.gridLayout.setObjectName("gridLayout")
        self.Record_PushButton = QtWidgets.QPushButton(self.COM_Wdget_Contents)
        self.Record_PushButton.setObjectName("Record_PushButton")
        self.gridLayout.addWidget(self.Record_PushButton, 1, 0, 1, 1)
        self.Freeze_PushButton = QtWidgets.QPushButton(self.COM_Wdget_Contents)
        self.Freeze_PushButton.setObjectName("Freeze_PushButton")
        self.gridLayout.addWidget(self.Freeze_PushButton, 1, 2, 1, 1)
        self.Clear_PushButton = QtWidgets.QPushButton(self.COM_Wdget_Contents)
        self.Clear_PushButton.setObjectName("Clear_PushButton")
        self.gridLayout.addWidget(self.Clear_PushButton, 1, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.CHANGEME_CheckBox = QtWidgets.QCheckBox(self.COM_Wdget_Contents)
        self.CHANGEME_CheckBox.setObjectName("CHANGEME_CheckBox")
        self.gridLayout.addWidget(self.CHANGEME_CheckBox, 1, 5, 1, 1)
        self.COM_TextBox = QtWidgets.QPlainTextEdit(self.COM_Wdget_Contents)
        self.COM_TextBox.setMinimumSize(QtCore.QSize(0, 0))
        self.COM_TextBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.COM_TextBox.setBaseSize(QtCore.QSize(0, 0))
        self.COM_TextBox.setObjectName("COM_TextBox")
        self.gridLayout.addWidget(self.COM_TextBox, 0, 0, 1, 6)
        # End COM Widget generation code
        ################################################################################################################
        # Begin Configure Widget generation code
        self.Configure_Widget_Dock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Configure_Widget_Dock.sizePolicy().hasHeightForWidth())
        self.Configure_Widget_Dock.setSizePolicy(sizePolicy)
        self.Configure_Widget_Dock.setMinimumSize(QtCore.QSize(350, 150))
        self.Configure_Widget_Dock.setMaximumSize(QtCore.QSize(450, 150))
        self.Configure_Widget_Dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable|QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.Configure_Widget_Dock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.Configure_Widget_Dock.setObjectName("Configure_Widget_Dock")
        self.Configure_Widget_Contents = QtWidgets.QWidget()
        self.Configure_Widget_Contents.setObjectName("Configure_Widget_Contents")
        self.Configure_Widget_Contents_Horiz_Layout = QtWidgets.QHBoxLayout(self.Configure_Widget_Contents)
        self.Configure_Widget_Contents_Horiz_Layout.setObjectName("Configure_Widget_Contents_Horiz_Layout")
        self.RS_Devices_GroupBox = QtWidgets.QGroupBox(self.Configure_Widget_Contents)
        self.RS_Devices_GroupBox.setObjectName("RS_Devices_GroupBox")
        self.RS_Devices_GroupBox_Horiz_Layout = QtWidgets.QHBoxLayout(self.RS_Devices_GroupBox)
        self.RS_Devices_GroupBox_Horiz_Layout.setObjectName("RS_Devices_GroupBox_Horiz_Layout")
        self.RS_Devices_ScrollArea = QtWidgets.QScrollArea(self.RS_Devices_GroupBox)
        self.Configure_Widget_Contents_Horiz_Layout.addWidget(self.RS_Devices_GroupBox)
        self.RS_Devices_ScrollArea.setWidgetResizable(True)
        self.RS_Devices_ScrollArea.setObjectName("RS_Devices_ScrollArea")
        self.RS_Devices_ScrollArea_Contents = QtWidgets.QWidget()
        self.RS_Devices_ScrollArea_Contents.setGeometry(QtCore.QRect(0, 0, 179, 94))
        self.RS_Devices_ScrollArea_Contents.setObjectName("RS_Devices_ScrollArea_Contents")
        self.RS_Devices_ScrollArea.setWidget(self.RS_Devices_ScrollArea_Contents)
        self.RS_Devices_GroupBox_Horiz_Layout.addWidget(self.RS_Devices_ScrollArea)
        self.RS_Devices_ScrollArea_Contents_Vert_Layout = QtWidgets.QVBoxLayout(self.RS_Devices_ScrollArea_Contents)
        self.RS_Devices_ScrollArea_Contents_Vert_Layout.setObjectName("RS_Devices_ScrollArea_Contents_Vert_Layout")
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
        self.MDI_View_GroupBox = QtWidgets.QGroupBox(self.Configure_Widget_Contents)
        self.MDI_View_GroupBox.setObjectName("MDI_View_GroupBox")
        self.MDI_View_GroupBox_Vert_Layout = QtWidgets.QVBoxLayout(self.MDI_View_GroupBox)
        self.MDI_View_GroupBox_Vert_Layout.setObjectName("MDI_View_GroupBox_Vert_Layout")
        self.MDI_View_Main_RadioButton = QtWidgets.QRadioButton(self.MDI_View_GroupBox)
        self.MDI_View_Main_RadioButton.setObjectName("MDI_View_Main_RadioButton")
        self.MDI_View_GroupBox_Vert_Layout.addWidget(self.MDI_View_Main_RadioButton)
        self.MDI_View_Tiled_RadioButton = QtWidgets.QRadioButton(self.MDI_View_GroupBox)
        self.MDI_View_Tiled_RadioButton.setObjectName("MDI_View_Tiled_RadioButton")
        self.MDI_View_GroupBox_Vert_Layout.addWidget(self.MDI_View_Tiled_RadioButton)
        self.MDI_View_Cascade_RadioButton = QtWidgets.QRadioButton(self.MDI_View_GroupBox)
        self.MDI_View_Cascade_RadioButton.setObjectName("MDI_View_Cascade_RadioButton")
        self.MDI_View_GroupBox_Vert_Layout.addWidget(self.MDI_View_Cascade_RadioButton)
        self.MDI_View_Vertical_RadioButton = QtWidgets.QRadioButton(self.MDI_View_GroupBox)
        self.MDI_View_Vertical_RadioButton.setObjectName("MDI_View_Vertical_RadioButton")
        self.MDI_View_GroupBox_Vert_Layout.addWidget(self.MDI_View_Vertical_RadioButton)
        self.MDI_View_Horizontal_RadioButton = QtWidgets.QRadioButton(self.MDI_View_GroupBox)
        self.MDI_View_Horizontal_RadioButton.setObjectName("MDI_View_Horizontal_RadioButton")
        self.MDI_View_GroupBox_Vert_Layout.addWidget(self.MDI_View_Horizontal_RadioButton)
        self.Configure_Widget_Contents_Horiz_Layout.addWidget(self.MDI_View_GroupBox)
        self.Configure_Widget_Dock.setWidget(self.Configure_Widget_Contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.Configure_Widget_Dock)
        # End MDI View option generation code
        ################################################################################################################
        # Begin MenuBar item generation code
        self.Begin_Experiment_Action = QtWidgets.QAction(MainWindow)
        self.Begin_Experiment_Action.setObjectName("Begin_Experiment_Action")
        self.COM_Messages_Action = QtWidgets.QAction(MainWindow)
        self.COM_Messages_Action.setCheckable(True)
        self.COM_Messages_Action.setObjectName("COM_Messages_Action")
        '''
        self.actionParameters = QtWidgets.QAction(MainWindow)
        self.actionParameters.setCheckable(True)
        self.actionParameters.setObjectName("actionParameters")
        self.actionLive_Data = QtWidgets.QAction(MainWindow)
        self.actionLive_Data.setCheckable(True)
        self.actionLive_Data.setObjectName("actionLive_Data")
        self.actionConfigure_Data_Buddy = QtWidgets.QAction(MainWindow)
        self.actionConfigure_Data_Buddy.setObjectName("actionConfigure_Data_Buddy")
        '''
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
        self.UDP_Controls_Menu.addAction(self.Output_Action)
        self.UDP_Controls_Menu.addAction(self.Input_Aciton)
        self.Settings_Menu.addAction(self.COM_Port_Action)
        self.Settings_Menu.addAction(self.UDP_Controls_Menu.menuAction())
        self.MenuBar.addAction(self.File_Menu.menuAction())
        self.MenuBar.addAction(self.Settings_Menu.menuAction())
        self.MenuBar.addAction(self.Window_Menu.menuAction())
        self.MenuBar.addAction(self.Help_Menu.menuAction())
        # End MenuBar item generation code
        ################################################################################################################
        # Begin final initialization
        self.SetAllObjectTexts(MainWindow)
        self.SetupButtonHandlers()
        self.Clear_PushButton.clicked.connect(self.COM_TextBox.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def SetAllObjectTexts(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        ################################################################################################################
        # Main Window SetTitle code
        MainWindow.setWindowTitle(_translate("MainWindow", "RS Device Companion"))
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
        self.File_Menu.setTitle(_translate("MainWindow", "File"))
        self.Window_Menu.setTitle(_translate("MainWindow", "Window"))
        self.Help_Menu.setTitle(_translate("MainWindow", "Help"))
        self.Settings_Menu.setTitle(_translate("MainWindow", "Settings"))
        self.UDP_Controls_Menu.setTitle(_translate("MainWindow", "UDP Controls"))
        self.Begin_Experiment_Action.setText(_translate("MainWindow", "Begin Experiment"))
        self.Begin_Experiment_Action.setToolTip(_translate("MainWindow", "Begin Experiment"))
        self.COM_Messages_Action.setText(_translate("MainWindow", "COM Messages"))
        '''
        self.actionParameters.setText(_translate("MainWindow", "Parameters"))
        self.actionLive_Data.setText(_translate("MainWindow", "Live Data"))
        self.actionConfigure_Data_Buddy.setText(_translate("MainWindow", "Configure Data Buddy"))
        '''
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
        # End MenuBar SetTitle code
        ################################################################################################################
        # Begin Control Widget SetTitle code
        self.Control_Widget_Dock.setWindowTitle(_translate("MainWindow", "Control"))
        self.Run_Trial_PushButton.setText(_translate("MainWindow", "Run\nTrial"))
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
        # End Control Widget SetTitle code
        ################################################################################################################
        # Begin COM Widget SetTitle code
        self.COM_Widget_Dock.setToolTip(_translate("MainWindow", "<html><head/><body><p>Displays all communications with Red Scientific Hardware. These can be saved for later browsing and debugging.</p></body></html>"))
        self.COM_Widget_Dock.setWindowTitle(_translate("MainWindow", "COM"))
        self.Record_PushButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Saves all raw COM messages to your data folder.</p></body></html>"))
        self.Record_PushButton.setText(_translate("MainWindow", "Record"))
        self.Freeze_PushButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Freezes the auto scrolling of COM messages.</p></body></html>"))
        self.Freeze_PushButton.setText(_translate("MainWindow", "Freeze"))
        self.Clear_PushButton.setToolTip(_translate("MainWindow", "<html><head/><body><p>Clears all COM messages in the pane above.</p></body></html>"))
        self.Clear_PushButton.setText(_translate("MainWindow", "Clear"))
        self.CHANGEME_CheckBox.setText(_translate("MainWindow", "CHANGEME_CheckBox"))
        # End COM Widget SetTitle code
        ################################################################################################################
        # Begin Configure Widget SetTitle code
        self.Configure_Widget_Dock.setWindowTitle(_translate("MainWindow", "Configure"))
        self.RS_Devices_GroupBox.setTitle(_translate("MainWindow", "Red Scientific Devices"))
        '''
        self.Device_GroupBox.setTitle(_translate("MainWindow", "DRT - Wireless 1"))
        self.Setup_PushButton.setText(_translate("MainWindow", "Setup"))
        self.Device_ToolButton.setText(_translate("MainWindow", "..."))
        '''
        self.MDI_View_GroupBox.setTitle(_translate("MainWindow", "MDI View"))
        self.MDI_View_Main_RadioButton.setText(_translate("MainWindow", "Main"))
        self.MDI_View_Tiled_RadioButton.setText(_translate("MainWindow", "Tiled"))
        self.MDI_View_Cascade_RadioButton.setText(_translate("MainWindow", "Cascade"))
        self.MDI_View_Vertical_RadioButton.setText(_translate("MainWindow", "Vertical"))
        self.MDI_View_Horizontal_RadioButton.setText(_translate("MainWindow", "Horizontal"))
        # End Configure Widget SetTitle code

    # TODO: Get buttons working (need to know what they should each do)
    # TODO: Make handlers for menu items
    def SetupButtonHandlers(self):
        self.MDI_View_Main_RadioButton.clicked.connect(self.MDI_Main_Handler)
        self.MDI_View_Tiled_RadioButton.clicked.connect(self.MDI_Tile_Handler)
        self.MDI_View_Cascade_RadioButton.clicked.connect(self.MDI_Cascade_Handler)
        self.MDI_View_Vertical_RadioButton.clicked.connect(self.MDI_Vert_Handler)
        self.MDI_View_Horizontal_RadioButton.clicked.connect(self.MDI_Horiz_Handler)
        self.Run_Trial_PushButton.clicked.connect(self.Run_Trial_Button_Handler)
        self.New_Block_PushButton.clicked.connect(self.New_Block_Button_Handler)
        self.Post_PushButton.clicked.connect(self.Post_Button_Handler)
        self.Record_PushButton.clicked.connect(self.Add_RS_Device)
        self.Freeze_PushButton.clicked.connect(self.Remove_RS_Device)
        self.Clear_PushButton.clicked.connect(self.Clear_Button_Handler)
        self.CHANGEME_CheckBox.toggled.connect(self.CHANGEME_CheckBox_Handler)

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def CHANGEME_CheckBox_Handler(self):
        print("CHANGEME CheckBox toggled")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def Run_Trial_Button_Handler(self):
        print("Run Trial Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def Record_Button_Handler(self):
        print("Record Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def Freeze_Button_Handler(self):
        print("Freeze Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def New_Block_Button_Handler(self):
        print("New Block Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def Clear_Button_Handler(self):
        print("Clear Button Pressed")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def Post_Button_Handler(self):
        print("Post Button Pressed")

    # Cascades the SubWindows in te MDI Dock
    def MDI_Cascade_Handler(self):
        self.MDI_Dock_Area.cascadeSubWindows()

    # Tiles the SubWindows in the MDI Dock
    def MDI_Tile_Handler(self):
        self.MDI_Dock_Area.tileSubWindows()

    # TODO: Remove prints in this function after debugging
    # TODO: Need to design own vert option, MDI widget doesn't natively have it
    # Vertically lays out the SubWindows in the MDI Dock
    def MDI_Vert_Handler(self):
        print("MDI_Vert_Handler called")
        if self.NumSubWindows < 2:
            print("MDI_Vert_Handler called MDI_Tile_Handler")
            self.MDI_Tile_Handler()
        else:
            print("MDI_Vert_Handler passed")

    # TODO: Remove prints in this function after debugging
    # TODO: Need to design own horiz option, MDI widget doesn't natively have it
    # Horizontally lays out the SubWindows in the MDI Dock
    def MDI_Horiz_Handler(self):
        print("MDI_Horiz_Handler called")

    # TODO: Remove prints in this function after debugging
    # TODO: Need to know what to put here
    # Sets SubWindows to a default layout in the MDI Dock?
    def MDI_Main_Handler(self):
        print("MDI_Main_Handler called")

    # Adds a new unique pair of RS Device box and RS SubWindow to the UI
    def Add_RS_Device(self):
        self.Add_RS_Device_Box()
        self.Add_RS_Device_SubWindow()

    # Removes an existing specific pair of RS Device box and RS Subwindow from the UI
    def Remove_RS_Device(self):
        self.Remove_RS_Device_Box()
        self.Remove_RS_Device_SubWindow()

    # Generates a new RS Device box, adds it to a collection and then displays it.
    def Add_RS_Device_Box(self):
        name = self.Block_Note_TextBox.toPlainText()
        if name:
            self.ListOfDevices[name] = Device_Box(name, self.RS_Devices_ScrollArea_Contents)
            self.RS_Devices_ScrollArea_Contents_Vert_Layout.addWidget(self.ListOfDevices[name])

    # Removes a specific RS Device box from the UI
    def Remove_RS_Device_Box(self):
        name = self.Block_Note_TextBox.toPlainText()
        if name in self.ListOfDevices and self.ListOfDevices[name]:
            self.RS_Devices_ScrollArea_Contents_Vert_Layout.removeWidget(self.ListOfDevices[name])
            self.ListOfDevices[name].deleteLater()
            del self.ListOfDevices[name]

    # Generates a new RS SubWindow, adds it to a collection and then displays it.
    def Add_RS_Device_SubWindow(self):
        # TODO: Remove prints in this function after debugging
        print("SubWindow Add called")
        name = self.Block_Note_TextBox.toPlainText()
        if name:
            self.NumSubWindows += 1
            print("Num subs =", self.NumSubWindows)
            sub = QtWidgets.QMdiSubWindow()
            sub.setWidget(QtWidgets.QTextEdit())
            sub.setWindowTitle("subwindow" + name)
            self.MDI_Dock_Area.addSubWindow(sub)
            self.ListOfSubWindows[name] = sub
            sub.show()
            # TODO: Get SubWindow class to work here instead
            '''
            self.ListOfSubWindows[name] = SubWindow(name, None)
            self.MDI_Dock_Area.addSubWindow(self.ListOfSubWindows[name])
            '''

    # TODO: Remove prints in this function after debugging
    def Remove_RS_Device_SubWindow(self):
        print("SubWindow Remove called")
        name = self.Block_Note_TextBox.toPlainText()
        if name in self.ListOfSubWindows and self.ListOfSubWindows[name]:
            self.NumSubWindows -= 1
            print("Num subs =", self.NumSubWindows)
            self.MDI_Dock_Area.removeSubWindow(self.ListOfSubWindows[name])
            self.ListOfSubWindows[name].deleteLater()
            del self.ListOfSubWindows[name]


class Device_Box(QtWidgets.QGroupBox):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.setObjectName(name)
        self.Device_GroupBox_Horiz_Layout = QtWidgets.QHBoxLayout(self)
        self.Device_GroupBox_Horiz_Layout.setObjectName("Device_GroupBox_Horiz_Layout")
        self.Setup_PushButton = QtWidgets.QPushButton(self)
        self.Setup_PushButton.setObjectName("Setup_PushButton")
        self.Device_GroupBox_Horiz_Layout.addWidget(self.Setup_PushButton)
        self.Device_ToolButton = QtWidgets.QToolButton(self)
        self.Device_ToolButton.setObjectName("Device_ToolButton")
        self.Device_GroupBox_Horiz_Layout.addWidget(self.Device_ToolButton)
        self.SetTexts(name)

    def SetTexts(self, name):
        _translate = QtCore.QCoreApplication.translate
        self.setTitle(_translate("MainWindow", name))
        self.Setup_PushButton.setText(_translate("MainWindow", "Setup"))
        self.Device_ToolButton.setText(_translate("MainWindow", "..."))


# TODO: Rename objects in subwindow class
class SubWindow(QtWidgets.QMdiSubWindow):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.setObjectName(name)
        '''
        self.subwindow = QtWidgets.QWidget()
        self.subwindow.setObjectName("subwindow")
        '''
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.frame_4 = QtWidgets.QFrame(self)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 265))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout.addWidget(self.frame_4)
        self.scrollArea_2 = QtWidgets.QScrollArea(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy)
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
        self.SetTexts(name)
        self.show()

    def SetTexts(self, name):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", name))
        self.groupBox_5.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_16.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_17.setText(_translate("MainWindow", "PushButton"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_3.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_4.setText(_translate("MainWindow", "CheckBox"))
        self.groupBox_6.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_15.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_14.setText(_translate("MainWindow", "PushButton"))