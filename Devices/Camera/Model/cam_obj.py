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


class CamObj:
    def __init__(self, cap, name, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.cap = cap
        self.name = name
        self.frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = 30
        self.writer = None
        self.active = True
        self.writing = False
        self.color_image = True
        self.alter_image_shape = True
        self.rotate_angle = 0  # in degrees
        self.scale = 1  # negative values cause 180 degree rotation as well as scaling
        self.logger.debug("Initialized")

    def toggle_activity(self):
        self.active = not self.active
        if not self.active:
            self.close_window()

    def setup_writer(self, timestamp, save_dir='', vid_ext='.avi', fps=None, frame_size=None, codec='DIVX'):
        self.logger.debug("running")
        if not frame_size:
            frame_size = self.frame_size
        if not fps:
            fps = self.fps
        print(type(self.frame_size), type(self.fps))
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
        i = 0
        while i < 20:
            try:
                return self.cap.read()
            except:
                # TODO: send signal?
                self.set_frame_size((640, 480))
            i += 1
        return False, 0

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

    def set_fps(self, fps):
        self.fps = fps

    def set_use_color(self, is_active):
        self.color_image = is_active

    def set_rotation(self, value):
        self.rotate_angle = value

    def get_current_rotation(self):
        return self.rotate_angle

    def get_current_fps(self):
        return self.fps

    def set_frame_size(self, size):
        x = size[0]
        y = size[1]
        self.toggle_activity()
        self.frame_size = (x, y)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, x)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, y)
        self.close_window()
        self.toggle_activity()

    def get_current_frame_size(self):
        return self.frame_size
