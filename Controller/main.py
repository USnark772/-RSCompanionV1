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

import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from Controller.controller import CompanionController
from Controller.single_instance import SingleInstance


def main():
    """
    Handles running application
    :return None:
    """

    si = SingleInstance()
    try:
        if si.is_running:
            sys.exit("This app is already running!")
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        app = QApplication(sys.argv)
        controller = CompanionController()  # Need reference else garbage collector has too much fun
        sys.exit(app.exec_())
    finally:
        si.clean_up()


if __name__ == "__main__":
    main()
