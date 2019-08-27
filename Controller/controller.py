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
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from os import path
from sys import argv
from tempfile import gettempdir
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QTimer, QDir, QSize
from PySide2.QtGui import QKeyEvent
from CompanionLib.time_funcs import get_current_time
from Model.general_defs import program_output_hdr, about_RS_text, about_RS_app_text, up_to_date, update_available, \
    device_connection_error
from View.MainWindow.main_window import CompanionWindow
from View.DockWidget.control_dock import ControlDock
from View.DockWidget.button_box import ButtonBox
from View.DockWidget.info_box import InfoBox
from View.DockWidget.flag_box import FlagBox
from View.DockWidget.note_box import NoteBox
from View.MenuBarWidget.menu_bar import MenuBar
from View.DisplayWidget.display_container import DisplayContainer
from View.DisplayWidget.graph_frame import GraphFrame
from View.TabWidget.device_tab import TabContainer
from Controller.version_checker import VersionChecker
from Controller.device_manager import DeviceManager
from Devices.DRT.Controller.drt_controller import DRTController
from Devices.DRT.View.drt_graph import DRTGraph
from Devices.VOG.Controller.vog_controller import VOGController
from Devices.VOG.View.vog_graph import VOGGraph


class CompanionController:
    def __init__(self):
        """ Creates the different element objects of the View and Controller """
        ui_min_size = QSize(450, 550)
        dock_size = QSize(850, 160)
        button_box_size = QSize(205, 120)
        info_box_size = QSize(230, 120)
        flag_box_size = QSize(80, 120)
        note_box_size = QSize(250, 120)
        tab_box_width_range = (350, 320)
        self.ui = CompanionWindow(ui_min_size)
        self.menu_bar = MenuBar(self.ui)
        self.control_dock = ControlDock(self.ui, dock_size)
        self.button_box = ButtonBox(self.control_dock, button_box_size)
        self.info_box = InfoBox(self.control_dock, info_box_size)
        self.flag_box = FlagBox(self.control_dock, flag_box_size)
        self.note_box = NoteBox(self.control_dock, note_box_size)
        self.graph_box = DisplayContainer(self.ui, self.__refresh_all_graphs)
        self.tab_box = TabContainer(self.ui, tab_box_width_range)
        self.file_dialog = QFileDialog(self.ui)

        self.device_manager = DeviceManager(self.receive_msg_from_device_manager)

        # Initialize storage and state
        self.__graphs = {}
        self.exp_created = False
        self.exp_running = False
        self.__dir_chosen = False
        self.__num_drts = 0
        self.__num_vogs = 0
        self.current_cond_name = ""
        self.program_output_save_file = self.__setup_output_file()
        self.devices = {}

        # Assemble View objects
        self.__initialize_view()

    ########################################################################################
    # public functions
    ########################################################################################

    def receive_msg_from_device_manager(self, msg):
        """
        Receives a message from the device manager. msg is expected to be a dict(). Handles the msg depending on
        what 'type' it is
        """
        msg_type = msg['type']
        if msg_type == "data":
            self.__update_save(msg)
            self.devices[msg['device']]['controller'].add_data_to_graph(get_current_time(graph=True), msg['values'])
        elif msg_type == "settings":
            self.devices[msg['device']]['controller'].update_config(msg['values'])
        elif msg_type == "add":
            self.__add_device(msg['device'])
        elif msg_type == "remove":
            self.__remove_device(msg['device'])
        elif msg_type == "save":
            self.__save_output_msg(msg['msg'])
        elif msg_type == "error":
            self.ui.show_help_window(msg_type, device_connection_error)

    ########################################################################################
    # initial setup
    ########################################################################################

    def __initialize_view(self):
        """ Assembles the different View objects into a window. Initializes some handlers and controller functions """
        self.__setup_file_dialog()
        self.__setup_handlers()
        self.__start_update_timer()
        self.control_dock.add_widget(self.button_box)
        self.control_dock.add_widget(self.flag_box)
        self.control_dock.add_widget(self.note_box)
        self.control_dock.add_widget(self.info_box)
        self.ui.add_menu_bar(self.menu_bar)
        self.ui.add_dock_widget(self.control_dock)
        self.ui.add_graph_container(self.graph_box)
        self.ui.add_tab_widget(self.tab_box)
        self.ui.show()

    def __setup_file_dialog(self):
        """
        Sets up a file dialog for 1. saving data from experiments and 2. opening previous experiments.
        2. not implemented yet
        """
        self.file_dialog.setOptions(QFileDialog.ShowDirsOnly)
        self.file_dialog.setViewMode(QFileDialog.Detail)
        self.file_dialog.setDirectory(QDir().homePath())
        self.file_dialog.setFileMode(QFileDialog.Directory)

    def __setup_handlers(self):
        """Wire up buttons etc. in the view."""
        self.button_box.add_create_button_handler(self.__create_end_exp)
        self.button_box.add_start_button_handler(self.__start_stop_exp)
        self.note_box.add_note_box_changed_handler(self.__check_toggle_post_button)
        self.note_box.add_post_handler(self.__post_handler)
        self.menu_bar.add_about_app_handler(self.__about_app)
        self.menu_bar.add_about_company_handler(self.__about_company)
        self.menu_bar.add_update_handler(self.__check_for_updates_handler)
        self.ui.keyPressEvent = self.__key_press_handler
        self.ui.add_close_handler(self.ui_close_event_handler)

    def __start_update_timer(self):
        """ A timer to trigger device manager to check for updates """
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.__device_update)
        self.update_timer.start(1)

    ########################################################################################
    # Experiment handling
    ########################################################################################

    def __create_end_exp(self):
        """
        Either begin or end an experiment. If beginning an experiment then get a dir path from the user to save
        experiment data and check output files. Path is required to continue.
        """
        if not self.exp_created:
            if not self.__get_save_dir_path():
                return
            self.__update_device_filenames()
            self.__check_save_file_hdrs()
            self.__create_exp()
        else:
            self.__end_exp()

    def __create_exp(self):
        self.exp_created = True
        self.button_box.toggle_create_button()
        self.device_manager.start_exp_all()
        self.info_box.set_start_time(get_current_time(time=True))

    def __end_exp(self):
        self.exp_created = False
        self.button_box.toggle_create_button()
        self.device_manager.end_exp_all()

    def __start_stop_exp(self):
        if self.exp_running:
            self.__stop_exp()
        else:
            self.__start_exp()

    def __start_exp(self):
        self.exp_running = True
        self.device_manager.start_block_all()
        self.current_cond_name = self.button_box.get_condition_name()
        self.__check_toggle_post_button()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()

    def __stop_exp(self):
        self.exp_running = False
        self.device_manager.end_block_all()
        self.__check_toggle_post_button()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()

    def __check_toggle_post_button(self):
        """ If an experiment is created and running and there is a note then allow user access to post button. """
        if self.exp_created and self.exp_running and len(self.note_box.get_note()) > 0:
            self.note_box.toggle_post_button(True)
        else:
            self.note_box.toggle_post_button(False)

    ########################################################################################
    # Data saving
    ########################################################################################

    def __key_press_handler(self, event):
        """ Only act on alphabetical key presses """
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.flag_box.set_flag(chr(event.key()))
            event.accept()
        else:
            event.ignore()

    def __save_output_msg(self, msg):
        """ Write a given msg to the program output file. """
        line = str(get_current_time(save=True)) + ", " + msg
        with open(self.program_output_save_file, 'a+') as file:
            file.write(line)

    def __post_handler(self):
        """ Write a given user note to all device output files. """
        note = self.note_box.get_note()
        self.note_box.clear_note()
        flag = self.flag_box.get_flag()
        time = get_current_time(True, True, True)
        name = self.current_cond_name
        for device in self.devices:
            spacer = self.__make_note_spacer(device[0])
            self.__write_line_to_file(self.devices[device]['fn'],
                                      "note, " + name + ", " + flag + ", " + time + spacer + ", " + note)

    def __get_save_dir_path(self):
        return self.file_dialog.exec_()

    def __write_line_to_file(self, fname, line):
        """ Write the given line to the given file using the save dir selected by user. """
        line = line + "\n"
        filepath = path.join(self.file_dialog.directory().path(), fname)
        filepath += ".txt"
        with open(filepath, 'a+') as file:
            file.write(line)

    def __check_for_updates_handler(self):
        """ Ask VersionChecker if there is an update then alert user to result. """
        vc = VersionChecker(self.__save_output_msg)
        is_available = vc.check_version()
        if is_available == 1:
            self.ui.show_help_window("Update", update_available)
        elif is_available == 0:
            self.ui.show_help_window("Update", up_to_date)
        elif is_available == -1:
            self.ui.show_help_window("Error", "There was an unexpected error connecting to the repository."
                                              " Please check https://github.com/redscientific/CompanionApp manually"
                                              " or contact Red Scientific directly.")

    def __update_save(self, msg):
        """ Save device output to file 'fn'. msg is expected to be a dictionary. """
        device = msg['device']
        cond_name = self.current_cond_name
        flag = self.flag_box.get_flag()
        time = get_current_time(True, True, True)
        prepend = device[0] + ", " + cond_name + ", " + flag + ", " + time
        line = self.devices[device]['controller'].format_output_for_save_file(msg['values'])
        self.__write_line_to_file(self.devices[device]['fn'], prepend + line)

    def __check_save_file_hdrs(self):
        """ Ensure that all device output files have headers. """
        for device in self.devices:
            if not self.devices[device]['hdr_bool']:
                self.__add_hdr_to_file(device)

    def __make_save_filename_for_device(self, device):
        """ Create a unique filename for device output save file. """
        self.devices[device]['fn'] = device[0] + " on " + device[1] + " " + get_current_time(save=True)
        self.devices[device]['hdr_bool'] = False

    def __update_device_filenames(self):
        """ Ensure all devices have new files to save output data to. """
        for device in self.devices:
            self.__make_save_filename_for_device(device)

    def __add_hdr_to_file(self, device):
        """ Add device specific header to given device's output file. """
        self.__write_line_to_file(self.devices[device]['fn'], self.devices[device]['controller'].get_hdr())
        self.devices[device]['hdr_bool'] = True

    @staticmethod
    def __setup_output_file():
        """ Create program output file to save log. """
        fname = gettempdir() + "\\companion_app_console_output.txt"
        with open(fname, "w") as temp:
            temp.write(program_output_hdr)
        return fname

    @staticmethod
    def __make_note_spacer(device):
        """ For formatting save files when certain data slots are empty. """
        if device == "drt":
            return ", , "
        elif device == "vog":
            return ", , , , "

    ########################################################################################
    # generic device handling
    ########################################################################################

    def __device_update(self):
        """ To be setup under a timer. """
        self.device_manager.update()

    def __add_device(self, device):
        """
        Handles when a new device is found by the device manager and added to the program's scope.
        Creates a device type specific graph if needed and connects device specific controller to device graph and
        device manager to let device controller handle device specific messages. Each device gets its own configure tab.
        """
        if device[0] == "drt":
            self.__num_drts += 1
            if not device[0] in self.__graphs:
                self.__make_drt_graph()
            device_controller = DRTController(self.tab_box, device, self.device_manager.handle_msg,
                                              self.add_data_to_graph)
        elif device[0] == "vog":
            self.__num_vogs += 1
            if not device[0] in self.__graphs:
                self.__make_vog_graph()
            device_controller = VOGController(self.tab_box, device, self.device_manager.handle_msg,
                                              self.add_data_to_graph)
        else:
            return
        self.__graphs[device[0]].get_graph().add_device(device[1])
        self.devices[device] = {}
        self.devices[device]['controller'] = device_controller
        self.tab_box.add_tab(device_controller.get_tab_obj(), device[1])
        self.__make_save_filename_for_device(device)
        if self.__dir_chosen:
            self.__add_hdr_to_file(device)

    def __remove_device(self, device):
        """ Removes device tab, graph link and device information """
        if device in self.devices:
            if device[0] == "drt":
                self.__num_drts -= 1
            elif device[0] == "vog":
                self.__num_vogs -= 1
            self.tab_box.remove_tab(device[1])
            self.__graphs[device[0]].get_graph().remove_device(device[1])
            del self.devices[device]
            self.__check_num_devices()

    ########################################################################################
    # Other handlers
    ########################################################################################

    def ui_close_event_handler(self):
        """ Shut down all devices before closing the app. """
        if self.exp_running:
            self.device_manager.end_block_all()
        if self.exp_created:
            self.device_manager.end_exp_all()

    def __about_company(self):
        """ Display company information. """
        self.ui.show_help_window("About Red Scientific", about_RS_text)

    def __about_app(self):
        """ Display app information. """
        self.ui.show_help_window("About Red Scientific Companion App", about_RS_app_text)

    ########################################################################################
    # graph handling
    ########################################################################################

    def __check_num_devices(self):
        if self.__num_drts == 0:
            self.__destroy_drt_graph()
        if self.__num_vogs == 0:
            self.__destroy_vog_graph()

    def __make_drt_graph(self):
        """ Create a drt type graph and add it to the display area. """
        graph = DRTGraph(self.graph_box)
        graph_frame = GraphFrame(self.graph_box, graph)
        self.__graphs["drt"] = graph_frame
        self.graph_box.add_display(graph_frame)

    def __destroy_drt_graph(self):
        """ Remove the drt graph. Typically called when all drt devices have been disconnected. """
        if "drt" in self.__graphs.keys():
            self.graph_box.remove_display(self.__graphs["drt"])
            del self.__graphs["drt"]

    def __make_vog_graph(self):
        """ Create a vog type graph and add it to the display area. """
        graph = VOGGraph(self.graph_box)
        graph_frame = GraphFrame(self.graph_box, graph)
        graph_frame.set_graph_height(500)
        self.__graphs["vog"] = graph_frame
        self.graph_box.add_display(graph_frame)

    def __destroy_vog_graph(self):
        """ Remove the vog graph. Typically called when all vog devices have been disconnected. """
        if "vog" in self.__graphs.keys():
            self.graph_box.remove_display(self.__graphs["vog"])
            del self.__graphs["vog"]

    def __refresh_all_graphs(self):
        for graph in self.__graphs:
            self.__graphs[graph].get_graph().refresh_self()

    def add_data_to_graph(self, device, data):
        """ Pass data to device type graph along with specific device id. """
        self.__graphs[device[0]].get_graph().add_data(device[1], data)
