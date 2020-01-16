import logging
from PySide2.QtWidgets import QWidget, QVBoxLayout
from PySide2.QtCore import QRect


# TODO: Figure out if subclassing with this is worth it right now.
class ABCDeviceTab(QWidget):
    def __init__(self, parent, max_height, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        try:
            super().__init__(parent)
        except Exception as e:
            self.logger.exception("Error making device tab, passed parent is invalid")
            return
        self.setLayout(QVBoxLayout(self))
        self.setGeometry(QRect(0, 0, 200, 500))
        self.setMaximumHeight(max_height)
