# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtWidgets import QMessageBox


class HelpWindow(QMessageBox):
    def __init__(self, name, text):
        super().__init__()
        self.setWindowTitle(name)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Close)
        self.setDefaultButton(QMessageBox.Close)
        self.setEscapeButton(QMessageBox.Close)
