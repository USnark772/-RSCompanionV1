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
from numpy import ndarray
from PySide2.QtCore import QThread, QObject, QMutex, Signal, QWaitCondition
from Devices.Camera.Model.cam_obj import CamObj


class CamWorker(QThread):
    def __init__(self, cam, cam_counter, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        QThread.__init__(self)
        self.signals = WorkerSig()
        self.cam = cam
        self.cam_counter = cam_counter
        self.running = True
        self.reading = True
        self.logger.debug("Initialized")

    def run(self):
        self.logger.debug("running")
        while self.running:
            self.signals.lock.lock()
            if not self.reading:
                self.signals.wcond.wait(self.signals.lock)
            self.signals.lock.unlock()
            ret, frame = self.cam.read_camera()
            if ret:
                self.signals.new_frame_sig.emit(frame)
            else:
                # Lost connection to camera.
                break
        self.cleanup()
        self.logger.debug("done")

    def cleanup(self):
        self.logger.debug("running")
        self.running = False
        self.cam_counter.get_lock()
        self.cam_counter.decrement_count()
        self.cam_counter.release_lock()
        self.signals.cleanup_sig.emit(self.cam)
        self.logger.debug("done")

    def toggle(self):
        self.reading = not self.reading


class WorkerSig(QObject):
    new_frame_sig = Signal(ndarray)
    cleanup_sig = Signal(CamObj)
    wcond = QWaitCondition()
    lock = QMutex()


class CamScanner(QThread):
    def __init__(self, counter, ch):
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

    def __check_for_cams(self, index=0):
        # self.logger.debug("running")
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap is None or not cap.isOpened():
                break
            else:
                cam_obj = CamObj(cap, "CAM_" + str(index + 1), self.ch)
                self.__increment_cam_count()
                self.signal.new_cam_sig.emit(cam_obj)
            index += 1
        # self.logger.debug("done")

    def __increment_cam_count(self):
        self.logger.debug("running")
        self.cam_counter.get_lock()
        self.cam_counter.increment_count()
        self.cam_counter.release_lock()
        self.logger.debug("done")


class ScannerSig(QObject):
    new_cam_sig = Signal(CamObj)


class CamCounter:
    def __init__(self, ch):
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
        self.logger.debug("done")


class CamConManSig(QObject):
    new_cam_sig = Signal(CamObj, classmethod)
    disconnect_sig = Signal(CamObj)


class CameraConnectionManager:
    def __init__(self, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.ch = ch
        self.signals = CamConManSig()
        self.cam_list = []
        self.worker_thread_list = []
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
        self.scanner_thread.start()

    def cleanup(self):
        self.logger.debug("running")
        if self.scanner_thread:
            self.scanner_thread.running = False
            self.scanner_thread.wait()
            self.scanner_thread = None
        for worker in self.worker_thread_list:
            worker.running = False
            worker.wait()
        for cam in self.cam_list:
            cam.cleanup()
        self.logger.debug("done")

    def handle_new_camera(self, cam_obj):
        self.logger.debug("running")
        self.cam_list.append(cam_obj)
        new_worker = CamWorker(cam_obj, self.cam_counter, self.ch)
        new_worker.signals.cleanup_sig.connect(self.cleanup_cam_and_thread)
        new_worker.start()
        self.worker_thread_list.append(new_worker)
        self.signals.new_cam_sig.emit(cam_obj, new_worker)
        self.logger.debug("done")

    def cleanup_cam_and_thread(self, cam_obj):
        self.logger.debug("running")
        self.cam_list.remove(cam_obj)
        cam_obj.cleanup()
        self.signals.disconnect_sig.emit(cam_obj)
        for worker in self.worker_thread_list:
            if not worker.running:
                self.worker_thread_list.remove(worker)
                worker.wait()
        del cam_obj
        self.logger.debug("done")

    def stop_recording(self):
        self.logger.debug("running")
        for cam in self.cam_list:
            cam.destroy_writer()
        self.logger.debug("done")
