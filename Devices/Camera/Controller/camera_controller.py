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
from Devices.Camera.View.camera_tab import CameraTab
from Devices.abc_device_controller import ABCDeviceController
from CompanionLib.companion_helpers import get_current_time
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.


# TODO: Add comments
# TODO: Turn this into per camera controller instead of camera manager controller.
class CameraController(ABCDeviceController):
    def __init__(self, cam_obj, tab_parent, ch):
        tab = CameraTab(tab_parent, name=cam_obj.name)
        super().__init__(tab)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.cam_obj = cam_obj
        self.save_dir = ''
        self.timestamp = None
        self.logger.debug("Initialized")

    def cleanup(self):
        self.logger.debug("running")
        pass
        self.logger.debug("done")

    def create_new_save_file(self, new_filename):
        self.logger.debug("running")
        self.save_dir = new_filename
        self.logger.debug("done")

    def set_start_time(self, timestamp):
        self.timestamp = timestamp

    def start_exp(self):
        self.logger.debug("running")
        self.cam_obj.setup_writer(save_dir=self.save_dir, timestamp=self.timestamp)
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.cam_obj.destroy_writer()
        self.logger.debug("done")
