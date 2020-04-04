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
from time import time
from multiprocessing.connection import Connection
from queue import Queue
from Devices.Camera.Model.cam_size_getters import SizeGetterFixed, SizeGetterFlexible
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_frame_handler import FrameHandler
from Devices.Camera.Model.cam_defs import CEnum
from Devices.Camera.Model.cam_proc_frame_output import FrameOutputQueueThread


def run_camera(pipe: Connection, frame_output_pipe: Connection, index: int, flexi: bool = False):
    stream = StreamReader(index)
    frame_queue = Queue()
    frame_handler = FrameHandler(frame_queue)
    if flexi:
        size_getter = SizeGetterFlexible(stream, pipe)
    else:
        size_getter = SizeGetterFixed(stream, pipe)
    size_getter.start()
    size_getter_alive = True
    frame_sender = FrameOutputQueueThread(frame_output_pipe)
    running = False
    show_feed = True
    num_frames = 0
    checkpoint = time()
    try:
        while True:
            if pipe.poll():  # Check for and handle message from controller
                msg = pipe.recv()
                msg_type = msg[0]
                if msg_type == CEnum.ACTIVATE_CAM:
                    running = True
                    stream.start()
                    frame_handler.start()
                    frame_sender.start()
                elif msg_type == CEnum.DEACTIVATE_CAM:
                    running = False
                    stream.stop()
                    frame_handler.stop()
                    frame_sender.stop()
                elif msg_type == CEnum.START_SAVING:
                    frame_handler.set_writing(True, msg[1], stream.get_current_frame_size())
                elif msg_type == CEnum.STOP_SAVING:
                    name = frame_handler.set_writing(False)
                    pipe.send((CEnum.STOP_SAVING, name))
                elif msg_type == CEnum.GET_RESOLUTION:
                    pipe.send((CEnum.SET_RESOLUTION, stream.get_current_frame_size()))
                elif msg_type == CEnum.SET_RESOLUTION:
                    stream.change_frame_size(msg[1])
                elif msg_type == CEnum.GET_ROTATION:
                    pipe.send((CEnum.SET_ROTATION, frame_handler.rotate))
                elif msg_type == CEnum.SET_ROTATION:
                    frame_handler.rotate = msg[1]
                elif msg_type == CEnum.WORKER_DONE:
                    size_getter.wait()
                    size_getter_alive = False
                elif msg_type == CEnum.SHOW_FEED:
                    show_feed = msg[1]
                    frame_handler.showing_feed = msg[1]
                elif msg_type == CEnum.CLEANUP:
                    pipe.close()
                    break
            if running:
                if stream.failure:
                    pipe.send((CEnum.CAM_FAILED,))
                    break
                else:
                    ret, frame = stream.get_latest_frame()
                    if ret:  # Means we have a new frame.
                        frame_queue.put(frame)
                        num_frames += 1
                        new_checkpoint = time()
                        if new_checkpoint - checkpoint > 1:
                            pipe.send((CEnum.FPS_UPDATE, num_frames))
                            num_frames = 0
                            checkpoint = new_checkpoint
                if show_feed and not frame_handler.output_queue.empty():
                    frame_sender.frame = frame_handler.output_queue.get()
                    frame_sender.new_frame = True
    except BrokenPipeError as bpe:
        pass
    if size_getter_alive:
        size_getter.running = False
        size_getter.wait()
    stream.cleanup()
    frame_handler.cleanup()
    frame_sender.stop()
