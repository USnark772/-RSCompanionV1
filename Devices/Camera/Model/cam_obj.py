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
from PySide2.QtCore import QObject, Signal


class CamObj:
    def __init__(self, cap, name, ch):  # , thread, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.cap = cap
        self.name = name
        # self.thread = thread
        self.frame_size = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = 30
        self.writer = None
        self.active = True
        self.writing = False
        self.color_image = True
        self.alter_image_shape = False
        self.rotate_angle = 0  # in degrees
        self.scale = 1  # negative values cause 180 degree rotation as well as scaling
        self.logger.debug("Initialized")

    def toggle_activity(self, is_active):
        self.active = is_active
        if not self.active:
            self.close_window()

    def setup_writer(self, timestamp, save_dir='', vid_ext='.avi', fps=None, frame_size=None, codec='DIVX'):
        self.logger.debug("running")
        if not frame_size:
            frame_size = (int(self.frame_size[0]), int(self.frame_size[1]))
        if not fps:
            fps = self.fps
        if self.active:
            self.writer = cv2.VideoWriter(save_dir + timestamp + self.name + '_output' + vid_ext,
                                          cv2.VideoWriter_fourcc(*codec), fps, frame_size)
            self.writing = True
        self.logger.debug("done")

    def destroy_writer(self):
        self.logger.debug("running")
        if self.writing:
            self.writer.release()
            self.writer = None
            self.writing = False
        self.logger.debug("done")

    def read_camera(self):
        ret, frame = self.cap.read()
        if frame is None:
            ret, frame = self.cap.read()
        return ret, frame

    def save_data(self, frame):
        if self.writing:
            self.writer.write(frame)

    def handle_new_frame(self, frame):
        if self.active:
            if self.alter_image_shape:
                rows, cols, a = frame.shape
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), self.rotate_angle, self.scale)
                frame = cv2.warpAffine(frame, M, (cols, rows))
            if not self.color_image:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow(self.name, frame)
            self.save_data(frame)

    def close_window(self):
        cv2.destroyWindow(self.name)

    def cleanup(self):
        self.logger.debug("running")
        self.active = False
        self.cap.release()
        self.destroy_writer()
        self.close_window()
        self.logger.debug("done")

    def set_use_color(self, is_active):
        self.color_image = is_active

    def get_current_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps

    def get_current_rotation(self):
        return self.rotate_angle

    def set_rotation(self, value):
        self.rotate_angle = value

    def get_current_frame_size(self):
        return self.frame_size

    def set_frame_size(self, size):
        x = float(size[0])
        y = float(size[1])
        self.toggle_activity(False)
        res1 = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, x)
        res2 = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)
        if not res1 or not res2:
            new_x = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            new_y = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            res3 = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
            res4 = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
        else:
            self.frame_size = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.close_window()
        self.toggle_activity(True)
