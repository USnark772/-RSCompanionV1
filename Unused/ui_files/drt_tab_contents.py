# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drt_tab_contents.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(237, 521)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tab_horiz_layout = QtWidgets.QHBoxLayout()
        self.tab_horiz_layout.setObjectName("tab_horiz_layout")
        self.scroll_area = QtWidgets.QScrollArea(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_area.sizePolicy().hasHeightForWidth())
        self.scroll_area.setSizePolicy(sizePolicy)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_contents = QtWidgets.QWidget()
        self.scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 187, 453))
        self.scroll_area_contents.setObjectName("scroll_area_contents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scroll_area_contents)
        self.verticalLayout.setObjectName("verticalLayout")



        self.config_horizontalLayout = QtWidgets.QHBoxLayout()
        self.config_horizontalLayout.setObjectName("config_horizontalLayout")
        self.config_label = QtWidgets.QLabel(self.scroll_area_contents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.config_label.setFont(font)
        self.config_label.setObjectName("config_label")
        self.config_horizontalLayout.addWidget(self.config_label)
        self.config_label_val_sep_line = QtWidgets.QFrame(self.scroll_area_contents)
        self.config_label_val_sep_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.config_label_val_sep_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.config_label_val_sep_line.setObjectName("config_label_val_sep_line")
        self.config_horizontalLayout.addWidget(self.config_label_val_sep_line)
        self.config_val_label = QtWidgets.QLabel(self.scroll_area_contents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.config_val_label.setFont(font)
        self.config_val_label.setObjectName("config_val_label")
        self.config_horizontalLayout.addWidget(self.config_val_label)
        self.verticalLayout.addLayout(self.config_horizontalLayout)
        self.iso_default_push_button = QtWidgets.QPushButton(self.scroll_area_contents)
        self.iso_default_push_button.setObjectName("iso_default_push_button")
        self.verticalLayout.addWidget(self.iso_default_push_button)
        self.config_stim_dur_sep_line = QtWidgets.QFrame(self.scroll_area_contents)
        self.config_stim_dur_sep_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.config_stim_dur_sep_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.config_stim_dur_sep_line.setObjectName("config_stim_dur_sep_line")
        self.verticalLayout.addWidget(self.config_stim_dur_sep_line)
        self.stim_dur_horizontalLayout = QtWidgets.QHBoxLayout()
        self.stim_dur_horizontalLayout.setObjectName("stim_dur_horizontalLayout")
        self.stim_dur_label = QtWidgets.QLabel(self.scroll_area_contents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.stim_dur_label.setFont(font)
        self.stim_dur_label.setObjectName("stim_dur_label")
        self.stim_dur_horizontalLayout.addWidget(self.stim_dur_label)
        self.stim_dur_lcdNumber = QtWidgets.QLCDNumber(self.scroll_area_contents)
        self.stim_dur_lcdNumber.setMinimumSize(QtCore.QSize(80, 40))
        self.stim_dur_lcdNumber.setObjectName("stim_dur_lcdNumber")
        self.stim_dur_horizontalLayout.addWidget(self.stim_dur_lcdNumber)
        self.verticalLayout.addLayout(self.stim_dur_horizontalLayout)
        self.stim_dur_slider = QtWidgets.QSlider(self.scroll_area_contents)
        self.stim_dur_slider.setMinimumSize(QtCore.QSize(175, 0))
        self.stim_dur_slider.setOrientation(QtCore.Qt.Horizontal)
        self.stim_dur_slider.setObjectName("stim_dur_slider")
        self.verticalLayout.addWidget(self.stim_dur_slider)
        self.stim_dur_intens_sep_line = QtWidgets.QFrame(self.scroll_area_contents)
        self.stim_dur_intens_sep_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.stim_dur_intens_sep_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stim_dur_intens_sep_line.setObjectName("stim_dur_intens_sep_line")
        self.verticalLayout.addWidget(self.stim_dur_intens_sep_line)
        self.stim_intens_horizontalLayout = QtWidgets.QHBoxLayout()
        self.stim_intens_horizontalLayout.setObjectName("stim_intens_horizontalLayout")
        self.stim_intens_label = QtWidgets.QLabel(self.scroll_area_contents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.stim_intens_label.setFont(font)
        self.stim_intens_label.setObjectName("stim_intens_label")
        self.stim_intens_horizontalLayout.addWidget(self.stim_intens_label)
        self.stim_intens_lcdNumber = QtWidgets.QLCDNumber(self.scroll_area_contents)
        self.stim_intens_lcdNumber.setMinimumSize(QtCore.QSize(80, 40))
        self.stim_intens_lcdNumber.setObjectName("stim_intens_lcdNumber")
        self.stim_intens_horizontalLayout.addWidget(self.stim_intens_lcdNumber)
        self.verticalLayout.addLayout(self.stim_intens_horizontalLayout)
        self.stim_intens_slider = QtWidgets.QSlider(self.scroll_area_contents)
        self.stim_intens_slider.setMinimumSize(QtCore.QSize(175, 0))
        self.stim_intens_slider.setOrientation(QtCore.Qt.Horizontal)
        self.stim_intens_slider.setObjectName("stim_intens_slider")
        self.verticalLayout.addWidget(self.stim_intens_slider)
        self.stim_intens_upper_isi_sep_line = QtWidgets.QFrame(self.scroll_area_contents)
        self.stim_intens_upper_isi_sep_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.stim_intens_upper_isi_sep_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stim_intens_upper_isi_sep_line.setObjectName("stim_intens_upper_isi_sep_line")
        self.verticalLayout.addWidget(self.stim_intens_upper_isi_sep_line)
        self.upper_isi_horizontalLayout = QtWidgets.QHBoxLayout()
        self.upper_isi_horizontalLayout.setObjectName("upper_isi_horizontalLayout")
        self.upper_isi_label = QtWidgets.QLabel(self.scroll_area_contents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.upper_isi_label.setFont(font)
        self.upper_isi_label.setObjectName("upper_isi_label")
        self.upper_isi_horizontalLayout.addWidget(self.upper_isi_label)
        self.upper_isi_lcdNumber = QtWidgets.QLCDNumber(self.scroll_area_contents)
        self.upper_isi_lcdNumber.setMinimumSize(QtCore.QSize(80, 40))
        self.upper_isi_lcdNumber.setObjectName("upper_isi_lcdNumber")
        self.upper_isi_horizontalLayout.addWidget(self.upper_isi_lcdNumber)
        self.verticalLayout.addLayout(self.upper_isi_horizontalLayout)
        self.upper_isi_slider = QtWidgets.QSlider(self.scroll_area_contents)
        self.upper_isi_slider.setMinimumSize(QtCore.QSize(175, 0))
        self.upper_isi_slider.setOrientation(QtCore.Qt.Horizontal)
        self.upper_isi_slider.setObjectName("upper_isi_slider")
        self.verticalLayout.addWidget(self.upper_isi_slider)
        self.upper_lower_isi_sep_line = QtWidgets.QFrame(self.scroll_area_contents)
        self.upper_lower_isi_sep_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.upper_lower_isi_sep_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.upper_lower_isi_sep_line.setObjectName("upper_lower_isi_sep_line")
        self.verticalLayout.addWidget(self.upper_lower_isi_sep_line)
        self.lower_isi_horizontalLayout = QtWidgets.QHBoxLayout()
        self.lower_isi_horizontalLayout.setObjectName("lower_isi_horizontalLayout")
        self.lower_isi_label = QtWidgets.QLabel(self.scroll_area_contents)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lower_isi_label.setFont(font)
        self.lower_isi_label.setObjectName("lower_isi_label")
        self.lower_isi_horizontalLayout.addWidget(self.lower_isi_label)
        self.lower_isi_lcdNumber = QtWidgets.QLCDNumber(self.scroll_area_contents)
        self.lower_isi_lcdNumber.setMinimumSize(QtCore.QSize(80, 40))
        self.lower_isi_lcdNumber.setObjectName("lower_isi_lcdNumber")
        self.lower_isi_horizontalLayout.addWidget(self.lower_isi_lcdNumber)
        self.verticalLayout.addLayout(self.lower_isi_horizontalLayout)
        self.lower_isi_horizontalSlider = QtWidgets.QSlider(self.scroll_area_contents)
        self.lower_isi_horizontalSlider.setMinimumSize(QtCore.QSize(175, 0))
        self.lower_isi_horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lower_isi_horizontalSlider.setObjectName("lower_isi_horizontalSlider")
        self.verticalLayout.addWidget(self.lower_isi_horizontalSlider)




        self.scroll_area.setWidget(self.scroll_area_contents)
        self.tab_horiz_layout.addWidget(self.scroll_area)
        self.verticalLayout_10.addLayout(self.tab_horiz_layout)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.config_label.setText(_translate("Form", "Configuration"))
        self.config_val_label.setText(_translate("Form", "ISO Default"))
        self.iso_default_push_button.setText(_translate("Form", "ISO Default"))
        self.stim_dur_label.setText(_translate("Form", "Stim Duration\n"
"(msecs)"))
        self.stim_intens_label.setText(_translate("Form", "Stim Intensity"))
        self.upper_isi_label.setText(_translate("Form", "Upper ISI"))
        self.lower_isi_label.setText(_translate("Form", "Lower ISI"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))

