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
# Author: Nathan Rogers
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from multiprocessing import Pipe
from threading import Thread
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QObject, Signal, Qt, QTimer
from Devices.abc_device_controller import ABCDeviceController
from Devices.Camera.View.cam_tab import CameraTab
from Devices.Camera.Model.cam_pipe_watcher import PipeWatcher
from Devices.Camera.Model.cam_runner import run_camera
from Devices.Camera.Model.cam_defs import CEnum
from Devices.Camera.Model.edit_vid_playback_speed import FileFixer
from Devices.Camera.Model.cam_feed_updater import FeedUpdater
from numpy import ndarray
from cv2 import cvtColor, COLOR_BGR2RGB


class ControllerSig(QObject):
    settings_error = Signal(str)
    cam_failed = Signal(str)
    cam_closed = Signal(str, int)
    send_msg_sig = Signal(tuple)
    update_save_prog = Signal(int, int)
    save_failed = Signal(str)


class CameraController(ABCDeviceController):
    def __init__(self, index: int, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.index = index
        self.name = "CAM_" + str(index + 1)
        super().__init__(CameraTab(ch, name=self.name))
        self.pipe, proc_pipe = Pipe()
        self.pipe_watcher = PipeWatcher(self.pipe, ch)
        self.pipe_watcher.connect_to_sig(self.handle_pipe)
        self.pipe_watcher.start()
        # TODO: Add settings access for user.
        # settings = QSettings("Red Scientific", "Companion")
        # settings.beginGroup('Camera settings')
        # if not settings.contains("Experimental"):
        #     settings.setValue("Experimental", "False")
        # proc_args = (args go here)
        self.frame_pipe_rcv, frame_pipe_send = Pipe(False)
        self.image_updater = FeedUpdater(self.frame_pipe_rcv)
        self.image_updater.signal.new_frame_sig.connect(self.handle_new_frame)
        proc_args = (proc_pipe, frame_pipe_send, self.index, False)
        self.cam_worker = Thread(target=run_camera, args=proc_args)
        self.cam_worker.start()
        self.file_fixer: FileFixer = FileFixer('', '', 0, False)
        self.file_fixer_running = False
        self.signals = ControllerSig()
        self.save_dir = ''
        self.timestamp = None
        self.cam_active = True
        self.feed_active = True
        self.__in_experiment = False
        self.__cam_ready = False
        self.__setup_handlers()
        self.current_size = 0
        self.frame_sizes = []
        self.worker_max_tries = 0
        self.temp_save_filename = ''
        self.save_filename = ''
        self.__add_loading_symbols_to_tab()
        self.logger.debug("Initialized")

    def get_name(self) -> str:
        return self.name

    def cleanup(self):
        self.logger.debug("running")
        self.pipe_watcher.running = False
        self.pipe_watcher.wait()
        if self.file_fixer_running:
            self.file_fixer.running = False
            self.file_fixer.wait()
        try:
            self.pipe.send((CEnum.CLEANUP,))
            self.pipe.close()
        except:
            pass
        try:
            self.frame_pipe_rcv.close()
        except:
            pass
        if self.image_updater.running:
            self.image_updater.running = False
            self.image_updater.wait()
        if self.cam_worker.is_alive():
            self.cam_worker.join()
        self.logger.debug("done")

    def handle_pipe(self):
        msg = None
        try:
            if self.pipe.poll():
                msg = self.pipe.recv()
        except:
            self.logger.exception("Pipe failed")
            self.cleanup()
            return
        if msg:
            msg_type = msg[0]
            if msg_type == CEnum.WORKER_DONE:
                self.__complete_setup(msg[1])
            elif msg_type == CEnum.CAM_FAILED:
                self.signals.cam_failed.emit(self.name + " failed. Possible disconnect.")
                self.signals.cam_closed.emit(self.name, self.index)
                self.cleanup()
            elif msg_type == CEnum.SET_RESOLUTION:
                self.__set_tab_size_val(msg[1])
            elif msg_type == CEnum.SET_ROTATION:
                self.__set_tab_rot_val(msg[1])
            elif msg_type == CEnum.WORKER_MAX_TRIES:
                self.worker_max_tries = msg[1]
            elif msg_type == CEnum.WORKER_STATUS_UPDATE:
                self.tab.set_init_progress_bar_val((self.worker_max_tries - msg[1]) / self.worker_max_tries * 100)
            elif msg_type == CEnum.FPS_UPDATE:
                self.display_fps(msg[1])
            elif msg_type == CEnum.STOP_SAVING and self.__in_experiment:
                if self.file_fixer_running:
                    self.file_fixer.wait()
                self.file_fixer = FileFixer(self.temp_save_filename, self.save_filename, msg[1], True)
                self.file_fixer.signal.update_sig.connect(self.__emit_save_update)
                self.file_fixer.signal.done_sig.connect(self.__emit_save_complete)
                self.file_fixer_running = True
                self.file_fixer.start()
                self.__in_experiment = False

    def create_new_save_file(self, new_dir: str):
        self.logger.debug("running")
        self.save_dir = new_dir
        self.logger.debug("done")

    def set_start_time(self, timestamp: str):
        self.logger.debug("running")
        self.timestamp = timestamp
        self.logger.debug("done")

    def make_save_filenames(self):
        name = self.timestamp + '_' + self.name + '_output.avi'
        self.temp_save_filename = self.save_dir + 'temp_' + name
        self.save_filename = self.save_dir + name

    def start_exp(self):
        self.logger.debug("running")
        self.make_save_filenames()
        if self.__cam_ready:
            self.pipe.send((CEnum.START_SAVING, self.temp_save_filename))
            self.tab.set_tab_active(False)
            if self.file_fixer_running:
                self.file_fixer.wait()
            self.__in_experiment = True
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.STOP_SAVING,))
        self.tab.set_tab_active(True)
        self.logger.debug("done")

    def toggle_cam(self, is_active: bool):
        self.logger.debug("running")
        if is_active:
            self.pipe.send((CEnum.ACTIVATE_CAM,))
            self.tab.set_tab_active(is_active, feed=True)
        else:
            self.pipe.send((CEnum.DEACTIVATE_CAM,))
            self.tab.set_tab_active(is_active, feed=True)
        self.logger.debug("done")

    def update_frame(self):
        try:
            if self.frame_pipe.poll():
                self.handle_new_frame(self.frame_pipe.recv())
        except BrokenPipeError as bpe:
            pass

    def handle_new_frame(self, frame: ndarray):
        rgb_image = cvtColor(frame, COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(248, 186, Qt.KeepAspectRatio)
        self.tab.update_feed(QPixmap.fromImage(p))

    def display_fps(self, fps: int):
        self.tab.update_fps_value(fps)

    def __emit_save_complete(self, success):
        if success:
            self.signals.update_save_prog.emit(self.index, 100)
        else:
            self.signals.save_failed.emit(self.name)

    def __emit_save_update(self, completed, total):
        perc = round(completed / total * 100)
        self.signals.update_save_prog.emit(self.index, perc)

    def __toggle_bw(self):
        self.logger.debug("running")
        if self.color_image:
            self.pipe.send((CEnum.SET_BW, True))
        else:
            self.pipe.send((CEnum.SET_BW, False))
        self.color_image = not self.color_image
        self.logger.debug("done")

    def __setup_handlers(self):
        self.logger.debug("running")
        # self.tab.add_use_cam_button_handler(self.__toggle_cam)
        self.tab.add_frame_size_selector_handler(self.__set_frame_size)
        # self.tab.add_settings_toggle_button_handler(self.__open_settings)
        self.tab.add_frame_rotation_handler(self.__rotation_entry_changed)
        self.tab.add_show_cam_button_handler(self.__toggle_show_feed)
        # self.tab.add_bw_button_handler(self.__toggle_bw)
        self.logger.debug("done")

    def __complete_setup(self, sizes: list):
        self.logger.debug("running")
        self.pipe.send((CEnum.WORKER_DONE,))
        self.__populate_sizes(sizes)
        self.__get_initial_values()
        self.pipe.send((CEnum.ACTIVATE_CAM,))
        self.tab.set_tab_active(True, feed=True)
        self.tab.remove_init_prog_bar()
        self.image_updater.running = True
        self.image_updater.start()
        self.__cam_ready = True
        self.logger.debug("done")

    def __toggle_show_feed(self, is_active: bool):
        self.logger.debug("running")
        self.tab.show_feed(is_active)
        self.logger.debug("done")

    def __set_frame_size(self):
        self.logger.debug("running")
        new_size = self.tab.get_frame_size()
        self.pipe.send((CEnum.SET_RESOLUTION, new_size))
        self.logger.debug("done")

    def __open_settings(self):
        self.pipe.send((CEnum.OPEN_SETTINGS,))

    def __rotation_entry_changed(self):
        if self.__validate_rotation():
            new_rotation = int(self.tab.get_rotation())
            try:
                self.pipe.send((CEnum.SET_ROTATION, new_rotation))
            except BrokenPipeError as e:
                self.logger.exception("Broken pipe")
                return
            self.tab.set_rotation_error(False)
        else:
            self.tab.set_rotation_error(True)

    def __validate_rotation(self):
        usr_input: str
        negative = False
        usr_input = self.tab.get_rotation()
        if len(usr_input) == 0:
            self.tab.set_rotation('0')
            return True
        if len(usr_input) > 0 and usr_input[0] == '-':
            negative = True
            usr_input = usr_input[1:]
        if usr_input.isdigit():
            if negative:
                rot_value = 0 - int(usr_input)
                self.tab.set_rotation(str(rot_value % -360))
            else:
                rot_value = int(usr_input)
                self.tab.set_rotation(str(rot_value % 360))
            return True
        else:
            return False

    def __add_loading_symbols_to_tab(self):
        self.logger.debug("running")
        self.tab.add_item_to_size_selector("Initializing...")
        self.logger.debug("done")

    def __populate_sizes(self, sizes: list):
        self.logger.debug("running")
        self.tab.empty_size_selector()
        self.frame_sizes = sizes
        self.tab.populate_frame_size_selector(self.frame_sizes)
        self.logger.debug("done")

    def __get_initial_values(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.GET_RESOLUTION,))
        self.pipe.send((CEnum.GET_ROTATION,))
        self.logger.debug("done")

    def __set_tab_size_val(self, value: tuple):
        self.tab.set_frame_size(self.__get_size_val_index(value))

    def __set_tab_rot_val(self, value: int):
        self.tab.set_rotation(str(value))

    def __get_size_val_index(self, value: tuple):
        for i in range(len(self.frame_sizes)):
            if self.frame_sizes[i][1] == value:
                return i