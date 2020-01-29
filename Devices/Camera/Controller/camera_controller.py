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
from PySide2.QtCore import QObject, Signal
from Devices.Camera.View.camera_tab import CameraTab
from Devices.abc_device_controller import ABCDeviceController
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.


class ControllerSig(QObject):
    toggle_signal = Signal()


class CameraController(ABCDeviceController):
    def __init__(self, cam_obj, thread, ch):
        super().__init__(CameraTab(name=cam_obj.name))
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.signals = ControllerSig()
        self.cam_obj = cam_obj
        self.cam_thread = thread
        self.save_dir = ''
        self.timestamp = None
        self.exp = False
        self.cam_active = True
        self.logger.debug("Initialized")
        self.__setup_handlers()
        self.current_size = 0
        self.sizes = []
        self.populate_sizes()

    def cleanup(self):
        self.logger.debug("running")
        if not self.cam_active:
            self.toggle_cam()
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
            self.cam_thread.reading = not self.cam_thread.reading
            self.cam_active = not self.cam_active
            if self.cam_active:
                self.cam_thread.signals.wcond.wakeAll()
            self.cam_obj.toggle_activity()

    def populate_sizes(self):
        self.sizes.append((1920, 1080))
        self.sizes.append((1280, 1024))
        self.sizes.append((800, 600))

    def cycle_image_size(self):
        self.current_size = (self.current_size + 1) % len(self.sizes)
        self.cam_obj.set_image_size(self.sizes[self.current_size])

    def __setup_handlers(self):
        self.tab.add_use_cam_button_handler(self.toggle_cam)
        self.tab.next_button.clicked.connect(self.cycle_image_size)
