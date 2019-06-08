# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QTabWidget, QSizePolicy
from PySide2.QtCore import QSize, Qt, QMetaObject
from PySide2.QtGui import QFont, QKeyEvent
from Model.defs import about_RS_text, about_RS_app_text
from Model.device import RSDevice
from View.GraphWidget.chart_container import GraphContainer
from View.DockWidget.control_dock import ControlDock
from View.help_window import HelpWindow
from View.TabWidget.device_tab import Tab
from View.TabWidget.saved_file_tab_contents import TabContents as SavedFileTabContents
from View.central_widget import CentralWidget
from View.MenuBarWidget.menu_bar import MenuBar


class CompanionWindow(QMainWindow):
    def __init__(self, msg_handler):
        super().__init__()
        self.setMinimumSize(QSize(450, 550))
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        self.setCentralWidget(CentralWidget())

        self.setMenuBar(MenuBar())

        self.__control_dock_widget = ControlDock(self)
        self.addDockWidget(Qt.DockWidgetArea(4), self.__control_dock_widget)

        self.__main_chart_area = GraphContainer()
        self.__graph_and_tab_layout = QHBoxLayout()
        self.__graph_and_tab_layout.addWidget(self.__main_chart_area)

        self.__tab_widget = QTabWidget(self.centralWidget())
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.__tab_widget.sizePolicy().hasHeightForWidth())
        self.__tab_widget.setSizePolicy(size_policy)
        self.__tab_widget.setMinimumWidth(250)
        self.__graph_and_tab_layout.addWidget(self.__tab_widget)
        self.centralWidget().layout().addLayout(self.__graph_and_tab_layout)

        self.__msg_callback = msg_handler
        self.__list_of_devices__ = {}
        self.__saved_file_tab = None
        self.__tab_contents = None
        self.__num_tab_buttons = 0
        self.__set_texts()
        self.__setup_handlers()

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.__control_dock_widget.set_key_flag(chr(event.key()))
                print(self.__control_dock_widget.get_key_flag())
            event.accept()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        event.accept()

    def closeEvent(self, event):
        self.__msg_callback({'action': "close"})
        for device in self.__list_of_devices__:
            self.__list_of_devices__[device].remove_self()

    def add_exp_create_end_handler(self, func):
        self.__control_dock_widget.add_create_end_button_handler(func)

    def add_exp_start_stop_handler(self, func):
        self.__control_dock_widget.add_start_button_handler(func)

    def add_post_handler(self, func):
        self.__control_dock_widget.add_post_handler(func)

    def add_update_handler(self, func):
        self.menuBar().add_update_handler(func)

    def add_note_box_changed_handler(self, func):
        self.__control_dock_widget.add_note_box_changed_handler(func)

    def set_exp_start_time(self, time):
        self.__control_dock_widget.set_start_time(time)

    def get_key_flag(self):
        return self.__control_dock_widget.get_key_flag()

    def get_note(self):
        return self.__control_dock_widget.get_note()

    def clear_note(self):
        self.__control_dock_widget.clear_note()

    def get_condition_name(self):
        return self.__control_dock_widget.get_condition_name()

    def toggle_post_button(self, is_active):
        self.__control_dock_widget.toggle_post_button(is_active)

    def add_saved_file_tab(self):
        self.__saved_file_tab = Tab()
        self.__tab_widget.setUpdatesEnabled(False)
        index = self.__tab_widget.addTab(self.__saved_file_tab, "")
        self.__tab_widget.setUpdatesEnabled(True)
        self.__tab_widget.setTabText(index, "Saved Files")
        self.__tab_contents = SavedFileTabContents(self.__saved_file_tab.scroll_area_contents,
                                                   self.remove_saved_file_from_tab)

    def remove_saved_file_tab(self):
        self.__tab_widget.removeTab(self.__tab_widget.indexOf(self.__saved_file_tab))
        self.__saved_file_tab.deleteLater()
        self.__saved_file_tab = None

    def add_saved_file_to_tab(self, filename, controller_callback):
        if not self.__saved_file_tab:
            self.add_saved_file_tab()
        self.__num_tab_buttons += 1
        self.__tab_contents.add_close_button(filename, controller_callback)

    def remove_saved_file_from_tab(self, filename):
        self.__main_chart_area.remove_device(filename)
        self.__num_tab_buttons -= 1
        if self.__num_tab_buttons == 0:
            self.remove_saved_file_tab()

    # Passes message received to proper device display object
    def handle_msg(self, msg_dict):
        if msg_dict['type'] == "add":
            del msg_dict['type']
            self.add_rs_device(msg_dict['device'])
        elif msg_dict['type'] == "remove":
            del msg_dict['type']
            self.remove_rs_device(msg_dict['device'])
        elif msg_dict['type'] == "settings":
            del msg_dict['type']
            for device in self.__list_of_devices__:
                if device == msg_dict['device']:
                    del msg_dict['device']
                    self.__list_of_devices__[device].handle_msg(msg_dict)
                    pass
        elif msg_dict['type'] == "data":
            del msg_dict['type']
            self.__main_chart_area.handle_msg(msg_dict)

    # Creates an RSDevice and adds it to the list of devices
    def add_rs_device(self, device):
        if device not in self.__list_of_devices__:
            self.__list_of_devices__[device] = RSDevice(device, self.__msg_callback, self.__tab_widget)
            self.__main_chart_area.add_device(device)

    # Deletes an RSDevice and removes it from the list of devices
    def remove_rs_device(self, device):
        if device in self.__list_of_devices__:
            self.__list_of_devices__[device].remove_self()
            del self.__list_of_devices__[device]
            self.__main_chart_area.remove_device(device)

    def __set_texts(self):
        self.setWindowTitle("RS Companion App")

    def __setup_handlers(self):
        self.menuBar().add_about_company_handler(self.__about_company)
        self.menuBar().add_about_app_handler(self.__about_app)

    def __about_app(self):
        self.help_window = HelpWindow("About Red Scientific Companion App", about_RS_app_text)
        self.help_window.show()

    def __about_company(self):
        self.help_window = HelpWindow("About Red Scientific", about_RS_text)
        self.help_window.show()

