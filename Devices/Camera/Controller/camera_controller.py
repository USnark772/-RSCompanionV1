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
    cam_failed = Signal(int)
    send_msg_sig = Signal(tuple)

# TODO: Figure out how to best deal with larger frames causing lower fps.
# Is measuring fps at any given time a good option?
# Is waiting until file is written and then altering it to the proper fps a good option?
#  (Look into ffmpeg for this, seems like using opencv won't be a good idea)
# Maybe ffmpeg is a good option in place of opencv, maybe not.
# Do we want to just let the user control the fps? (Seems like an easy way out and not a good user experience)
# Actual fps will never be quite the same between machines because each machine will grab frames at different rates.
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
        except BrokenPipeError as e:
            pass
        if self.cam_worker.is_alive():
            self.cam_worker.join()
        self.logger.debug("done")

    def handle_pipe(self):
        msg = None
        try:
            if self.pipe.poll():
                msg = self.pipe.recv()
        except BrokenPipeError as e:
            self.logger.exception("Pipe failed")
            self.cleanup()
            return
        if msg:
            msg_type = msg[0]
            if msg_type == CEnum.WORKER_DONE:
                self.__complete_setup(msg[1])
            elif msg_type == CEnum.CAM_FAILED:
                self.signals.cam_failed.emit(self.index)
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
        self.pipe.send((CEnum.ACTIVATE_CAM,))
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

    def toggle_color(self):
        self.color_image = not self.color_image
        self.pipe.send((CEnum.SET_BW,))

    def set_rotation(self):
        new_rotation = self.tab.get_rotation()
        self.pipe.send((CEnum.SET_ROTATION, new_rotation))

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
        self.tab.add_color_toggle_button_handler(self.toggle_color)
        self.tab.add_frame_rotation_handler(self.set_rotation)
        self.logger.debug("done")

    def __get_initial_values(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.GET_RESOLUTION,))
        self.pipe.send((CEnum.GET_FPS,))
        self.logger.debug("done")

    def __set_tab_fps_val(self, value: int):
        self.tab.set_fps(self.__get_fps_val_index(value))

    # TODO: Fix the error with the value being (0, 0). (0, 0) seems to happen if VideoCapture object fails.
    def __set_tab_size_val(self, value: tuple):
        print(value)
        self.tab.set_frame_size(self.__get_size_val_index(value))

    def __set_tab_rot_val(self, value: int):
        self.tab.set_rotation(value)

    def __complete_setup(self, sizes: list):
        self.logger.debug("running")
        self.pipe.send((CEnum.WORKER_DONE,))
        self.__populate_sizes(sizes)
        self.__populate_fps_selections()
        self.__get_initial_values()
        self.pipe.send((CEnum.ACTIVATE_CAM,))
        self.tab.set_tab_active(True)
        self.logger.debug("done")

    def __get_size_val_index(self, value: tuple):
        for i in range(len(self.frame_sizes)):
            if self.frame_sizes[i][1] == value:
                return i

    def __get_fps_val_index(self, value: int):
        return self.fps_values.index((str(value), value))
