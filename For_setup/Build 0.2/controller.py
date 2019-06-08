# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtCore import QTimer, QDir
from PySide2.QtWidgets import QFileDialog
from os import path
import datetime
import sys
from main_view import CompanionWindow
from help_window import HelpWindow
from version_checker import VersionChecker
import device_manager as manager
import defs as defs


class CompanionController:
    def __init__(self):
        """Set up view and device manager."""
        self.ui = CompanionWindow(self.receive_msg_from_ui)
        self.ui.show()
        self.device_manager = manager.DeviceManager(self.receive_msg_from_device_manager, self.save_com_msgs)

        # Experiment data structure
        self.exp_hdrs = []
        self.blk_hdrs = []
        self.blk_notes = []
        self.blk_data = []
        self.device_data = {}
        self.current_exp_number = 0
        self.current_block_number = 0
        self.current_exp_name = "N/A"
        self.current_block_name = "N/A"

        self.closing = False

        self.exp_running = False
        self.block_running = False
        self.__setup_handlers()
        self.__start_update_timer()
        self.directory = ""
        self.fnames_to_save_to = {}
        self.com_output_save_file = self.__setup_output_file()

        self.saved_files_open = []

    def __setup_handlers(self):
        """Wire up all buttons etc. from the view."""
        self.ui.set_open_handler(self.__open_action_handler)
        self.ui.add_exp_create_end_handler(self.__begin_exp_action_handler)
        self.ui.set_end_exp_handler(self.__end_exp_action_handler)
        self.ui.add_exp_start_stop_handler(self.__begin_block_button_handler)
        self.ui.set_end_block_handler(self.__end_block_button_handler)
        self.ui.add_post_handler(self.__save_block_note_button_handler)
        self.ui.add_update_handler(self.__check_for_updates_handler)
        self.ui.add_note_box_changed_handler(self.__check_note_button_activity)

    def __check_note_button_activity(self):
        if self.exp_running and self.block_running and len(self.ui.get_note()) > 0:
            self.ui.toggle_post_button()
        else:
            self.ui.deactivate_save_button()

    def __check_save_dir(self):
        if self.directory != "":
            return True
        return False

    def __check_for_updates_handler(self):
        vc = VersionChecker()
        if vc.check_version():
            self.window = HelpWindow("Update", "An update is available")
            self.window.show()

    def __open_action_handler(self):
        """Gets a file to open from the user."""
        directory = QDir()
        fname = QFileDialog.getOpenFileName(None, 'Open file', directory.homePath(), '*.txt')
        if path.exists(fname[0]):
            self.__parse_file(fname)

    def __begin_exp_action_handler(self):
        self.__get_save_dir_path()
        if not self.exp_running:
            for device in self.fnames_to_save_to:
                if not self.fnames_to_save_to[device]['hdr']:
                    self.__add_hdr_to_file(device)
            self.ui.toggle_exp_buttons()
            self.__begin_exp()
        else:
            self.__end_block_button_handler()
            self.__end_exp()
            self.__begin_exp()

    def __end_exp_action_handler(self):
        """Ends an experiment. If a block is currently running, ends the block as well."""
        if self.exp_running:
            self.ui.toggle_exp_buttons()
            self.__end_exp()

    def __begin_exp(self):
        self.exp_running = True
        msg_dict = {'type': "start exp all"}
        self.device_manager.handle_msg(msg_dict)
        self.current_exp_number += 1
        self.ui.set_current_exp_number(self.current_exp_number)
        exp_name = self.ui.get_condition_name()
        if exp_name == "":
            exp_name = "N/A"
        self.current_exp_name = exp_name
        self.ui.set_exp_start_time(self.__get_current_time(time=True))

    def __end_exp(self):
        self.exp_running = False
        msg_dict = {'type': "stop exp all"}
        self.device_manager.handle_msg(msg_dict)
        self.current_block_number = 0
        self.ui.set_current_block_number(self.current_block_number)
        if self.block_running:
            self.__end_block_button_handler()

    def __begin_block_button_handler(self):
        if self.exp_running and not self.block_running:
            self.ui.toggle_blk_buttons()
            self.__begin_block()
        elif self.exp_running and self.block_running:
            self.__end_block()
            self.__begin_block()

    def __end_block_button_handler(self):
        """Ends a block if one is currently running."""
        if self.block_running:
            self.ui.toggle_blk_buttons()
            self.__end_block()

    def __begin_block(self):
        self.block_running = True
        self.current_block_number += 1
        self.ui.set_current_block_number(self.current_block_number)
        msg_dict = {'type': "start block all"}
        self.device_manager.handle_msg(msg_dict)
        block_name = self.ui.get_block_name()
        if block_name == "":
            block_name = "N/A"
        self.current_block_name = block_name
        self.ui.set_current_block_time(self.__get_current_time(time=True))
        self.__check_note_button_activity()

    def __end_block(self):
        self.block_running = False
        msg_dict = {'type': "stop block all"}
        self.device_manager.handle_msg(msg_dict)
        self.__check_note_button_activity()

    '''
    def __trial_controls_action_handler(self):
        print("Trial Controls Action triggered")

    def __input_action_handler(self):
        print("Input Action triggered")

    def __output_action_handler(self):
        print("Output Action triggered")

    def __display_tooltips_action_handler(self):
        print("Display Tooltips Action triggered")

    def __configure_action_handler(self):
        print("Configure Action triggered")

    def __com_port_action_handler(self):
        print("COM Port Action triggered")

    def __com_messages_action_handler(self):
        print("COM Messages Action triggered")

    def __append_experiment_action_handler(self):
        print("Append Experiment Action triggered")
    '''

    def __save_block_note_button_handler(self):
        if self.block_running:
            note = self.ui.get_note()
            if note != "":
                for device in self.fnames_to_save_to:
                    self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], "note: " + self.current_exp_name
                                              + ", " + self.current_block_name + ", " + self.ui.get_key_flag() + ", "
                                              + self.__get_current_time(True, True, True) + ", block note: " + note)

    def __parse_file(self, fname):
        """Opens a file and reads data to view."""
        file = open(fname[0], 'r')
        device_type = ""
        line = file.readline()
        if "device type:" in line:
            if "vog" in line:
                device_type = "vog"
            elif "drt" in line:
                device_type = "drt"
        else:
            return
        device = self.__add_file_to_graphs(device_type, fname)
        for line in file:
            if "data: " in line:
                data = None
                if device_type == "vog":
                    data = self.__parse_vog_line(line)
                elif device_type == "drt":
                    data = self.__parse_drt_line(line)
                if data:
                    self.ui.main_chart_area.add_data_point(device, data)

    def __add_file_to_graphs(self, device_type, fname):
        device = [device_type, fname[0][fname[0].rindex("COM"):] + "(1)"]
        while device in self.saved_files_open:
            the_num = int(device[1][device[1].index("(")+1:device[1].index(")")])
            device[1] = device[1][:-3] + "(" + str(the_num + 1) + ")"
        self.saved_files_open.append(device)
        device = (device[0], device[1])
        self.ui.main_chart_area.add_device(device)
        self.ui.add_saved_file_to_tab(device, self.close_file)
        return device

    def __get_save_dir_path(self):
        fname = QFileDialog.getExistingDirectory(None, 'Save Directory', QDir().homePath(), QFileDialog.ShowDirsOnly)
        if fname[0] != "":
            self.directory = fname

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
            self.__add_drt_line(msg_dict)
        elif msg_dict['device'][0] == "vog":
            self.__add_vog_line(msg_dict)

    def __finish_line_and_write(self, device, line):
        prepend = "data: " \
                  + self.current_exp_name + ", " \
                  + self.current_block_name + ", " \
                  + self.ui.get_key_flag() + ", " \
                  + self.__get_current_time(True, True, True)
        line = prepend + line
        self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], line)

    def __add_drt_line(self, msg_dict):
        line = ""
        for i in range(0, len(defs.drt_trial_fields)):
            line += ", " + msg_dict[defs.drt_trial_fields[i]]
        print(line)
        line = line[0:-2]
        print(line)
        self.__finish_line_and_write(msg_dict['device'], line)

    def __add_vog_line(self, msg_dict):
        line = ""
        for i in range(len(defs.vog_block_field)):
            line += ", " + msg_dict[defs.vog_block_field[i]]
        line = line[0:-2]
        self.__finish_line_and_write(msg_dict['device'], line)

    def __add_device(self, msg_dict):
        device = msg_dict['device']
        self.fnames_to_save_to[device] = {}
        self.fnames_to_save_to[device]['fn'] = device[0] + " on " + device[1] + " " + self.__get_current_time(save=True)
        if self.__check_save_dir():
            self.__add_hdr_to_file(device)
            if device[0] == "vog":
                self.device_manager.handle_msg({'type': "send", 'device': msg_dict['device'], 'cmd': "do_expStart"})
            if self.block_running:
                if device[0] == "vog":
                    self.device_manager.handle_msg({'type': "send", 'device': msg_dict['device'], 'cmd': "do_trialStart"})
                elif device[0] == "drt":
                    self.device_manager.handle_msg({'type': "send", 'device': msg_dict['device'], 'cmd': "expStart"})
        else:
            self.fnames_to_save_to[device]['hdr'] = False

    def __add_hdr_to_file(self, device):
        if device[0] == 'drt':
            self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], defs.drt_file_hdr + "\n"
                                      + defs.block_note_hdr)
            self.fnames_to_save_to[device]['hdr'] = True
        elif device[0] == 'vog':
            self.__write_line_to_file(self.fnames_to_save_to[device]['fn'], defs.vog_file_hdr + "\n"
                                      + defs.block_note_hdr)
            self.fnames_to_save_to[device]['hdr'] = True

    @staticmethod
    def __parse_vog_line(line):
        the_parts = line.split(", ")
        print(the_parts)
        data = (int(the_parts[-2]), int(the_parts[-1]))
        return data

    @staticmethod
    def __parse_drt_line(line):
        the_parts = line.split(", ")
        data = the_parts[-1]
        return int(data)

    def __setup_output_file(self):
        fname = path.dirname(sys.argv[0]) + "\\com_output.txt"
        if path.exists(fname):
            with open(fname, "w") as temp:
                temp.write(defs.com_output_hdr)
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

    def close_file(self, fname):
        if fname in self.saved_files_open:
            self.saved_files_open.remove([fname[0], fname[1]])

    def save_com_msgs(self, msg):
        line = str(self.__get_current_time(save=True)) + ", " + msg
        with open(self.com_output_save_file, 'a+') as file:
            file.write(line)

    def receive_msg_from_ui(self, msg):
        if 'action' in msg.keys() and msg['action'] == "close":
            self.closing = True
            self.__end_exp_action_handler()
        elif 'control' in msg.keys() and msg['control'] == "run":
            self.device_manager.handle_msg({'type': "start device", 'device': msg['device']})
        elif 'control' in msg.keys() and msg['control'] == "stop":
            self.device_manager.handle_msg({'type': "stop device", 'device': msg['device']})
        else:
            self.device_manager.handle_msg(msg)

    def receive_msg_from_device_manager(self, msg):
        if msg['type'] == "data":
            self.__update_save(msg)
        if msg['type'] == "add":
            self.__add_device(msg)
        self.ui.handle_msg(msg)