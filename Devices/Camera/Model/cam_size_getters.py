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


from multiprocessing.connection import Connection
from PySide2.QtCore import QThread
from Devices.Camera.Model.cam_stream_reader import StreamReader
from Devices.Camera.Model.cam_defs import CEnum, list_of_common_sizes
from Model.app_helpers import take_a_moment


class SizeGetterFixed(QThread):
    def __init__(self, stream: StreamReader, pipe: Connection):
        QThread.__init__(self)
        self.stream = stream
        self.pipe = pipe
        self.running = True

    def run(self):
        self.setPriority(QThread.HighestPriority)
        sizes = []
        initial_size = self.stream.get_current_frame_size()
        if initial_size in list_of_common_sizes:
            new_tup = (str(initial_size[0]) + ", " + str(initial_size[1]), initial_size)
            sizes.append(new_tup)
        list_index = list_of_common_sizes.index(initial_size) + 1
        try:
            self.pipe.send((CEnum.WORKER_MAX_TRIES, len(list_of_common_sizes) - list_index))
        except BrokenPipeError as e:
            return
        except OSError as ose:
            return
        while list_index < len(list_of_common_sizes) and self.running:
            ret, result = self.stream.test_frame_size(list_of_common_sizes[list_index])
            if ret and result in list_of_common_sizes:
                new_tup = (str(result[0]) + ", " + str(result[1]), result)
                if new_tup not in sizes:
                    sizes.append(new_tup)
            list_index += 1
            try:
                self.pipe.send((CEnum.WORKER_STATUS_UPDATE, len(list_of_common_sizes) - list_index))
            except BrokenPipeError as bpe:
                return
            except OSError as ose:
                return
            take_a_moment()
        if self.running:
            # self.stream.fourcc_bool = True
            self.stream.change_frame_size(initial_size)
            try:
                self.pipe.send((CEnum.WORKER_DONE, sizes))
            except BrokenPipeError as e:
                return
            except OSError as ose:
                return


class SizeGetterFlexible(QThread):
    def __init__(self, stream: StreamReader, pipe: Connection):
        QThread.__init__(self)
        self.stream = stream
        self.pipe = pipe
        self.running = True

    def run(self):
        self.setPriority(QThread.HighestPriority)
        sizes = []
        initial_size = self.stream.get_current_frame_size()
        new_tup = (str(initial_size[0]) + ", " + str(initial_size[1]), initial_size)
        sizes.append(new_tup)
        large_size = (8000, 8000)
        step = 100
        ret, max_size = self.stream.test_frame_size(large_size)
        max_tries = (max_size[0] - initial_size[0]) / step
        try:
            self.pipe.send((CEnum.WORKER_MAX_TRIES, max_tries))
        except BrokenPipeError as e:
            return
        current_size = (initial_size[0] + step, initial_size[1] + step)
        while current_size[0] <= max_size[0] and self.running:
            ret, result = self.stream.test_frame_size(current_size)
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
            # self.stream.fourcc_bool = True
            self.stream.change_frame_size(initial_size)
            try:
                self.pipe.send((CEnum.WORKER_DONE, sizes))
            except BrokenPipeError as e:
                return
