# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtCore import QTimer, QDir
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from View.main_view import CompanionWindow
import Controller.device_manager as manager
from os import path
import datetime
from View.help_window import HelpWindow
import Model.defs as defs


class CompanionController:
    def __init__(self):
        """Set up view and device manager."""
        self.ui = CompanionWindow(self.receive_msg_from_ui)
        self.ui.show()
        self.device_manager = manager.DeviceManager(self.receive_msg_from_device_manager)
        # Experiment data structure
        self.exp_hdrs = []
        self.blk_hdrs = []
        self.blk_notes = []
        self.blk_data = []
        self.device_data = {}
        self.current_exp_number = 0
        self.current_block_number = -1
        self.current_exp_name = "N\A"
        self.closing = False

        self.exp_running = False
        self.block_running = False
        self.__setup_handlers()
        self.__start_update_timer()
        self.fname_to_save_to = ("", "")

    def __setup_handlers(self):
        """Wire up all buttons etc. from the view."""
        self.ui.save_action.triggered.connect(self.__save_handler)
        self.ui.save_as_action.triggered.connect(self.__save_as_handler)
        self.ui.open_file_action.triggered.connect(self.__open_action_handler)
        self.ui.trial_controls_action.triggered.connect(self.__trial_controls_action_handler)
        self.ui.input_action.triggered.connect(self.__input_action_handler)
        self.ui.output_action.triggered.connect(self.__output_action_handler)
        self.ui.run_new_exp_push_button.clicked.connect(self.__begin_exp_action_handler)
        self.ui.end_exp_push_button.clicked.connect(self.__end_exp_action_handler)
        self.ui.display_tool_tips_action.triggered.connect(self.__display_tooltips_action_handler)
        self.ui.configure_action.triggered.connect(self.__configure_action_handler)
        self.ui.com_port_action.triggered.connect(self.__com_port_action_handler)
        self.ui.com_messages_action.triggered.connect(self.__com_messages_action_handler)
        self.ui.append_exp_action.triggered.connect(self.__append_experiment_action_handler)
        self.ui.run_new_block_push_button.clicked.connect(self.__begin_block_button_handler)
        self.ui.end_block_push_button.clicked.connect(self.__end_block_button_handler)
        self.ui.save_block_note_push_button.clicked.connect(self.__save_block_note_button_handler)

    def __save_handler(self):
        if path.exists(self.fname_to_save_to[0]):
            self.__save()
        else:
            self.__save_as_handler()

    def __save_as_handler(self):
        directory = QDir()
        fname = QFileDialog.getExistingDirectory(None, 'Save Directory', directory.homePath(), QFileDialog.ShowDirsOnly)
        if fname[0] != "":
            self.fname_to_save_to = fname
            self.__save()

    def __open_action_handler(self):
        """Gets a file to open from the user."""
        directory = QDir()
        fname = QFileDialog.getOpenFileName(None, 'Open file', directory.homePath(), '*.txt')
        if path.exists(fname[0]):
            self.__parse_file(fname)

    def __begin_exp_action_handler(self):
        """Begins a new experiment as long as no other experiment is currently running."""
        if not self.exp_running:
            self.exp_running = True
            msg_dict = {'type': "start exp"}
            self.device_manager.handle_msg(msg_dict)
            self.ui.exp_num_val_label.setText(str(self.current_exp_number + 1))
            exp_name = self.ui.exp_name_input_box.text()
            current_time = self.__get_current_time()
            if exp_name == "":
                exp_name = "N/A"
            self.exp_hdrs.append("Experiment name: " + exp_name +
                                 ", start date/time: " + current_time)
            self.blk_hdrs.append([])
            self.blk_notes.append([])
            self.blk_data.append([])
            self.current_exp_name = exp_name
            self.ui.set_current_exp_time(current_time)
        else:
            self.message = HelpWindow("Error", "An experiment is already running")
            self.message.show()

    def __end_exp_action_handler(self):
        """Ends an experiment. If a block is currently running, ends the block as well."""
        if self.exp_running:
            self.exp_running = False
            msg_dict = {'type': "stop exp"}
            self.device_manager.handle_msg(msg_dict)
            self.current_exp_number += 1
            self.current_block_number = -1
            self.ui.block_num_val_label.setText(str(self.current_block_number + 1))
            if self.block_running:
                self.__end_block_button_handler()
        elif not self.closing:
            self.message = HelpWindow("Error", "No experiment running")
            self.message.show()

    def __begin_block_button_handler(self):
        """Begins a new block as long as an experiment is running and no other block is running."""
        if self.exp_running and not self.block_running:
            self.block_running = True
            self.current_block_number += 1
            self.ui.block_num_val_label.setText(str(self.current_block_number + 1))
            msg_dict = {'type': "start block"}
            self.device_manager.handle_msg(msg_dict)
            block_name = self.ui.block_name_label.text()
            current_time = self.__get_current_time()
            if block_name == "":
                block_name = "N/A"
            self.blk_hdrs[self.current_exp_number].append("Block name: " + block_name +
                                                          ", start date/time: " + current_time)
            self.blk_notes[self.current_exp_number].append([])
            self.blk_data[self.current_exp_number].append([])
            self.ui.set_current_block_time(current_time)
        elif self.exp_running and self.block_running:
            self.message = HelpWindow("Error", "A block is already running")
            self.message.show()
        else:
            self.message = HelpWindow("Error", "You must start an experiment first")
            self.message.show()

    def __end_block_button_handler(self):
        """Ends a block if one is currently running."""
        if self.block_running:
            self.block_running = False
            msg_dict = {'type': "stop block"}
            self.receive_msg_from_ui(msg_dict)
        else:
            self.message = HelpWindow("Error", "No block running")
            self.message.show()

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

    # TODO: Is this where keyflag goes?
    def __save_block_note_button_handler(self):
        if self.block_running:
            note = self.ui.get_block_note()
            if note != "":
                current_time = self.__get_current_time(True)
                self.blk_notes[self.current_exp_number][self.current_block_number].append(
                    "timestamp: " + current_time + ", note: " + note)
            else:
                self.message = HelpWindow("Error", "You must write a note before posting it.")
                self.message.show()
        else:
            self.message = HelpWindow("Error", "A block must be running first.")
            self.message.show()

    def __parse_file(self, fname):
        """Opens a file and reads data to view."""
        file = open(fname[0], 'r')
        # TODO: make this work from here on.
        # Need to check and make sure file is a valid saved file before parsing, use headers?

    def __save(self):
        # TODO: Save all data from self.exp_data to new file(s) based on number of devices
        lines = []
        for i in range(len(self.exp_hdrs)):
            lines.append(self.exp_hdrs[i] + "\n")
            for j in range(len(self.blk_hdrs[i])):
                #lines.append("\t" + self.blk_hdrs[i][j] + "\n")
                lines.append(self.blk_hdrs[i][j] + "\n")
                for h in range(len(self.blk_data[i][j])):
                    #lines.append("\t\t" + self.blk_data[i][j][h] + "\n")
                    lines.append(self.blk_data[i][j][h] + "\n")
        self.__write_lines_to_file(lines)

    def __write_lines_to_file(self, lines):
        file = open(self.fname_to_save_to[0], 'w+')
        file.writelines(lines)
        file.close()

    def __start_update_timer(self):
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.__device_update)
        self.update_timer.start(1)

    def __device_update(self):
        """To be run under a timer/loop."""
        self.device_manager.update()

    def __update_dict(self, msg_dict):
        if msg_dict['device'][0] == "drt":
            self.__add_drt_line(msg_dict)
        elif msg_dict['device'][0] == "vog":
            self.__add_vog_line(msg_dict)

    def __add_drt_line(self, msg_dict):
        line = "device: " + msg_dict['device'][0] + " on " + msg_dict['device'][1] + ", timestamp: " + \
               self.__get_current_time(True) + ", "
        for i in range(0, len(defs.drt_trial_fields)):
            line += defs.drt_ui_fields[i] + ": " + msg_dict[defs.drt_trial_fields[i]] + ", "
        line = line[0:-3]
        self.device_data[msg_dict['device']].append(line)

    def __add_vog_line(self, msg_dict):
        line = "device: " + msg_dict['device'][0] + " on " + msg_dict['device'][1] +\
               ", timestamp: " + self.__get_current_time(True) + ", "
        for i in range(len(defs.vog_block_field)):
            line += defs.vog_ui_fields[i] + ": " + msg_dict[defs.vog_block_field[i]] + ", "
        line = line[0:-3]
        self.blk_data[self.current_exp_number][self.current_block_number].append(line)

    def __add_device(self, msg_dict):
        self.device_data[msg_dict['device']] = []

    @staticmethod
    def __get_current_time(mil=False):
        if mil:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def receive_msg_from_ui(self, msg):
        if 'action' in msg.keys() and msg['action'] == "close":
            self.closing = True
            self.__end_exp_action_handler()
        else:
            self.device_manager.handle_msg(msg)

    def receive_msg_from_device_manager(self, msg):
        if msg['type'] == "data":
            self.__update_dict(msg)
        if msg['type'] == "add":
            self.__add_device(msg)
        self.ui.handle_msg(msg)
