# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from PySide2.QtCore import QTimer, QDir
from PySide2.QtWidgets import QMainWindow, QFileDialog
from View.main_view import CompanionWindow
import Controller.device_manager as manager
from os import path
import datetime


class CompanionController:
    def __init__(self):
        """ Set up view and device manager """
        self.view = QMainWindow()
        self.ui = CompanionWindow(self.view, self.send_msg_to_device_manager)
        self.view.show()
        self.device_manager = manager.DeviceManager(self.send_msg_to_ui)
        self.exp_data = {}
        self.current_exp_number = 0
        self.current_block_number = 0
        self.__setup_handlers()
        self.__start_update_timer()
        self.fname_to_save_to = ("", "")  # (r"C:\Users\phill\test.txt", '')  # Temporary save file name

    def __setup_handlers(self):
        """ Wire up all buttons etc. from the view """
        self.ui.save_action.triggered.connect(self.__save_handler)
        self.ui.save_as_action.triggered.connect(self.__save_as_handler)
        self.ui.open_file_action.triggered.connect(self.__open_action_handler)
        self.ui.trial_controls_action.triggered.connect(self.__trial_controls_action_handler)
        self.ui.input_action.triggered.connect(self.__input_action_handler)
        self.ui.output_action.triggered.connect(self.__output_action_handler)
        self.ui.begin_exp_action.triggered.connect(self.__begin_experiment_action_handler)
        self.ui.end_exp_action.triggered.connect(self.__end_experiment_action_handler)
        self.ui.display_tool_tips_action.triggered.connect(self.__display_tooltips_action_handler)
        self.ui.configure_action.triggered.connect(self.__configure_action_handler)
        self.ui.com_port_action.triggered.connect(self.__com_port_action_handler)
        self.ui.com_messages_action.triggered.connect(self.__com_messages_action_handler)
        self.ui.append_exp_action.triggered.connect(self.__append_experiment_action_handler)
        self.ui.run_block_push_button.clicked.connect(self.__begin_block_button_handler)
        self.ui.end_block_push_button.clicked.connect(self.__end_block_button_handler)
        self.ui.post_push_button.clicked.connect(self.__post_button_handler)

    def __save_handler(self):
        if path.exists(self.fname_to_save_to[0]):
            self.__save()
        else:
            self.__save_as_handler()

    def __save_as_handler(self):
        directory = QDir()
        fname = QFileDialog.getSaveFileName(None, 'Open file', directory.homePath(), '*.txt')
        if path.exists(fname[0]):
            self.fname_to_save_to = fname
            self.__save()

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    # Allows user to select a file through file explorer and opens it
    def __open_action_handler(self):
        """ Gets a file to open from the user """
        print("Open Action happening")
        directory = QDir()
        fname = QFileDialog.getOpenFileName(None, 'Open file', directory.homePath(), '*.txt')
        if path.exists(fname[0]):
            self.__parse_file(fname)

    def __begin_experiment_action_handler(self):
        # Check with user that they really do want to begin a new experiment
        # TODO: Add ui.experiment name?
        self.exp_data[self.current_exp_number] = \
            {'hdr': "Experiment number: " + str(self.current_exp_number) + # ", name: " + str(self.ui.block_name_label.text) +
                    ", start date/time: " + self.__get_current_time()}
        print("controller.CompanionController.__begin_exp_action_handler() Beginning Experiment, exp number is",
              self.current_exp_number)
        print(self.exp_data[self.current_exp_number]['hdr'])

    # TODO: Make this function useful
    # TODO: Remove prints in this function after debugging
    def __end_experiment_action_handler(self):
        # Check with user that they really do want to end the experiment
        self.current_exp_number += 1
        print("controller.CompanionController.__end_experiment_action_handler() Ending Experiment, new exp number is",
              self.current_exp_number)

    # TODO: Remove prints in this function after debugging
    # TODO: Fix this thing
    def __begin_block_button_handler(self):
        print("Run Block Button Pressed")
        msg_dict = {'type': "start block"}
        self.send_msg_to_device_manager(msg_dict)
        self.exp_data[self.current_exp_number][self.current_block_number] = \
            {'hdr': "\tblock " + str(self.current_block_number) + " start date/time: " +
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def __end_block_button_handler(self):
        print("New Block Button Pressed")
        msg_dict = {'type': "stop block"}
        self.send_msg_to_device_manager(msg_dict)
        self.current_block_number = 0

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def __trial_controls_action_handler(self):
        print("Trial Controls Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def __input_action_handler(self):
        print("Input Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def __output_action_handler(self):
        print("Output Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def __display_tooltips_action_handler(self):
        print("Display Tooltips Action triggered")

    # TODO: Make this function useful
    # TODO: Remove prints in this function after debugging
    def __configure_action_handler(self):
        print("Configure Action triggered")

    # TODO: Make this function useful
    # TODO: Remove prints in this function after debugging
    def __com_port_action_handler(self):
        print("COM Port Action triggered")

    # TODO: Make this function useful
    # TODO: Remove prints in this function after debugging
    def __com_messages_action_handler(self):
        print("COM Messages Action triggered")

    # TODO: Make this function useful
    # TODO: Remove prints in this function after debugging
    def __append_experiment_action_handler(self):
        print("Append Experiment Action triggered")

    # TODO: Remove prints in this function after debugging
    # TODO: Make this function useful
    def __post_button_handler(self):
        print("Post Button Pressed")

    def __parse_file(self, fname):
        """ Opens a file and reads data to view """
        file = open(fname[0], 'r')
        # TODO: make this work from here on.
        # Need to check and make sure file is a valid saved file before parsing, use headers?

    def __save(self):
        # TODO: Save all data from self.exp_data to file(s)
        self.__write_lines_to_file(("This is a test\n", "\tThis is a second test\n"))

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
        """ To be run under a timer/loop """
        self.device_manager.update()

    def __update_dict(self, msg_dict):
        if msg_dict['device'][0] == "drt":
            self.__add_drt_line(msg_dict)
        elif msg_dict['device'][0] == "vog":
            self.__add_vog_line(msg_dict)

    # TODO: Make this work
    def __add_drt_line(self, msg_dict):
        # Need milliseconds in here, __get_current_time wont work
        temp = self.exp_data[self.current_exp_number][self.current_block_number][self.__get_current_time()]

    # TODO: Make this work
    def __add_vog_line(self, msg_dict):
        pass

    @staticmethod
    def __get_current_time():
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def send_msg_to_device_manager(self, msg):
        self.device_manager.handle_msg(msg)

    def send_msg_to_ui(self, msg):
        if msg['type'] == "update":
            self.__update_dict(msg)
        self.ui.handle_msg(msg)
