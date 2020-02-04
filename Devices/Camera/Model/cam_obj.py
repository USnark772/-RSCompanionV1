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
        self.frame_size = (1920, 1080)
        self.fps = 30
        self.writer = None
        self.active = True
        self.writing = False
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
        return self.cap.read()

    def save_data(self, frame):
        if self.writing:
            self.writer.write(frame)

    def handle_new_frame(self, frame):
        if self.active:
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

    def get_current_fps(self):
        return self.fps

    def set_frame_size(self, size):
        self.frame_size = (size[0], size[1])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[1])

    def get_current_frame_size(self):
        return self.frame_size
