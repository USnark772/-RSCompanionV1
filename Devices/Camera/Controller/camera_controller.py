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
from Controller.Camera_Manager.camera_manager import CameraManager  # TODO: Circular dependency?
from CompanionLib.companion_helpers import get_current_time
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.

# TODO: Add tab per camera?
# TODO: Add comments


class CameraController(ABCDeviceController):
    def __init__(self, tab_parent, ch):
        tab = CameraTab(tab_parent, name="Cameras")
        super().__init__(tab)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.save_dir = ''
        self.cam_man = CameraManager(ch)  # TODO: Move this to main controller and reformat code. Need controller per cam
        self.logger.debug("Initialized")

    def cleanup(self):
        self.logger.debug("running")
        self.cam_man.cleanup()
        self.logger.debug("done")

    def create_new_save_file(self, new_filename):
        self.logger.debug("running")
        self.save_dir = new_filename
        self.logger.debug("done")

    def start_exp(self):
        self.logger.debug("running")
        self.cam_man.start_recording(timestamp=get_current_time(save=True), save_dir=self.save_dir)
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.cam_man.stop_recording()
        self.logger.debug("done")
