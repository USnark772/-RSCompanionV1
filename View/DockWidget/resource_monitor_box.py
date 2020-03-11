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

import logging
from psutil import cpu_count
from PySide2.QtWidgets import QGroupBox, QGridLayout, QLabel
from PySide2.QtCore import Qt

class MonitorBox(QGroupBox):
    def __init__(self, parent, size, ch, num_labels: int = cpu_count()):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__(parent)
        self.setMaximumSize(size)
        self.setLayout(QGridLayout())

        self.title = QLabel()
        self.layout().addWidget(self.title, 0, 0, Qt.AlignHCenter)

        self.values = []
        self.labels = []

        for i in range(num_labels):
            self.values.append(QLabel())
            self.labels.append(QLabel())
            self.layout().addWidget(self.labels[i], i + 1, 0, Qt.AlignLeft)
            self.layout().addWidget(self.values[i], i + 1, 1, Qt.AlignRight)

        self.__set_texts()

    def set_cpu_value(self, label: QLabel, value: int):
        label.setText(str(value) + "%")

    def update_values(self, values):
        for i in range(len(values)):
            self.set_cpu_value(self.values[i], values[i])

    def __set_texts(self):
        self.title.setText("CPU Usage")
        for value in self.values:
            self.set_cpu_value(value, 0)
        for i in range(len(self.labels)):
            self.labels[i].setText('cpu ' + str(i) + ':')
