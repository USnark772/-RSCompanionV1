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
# Author: Nathan Rogers
# Date: 2019 - 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from PySide2.QtWidgets import QMenuBar, QMenu, QAction
from PySide2.QtCore import QRect


class MenuBar(QMenuBar):
    """ This code is for the menu bar at the top of the main window. File, help, etc. """
    def __init__(self, parent, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 840, 22))

        self.__file = QMenu(self)
        self.addAction((self.__file.menuAction()))

        self.__open_last_save_dir = QAction(self)
        self.__file.addAction(self.__open_last_save_dir)

        self.__help = QMenu(self)
        self.addAction(self.__help.menuAction())

        self.__about_app = QAction(self)
        self.__help.addAction(self.__about_app)

        self.__about_company = QAction(self)
        self.__help.addAction(self.__about_company)

        self.__update = QAction(self)
        self.__help.addAction(self.__update)

        self.__log_window = QAction(self)
        self.__help.addAction(self.__log_window)

        self.__set_texts()
        self.logger.debug("Initialized")

    def add_open_last_save_dir_handler(self, func):
        self.logger.debug("running")
        self.__open_last_save_dir.triggered.connect(func)
        self.logger.debug("done")

    def add_about_app_handler(self, func):
        self.logger.debug("running")
        self.__about_app.triggered.connect(func)
        self.logger.debug("done")

    def add_about_company_handler(self, func):
        self.logger.debug("running")
        self.__about_company.triggered.connect(func)
        self.logger.debug("done")

    def add_update_handler(self, func):
        self.logger.debug("running")
        self.__update.triggered.connect(func)
        self.logger.debug("done")

    def add_log_window_handler(self, func):
        self.logger.debug("running")
        self.__log_window.triggered.connect(func)
        self.logger.debug("done")

    def __set_texts(self):
        self.logger.debug("running")
        self.__file.setTitle("File")
        self.__open_last_save_dir.setText("Open last save location")
        self.__help.setTitle("Help")
        self.__about_app.setText("About RS Companion")
        self.__about_company.setText("About Red Scientific")
        self.__update.setText("Check For Updates")
        self.__log_window.setText("Show log window")
        self.logger.debug("done")
