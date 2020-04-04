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

from threading import Thread
from imutils import rotate
from queue import Queue
from datetime import datetime
from Devices.Camera.Model.cam_stream_writer import StreamWriter
from Model.app_helpers import take_a_moment


class FrameHandler:
    def __init__(self, input_queue: Queue):
        self.rotate = 0
        self.writing = False
        self.showing_feed = True
        self.input_queue = input_queue
        self.write_queue = Queue()
        self.output_queue = Queue()
        self.writer = StreamWriter(self.write_queue)
        self.t: Thread = Thread()
        self.running = True
        self.start_time = datetime.now()
        self.stop_time = self.start_time

    def cleanup(self):
        self.stop()
        self.writer.cleanup()

    def start(self):
        self.running = True
        self.t = Thread(target=self.__update, args=())
        self.t.start()

    def stop(self):
        self.running = False
        if self.t.is_alive():
            self.t.join()
        self.output_queue = Queue()

    def __update(self):
        while self.running:
            if not self.input_queue.empty():
                frame = self.input_queue.get()
                if self.rotate != 0:
                    frame = rotate(frame, self.rotate)
                if self.showing_feed:
                    self.output_queue.put(frame)
                if self.writing:
                    self.write_queue.put(frame)
            else:
                take_a_moment()

    def set_writing(self, is_active: bool, filename: str = '', size: (float, float) = (0.0, 0.0)):
        size = (int(size[0]), int(size[1]))
        if is_active:
            self.start_time = datetime.now()
            self.writer.start(filename, 30, size)
            self.writing = True
            return 0
        else:
            self.stop_time = datetime.now()
            self.writer.stop()
            self.writing = False
            return (self.stop_time - self.start_time).total_seconds()
