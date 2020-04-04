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
import cv2
from PySide2.QtCore import QThread, QObject, QMutex, Signal
from Model.app_helpers import take_a_moment
from Devices.Camera.Model.cam_defs import cap_backend


class CamCounter:
    def __init__(self, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.lock = QMutex()
        self.count = 0
        self.indicies = []
        self.logger.debug("Initialized")

    def reset(self):
        self.count = 0
        self.indicies = []

    def get_lock(self):
        # self.logger.debug("running")
        self.lock.lock()
        # self.logger.debug("done")

    def release_lock(self):
        # self.logger.debug("running")
        self.lock.unlock()
        # self.logger.debug("done")

    def get_next_index(self):
        if len(self.indicies) > 0:
            return self.find_missing()[0]
        else:
            return 0

    def find_missing(self):
        ret = sorted(set(range(0, self.indicies[-1] + 2)) - set(self.indicies))
        return ret

    def add_index(self, index):
        self.logger.debug("running")
        self.indicies.append(index)
        self.indicies.sort()
        self.logger.debug("done")

    def remove_index(self, index):
        self.logger.debug("running")
        self.indicies.remove(index)
        self.logger.debug("done")


class CamScanner(QThread):
    def __init__(self, counter: CamCounter, ch: logging.Handler):
        self.ch = ch
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        QThread.__init__(self)
        self.signal = ScannerSig()
        self.cam_counter = counter
        self.running = True
        self.logger.debug("Initialized")

    # Try to connect new cam from latest index and up
    def run(self):
        self.logger.debug("running")
        self.setPriority(QThread.LowestPriority)
        while self.running:
            self.__check_for_cams(self.__get_index())
            take_a_moment()
        self.logger.debug("done")

    def __get_index(self):
        # self.logger.debug("running")
        self.cam_counter.get_lock()
        i = self.cam_counter.get_next_index()
        self.cam_counter.release_lock()
        # self.logger.debug("done")
        return i

    def __check_for_cams(self, index: int = 0):
        # self.logger.debug("running")
        cap = cv2.VideoCapture(index, cap_backend)
        if cap and cap.isOpened():
            cap.release()
            self.__increment_cam_count(index)
            self.signal.new_cam_sig.emit(index)
        # self.logger.debug("done")

    def __increment_cam_count(self, index):
        self.logger.debug("running")
        self.cam_counter.get_lock()
        self.cam_counter.add_index(index)
        self.cam_counter.release_lock()
        self.logger.debug("done")


class ScannerSig(QObject):
    new_cam_sig = Signal(int)


class CamConManSig(QObject):
    new_cam_sig = Signal(int)


class CameraConnectionManager:
    def __init__(self, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.ch = ch
        self.signals = CamConManSig()
        self.cam_counter = CamCounter(ch)
        self.scanner_thread = None
        self.active = False
        self.logger.debug("Initialized")

    def deactivate(self):
        self.active = False
        self.cam_counter.reset()
        self.cleanup()

    def activate(self):
        self.active = True
        self.scanner_thread = CamScanner(self.cam_counter, self.ch)
        self.scanner_thread.signal.new_cam_sig.connect(self.handle_new_camera)
        self.scanner_thread.start()

    def cleanup(self):
        self.logger.debug("running")
        if self.scanner_thread:
            self.scanner_thread.running = False
            self.scanner_thread.wait()
            self.scanner_thread = None
        self.logger.debug("done")

    def handle_new_camera(self, index: int):
        self.logger.debug("running")
        self.signals.new_cam_sig.emit(index)
        self.logger.debug("done")

    def decrement_cam_count(self, index):
        self.cam_counter.get_lock()
        self.cam_counter.remove_index(index)
        self.cam_counter.release_lock()
