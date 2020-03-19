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
from threading import Lock
from PySide2.QtCore import QObject, Signal, QThread
from Unused.OldCode.camera.cam_obj_threading import CamObj
from CompanionLib.companion_helpers import take_a_moment


class CamUpdaterSig(QObject):
    fail_sig = Signal()


class CamUpdater(QThread):
    def __init__(self, cam: CamObj, cam_lock: Lock, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        QThread.__init__(self)
        self.signal = CamUpdaterSig()
        self.running = True
        self.stop = False
        self.cam = cam
        self.lock = cam_lock
        self.logger.debug("Initialized")

    def run(self):
        self.logger.debug("running")
        self.setPriority(QThread.LowPriority)
        while True:
            if self.stop:
                break
            if self.running:
                with self.lock:
                    if not self.cam.update():
                        self.signal.fail_sig.emit()
                        break
            else:
                self.cam.close_window()
                # take_a_moment()
        self.logger.debug("done")


class SizeGetterSig(QObject):
    done_sig = Signal(list)


class SizeGetter(QThread):
    def __init__(self, cam_obj: CamObj, cam_lock: Lock, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        QThread.__init__(self)
        self.cam_obj = cam_obj
        self.lock = cam_lock
        self.signal = SizeGetterSig()
        self.running = True
        self.logger.debug("Initialized")

    def run(self):
        self.setPriority(QThread.HighestPriority)
        with self.lock:
            sizes = []
            initial_size = self.cam_obj.get_current_frame_size()
            new_tup = (str(initial_size[0]) + ", " + str(initial_size[1]), initial_size)
            sizes.append(new_tup)
            large_size = (8000, 8000)
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
                take_a_moment()
            if self.running:
                self.cam_obj.fourcc_bool = True
                self.cam_obj.set_frame_size(initial_size)
                self.signal.done_sig.emit(sizes)
