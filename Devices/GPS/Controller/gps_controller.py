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

# Author: Nathan Rogers
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from math import trunc, ceil
import logging
from typing import Tuple, Optional
from datetime import datetime
from PySide2.QtCore import QObject, Signal
from Devices.abc_device_controller import ABCDeviceController
from Controller.RS_Device_Manager.rs_device_manager import PortWorker

class GPSSig(QObject):
    send_device_msg_sig = Signal(str)

class GPSController(ABCDeviceController):
    def __init__(self, device: Tuple[str, str], thread: PortWorker,
                 ch: logging.StreamHandler, save_callback) -> None:
        """
        GPS controller
        :param device: Tuple[str, str] of device type and name
        :param thread: Device communication thread
        :param ch:
        :param save_callback:
        :return None:
        """

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.signals = GPSSig()
        self.device_name = device[0].upper(), "_" + device[1][3:]
        # add tab stuff here
        self.__device_info = device
        self.__save_callback = save_callback
        self.exp = False
        # info to send to gps
        self.__connect_signals(thread)
        self.save_file = str()
        self.__set_handlers()
        self.init_values()
        self.logger.debug("Initialized")

    def cleanup(self) -> None:
        """

        :return None:
        """

        self.logger.debug("running")
        if self.exp:
            self.end_block()
        self.logger.debug("done")

    def get_tab_obj(self):
        return self.tab

