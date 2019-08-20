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

from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QSize
from Model.general_defs import image_file_path


class ButtonBox(QGroupBox):
    """ This code is to contain the overall controls which govern running experiments. """
    def __init__(self, parent, size):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.setMaximumSize(size)
        self.__button_layout = QHBoxLayout()

        self.__create_button = QPushButton()
        self.__create_button.setFixedSize(60, 40)
        self.__start_button = QPushButton()
        self.__start_button.setFixedSize(120, 40)
        self.__button_layout.addWidget(self.__create_button)
        self.__button_layout.addWidget(self.__start_button)
        self.__text_entry = QLineEdit()
        self.layout().addLayout(self.__button_layout)
        self.layout().addWidget(self.__text_entry)

        self.__play_icon = QIcon()
        self.__play_icon.addPixmap(QPixmap(image_file_path + "green_arrow.png"))
        self.__pause_icon = QIcon()
        self.__pause_icon.addPixmap(QPixmap(image_file_path + "red_vertical_bars.png"))
        self.__playing = False

        self.__set_texts()
        self.__set_button_states()
        self.__set_tooltips()

    def get_condition_name(self):
        return self.__text_entry.text()

    def add_create_button_handler(self, func):
        self.__create_button.clicked.connect(func)

    def add_start_button_handler(self, func):
        self.__start_button.clicked.connect(func)

    def toggle_condition_name_box(self):
        self.__text_entry.setEnabled(not self.__text_entry.isEnabled())
        '''
        if self.__text_entry.isEnabled():
            self.__text_entry.setEnabled(False)
        else:
            self.__text_entry.setEnabled(True)
        '''

    def toggle_create_button(self):
        """ Set create button to either create or end depending on what state any current experiment is in. """
        if self.__create_button.text() == "Create":
            self.__create_button.setText("End")
            self.__create_button.setToolTip("End experiment")
            self.__start_button.setEnabled(True)
        else:
            self.__create_button.setText("Create")
            self.__create_button.setToolTip("Create a new experiment")
            self.__start_button.setToolTip("Begin experiment")
            self.__start_button.setEnabled(False)

    def toggle_start_button(self):
        """ Set start button state depending on if there is an experiment created and running or not. """
        if self.__playing:
            self.__playing = False
            self.__start_button.setIcon(self.__play_icon)
            self.__start_button.setIconSize(QSize(26, 26))
            self.__create_button.setEnabled(True)
            self.__start_button.setToolTip("Resume experiment")
        else:
            self.__playing = True
            self.__start_button.setIcon(self.__pause_icon)
            self.__start_button.setIconSize(QSize(36, 36))
            self.__create_button.setEnabled(False)
            self.__start_button.setToolTip("Pause experiment")

    def __set_texts(self):
        self.setTitle("Experiment")
        self.__text_entry.setPlaceholderText("Optional condition name")
        self.__create_button.setText("Create")
        self.__start_button.setIcon(self.__play_icon)
        self.__start_button.setIconSize(QSize(32, 32))

    def __set_button_states(self):
        """ Set default button states. """
        self.__start_button.setEnabled(False)

    def __set_tooltips(self):
        self.__create_button.setToolTip("Create a new experiment")
        self.__start_button.setToolTip("Begin experiment")
