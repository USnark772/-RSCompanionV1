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
from datetime import datetime
from multiprocessing import Process, Pipe, Value
from PySide2.QtCore import QObject, Signal
from Devices.abc_device_controller import ABCDeviceController
from Devices.Camera.View.camera_tab import CameraTab
from Devices.Camera.Controller.pipe_watcher import PipeWatcher
from Devices.Camera.Controller.cam_runner import run_camera, CEnum


class ControllerSig(QObject):
    settings_error = Signal(str)
    cam_failed = Signal(str)
    cam_closed = Signal(str)
    send_msg_sig = Signal(tuple)


class CameraController(ABCDeviceController):
    def __init__(self, index: int, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.index = index
        self.name = "CAM_" + str(index + 1)
        super().__init__(CameraTab(ch, name=self.name))
        self.pipe, proc_pipe = Pipe()
        self.pipe_watcher = PipeWatcher(self.pipe, ch)
        self.pipe_watcher.connect_to_sig(self.handle_pipe)
        self.pipe_watcher.start()
        self.proc_bool = Value('b', False)
        self.cam_worker = Process(target=run_camera, args=(proc_pipe, self.index, self.name,))
        self.cam_worker.start()
        self.signals = ControllerSig()
        self.save_dir = ''
        self.timestamp = None
        self.cam_active = True
        self.color_image = True
        self.__setup_handlers()
        self.current_size = 0
        self.frame_sizes = []
        self.fps_values = []
        self.__add_loading_symbols_to_tab()
        self.logger.debug("Initialized")

    def get_name(self) -> str:
        return self.name

    def cleanup(self):
        self.logger.debug("running")
        self.pipe_watcher.running = False
        self.pipe_watcher.wait()
        try:
            self.pipe.send((CEnum.CLEANUP,))
            self.pipe.close()
        except:
            pass
        if self.cam_worker.is_alive():
            self.cam_worker.join()
        self.logger.debug("done")

    def handle_pipe(self):
        msg = None
        try:
            if self.pipe.poll():
                msg = self.pipe.recv()
        except:
            self.logger.exception("Pipe failed")
            self.cleanup()
            return
        if msg:
            msg_type = msg[0]
            if msg_type == CEnum.WORKER_DONE:
                self.__complete_setup(msg[1])
            elif msg_type == CEnum.CAM_FAILED:
                self.signals.cam_failed.emit(self.name + " failed. Possible disconnect or other issue getting next"
                                                         " frame")
                self.signals.cam_closed.emit(self.name)
                self.cleanup()
            elif msg_type == CEnum.SET_RESOLUTION:
                self.__set_tab_size_val(msg[1])
            elif msg_type == CEnum.SET_FPS:
                self.__set_tab_fps_val(msg[1])
            elif msg_type == CEnum.SET_ROTATION:
                self.__set_tab_rot_val(msg[1])

    def create_new_save_file(self, new_filename: str):
        self.logger.debug("running")
        self.save_dir = new_filename
        self.logger.debug("done")

    def set_start_time(self, timestamp: datetime):
        self.logger.debug("running")
        self.timestamp = timestamp
        self.logger.debug("done")

    def start_exp(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.START_SAVING,))
        self.tab.set_controls_active(False)
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.STOP_SAVING,))
        self.tab.set_controls_active(True)
        self.logger.debug("done")

    def toggle_cam(self):
        self.logger.debug("running")
        if self.cam_active:
            self.pipe.send((CEnum.DEACTIVATE_CAM,))
        else:
            self.pipe.send((CEnum.ACTIVATE_CAM,))
        self.cam_active = not self.cam_active
        self.logger.debug("done")

    def set_frame_size(self):
        self.logger.debug("running")
        new_size = self.tab.get_frame_size()
        self.pipe.send((CEnum.SET_RESOLUTION, new_size))
        self.logger.debug("done")

    def set_fps(self):
        self.logger.debug("running")
        new_fps = self.tab.get_fps()
        self.pipe.send((CEnum.SET_FPS, new_fps))
        self.logger.debug("done")

    def open_settings(self):
        self.pipe.send((CEnum.OPEN_SETTINGS,))

    def __rotation_entry_changed(self):
        if self.__validate_rotation():
            new_rotation = int(self.tab.get_rotation())
            self.pipe.send((CEnum.SET_ROTATION, new_rotation))
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
        self.tab.add_item_to_fps_selector("Initializing...")
        self.logger.debug("done")

    def __populate_fps_selections(self):
        self.logger.debug("running")
        self.tab.empty_fps_selector()
        for i in range(11):
            self.fps_values.append((str(30 - i), 30-i))
        self.tab.populate_fps_selector(self.fps_values)
        self.logger.debug("done")

    def __populate_sizes(self, sizes: list):
        self.logger.debug("running")
        self.tab.empty_size_selector()
        self.frame_sizes = sizes
        self.tab.populate_frame_size_selector(self.frame_sizes)
        self.logger.debug("done")

    def __setup_handlers(self):
        self.logger.debug("running")
        self.tab.add_use_cam_button_handler(self.toggle_cam)
        self.tab.add_fps_selector_handler(self.set_fps)
        self.tab.add_frame_size_selector_handler(self.set_frame_size)
        self.tab.add_settings_toggle_button_handler(self.open_settings)
        self.tab.add_frame_rotation_handler(self.__rotation_entry_changed)
        self.logger.debug("done")

    def __get_initial_values(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.GET_RESOLUTION,))
        self.pipe.send((CEnum.GET_FPS,))
        self.logger.debug("done")

    def __set_tab_fps_val(self, value: int):
        self.tab.set_fps(self.__get_fps_val_index(value))

    def __set_tab_size_val(self, value: tuple):
        self.tab.set_frame_size(self.__get_size_val_index(value))

    def __set_tab_rot_val(self, value: int):
        self.tab.set_rotation(str(value))

    def __complete_setup(self, sizes: list):
        self.logger.debug("running")
        self.pipe.send((CEnum.WORKER_DONE,))
        self.__populate_sizes(sizes)
        self.__populate_fps_selections()
        self.__get_initial_values()
        self.pipe.send((CEnum.ACTIVATE_CAM,))
        self.pipe.send((CEnum.GET_ROTATION,))
        self.tab.set_tab_active(True)
        self.logger.debug("done")

    def __get_size_val_index(self, value: tuple):
        for i in range(len(self.frame_sizes)):
            if self.frame_sizes[i][1] == value:
                return i

    def __get_fps_val_index(self, value: int):
        return self.fps_values.index((str(value), value))
