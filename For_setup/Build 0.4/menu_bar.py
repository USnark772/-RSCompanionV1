# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QMenuBar, QMenu, QAction
from PySide2.QtCore import QRect


class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(QRect(0, 0, 840, 22))

        self.__help = QMenu(self)
        self.addAction(self.__help.menuAction())

        self.__about_app = QAction(self)
        self.__help.addAction(self.__about_app)

        self.__about_company = QAction(self)
        self.__help.addAction(self.__about_company)

        self.__update = QAction(self)
        self.__help.addAction(self.__update)

        self.__set_texts()

    def add_about_app_handler(self, func):
        self.__about_app.triggered.connect(func)

    def add_about_company_handler(self, func):
        self.__about_company.triggered.connect(func)

    def add_update_handler(self, func):
        self.__update.triggered.connect(func)

    def __set_texts(self):
        self.__help.setTitle("Help")
        self.__about_app.setText("About RS Companion")
        self.__about_company.setText("About Red Scientific")
        self.__update.setText("Check For Updates")
