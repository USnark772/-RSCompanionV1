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
# Date: 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

"""
Simply display the contents of the camera with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import logging
from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *
from Devices.Camera.View.camera_viewer import CamViewer
from Devices.Camera.View.camera_tab import CameraTab


class CameraController:
    def __init__(self, tab_parent, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.online_cameras = self.__check_for_cams()
        if not self.online_cameras:
            pass  # TODO: Handle this better

        self.viewer = CamViewer()
        self.my_camera = None

        self.current_cam_index = 0
        self.__get_camera(self.current_cam_index)
        self.__tab = CameraTab(tab_parent)
        self.__update_tab_cam_list()
        self.__set_handlers()
        self.logger.debug("Initialized")

    def create_new_save_file(self, new_filename):
        pass

    def start_exp(self):
        """ Required function for all device controllers. """
        pass

    def end_exp(self):
        """ Required function for all device controllers. """
        pass

    def start_block(self):
        pass

    def end_block(self):
        pass

    def get_tab_obj(self):
        return self.__tab

    def get_viewer(self):
        return self.viewer.get_viewfinder()

    def change_camera(self):
        print("Boom")
        self.logger.debug("running")
        index = self.__tab.get_cam_index()
        self.__get_camera(index)
        self.logger.debug("done")

    def alert(self, s):
        """
        This handles errors and displays alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)

    def __update_tab_cam_list(self):
        for i in range(len(self.online_cameras)):
            self.__tab.add_cam(i)

    def __set_handlers(self):
        self.logger.debug("running")
        self.__tab.add_cam_selector_button_handler(self.change_camera)
        self.logger.debug("done")

    def __get_camera(self, i):
        self.logger.debug("running")
        self.my_camera = QCamera(self.online_cameras[i])
        self.my_camera.setViewfinder(self.viewer.get_viewfinder())
        self.my_camera.setCaptureMode(QCamera.CaptureStillImage)
        self.my_camera.error.connect(lambda: self.alert(self.my_camera.errorString()))
        self.my_camera.start()
        self.logger.debug("done")

    @staticmethod
    def __check_for_cams():
        return QCameraInfo.availableCameras()