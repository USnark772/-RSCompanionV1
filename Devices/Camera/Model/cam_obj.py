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


# import logging
import cv2
from os import remove
from imutils import rotate, resize
from time import time
from numpy import ndarray
from threading import Thread
from Model.general_defs import cap_backend, cap_temp_codec, cap_codec


class CamObj:
    def __init__(self, index: int, name: str):  # , ch: logging.Handler):
        # self.logger = logging.getLogger(__name__)
        # self.logger.addHandler(ch)
        # self.logger.debug("Initializing")
        self.cap = cv2.VideoCapture(index, cap_backend)
        self.name = name
        self.cur_res = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = 30
        self.writer = None
        self.active = True
        self.writing = False
        self.bw_image = False
        self.show_feed = True
        self.fourcc_bool = False
        self.rotate_angle = 0  # in degrees
        # self.scale = .5  # TODO: Figure out if this is different than setting frame size differently.
        self.save_file = str()
        self.temp_save_file = str()
        self.total_frames = 0
        self.start_time = 0
        self.end_time = 0
        self.actual_fps = 0
        self.saved_resolution = (0, 0)
        self.file_fixer = None
        # self.logger.debug("Initialized")

    def toggle_activity(self, is_active: bool):
        self.active = is_active
        if not self.active:
            self.close_window()

    def set_show_feed(self, is_active):
        self.show_feed = is_active
        if not self.show_feed:
            self.close_window()

    def start_writing(self, timestamp: str, save_dir: str):
        if self.active:
            self.total_frames = 0
            self.writer = self.__setup_writer(timestamp, save_dir)
            self.start_time = time()
            self.writing = True

    def __setup_writer(self, timestamp: str = None, save_dir: str = None, save_file: str = None,
                       vid_ext: str = '.avi', fps: int = 30, res: tuple = None) -> cv2.VideoWriter:
        # self.logger.debug("running")
        if not res:
            res = (int(self.cur_res[0]), int(self.cur_res[1]))
            self.saved_resolution = res
        if not save_file:
            self.temp_save_file = save_dir + 'temp_' + timestamp + '_' + self.name + '_output' + vid_ext
            self.save_file = save_dir + timestamp + '_' + self.name + '_output' + vid_ext
            file_name = self.temp_save_file
        else:
            file_name = save_file
        writer = cv2.VideoWriter(file_name, cap_codec, fps, res)
        return writer
        # self.logger.debug("done")

    def open_settings_window(self):
        self.cap.set(cv2.CAP_PROP_SETTINGS, 1)  # Seems like we can only open the window, not close it.

    def stop_writing(self):
        self.__destroy_writer()

    def __destroy_writer(self):
        # self.logger.debug("running")
        if self.writing:
            self.end_time = time()
            self.writer.release()
            self.writer = None
            self.writing = False
            self.file_fixer = Thread(target=self.__set_file_fps)
            self.file_fixer.start()
        # self.logger.debug("done")

    def update(self):
        if self.active:
            ret: bool
            frame: ndarray
            start = time()
            ret, frame = self.__read_camera()
            end = time()
            if end - start > 0.5:
                return False
            if ret and frame is not None:
                if self.bw_image:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # if self.scale != 1:
                #     frame = resize(frame, round(self.frame_size[0] * self.scale))
                if self.rotate_angle != 0:
                    frame = rotate(frame, self.rotate_angle)
                if self.show_feed:
                    cv2.imshow(self.name, frame)
                    cv2.waitKey(1)  # Required for frame to appear
                if self.writing:
                    self.writer.write(frame)
                    self.total_frames += 1
            else:
                return False
        return True

    def close_window(self):
        cv2.destroyWindow(self.name)

    def cleanup(self):
        # self.logger.debug("running")
        self.active = False
        self.cap.release()
        self.__destroy_writer()
        if self.file_fixer:
            self.file_fixer.join()
        self.close_window()
        # self.logger.debug("done")

    def set_bw(self, is_active: bool):
        self.bw_image = is_active

    def get_bw(self):
        return self.bw_image

    def get_current_fps(self):
        return self.fps

    def set_fps(self, fps):
        self.fps = fps

    def get_current_rotation(self):
        return self.rotate_angle

    def set_rotation(self, value):
        self.rotate_angle = value

    def get_current_frame_size(self):
        return self.cur_res

    def set_frame_size(self, size: tuple):
        x = float(size[0])
        y = float(size[1])
        self.toggle_activity(False)
        if self.fourcc_bool:
            self.__set_fourcc()
        res1 = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, x)
        res2 = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)
        if not res1 or not res2:
            res3 = self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cur_res[0])
            res4 = self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cur_res[1])
        else:
            self.cur_res = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.close_window()
        self.toggle_activity(True)

    def __set_fourcc(self):
        self.cap.set(cv2.CAP_PROP_FOURCC, cap_temp_codec)  # This line required because opencv is dumb
        self.cap.set(cv2.CAP_PROP_FOURCC, cap_codec)

    def __read_camera(self):
        ret, frame = self.cap.read()
        if frame is None:
            ret, frame = self.cap.read()
        return ret, frame

    # TODO: Figure out more accurate actual_fps
    def __set_file_fps(self):
        time_taken = self.end_time - self.start_time
        if time_taken <= 0:
            return False
        actual_fps = int(self.total_frames / time_taken)
        from_file = cv2.VideoCapture(self.temp_save_file)
        to_file = self.__setup_writer(save_file=self.save_file, fps=actual_fps)
        ret, frame = from_file.read()
        while ret and frame is not None:
            to_file.write(frame)
            ret, frame = from_file.read()
        from_file.release()
        to_file.release()
        remove(self.temp_save_file)
        return True
