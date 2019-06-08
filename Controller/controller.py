# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from os import path, mkdir
import datetime
import sys
from PySide2.QtCore import QTimer, QDir
from PySide2.QtWidgets import QFileDialog
from Model.defs import update_available, up_to_date, vog_block_field, drt_trial_fields, drt_file_hdr, vog_file_hdr, \
    block_note_hdr, program_output_hdr
from View.main_view import CompanionWindow
from View.help_window import HelpWindow
from Controller.version_checker import VersionChecker
from Controller.device_manager import DeviceManager


class CompanionController:
    def __init__(self):
        """Set up view and device manager."""
        self.ui = CompanionWindow(self.receive_msg_from_ui)
        self.ui.show()
        self.device_manager = DeviceManager(self.receive_msg_from_device_manager, self.save_output_msg)

        # Experiment data structure
        self.exp_hdrs = []
        self.blk_hdrs = []
        self.blk_notes = []
        self.blk_data = []
        self.device_data = {}
        self.current_cond_name = ""

        self.closing = False

        self.exp_created = False
        self.exp_running = False
        self.__setup_handlers()
        self.__start_update_timer()
        self.directory = ""
        self.fnames_to_save_to = {}
        self.program_output_save_file = self.__setup_output_file()

        self.saved_files_open = []

    def close_file(self, fname):
        if fname in self.saved_files_open:
            self.saved_files_open.remove([fname[0], fname[1]])

    def save_output_msg(self, msg):
        line = str(self.__get_current_time(save=True)) + ", " + msg
        with open(self.program_output_save_file, 'a+') as file:
            file.write(line)

    def receive_msg_from_ui(self, msg):
        if 'action' in msg.keys() and msg['action'] == "close":
            self.closing = True
            self.device_manager.end_block_all()
            self.device_manager.end_exp_all()
        elif 'control' in msg.keys() and msg['control'] == "run":
            self.device_manager.handle_msg({'type': "start device", 'device': msg['device']})
        elif 'control' in msg.keys() and msg['control'] == "stop":
            self.device_manager.handle_msg({'type': "stop device", 'device': msg['device']})
        else:
            self.device_manager.handle_msg(msg)

    def receive_msg_from_device_manager(self, msg):
        if msg['type'] == "data":
            self.__update_save(msg)
        elif msg['type'] == "add":
            self.__add_device(msg)
        elif msg['type'] == "remove":
            self.__remove_device(msg)
        self.ui.handle_msg(msg)

    def __begin_exp_action_handler(self):
        """Begin an experiment. Get a directory to save to, """
        if not self.exp_created:
            self.__get_save_dir_path()
            self.__update_device_filenames()
            self.__check_save_file_hdrs()
            self.__create_exp()
        else:
            self.__end_exp()

    def __create_exp(self):
        self.exp_created = True
        self.device_manager.start_exp_all()
        cond_name = self.ui.get_condition_name()
        if cond_name == "":
            cond_name = "N/A"
        self.current_cond_name = cond_name
        self.ui.set_exp_start_time(self.__get_current_time(time=True))

    def __end_exp(self):
        self.exp_created = False
        self.device_manager.end_exp_all()

    def __start_stop_exp(self):
        if self.exp_running:
            self.__stop_exp()
        else:
            self.__start_exp()

    def __start_exp(self):
        self.exp_running = True
        self.device_manager.start_block_all()
        self.__check_toggle_post_button()

    def __stop_exp(self):
        self.exp_running = False
        self.device_manager.end_block_all()
        self.__check_toggle_post_button()

    def __setup_handlers(self):
        """Wire up buttons etc. in the view."""
        self.ui.add_exp_create_end_handler(self.__begin_exp_action_handler)
        self.ui.add_exp_start_stop_handler(self.__start_stop_exp)
        self.ui.add_post_handler(self.__save_block_note_button_handler)
        self.ui.add_update_handler(self.__check_for_updates_handler)
        self.ui.add_note_box_changed_handler(self.__check_toggle_post_button)

    def __check_toggle_post_button(self):
        if self.exp_created and self.exp_running and len(self.ui.get_note()) > 0:
            self.ui.toggle_post_button(True)
        else:
            self.ui.toggle_post_button(False)

    def __check_save_dir(self):
        """Check to see if user has chosen a dir path and that the chosen dir path is valid"""
        if self.directory != "" and path.isdir(self.directory):
            return True
        return False

    def __check_for_updates_handler(self):
        """Check to see if there is an updated version of the app and let user know result"""
        vc = VersionChecker()
        if vc.check_version():
            self.window = HelpWindow("Update", update_available)
        else:
            self.window = HelpWindow("Update", up_to_date)
        self.window.show()

    def __save_block_note_button_handler(self):
        for device in self.fnames_to_save_to:
            self.__write_line_to_file(self.fnames_to_save_to[device]['fn'],
                                      self.current_cond_name
                                      + ", " + self.ui.get_key_flag()
                                      + ", " + self.__get_current_time(True, True, True)
                                      + ", " + self.ui.get_note())
        self.ui.clear_note()

    # TODO: If directory does not exist, make it.
    def __get_save_dir_path(self):
        fname = QFileDialog.getExistingDirectory(None, 'Save Directory', QDir().homePath(), QFileDialog.ShowDirsOnly)
        if fname[0] != "":
            self.directory = fname
            # if not self.__check_save_dir():
                # mkdir(self.directory, )

    def __write_line_to_file(self, fname, line):
        line = line + "\n"
        filepath = path.join(self.directory, fname)
        filepath += ".txt"
        with open(filepath, 'a+') as file:
            file.write(line)

    def __start_update_timer(self):
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.__device_update)
        self.update_timer.start(1)

    def __device_update(self):
        self.device_manager.update()

    def __update_save(self, msg_dict):
        if msg_dict['device'][0] == "drt":
            self.__format_drt_line(msg_dict)
        elif msg_dict['device'][0] == "vog":
            self.__format_vog_line(msg_dict)

    def __finish_line_and_write(self, device, line):
        prepend = "data: " \
                  + self.current_cond_name + ", " \
                  + self.current_block_name + ", " \
                  + self.ui.get_key_flag() + ", " \
                  + self.__get_current_time(True, True, True)
        line = prepend + line
        self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], line)

    def __format_drt_line(self, msg_dict):
        line = ""
        for i in range(0, len(drt_trial_fields)):
            line += ", " + msg_dict[drt_trial_fields[i]]
        line = line[0:-2]
        self.__finish_line_and_write(msg_dict['device'], line)

    def __format_vog_line(self, msg_dict):
        line = ""
        for i in range(len(vog_block_field)):
            line += ", " + msg_dict[vog_block_field[i]]
        line = line[0:-2]
        self.__finish_line_and_write(msg_dict['device'], line)

    def __check_save_file_hdrs(self):
        for device in self.fnames_to_save_to:
            if not self.fnames_to_save_to[device]['hdr']:
                self.__add_hdr_to_file(device)

    def __make_save_filename_for_device(self, device):
        self.fnames_to_save_to[device]['fn'] = device[0] + " on " + device[1] + " " + self.__get_current_time(save=True)
        self.fnames_to_save_to[device]['hdr'] = False

    def __update_device_filenames(self):
        for device in self.fnames_to_save_to:
            self.__make_save_filename_for_device(device)

    def __add_device(self, msg_dict):
        device = msg_dict['device']
        self.fnames_to_save_to[device] = {}
        self.__make_save_filename_for_device(device)
        if self.__check_save_dir():
            self.__add_hdr_to_file(device)

    def __remove_device(self, msg_dict):
        device = msg_dict['device']
        del(self.fnames_to_save_to[device])

    def __add_hdr_to_file(self, device):
        if device[0] == 'drt':
            self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], drt_file_hdr + "\n"
                                      + block_note_hdr)
            self.fnames_to_save_to[device]['hdr'] = True
        elif device[0] == 'vog':
            self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], vog_file_hdr + "\n"
                                      + block_note_hdr)
            self.fnames_to_save_to[device]['hdr'] = True

    @staticmethod
    def __parse_vog_line(line):
        the_parts = line.split(", ")
        data = (int(the_parts[-2]), int(the_parts[-1]))
        return data

    @staticmethod
    def __parse_drt_line(line):
        the_parts = line.split(", ")
        data = the_parts[-1]
        return int(data)

    @staticmethod
    def __setup_output_file():
        fname = path.dirname(sys.argv[0]) + "\\program_output.txt"
        if path.exists(fname):
            with open(fname, "w") as temp:
                temp.write(program_output_hdr)
        return fname

    @staticmethod
    def __get_current_time(day=False, time=False, mil=False, save=False):
        if day and time and mil:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        elif day and time and not mil:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif day and not time and not mil:
            return datetime.datetime.now().strftime("%Y-%m-%d")
        elif not day and time and not mil:
            return datetime.datetime.now().strftime("%H:%M:%S")
        elif not day and time and mil:
            return datetime.datetime.now().strftime("%H:%M:%S.%f")
        elif save:
            return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

