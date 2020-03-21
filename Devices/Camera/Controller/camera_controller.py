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
from PySide2.QtCore import QObject, Signal
from Devices.abc_device_controller import ABCDeviceController
from Devices.Camera.View.camera_tab import CameraTab
from Devices.Camera.Controller.pipe_watcher import PipeWatcher
from Devices.Camera.Controller.cam_runner import run_camera, CEnum
from Devices.Camera.Controller.edit_vid_playback_speed import FileFixer

# TODO: Fix crash bug when changing cam3 res to higher than 1080p (unsupported resolutions) Some issue with threading
#  memory corruption.
#  Process finished with exit code -1073740940 (0xC0000374)
#  Process finished with exit code -1073741819 (0xC0000005)


class ControllerSig(QObject):
    settings_error = Signal(str)
    cam_failed = Signal(str)
    cam_closed = Signal(str, int)
    send_msg_sig = Signal(tuple)
    update_save_prog = Signal(int, int)


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
        # proc_args = (proc_pipe, self.index, self.name, eval(settings.value('Experimental')))
        proc_args = (proc_pipe, self.index, self.name, True)
        self.cam_worker = Thread(target=run_camera, args=proc_args)
        self.cam_worker.start()
        self.file_fixer: FileFixer = FileFixer('', '', 0, False)
        self.file_fixer_running = False
        self.signals = ControllerSig()
        self.save_dir = ''
        self.timestamp = None
        self.cam_active = True
        self.feed_active = True
        self.color_image = True
        self.__setup_handlers()
        self.current_size = 0
        self.frame_sizes = []
        self.worker_max_tries = 0
        # self.fps_values = []
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
            elif msg_type == CEnum.STOP_SAVING:
                if self.file_fixer_running:
                    self.file_fixer.wait()
                self.file_fixer = FileFixer(msg[1], msg[2], msg[3], True)
                self.file_fixer.signal.update_sig.connect(self.__emit_save_update)
                self.file_fixer.signal.done_sig.connect(self.__emit_save_complete)
                self.file_fixer_running = True
                self.file_fixer.start()

    def create_new_save_file(self, new_filename: str):
        self.logger.debug("running")
        self.save_dir = new_filename
        self.logger.debug("done")

    def set_start_time(self, timestamp: str):
        self.logger.debug("running")
        self.timestamp = timestamp
        self.logger.debug("done")

    def start_exp(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.START_SAVING, self.timestamp, self.save_dir))
        self.tab.set_tab_active(False)
        if self.file_fixer_running:
            self.file_fixer.wait()
        self.logger.debug("done")

    def end_exp(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.STOP_SAVING,))
        self.tab.set_tab_active(True)
        self.logger.debug("done")

    def __emit_save_complete(self, success):
        if success:
            self.signals.update_save_prog.emit(self.index, 100)
        else:
            pass  # TODO: Figure out what to do here.

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
        self.tab.add_use_cam_button_handler(self.__toggle_cam)
        # self.tab.add_fps_selector_handler(self.__set_fps)
        self.tab.add_frame_size_selector_handler(self.__set_frame_size)
        self.tab.add_settings_toggle_button_handler(self.__open_settings)
        self.tab.add_frame_rotation_handler(self.__rotation_entry_changed)
        self.tab.add_show_cam_button_handler(self.__toggle_show_feed)
        self.tab.add_bw_button_handler(self.__toggle_bw)
        self.logger.debug("done")

    def __complete_setup(self, sizes: list):
        self.logger.debug("running")
        self.pipe.send((CEnum.WORKER_DONE,))
        self.__populate_sizes(sizes)
        self.__get_initial_values()
        self.pipe.send((CEnum.ACTIVATE_CAM,))
        self.tab.set_tab_active(True)
        self.tab.remove_init_prog_bar()
        self.logger.debug("done")

    def __toggle_cam(self):
        self.logger.debug("running")
        if self.cam_active:
            self.pipe.send((CEnum.DEACTIVATE_CAM,))
            self.tab.set_tab_active(False, toggle_toggler=False)
        else:
            self.pipe.send((CEnum.ACTIVATE_CAM,))
            self.tab.set_tab_active(True, toggle_toggler=False)
        self.cam_active = not self.cam_active
        self.logger.debug("done")

    def __toggle_show_feed(self):
        self.logger.debug("running")
        if self.feed_active:
            self.pipe.send((CEnum.HIDE_FEED,))
        else:
            self.pipe.send((CEnum.SHOW_FEED,))
        self.feed_active = not self.feed_active
        self.logger.debug("done")

    def __set_frame_size(self):
        self.logger.debug("running")
        new_size = self.tab.get_frame_size()
        self.pipe.send((CEnum.SET_RESOLUTION, new_size))
        self.logger.debug("done")

    # def __set_fps(self):
    #     self.logger.debug("running")
    #     new_fps = self.tab.get_fps()
    #     self.pipe.send((CEnum.SET_FPS, new_fps))
    #     self.logger.debug("done")

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
        # self.tab.add_item_to_fps_selector("Initializing...")
        self.logger.debug("done")

    # def __populate_fps_selections(self):
    #     self.logger.debug("running")
    #     self.tab.empty_fps_selector()
    #     for i in range(11):
    #         self.fps_values.append((str(30 - i), 30-i))
    #     self.tab.populate_fps_selector(self.fps_values)
    #     self.logger.debug("done")

    def __populate_sizes(self, sizes: list):
        self.logger.debug("running")
        self.tab.empty_size_selector()
        self.frame_sizes = sizes
        self.tab.populate_frame_size_selector(self.frame_sizes)
        self.logger.debug("done")

    def __get_initial_values(self):
        self.logger.debug("running")
        self.pipe.send((CEnum.GET_RESOLUTION,))
        # self.pipe.send((CEnum.GET_FPS,))
        self.pipe.send((CEnum.GET_ROTATION,))
        self.logger.debug("done")

    # def __set_tab_fps_val(self, value: int):
    #     self.tab.set_fps(self.__get_fps_val_index(value))

    def __set_tab_size_val(self, value: tuple):
        self.tab.set_frame_size(self.__get_size_val_index(value))

    def __set_tab_rot_val(self, value: int):
        self.tab.set_rotation(str(value))

    def __get_size_val_index(self, value: tuple):
        for i in range(len(self.frame_sizes)):
            if self.frame_sizes[i][1] == value:
                return i

    # def __get_fps_val_index(self, value: int):
    #     return self.fps_values.index((str(value), value))
