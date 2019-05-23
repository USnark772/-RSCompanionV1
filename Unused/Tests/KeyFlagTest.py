from PySide2.QtCharts import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys


class TheThing(QMainWindow):
    def __init__(self):
        super().__init__()
        self.key_flag_label = QLabel()
        self.key_flag_label.setText("Test")
        self.setCentralWidget(self.key_flag_label)

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            self.key_flag_label.setText(str(event.key()))
            event.accept()
        else:
            event.ignore()


a = QApplication(sys.argv)

window = TheThing()
window.resize(420, 300)
window.show()

a.exec_()
