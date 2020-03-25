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


# import logging
from multiprocessing.connection import Connection
from enum import Enum, auto
from PySide2.QtCore import QThread
from CompanionLib.companion_helpers import take_a_moment
from Devices.Camera.Model.cam_obj import CamObj

list_of_common_sizes = \
    [
        (640.0, 480.0),
        (640.0, 640.0),
        (800.0, 600.0),
        (960.0, 720.0),
        (1024.0, 768.0),
        (1248.0, 1536.0),
        (1280.0, 720.0),
        (1280.0, 960.0),
        (1440.0, 1080.0),
        (1600.0, 900.0),
        (1600.0, 1200.0),
        (1920.0, 1080.0),
        # (2048.0, 1536.0),
        # (2560.0, 1440.0),
        # (3840.0, 2160.0),
    ]


class CEnum(Enum):
    WORKER_MAX_TRIES = auto()
    WORKER_STATUS_UPDATE = auto()
    WORKER_DONE = auto()
    SAVE_STATUS_UPDATE = auto()
    CAM_FAILED = auto()
    OPEN_SETTINGS = auto()
    GET_RESOLUTION = auto()
    SET_RESOLUTION = auto()
    GET_FPS = auto()
    SET_FPS = auto()
    GET_BW = auto()
    SET_BW = auto()
    GET_ROTATION = auto()
    SET_ROTATION = auto()
    ACTIVATE_CAM = auto()
    DEACTIVATE_CAM = auto()
    SHOW_FEED = auto()
    HIDE_FEED = auto()
    START_SAVING = auto()
    STOP_SAVING = auto()
    CLEANUP = auto()


class SizeGetterFixed(QThread):
    def __init__(self, cam_obj: CamObj, pipe: Connection):
        QThread.__init__(self)
        self.cam_obj = cam_obj
        self.pipe = pipe
        self.running = True

    def run(self):
        self.setPriority(QThread.HighestPriority)
        sizes = []
        initial_size = self.cam_obj.get_current_frame_size()
        if initial_size in list_of_common_sizes:
            new_tup = (str(initial_size[0]) + ", " + str(initial_size[1]), initial_size)
            sizes.append(new_tup)
        list_index = list_of_common_sizes.index(initial_size) + 1
        try:
            self.pipe.send((CEnum.WORKER_MAX_TRIES, len(list_of_common_sizes) - list_index))
        except BrokenPipeError as e:
            return
        while list_index < len(list_of_common_sizes) and self.running:
            self.cam_obj.set_frame_size(list_of_common_sizes[list_index])
            result = self.cam_obj.get_current_frame_size()
            if result in list_of_common_sizes:
                new_tup = (str(result[0]) + ", " + str(result[1]), result)
                if new_tup not in sizes:
                    sizes.append(new_tup)
            list_index += 1
            try:
                self.pipe.send((CEnum.WORKER_STATUS_UPDATE, len(list_of_common_sizes) - list_index))
            except BrokenPipeError as e:
                return
            take_a_moment()
        if self.running:
            self.cam_obj.fourcc_bool = True
            self.cam_obj.set_frame_size(initial_size)
            try:
                self.pipe.send((CEnum.WORKER_DONE, sizes))
            except BrokenPipeError as e:
                return


class SizeGetterFlexible(QThread):
    def __init__(self, cam_obj: CamObj, pipe: Connection):
        QThread.__init__(self)
        self.cam_obj = cam_obj
        self.pipe = pipe
        self.running = True

    def run(self):
        self.setPriority(QThread.HighestPriority)
        sizes = []
        initial_size = self.cam_obj.get_current_frame_size()
        new_tup = (str(initial_size[0]) + ", " + str(initial_size[1]), initial_size)
        sizes.append(new_tup)
        large_size = (8000, 8000)
        step = 100
        self.cam_obj.set_frame_size(large_size)
        max_size = self.cam_obj.get_current_frame_size()
        max_tries = (max_size[0] - initial_size[0]) / step
        try:
            self.pipe.send((CEnum.WORKER_MAX_TRIES, max_tries))
        except BrokenPipeError as e:
            return
        current_size = (initial_size[0] + step, initial_size[1] + step)
        while current_size[0] <= max_size[0] and self.running:
            self.cam_obj.set_frame_size(current_size)
            result = self.cam_obj.get_current_frame_size()
            new_tup = (str(result[0]) + ", " + str(result[1]), result)
            if new_tup not in sizes:
                sizes.append(new_tup)
            new_x = current_size[0] + step
            new_y = current_size[1] + step
            if result[0] > new_x:
                new_x = result[0] + step
            if result[1] > new_y:
                new_y = result[1] + step
            current_size = (new_x, new_y)
            tries_left = (max_size[0] - current_size[0]) / step
            try:
                self.pipe.send((CEnum.WORKER_STATUS_UPDATE, tries_left))
            except BrokenPipeError as e:
                break
            take_a_moment()
        if self.running:
            self.cam_obj.fourcc_bool = True
            self.cam_obj.set_frame_size(initial_size)
            try:
                self.pipe.send((CEnum.WORKER_DONE, sizes))
            except BrokenPipeError as e:
                return


