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
        self.__setup_handlers()
        self.current_size = 0
        self.frame_sizes = []
        self.fps_values = []
        self.__populate_sizes()
        self.__populate_fps_selections()
        self.logger.debug("Initialized")

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
        self.logger.debug("running")
        self.timestamp = timestamp
        self.logger.debug("done")

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
        self.logger.debug("running")
        if not self.exp:
            self.cam_thread.reading = not self.cam_thread.reading
            self.cam_active = not self.cam_active
            if self.cam_active:
                self.cam_thread.signals.wcond.wakeAll()
            self.cam_obj.toggle_activity()
        self.logger.debug("done")

    def set_frame_size(self):
        self.logger.debug("running")
        if not self.exp:
            new_size = self.tab.get_frame_size()
            self.cam_obj.set_frame_size((int(new_size[0]), int(new_size[1])))
        else:
            old_size = str(self.cam_obj.get_current_frame_size())
            old_size = old_size.strip('(')
            old_size = old_size.rstrip(')')
            index = self.frame_sizes.index(old_size)
            self.tab.set_frame_size_selector(index)
        self.logger.debug("done")

    def set_fps(self):
        self.logger.debug("running")
        if not self.exp:
            self.cam_obj.set_fps(self.tab.get_fps())
        else:
            index = self.fps_values.index(str(self.cam_obj.get_current_fps()))
            self.tab.set_fps_selector(index)
        self.logger.debug("done")

    def __populate_fps_selections(self):
        self.logger.debug("running")
        for i in range(11):
            self.fps_values.append(str(30 - i))
        self.tab.populate_fps_selector(self.fps_values)
        self.logger.debug("done")

    def __populate_sizes(self):
        self.logger.debug("running")
        self.frame_sizes.append('1920, 1080')
        self.frame_sizes.append('1280, 1024')
        self.frame_sizes.append('800, 600')
        self.frame_sizes.append('640, 480')
        self.tab.populate_frame_size_selector(self.frame_sizes)
        self.logger.debug("done")

    def __setup_handlers(self):
        self.logger.debug("running")
        self.tab.add_use_cam_button_handler(self.toggle_cam)
        self.tab.add_fps_selector_handler(self.set_fps)
        self.tab.add_frame_size_selector_handler(self.set_frame_size)
        self.logger.debug("done")
