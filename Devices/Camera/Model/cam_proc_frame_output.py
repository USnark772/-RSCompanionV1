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
from multiprocessing.connection import Connection
from numpy import ndarray
from Model.app_helpers import take_a_moment


class FrameOutputQueueThread:
    def __init__(self, pipe: Connection):
        self.pipe = pipe
        self.running = False
        self.new_frame = False
        self.frame: ndarray = None
        self.t = Thread()

    def start(self):
        self.t = Thread(target=self.update, args=())
        self.running = True
        self.t.start()

    def cleanup(self):
        self.stop()
        self.pipe.close()

    def stop(self):
        if self.t.is_alive():
            self.running = False
            self.t.join()

    def update(self):
        try:
            while self.running:
                if self.new_frame:
                    self.pipe.send(self.frame)
                    self.new_frame = False
                else:
                    take_a_moment()
        except BrokenPipeError as bpe:
            pass
        except OSError as ose:
            pass
