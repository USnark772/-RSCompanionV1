""" Licensed under GNU GPL-3.0-or-later """
"""
This file is part of RS Companion.

RS Companion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RS Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RS Companion.  If not, see <https://www.gnu.org/licenses/>.
"""

# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QFrame
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QIcon
from View.MainWindow.help_window import HelpWindow
from View.MainWindow.central_widget import CentralWidget
from Model.general_defs import image_file_path


class CompanionWindow(QMainWindow):
    """ The main window the app will be displayed in. """
    def __init__(self, min_size):
        super().__init__()
        self.setMinimumSize(min_size)
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setCentralWidget(CentralWidget(self))
        self.__graph_and_tab_layout = QHBoxLayout(self)
        self.__graph_frame = QFrame(self)
        self.__graph_frame.setLayout(QHBoxLayout())
        self.__tab_frame = QFrame(self)
        self.__tab_frame.setLayout(QHBoxLayout())
        self.__graph_and_tab_layout.addWidget(self.__graph_frame)
        self.__graph_and_tab_layout.addWidget(self.__tab_frame)
        self.centralWidget().layout().addLayout(self.__graph_and_tab_layout)

        self.__icon = QIcon(image_file_path + "rs_icon.png")
        self.setWindowIcon(self.__icon)
        self.close_callback = None
        self.__help_window = None
        self.__set_texts()

    def closeEvent(self, event):
        """ Alert controller if desired to the app closing event"""
        if self.close_callback:
            self.close_callback()

    def add_close_handler(self, func):
        self.close_callback = func

    def add_dock_widget(self, widget):
        self.addDockWidget(Qt.DockWidgetArea(4), widget)

    def add_menu_bar(self, widget):
        self.setMenuBar(widget)

    def add_graph_container(self, widget):
        self.__graph_frame.layout().addWidget(widget)

    def add_tab_widget(self, widget):
        self.__tab_frame.layout().addWidget(widget)

    def show_help_window(self, title, msg):
        """ Show msg in a help window with the title. """
        self.__help_window = HelpWindow(title, msg)
        self.__help_window.setWindowIcon(self.__icon)
        self.__help_window.show()

    def __set_texts(self):
        self.setWindowTitle("RS Companion App")
