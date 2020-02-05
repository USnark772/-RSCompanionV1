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
from PySide2.QtCore import QObject, Signal, QThread
from Devices.Camera.View.camera_tab import CameraTab
from Devices.abc_device_controller import ABCDeviceController
from Devices.Camera.Model.cam_obj import CamObj
import Unused.Tests.tracemalloc_helper as tracer


class ControllerSig(QObject):
    toggle_signal = Signal()
    settings_error = Signal(str)


class CameraController(ABCDeviceController):
    def __init__(self, cap, index, thread, ch):
        tracer.tracemalloc.start()
        tracer.display_top(tracer.tracemalloc.take_snapshot())
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.index = index
        self.cam_obj = CamObj(cap, "CAM_" + str(self.index), ch)
        super().__init__(CameraTab(name=self.cam_obj.name))
        self.signals = ControllerSig()
        self.cam_thread = thread
        self.cam_thread.signals.new_frame_sig.connect(self.cam_obj.handle_new_frame)
        self.save_dir = ''
        self.timestamp = None
        self.cam_active = True
        self.color_image = True
        self.reading = True
        self.__setup_handlers()
        self.current_size = 0
        self.frame_sizes = []
        self.fps_values = []
        self.cam_obj.signals.frame_size_fail_sig.connect(self.handle_resolution_error)
        self.__populate_sizes()
        self.__populate_fps_selections()
        self.__initialize_tab_values()
        self.cam_thread.start(priority=QThread.LowestPriority)
        self.logger.debug("Initialized")
        tracer.display_top(tracer.tracemalloc.take_snapshot())

    def get_name(self):
        return self.cam_obj.name

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
        self.tab.set_controls_active(False)
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.cam_obj.destroy_writer()
        self.tab.set_controls_active(True)
        self.logger.debug("done")

    def toggle_cam(self):
        self.logger.debug("running")
        self.cam_active = not self.cam_active
        self.cam_thread.reading = self.cam_active
        if self.cam_active:
            self.cam_thread.signals.wcond.wakeAll()
        self.cam_obj.toggle_activity()
        self.logger.debug("done")

    def set_frame_size(self):
        self.logger.debug("running")
        new_size = self.tab.get_frame_size()
        self.cam_obj.set_frame_size((int(new_size[0]), int(new_size[1])))
        self.logger.debug("done")

    # TODO: Alert user to failure?
    def handle_resolution_error(self):
        new_size = self.cam_obj.get_current_frame_size()
        size_index = self.__get_size_val_index(new_size)
        self.tab.set_frame_size(size_index)
        self.signals.settings_error.emit("Invalid resolution setting for this camera. Resolution set to: "
                                         + str(new_size))

    def set_fps(self):
        self.logger.debug("running")
        self.cam_obj.set_fps(self.tab.get_fps())
        self.logger.debug("done")

    def toggle_color(self):
        self.color_image = not self.color_image
        self.cam_obj.set_use_color(self.color_image)

    def set_rotation(self):
        new_rotation = self.tab.get_rotation()
        self.cam_obj.set_rotation(new_rotation)

    def __populate_fps_selections(self):
        self.logger.debug("running")
        for i in range(11):
            self.fps_values.append((str(30 - i), 30-i))
        self.tab.populate_fps_selector(self.fps_values)
        self.logger.debug("done")

    def __populate_sizes(self):
        self.logger.debug("running")

        initial_size = self.cam_obj.get_current_frame_size()
        large_size = (4000, 4000)
        step = 100
        self.cam_obj.set_frame_size(large_size)
        max_size = self.cam_obj.get_current_frame_size()
        current_size = initial_size

        while current_size[0] <= max_size[0]:
            self.cam_obj.set_frame_size(current_size)
            result = self.cam_obj.get_current_frame_size()
            new_tup = (str(result[0]) + ", " + str(result[1]), result)
            if new_tup not in self.frame_sizes:
                self.frame_sizes.append(new_tup)
            new_x = current_size[0] + step
            new_y = current_size[1] + step
            if result[0] > new_x:
                new_x = result[0] + step
            if result[1] > new_y:
                new_y = result[1] + step
            current_size = (new_x, new_y)

        self.cam_obj.set_frame_size(initial_size)

        # self.frame_sizes.append(('1920, 1440', (2304, 1536)))
        # self.frame_sizes.append(('1920, 1440', (1920, 1440)))
        # self.frame_sizes.append(('1920, 1080', (1920, 1080)))
        # self.frame_sizes.append(('1600, 900', (1600, 896)))
        # self.frame_sizes.append(('1280, 720', (1280, 720)))
        # self.frame_sizes.append(('1960, 720', (960, 720)))
        # self.frame_sizes.append(('640, 480', (640, 640)))
        # self.frame_sizes.append(('640, 480', (640, 480)))

        # self.frame_sizes.append(('1920, 1280', (1920, 1280)))
        # self.frame_sizes.append(('1920, 1200', (1920, 1200)))
        # self.frame_sizes.append(('1856, 1392', (1856, 1392)))
        # self.frame_sizes.append(('1792, 1344', (1792, 1344)))
        # self.frame_sizes.append(('1680, 1050', (1680, 1050)))
        # self.frame_sizes.append(('1600, 1200', (1600, 1200)))
        # self.frame_sizes.append(('1600, 900', (1600, 900)))
        # self.frame_sizes.append(('1440, 1050', (1440, 1050)))
        # self.frame_sizes.append(('1440, 900', (1440, 900)))
        # self.frame_sizes.append(('1366, 768', (1366, 768)))
        # self.frame_sizes.append(('1360, 768', (1360, 768)))
        # self.frame_sizes.append(('1280, 1024', (1280, 1024)))
        # self.frame_sizes.append(('1280, 960', (1280, 960)))
        # self.frame_sizes.append(('1280, 800', (1280, 800)))
        # self.frame_sizes.append(('1280, 768', (1280, 768)))
        # self.frame_sizes.append(('1152, 864', (1152, 864)))
        # self.frame_sizes.append(('1024, 768', (1024, 768)))
        # self.frame_sizes.append(('1960, 720', (960, 720)))
        # self.frame_sizes.append(('800, 600', (800, 600)))
        self.tab.populate_frame_size_selector(self.frame_sizes)
        self.logger.debug("done")

    def __setup_handlers(self):
        self.logger.debug("running")
        self.tab.add_use_cam_button_handler(self.toggle_cam)
        self.tab.add_fps_selector_handler(self.set_fps)
        self.tab.add_frame_size_selector_handler(self.set_frame_size)
        self.tab.add_color_toggle_button_handler(self.toggle_color)
        self.tab.add_frame_rotation_handler(self.set_rotation)
        self.logger.debug("done")

    def __initialize_tab_values(self):
        rotation_val = self.cam_obj.get_current_rotation()
        fps_val = self.cam_obj.get_current_fps()
        size_val = self.cam_obj.get_current_frame_size()
        self.tab.set_rotation(rotation_val)
        self.tab.set_fps(self.__get_fps_val_index(fps_val))
        self.tab.set_frame_size(self.__get_size_val_index(size_val))

    # TODO: handle x not in list.
    def __get_size_val_index(self, value):
        for i in range(len(self.frame_sizes)):
            if self.frame_sizes[i][1] == value:
                return i

    def __get_fps_val_index(self, value):
        return self.fps_values.index((str(value), value))