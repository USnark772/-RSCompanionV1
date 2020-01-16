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

import cv2
import logging
from numpy import ndarray
from PySide2.QtCore import QThread, QObject, Signal, QMutex
from Devices.Camera.View.camera_tab import CameraTab
from Devices.abc_device_controller import ABCDeviceController
from CompanionLib.companion_helpers import get_current_time
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.

# TODO: Add tab per camera?
# TODO: Add logging to this file


class CamScanner(QThread):
    def __init__(self, counter):
        QThread.__init__(self)
        self.signal = ScannerSig()
        self.cam_counter = counter
        self.running = True

    # Try to connect new cam from latest index and up
    def run(self):
        while self.running:
            self.check_for_cams(self.get_index())

    def get_index(self):
        self.cam_counter.get_lock()
        i = self.cam_counter.get_count()
        self.cam_counter.release_lock()
        return i

    def check_for_cams(self, index=0):
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap is None or not cap.isOpened():
                break
            else:
                cam_obj = CamObj(cap, "Camera " + str(index))
                self.increment_cam_count()
                self.signal.new_cam_sig.emit(cam_obj)
            index += 1

    def increment_cam_count(self):
        self.cam_counter.get_lock()
        self.cam_counter.increment_count()
        self.cam_counter.release_lock()


class CamWorker(QThread):
    def __init__(self, cam, cam_counter):
        QThread.__init__(self)
        self.signal = WorkerSig()
        self.cam = cam
        self.cam_counter = cam_counter
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cam.read_camera()
            if ret:
                self.signal.new_frame_sig.emit(self.cam, frame)
            else:
                # Error with read_camera() due to lost camera connection
                self.cleanup()
                break

    def cleanup(self):
        self.cam_counter.get_lock()
        self.cam_counter.decrement_count()
        self.cam_counter.release_lock()
        self.signal.cleanup_sig.emit(self.cam)


class CamObj:
    def __init__(self, cap, name):
        self.cap = cap
        self.name = name
        self.writer = None

    def setup_writer(self, timestamp, save_dir='', vid_ext='.avi', fps=20, frame_size=(640, 480), codec='DIVX'):
        self.writer = cv2.VideoWriter(save_dir + timestamp + self.name + '_output' + vid_ext,
                                      cv2.VideoWriter_fourcc(*codec), fps, frame_size)

    def destroy_writer(self):
        if self.writer:
            self.writer.release()
            self.writer = None

    def read_camera(self):
        return self.cap.read()

    def save_data(self, frame):
        if self.writer:
            self.writer.write(frame)

    def cleanup(self):
        self.cap.release()
        self.destroy_writer()
        cv2.destroyWindow(self.name)


class ScannerSig(QObject):
    new_cam_sig = Signal(CamObj)


class WorkerSig(QObject):
    new_frame_sig = Signal((CamObj, ndarray))
    cleanup_sig = Signal(CamObj)


class CamCounter:
    def __init__(self):
        self.lock = QMutex()
        self.count = 0

    def get_lock(self):
        self.lock.lock()

    def release_lock(self):
        self.lock.unlock()

    def get_count(self):
        return self.count

    def increment_count(self):
        self.count += 1

    def decrement_count(self):
        self.count -= 1


class CamMan:
    def __init__(self):
        self.cam_list = []
        self.worker_thread_list = []
        self.cam_counter = CamCounter()
        self.scanner_thread = CamScanner(self.cam_counter)
        self.scanner_thread.signal.new_cam_sig.connect(self.handle_new_camera)
        self.scanner_thread.start()

    def cleanup(self):
        self.scanner_thread.running = False
        self.scanner_thread.wait()
        for worker in self.worker_thread_list:
            worker.running = False
            worker.wait()
        for cam in self.cam_list:
            cam.cleanup()

    def handle_new_camera(self, cam_obj):
        self.cam_list.append(cam_obj)
        new_worker = CamWorker(cam_obj, self.cam_counter)
        new_worker.signal.new_frame_sig.connect(self.handle_new_frame)
        new_worker.signal.cleanup_sig.connect(self.cleanup_cam_obj)
        new_worker.start()
        self.worker_thread_list.append(new_worker)

    def cleanup_cam_obj(self, cam):
        self.cam_list.remove(cam)
        cam.cleanup()
        del cam

    def start_recording(self, timestamp, save_dir):
        for cam in self.cam_list:
            cam.setup_writer(timestamp, save_dir=save_dir)

    def stop_recording(self):
        for cam in self.cam_list:
            cam.destroy_writer()

    @staticmethod
    def handle_new_frame(cam_obj, frame):
        cv2.imshow(cam_obj.name, frame)
        cam_obj.save_data(frame)


# TODO: Pipe save directory name through to here somehow or figure out if this is not the right structure.
#  Maybe CamMan is the controller and CameraController is more like device manager?
class CameraController(ABCDeviceController):
    def __init__(self, tab_parent, ch):
        tab = CameraTab(tab_parent, name="Cameras")
        super().__init__(tab)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.save_dir = ''
        self.cam_man = CamMan()

    def cleanup(self):
        self.cam_man.cleanup()

    def create_new_save_file(self, new_filename):
        self.save_dir = new_filename

    def start_exp(self):
        self.cam_man.start_recording(timestamp=get_current_time(save=True), save_dir=self.save_dir)

    def end_exp(self):
        self.cam_man.stop_recording()
