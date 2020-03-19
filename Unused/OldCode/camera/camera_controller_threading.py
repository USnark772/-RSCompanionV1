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
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from threading import Lock
from PySide2.QtCore import QObject, Signal
from Unused.OldCode.camera.cam_obj_threading import CamObj
from Devices.abc_device_controller import ABCDeviceController
from Devices.Camera.View.camera_tab import CameraTab
from Unused.OldCode.camera.cam_threads import CamUpdater, SizeGetter

# TODO: Fix crash bug when changing cam3 res to higher than 1080p (unsupported resolutions) Some issue with threading
#  memory corruption.
#  Process finished with exit code -1073740940 (0xC0000374)
#  Process finished with exit code -1073741819 (0xC0000005)


class ControllerSig(QObject):
    settings_error = Signal(str)
    cam_failed = Signal(str)
    cam_closed = Signal(str, int)
    send_msg_sig = Signal(tuple)


class CameraController(ABCDeviceController):
    def __init__(self, index: int, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.index = index
        self.name = "CAM_" + str(index + 1)
        super().__init__(CameraTab(ch, name=self.name))
        self.cam_obj = CamObj(index, self.name, ch)
        self.cam_lock = Lock()
        self.size_getter = SizeGetter(self.cam_obj, self.cam_lock, ch)
        self.cam_updater = CamUpdater(self.cam_obj, self.cam_lock, ch)
        self.signals = ControllerSig()
        self.save_dir = ''
        self.timestamp = None
        self.cam_active = True
        self.feed_active = True
        self.color_image = True
        self.__setup_handlers()
        self.frame_sizes = []
        self.__add_loading_symbols_to_tab()
        self.size_getter.start()
        self.logger.debug("Initialized")

    def get_name(self) -> str:
        return self.name

    def cleanup(self):
        self.logger.debug("running")
        self.cam_obj.cleanup()
        self.cam_updater.stop = True
        self.cam_updater.wait()
        self.logger.debug("done")

    def create_new_save_file(self, new_filename: str):
        self.logger.debug("running")
        self.save_dir = new_filename
        self.logger.debug("done")

    def set_start_time(self, timestamp: str):
        self.logger.debug("running")
        self.timestamp = timestamp
        self.logger.debug("done")

    def start_exp(self):
        self.logger.debug("running")
        with self.cam_lock:
            self.cam_obj.start_writing(self.timestamp, self.save_dir)
        self.tab.set_tab_active(False)
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        with self.cam_lock:
            self.cam_obj.stop_writing()
        self.tab.set_tab_active(True)
        self.logger.debug("done")

    def __handle_cam_failure(self):
        self.signals.cam_failed.emit(self.name + " failed. Possible disconnect.")
        self.signals.cam_closed.emit(self.name, self.index)
        self.cleanup()

    def __toggle_bw(self):
        self.logger.debug("running")
        if self.color_image:
            self.cam_obj.set_bw(True)
        else:
            self.cam_obj.set_bw(False)
        self.color_image = not self.color_image
        self.logger.debug("done")

    def __setup_handlers(self):
        self.logger.debug("running")
        self.size_getter.signal.done_sig.connect(self.__complete_setup)
        self.cam_updater.signal.fail_sig.connect(self.__handle_cam_failure)
        self.tab.add_use_cam_button_handler(self.__toggle_cam)
        self.tab.add_frame_size_selector_handler(self.__set_frame_size)
        self.tab.add_settings_toggle_button_handler(self.__open_settings)
        self.tab.add_frame_rotation_handler(self.__rotation_entry_changed)
        self.tab.add_show_cam_button_handler(self.__toggle_show_feed)
        self.tab.add_bw_button_handler(self.__toggle_bw)
        self.logger.debug("done")

    def __complete_setup(self, sizes: list):
        self.logger.debug("running")
        self.size_getter.wait()
        self.__populate_sizes(sizes)
        self.__get_initial_values()
        self.cam_updater.start()
        self.tab.set_tab_active(True)
        self.logger.debug("done")

    def __toggle_cam(self):
        self.logger.debug("running")
        if self.cam_active:
            self.cam_updater.running = False
            self.tab.set_tab_active(False, toggle_toggler=False)
        else:
            self.cam_updater.running = True
            self.tab.set_tab_active(True, toggle_toggler=False)
        self.cam_active = not self.cam_active
        self.logger.debug("done")

    def __toggle_show_feed(self):
        self.logger.debug("running")
        self.feed_active = not self.feed_active
        with self.cam_lock:
            self.cam_obj.set_show_feed(self.feed_active)
        self.logger.debug("done")

    def __set_frame_size(self):
        self.logger.debug("running")
        new_size = self.tab.get_frame_size()
        with self.cam_lock:
            self.cam_obj.set_frame_size(new_size)
        self.logger.debug("done")

    def __open_settings(self):
        with self.cam_lock:
            self.cam_obj.open_settings_window()

    def __rotation_entry_changed(self):
        if self.__validate_rotation():
            new_rotation = int(self.tab.get_rotation())
            with self.cam_lock:
                self.cam_obj.set_rotation(new_rotation)
            self.tab.set_rotation_error(False)
        else:
            self.tab.set_rotation_error(True)

    def __validate_rotation(self):
        usr_input: str
        negative = False
        usr_input = self.tab.get_rotation()
        if len(usr_input) > 0 and usr_input[0] == '-':
            negative = True
            usr_input = usr_input[1:]
        if usr_input.isdigit():
            if negative:
                rot_value = 0 - int(usr_input)
                self.tab.set_rotation(str(rot_value % -360))
            else:
                rot_value = int(usr_input)
                self.tab.set_rotation(str(rot_value % 360))
            return True
        else:
            return False

    def __add_loading_symbols_to_tab(self):
        self.logger.debug("running")
        self.tab.add_item_to_size_selector("Initializing...")
        # self.tab.add_item_to_fps_selector("Initializing...")
        self.logger.debug("done")

    def __populate_sizes(self, sizes: list):
        self.logger.debug("running")
        self.tab.empty_size_selector()
        self.frame_sizes = sizes
        self.tab.populate_frame_size_selector(self.frame_sizes)
        self.logger.debug("done")

    def __get_initial_values(self):
        self.logger.debug("running")
        new_size = self.cam_obj.get_current_frame_size()
        new_rotation = self.cam_obj.get_current_rotation()
        self.__set_tab_size_val(new_size)
        self.__set_tab_rot_val(new_rotation)
        self.logger.debug("done")

    def __set_tab_size_val(self, value: tuple):
        self.tab.set_frame_size(self.__get_size_val_index(value))

    def __set_tab_rot_val(self, value: int):
        self.tab.set_rotation(str(value))

    def __get_size_val_index(self, value: tuple):
        for i in range(len(self.frame_sizes)):
            if self.frame_sizes[i][1] == value:
                return i
