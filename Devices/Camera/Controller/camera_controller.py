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
import cv2
from Devices.Camera.View.camera_tab import CameraTab
from Devices.abc_device_controller import ABCDeviceController
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.


class CameraController(ABCDeviceController):
    def __init__(self, cam_obj, tab_parent, ch):
        super().__init__(CameraTab(tab_parent, name=cam_obj.name))
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.cam_obj = cam_obj
        self.save_dir = ''
        self.timestamp = None
        self.exp = False
        self.logger.debug("Initialized")
        self.__setup_handlers()

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
        if self.cam_obj.active:
            self.cam_obj.setup_writer(save_dir=self.save_dir, timestamp=self.timestamp)
        self.exp = True
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.cam_obj.destroy_writer()
        self.exp = False
        self.logger.debug("done")

    def toggle_cam(self):
        if not self.exp:
            self.cam_obj.active = not self.cam_obj.active
            if not self.cam_obj.active:
                self.cam_obj.close_window()

    def __setup_handlers(self):
        self.tab.add_use_cam_button_handler(self.toggle_cam)
