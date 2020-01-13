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
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html


from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide2.QtGui import QPixmap


class CamViewer(QWidget):
    def __init__(self, name):
        super().__init__()
        self.resize(400, 200)
        self.move(100, 100)
        self.setWindowTitle(name)
        self.setLayout(QVBoxLayout())
        self.image_display = QLabel()
        self.image_display.resize(640, 480)
        self.layout().addWidget(self.image_display)
        self.show()

    def set_image(self, frame):
        self.image_display.setPixmap(QPixmap.fromImage(frame))
