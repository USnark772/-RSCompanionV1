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
from Model.general_defs import cap_backend

class CamCounter:
    def __init__(self, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.lock = QMutex()
        self.count = 0
        self.logger.debug("Initialized")

    def get_lock(self):
        # self.logger.debug("running")
        self.lock.lock()
        # self.logger.debug("done")

    def release_lock(self):
        # self.logger.debug("running")
        self.lock.unlock()
        # self.logger.debug("done")

    def get_count(self):
        return self.count

    def increment_count(self):
        self.logger.debug("running")
        self.count += 1
        self.logger.debug("done")

    def decrement_count(self):
        self.logger.debug("running")
        self.count -= 1
        if self.count < 0:
            self.count = 0
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
    # TODO: Put loop back when done testing.
    def run(self):
        self.logger.debug("running")
        while self.running:
            self.__check_for_cams(self.__get_index())
        self.logger.debug("done")

    def __get_index(self):
        # self.logger.debug("running")
        self.cam_counter.get_lock()
        i = self.cam_counter.get_count()
        self.cam_counter.release_lock()
        # self.logger.debug("done")
        return i

    def __check_for_cams(self, index: int = 0):
        # self.logger.debug("running")
        while self.running:
            cap = cv2.VideoCapture(index, cap_backend)
            if cap is None or not cap.isOpened():
                break
            else:
                cap.release()
                self.__increment_cam_count()
                self.signal.new_cam_sig.emit(index)
                index += 1
        # self.logger.debug("done")

    def __increment_cam_count(self):
        self.logger.debug("running")
        self.cam_counter.get_lock()
        self.cam_counter.increment_count()
        self.cam_counter.release_lock()
        self.logger.debug("done")


class ScannerSig(QObject):
    new_cam_sig = Signal(int)


class CamConManSig(QObject):
    new_cam_sig = Signal(int)


# TODO: Figure out how to number cameras better. If a camera fails and then plugs in again
#  then it could override a cam that is currently plugged in under the same index.
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
        self.cleanup()

    def activate(self):
        self.active = True
        self.scanner_thread = CamScanner(self.cam_counter, self.ch)
        self.scanner_thread.signal.new_cam_sig.connect(self.handle_new_camera)
        self.scanner_thread.start(priority=QThread.LowestPriority)

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

    def decrement_cam_count(self):
        self.cam_counter.decrement_count()
