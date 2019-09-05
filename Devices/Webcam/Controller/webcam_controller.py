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
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

from PySide2.QtWidgets import *
from PySide2.QtMultimedia import *
from PySide2.QtMultimediaWidgets import *
from Devices.Webcam.View.webcam_viewer import CamViewer


class WebcamController:
    def __init__(self, parent):
        self.online_webcams = self.__check_for_cams()
        if not self.online_webcams:
            pass  # TODO: Handle this better

        self.viewer = CamViewer()
        self.my_webcam = None

        self.current_cam_index = 0
        self.get_webcam(self.current_cam_index)

    def __check_for_cams(self):
        return QCameraInfo.availableCameras()

    def change_webcam(self, increment=False):
        if increment:
            if self.current_cam_index + 1 < len(self.online_webcams):
                self.current_cam_index += 1
                self.get_webcam(self.current_cam_index)
        else:
            if self.current_cam_index - 1 >= 0:
                self.current_cam_index -= 1
                self.get_webcam(self.current_cam_index)

    def get_webcam(self, i):
        self.my_webcam = QCamera(self.online_webcams[i])
        self.my_webcam.setViewfinder(self.viewer.get_viewfinder())
        self.my_webcam.setCaptureMode(QCamera.CaptureStillImage)
        self.my_webcam.error.connect(lambda: self.alert(self.my_webcam.errorString()))
        self.my_webcam.start()

    def alert(self, s):
        """
        This handles errors and displays alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)