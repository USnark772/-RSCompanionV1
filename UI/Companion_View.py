# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific

import sys
from UI.RS_Companion_Window_Class import *

# Testing if buttons can be assigned to external funtions
# This seems to work fine
def Ext_Clear_Button_Handler(object):
    print("Ext Clear Button Pressed")

# The problem here is that this function needs to know about the UI's buttons, I don't like it.
def SetButtonHandlers(obj):
    obj.Clear_PushButton.clicked.connect(Ext_Clear_Button_Handler)


def main():
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    companion_app = QtWidgets.QMainWindow()
    ui = CompanionWindow(companion_app)
    #SetButtonHandlers(ui)
    companion_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":main()