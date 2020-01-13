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
import threading
import logging
from PySide2.QtCore import Qt, QThread, QObject, Signal, Slot
from PySide2.QtGui import QImage
from Devices.Camera.View.camera_tab import CameraTab
from CompanionLib.companion_helpers import get_current_time
from Devices.Camera.View.camera_viewer import CamViewer
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.


class CamObj:
    def __init__(self, cap, name):
        self.cap = cap
        self.name = name
        self.writer = None
        self.window = CamViewer(self.name)

    def setup_writer(self, timestamp, save_dir='', vid_ext='.avi', fps=20, frame_size=(640, 480), codec='DIVX'):
        self.writer = cv2.VideoWriter(save_dir + timestamp + self.name + '_output' + vid_ext,
                                      cv2.VideoWriter_fourcc(*codec), fps, frame_size)

    def destroy_writer(self):
        if self.writer:
            self.writer.release()
            self.writer = None

    def get_data(self):
        return self.cap.read()

    def show_data(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        image = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        print("setting image")
        self.window.set_image(image)
        print("Done setting image")

    def save_data(self, frame):
        if self.writer:
            self.writer.write(frame)

    def release(self):
        self.cap.release()
        self.destroy_writer()
        cv2.destroyWindow(self.name)


class CamScanner(QThread):
    def __init__(self, the_list):
        QThread.__init__(self)
        self.list = the_list

    # Try to connect new cam from latest index and up
    def run(self):
        while True:
            i = self.list.get_num_cams()
            self.check_for_cams(i)
            print("scanner thread Sleeping")
            self.sleep(10)
            print("scanner thread Done sleeping")

    def check_for_cams(self, index=0):
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap is None or not cap.isOpened():
                break
            else:
                self.list.add_cam_to_list(CamObj(cap, "Camera " + str(index)))
            index += 1


class CameraList:
    def __init__(self):
        self.write_lock = threading.Lock()
        self.read_lock = threading.Lock()
        self.__cams = []

    def get_num_cams(self):
        self.read_lock.acquire()
        try:
            return len(self.__cams)
        finally:
            self.read_lock.release()

    def add_cam_to_list(self, cam):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            self.__cams.append(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def remove_cams(self, cams_to_remove):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            for cam in cams_to_remove:
                self.__remove_cam_from_list(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def empty_cam_list(self):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            for cam in self.__cams:
                self.__remove_cam_from_list(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def __remove_cam_from_list(self, cam):
        self.__release_cam(cam)
        self.__cams.remove(cam)

    def iterate_cams(self):
        self.read_lock.acquire()
        try:
            for cam in self.__cams:
                yield cam
        finally:
            self.read_lock.release()

    @staticmethod
    def __release_cam(cam):
        cam.release()


class CameraManager:
    def __init__(self):
        self.cam_list = CameraList()
        self.cam_scanner = CamScanner(self.cam_list)
        self.cam_refresher = CamRefresher(self.refresh_all_cams)
        self.cam_scanner.start()
        self.cam_refresher.start()
        self.vid_writer = cv2.VideoWriter()
        self.saving = False

    def setup_savers(self, timestamp, save_dir='', vid_ext='.avi', fps=20, frame_size=(640, 480), codec='DIVX'):
        for cam in self.cam_list.iterate_cams():
            cam.setup_writer(timestamp, save_dir=save_dir, vid_ext=vid_ext, fps=fps, frame_size=frame_size, codec=codec)

    def destroy_savers(self):
        for cam in self.cam_list.iterate_cams():
            cam.destroy_writer()

    def set_saving(self, new_val):
        self.saving = new_val

    def cleanup(self):
        self.cam_list.empty_cam_list()

    def controller_callback(self, cam):
        self.cam_list.remove_cams([cam])

    def refresh_all_cams(self):
        to_remove = []
        print("In refresh all cams")
        for cam in self.cam_list.iterate_cams():
            print("getting ret, frame")
            ret, frame = cam.get_data()
            if ret:
                print("doing cam.show_data(frame)")
                cam.show_data(frame)
                if self.saving:
                    cam.save_data(frame)
            else:
                to_remove.append(cam)
        if len(to_remove) > 0:
            self.cam_list.remove_cams(to_remove)


class Communicator(QObject):
    signal_image = Signal(QImage)


class CamRefresher(QThread):
    def __init__(self, func):
        QThread.__init__(self)
        self.signals = Communicator()
        self.to_run = func
        #self.signals.signal_image.connect()

    def run(self):
        while True:
            self.to_run()
            print("refresher thread Sleeping")
            self.sleep(100)
            print("refresher thread Done sleeping")


class CameraController:
    def __init__(self, tab_parent, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.tab_parent = tab_parent
        self.__tab = CameraTab(tab_parent, name="Cameras")
        self.save_dir = 'C:/Users/phill/Companion App Save Folder/'
        self.cam_man = CameraManager()

    def create_new_save_file(self, new_filename):
        pass

    def start_exp(self):
        """ Required function for all device controllers. """
        pass

    def end_exp(self):
        """ Required function for all device controllers. """
        pass

    def start_block(self):
        self.cam_man.setup_savers(timestamp=get_current_time(save=True), save_dir=self.save_dir)
        self.cam_man.set_saving(True)

    def end_block(self):
        self.cam_man.set_saving(False)
        self.cam_man.destroy_savers()

    def get_tab_obj(self):
        return self.__tab

'''
def main():
    cam_man = CameraManager()
    while True:
        cam_man.refresh_all_cams()
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            break
        elif keypress == ord('s'):
            cam_man.setup_savers(get_current_time(save=True))
            cam_man.set_saving(True)
        elif keypress == ord('d'):
            cam_man.set_saving(False)
            cam_man.destroy_savers()
    # When everything done, release the capture
    cam_man.cleanup()


main()
'''