# TODO: Figure out if/how possible to add logging here
def run_camera(pipe: Connection, index: int, name: str, flexi: bool = False, frame_sig_handler: classmethod = None,
               fps_sig_handler: classmethod = None):  # , ch: logging.Handler):
    # logger = logging.getLogger(__name__)
    # logger.addHandler(ch)
    # logger.debug("Initializing")
    cam_obj = CamObj(index, name)  #, ch)
    # TODO: These signals will need to be redone for multiprocessing.
    if frame_sig_handler:
        cam_obj.signal.new_frame_sig.connect(frame_sig_handler)
    if fps_sig_handler:
        cam_obj.signal.fps_sig.connect(fps_sig_handler)
    if flexi:
        size_getter = SizeGetterFlexible(cam_obj, pipe)
    else:
        size_getter = SizeGetterFixed(cam_obj, pipe)
    size_getter.start()
    size_getter_alive = True
    running = False
    # logger.debug("Initialized")
    # logger.debug("running")
    while True:
        try:
            if pipe.poll():  # Check for and handle message from controller
                msg = pipe.recv()
                msg_type = msg[0]
                if msg_type == CEnum.ACTIVATE_CAM:
                    running = True
                elif msg_type == CEnum.DEACTIVATE_CAM:
                    running = False
                    cam_obj.close_window()
                elif msg_type == CEnum.WORKER_DONE:
                    size_getter.wait()
                    size_getter_alive = False
                elif msg_type == CEnum.CLEANUP:
                    if size_getter_alive:
                        size_getter.running = False
                        size_getter.wait()
                    cam_obj.cleanup()
                    pipe.close()
                    break
                else:
                    handle_pipe(msg, cam_obj, pipe)
        except BrokenPipeError as e:
            cam_obj.cleanup()
            if size_getter_alive:
                size_getter.running = False
                size_getter.wait()
            break
        if running:  # Get and handle frame from camera
            if not cam_obj.update():
                if size_getter_alive:
                    size_getter.running = False
                    size_getter.wait()
                pipe.send((CEnum.CAM_FAILED,))
                cam_obj.cleanup()
                break
    # logger.debug("done")


def handle_pipe(msg: tuple, cam_obj: CamObj, pipe: Connection):
    msg_type = msg[0]
    if msg_type == CEnum.SHOW_FEED:
        cam_obj.set_show_feed(True)
    elif msg_type == CEnum.HIDE_FEED:
        cam_obj.set_show_feed(False)
    elif msg_type == CEnum.OPEN_SETTINGS:
        cam_obj.open_settings_window()
    elif msg_type == CEnum.GET_RESOLUTION:
        pipe.send((CEnum.SET_RESOLUTION, cam_obj.get_current_frame_size()))
    elif msg_type == CEnum.SET_RESOLUTION:
        cam_obj.set_frame_size(msg[1])
    elif msg_type == CEnum.GET_ROTATION:
        pipe.send((CEnum.SET_ROTATION, cam_obj.get_current_rotation()))
    elif msg_type == CEnum.SET_ROTATION:
        cam_obj.set_rotation(msg[1])
    elif msg_type == CEnum.GET_FPS:
        pipe.send((CEnum.SET_FPS, cam_obj.get_current_fps()))
    elif msg_type == CEnum.SET_FPS:
        cam_obj.set_fps(msg[1])
    elif msg_type == CEnum.START_SAVING:
        cam_obj.start_writing(msg[1], msg[2])
    elif msg_type == CEnum.STOP_SAVING:
        cam_obj.stop_writing()
        pipe.send((CEnum.STOP_SAVING, cam_obj.temp_save_file, cam_obj.save_file, cam_obj.total_secs))
    elif msg_type == CEnum.GET_BW:
        pipe.send((CEnum.SET_BW, cam_obj.get_bw()))
    elif msg_type == CEnum.SET_BW:
        cam_obj.set_bw(msg[1])
