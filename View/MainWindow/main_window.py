# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QMainWindow, QHBoxLayout, QFrame
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QFont
from Model.defs import about_RS_text, about_RS_app_text, up_to_date, update_available
from View.MainWindow.help_window import HelpWindow
from View.MainWindow.central_widget import CentralWidget


class CompanionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(450, 550))
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

        self.__help_window = None
        self.__set_texts()

    def add_dock_widget(self, widget):
        self.addDockWidget(Qt.DockWidgetArea(4), widget)

    def add_menu_bar(self, widget):
        self.setMenuBar(widget)

    def add_graph_container(self, widget):
        self.__graph_frame.layout().addWidget(widget)

    def add_tab_widget(self, widget):
        self.__tab_frame.layout().addWidget(widget)

    def show_update_available(self, is_available):
        if is_available:
            self.__help_window = HelpWindow("Update", update_available)
        else:
            self.__help_window = HelpWindow("Update", up_to_date)
        self.__help_window.show()

    '''
    def add_update_handler(self, func):
        self.menuBar().add_update_handler(func)
    '''

    def about_app(self):
        self.__help_window = HelpWindow("About Red Scientific Companion App", about_RS_app_text)
        self.__help_window.show()

    def about_company(self):
        self.__help_window = HelpWindow("About Red Scientific", about_RS_text)
        self.__help_window.show()

    def raise_error(self, title, msg):
        self.__help_window = HelpWindow(title, msg)
        self.__help_window.show()

    def __set_texts(self):
        self.setWindowTitle("RS Companion App")
