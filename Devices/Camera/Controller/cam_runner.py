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
import cv2
from multiprocessing.connection import Connection
from enum import Enum, auto
from PySide2.QtCore import QThread
from Devices.Camera.Model.cam_obj import CamObj


class CEnum(Enum):
    WORKER_DONE = auto()
    CAM_FAILED = auto()
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
    START_SAVING = auto()
    STOP_SAVING = auto()
    CLEANUP = auto()


class SizeGetter(QThread):
    def __init__(self, cam_obj: CamObj, pipe: Connection):
        QThread.__init__(self)
        self.cam_obj = cam_obj
        self.pipe = pipe
        self.running = True

    def run(self):
        sizes = []
        initial_size = self.cam_obj.get_current_frame_size()
        new_tup = (str(initial_size[0]) + ", " + str(initial_size[1]), initial_size)
        sizes.append(new_tup)
        large_size = (3000, 3000)
        step = 100
        self.cam_obj.set_frame_size(large_size)
        max_size = self.cam_obj.get_current_frame_size()
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
        if self.running:
            self.cam_obj.set_frame_size(initial_size)
            self.pipe.send((CEnum.WORKER_DONE, sizes))

# TODO: Figure out if/how possible to add logging here
def run_camera(pipe: Connection, index: int, name: str):  # , ch: logging.Handler):
    # logger = logging.getLogger(__name__)
    # logger.addHandler(ch)
    # logger.debug("Initializing")
    cam_obj = CamObj(index, name)  #, ch)
    size_getter = SizeGetter(cam_obj, pipe)
    size_getter.start()
    size_getter_alive = True
    running = False
    # logger.debug("Initialized")
    # logger.debug("running")
    # pipe.send((CEnum.WORKER_DONE, [("(640, 480)", (640, 480))]))
    while True:
        try:
            if pipe.poll():  # Check for and handle message from controller
                msg = pipe.recv()
                msg_type = msg[0]
                if msg_type == CEnum.ACTIVATE_CAM:
                    running = True
                elif msg_type == CEnum.DEACTIVATE_CAM:
                    running = False
                elif msg_type == CEnum.WORKER_DONE:
                    size_getter.wait()
                    size_getter_alive = False
                elif msg_type == CEnum.CLEANUP:
                    if size_getter_alive:
                        size_getter.running = False
                        size_getter.wait()
                    pipe.close()
                    cam_obj.cleanup()
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
            ret, frame = cam_obj.read_camera()
            if ret and frame is not None:
                cam_obj.handle_new_frame(frame)
                cv2.waitKey(1)  # Required for frame to appear
            else:  # Camera failed, cleanup.
                if size_getter_alive:
                    size_getter.running = False
                    size_getter.wait()
                pipe.send((CEnum.CAM_FAILED,))
                cam_obj.cleanup()
                break
    # logger.debug("done")


def handle_pipe(msg: tuple, cam_obj: CamObj, pipe: Connection):
    msg_type = msg[0]
    if msg_type == CEnum.GET_RESOLUTION:
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
        cam_obj.setup_writer(msg[1], msg[2])
    elif msg_type == CEnum.STOP_SAVING:
        cam_obj.destroy_writer()
    elif msg_type == CEnum.GET_BW:
        pipe.send((CEnum.SET_BW, False))  # replace False with cam_obj.get_bw()
    elif msg_type == CEnum.SET_BW:
        pass  # cam_obj.set_bw(msg[1])