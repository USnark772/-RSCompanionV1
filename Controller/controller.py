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
# Date: 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from os import path
import logging
import logging.config
import configparser
from tempfile import gettempdir
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QTimer, QDir, QSize
from PySide2.QtGui import QKeyEvent
from CompanionLib.time_funcs import get_current_time
import CompanionLib.checkers as checker
from Model.general_defs import program_output_hdr, about_RS_text, about_RS_app_text, up_to_date, update_available, \
    device_connection_error, config_file_path
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
from Devices.Webcam.Controller.webcam_controller import WebcamController
from Devices.Webcam.View.webcam_tab import WebcamViewer


class CompanionController:
    def __init__(self):
        """ Creates the different element objects of the View and Controller """
        config = configparser.ConfigParser()
        try:
            config.read(config_file_path)
            logginglevel = eval('logging.' + config.get('logging', 'level'))
            inierror = False
        except configparser.NoSectionError as e:
            logginglevel = logging.DEBUG
            inierror = True
        logging.basicConfig(filename=self.__setup_output_file("companion_app_log.txt"), filemode='w',
                            level=logginglevel, format='%(levelname)s - %(name)s - %(funcName)s: %(message)s')
        self.logger = logging.getLogger(__name__)
        if inierror:
            self.logger.debug("Error reading config.ini, logging level set to debug")
        self.logger.debug("Initializing")
        # self.program_output_save_file = self.__setup_output_file("companion_app_console_output.txt")
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
        self.devices = {}

        # Assemble View objects
        self.__initialize_view()

        # self.__add_webcam_tab()
        self.logger.debug("Initialized")

    ########################################################################################
    # public functions
    ########################################################################################

    def receive_msg_from_device_manager(self, msg):
        """
        Receives a message from the device manager. msg is expected to be a dict(). Handles the msg depending on
        what 'type' it is
        """
        self.logger.debug("running")
        if not checker.check_dict(msg):
            self.logger.warning("expected dictionary, got: " + str(type(msg)))
            return
        if 'type' not in msg:
            self.logger.warning("Error in dictionary format from device manager, 'type' not found.")
            return
        msg_type = msg['type']
        if msg_type == "data":
            self.logger.debug("type was data")
            self.__update_save(msg)
            self.devices[msg['device']]['controller'].add_data_to_graph(get_current_time(graph=True), msg['values'])
        elif msg_type == "settings":
            self.logger.debug("type was settings")
            self.devices[msg['device']]['controller'].update_config(msg['values'])
        elif msg_type == "add":
            self.logger.debug("type was add")
            self.__add_device(msg['device'])
        elif msg_type == "remove":
            self.logger.debug("type was remove")
            self.__remove_device(msg['device'])
        elif msg_type == "error":
            self.logger.debug("type was error")
            self.ui.show_help_window(msg_type, device_connection_error)
        self.logger.debug("done")

    ########################################################################################
    # initial setup
    ########################################################################################

    def __initialize_view(self):
        """ Assembles the different View objects into a window. Initializes some handlers and controller functions """
        self.logger.debug("running")
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
        self.logger.debug("done")

    def __setup_file_dialog(self):
        """
        Sets up a file dialog for 1. saving data from experiments and 2. opening previous experiments.
        2. not implemented yet
        """
        self.logger.debug("running")
        self.file_dialog.setOptions(QFileDialog.ShowDirsOnly)
        self.file_dialog.setViewMode(QFileDialog.Detail)
        self.file_dialog.setDirectory(QDir().homePath())
        self.file_dialog.setFileMode(QFileDialog.Directory)
        self.logger.debug("done")

    def __setup_handlers(self):
        """Wire up buttons etc. in the view."""
        self.logger.debug("running")
        self.button_box.add_create_button_handler(self.__create_end_exp)
        self.button_box.add_start_button_handler(self.__start_stop_exp)
        self.note_box.add_note_box_changed_handler(self.__check_toggle_post_button)
        self.note_box.add_post_handler(self.__post_handler)
        self.menu_bar.add_about_app_handler(self.__about_app)
        self.menu_bar.add_about_company_handler(self.__about_company)
        self.menu_bar.add_update_handler(self.__check_for_updates_handler)
        self.ui.keyPressEvent = self.__key_press_handler
        self.ui.add_close_handler(self.ui_close_event_handler)
        self.logger.debug("done")

    def __start_update_timer(self):
        """ A timer to trigger device manager to check for updates """
        self.logger.debug("running")
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.__device_update)
        self.update_timer.start(1000)
        self.logger.debug("done")

    ########################################################################################
    # Experiment handling
    ########################################################################################

    def __create_end_exp(self):
        """
        Either begin or end an experiment. If beginning an experiment then get a dir path from the user to save
        experiment data and check output files. Path is required to continue.
        """
        self.logger.debug("running")
        if not self.exp_created:
            self.logger.debug("creating experiment")
            if not self.__get_save_dir_path():
                self.logger.debug("no save directory selected, done running __create_end_exp()")
                return
            self.__update_device_filenames()
            self.__check_save_file_hdrs()
            self.__create_exp()
            self.logger.debug("done")
        else:
            self.logger.debug("ending experiment")
            self.__end_exp()
        self.logger.debug("done")

    def __create_exp(self):
        self.logger.debug("running")
        self.exp_created = True
        self.button_box.toggle_create_button()
        try:
            self.device_manager.start_exp_all()
        except Exception as e:
            self.logger.exception("Failed trying to start_exp_all")
            self.button_box.toggle_create_button()
            self.exp_created = False
            return
        self.info_box.set_start_time(get_current_time(time=True))
        self.logger.debug("done")

    def __end_exp(self):
        self.logger.debug("running")
        self.exp_created = False
        self.button_box.toggle_create_button()
        try:
            self.device_manager.end_exp_all()
        except Exception as e:
            self.logger.exception("Failed trying to end_exp_all")
        self.logger.debug("done")

    def __start_stop_exp(self):
        self.logger.debug("running")
        if self.exp_running:
            self.logger.debug("stopping experiment")
            self.__stop_exp()
        else:
            self.logger.debug("starting experiment")
            self.__start_exp()
        self.logger.debug("done")

    def __start_exp(self):
        #print("start exp")
        self.logger.debug("running")
        self.exp_running = True
        try:
            #print("Start block all()")
            self.device_manager.start_block_all()
        except Exception as e:
            #print("caught exception")
            self.logger.exception("Failed trying to start_block_all")
            #print(str(e))
            self.exp_running = False
            return
        #print("updating other stuff")
        self.current_cond_name = self.button_box.get_condition_name()
        self.__check_toggle_post_button()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self.logger.debug("done")

    def __stop_exp(self):
        self.logger.debug("running")
        self.exp_running = False
        try:
            self.device_manager.end_block_all()
        except Exception as e:
            self.logger.exception("Failed trying to end_block_all")
        self.__check_toggle_post_button()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self.logger.debug("done")

    def __check_toggle_post_button(self):
        """ If an experiment is created and running and there is a note then allow user access to post button. """
        self.logger.debug("running")
        if self.exp_created and self.exp_running and len(self.note_box.get_note()) > 0:
            self.logger.debug("button = true")
            self.note_box.toggle_post_button(True)
        else:
            self.logger.debug("button = false")
            self.note_box.toggle_post_button(False)
        self.logger.debug("done")

    ########################################################################################
    # Data saving
    ########################################################################################

    def __key_press_handler(self, event):
        """ Only act on alphabetical key presses """
        self.logger.debug("running")
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.flag_box.set_flag(chr(event.key()))
            event.accept()
        else:
            event.ignore()
        self.logger.debug("done")

    def __post_handler(self):
        """ Write a given user note to all device output files. """
        self.logger.debug("running")
        note = self.note_box.get_note()
        self.note_box.clear_note()
        flag = self.flag_box.get_flag()
        time = get_current_time(True, True, True)
        name = self.current_cond_name
        for device in self.devices:
            self.logger.debug("writing to: " + device[0] + " " + device[1])
            spacer = self.__make_note_spacer(device[0])
            try:
                self.__write_line_to_file(self.devices[device]['fn'],
                                          "note, " + name + ", " + flag + ", " + time + spacer + ", " + note)
            except Exception as e:
                self.logger.exception("Failed writing to file")
        self.logger.debug("done")

    def __get_save_dir_path(self):
        return self.file_dialog.exec_()

    def __write_line_to_file(self, fname, line):
        """ Write the given line to the given file using the save dir selected by user. """
        self.logger.debug("running")
        if not line.endswith("\n"):
            line = line + "\n"
        filepath = path.join(self.file_dialog.directory().path(), fname)
        filepath += ".txt"
        with open(filepath, 'a+') as file:
            self.logger.debug("writing line: " + line + " to fname: " + fname)
            file.write(line)
        self.logger.debug("done")

    def __check_for_updates_handler(self):
        """ Ask VersionChecker if there is an update then alert user to result. """
        self.logger.debug("running")
        vc = VersionChecker()
        is_available = vc.check_version()
        if is_available == 1:
            self.ui.show_help_window("Update", update_available)
        elif is_available == 0:
            self.ui.show_help_window("Update", up_to_date)
        elif is_available == -1:
            self.ui.show_help_window("Error", "There was an unexpected error connecting to the repository."
                                              " Please check https://github.com/redscientific/CompanionApp manually"
                                              " or contact Red Scientific directly.")
        self.logger.debug("done")

    def __update_save(self, msg):
        """ Save device output to file 'fn'. msg is expected to be a dictionary. """
        self.logger.debug("running")
        if not checker.check_dict(msg):
            self.logger.warning("expected dictionary, got: " + str(type(msg)))
            return
        if 'device' in msg.keys():
            device = msg['device']
        else:
            self.logger.warning("key error, 'device' not in msg keys")
            return
        cond_name = self.current_cond_name
        flag = self.flag_box.get_flag()
        time = get_current_time(True, True, True)
        prepend = device[0] + ", " + cond_name + ", " + flag + ", " + time
        if device in self.devices:
            line = self.devices[device]['controller'].format_output_for_save_file(msg['values'])
        else:
            self.logger.warning("key error, device not in self.devices")
            return
        self.__write_line_to_file(self.devices[device]['fn'], prepend + line)
        self.logger.debug("done")

    def __check_save_file_hdrs(self):
        """ Ensure that all device output files have headers. """
        self.logger.debug("running")
        for device in self.devices:
            if not self.devices[device]['hdr_bool']:
                self.__add_hdr_to_file(device)
        self.logger.debug("done")

    def __make_save_filename_for_device(self, device):
        """ Create a unique filename for device output save file. """
        self.logger.debug("running")
        if not checker.check_device_tuple(device):
            self.logger.warning("expected tuple of two strings, got otherwise")
            return
        if device not in self.devices:
            self.logger.debug("done, device not found in self.devices")
            return
        self.devices[device]['fn'] = device[0] + " on " + device[1] + " " + get_current_time(save=True)
        self.devices[device]['hdr_bool'] = False
        self.logger.debug("done")

    def __update_device_filenames(self):
        """ Ensure all devices have new files to save output data to. """
        self.logger.debug("running")
        for device in self.devices:
            self.__make_save_filename_for_device(device)
        self.logger.debug("done")

    def __add_hdr_to_file(self, device):
        """ Add device specific header to given device's output file. """
        self.logger.debug("running")
        if not checker.check_device_tuple(device):
            self.logger.warning("expected tuple of two strings, got otherwise")
            return
        if device not in self.devices:
            self.logger.debug("done, device not found in self.devices")
            return
        self.__write_line_to_file(self.devices[device]['fn'], self.devices[device]['controller'].get_hdr())
        self.devices[device]['hdr_bool'] = True
        self.logger.debug("done")

    @staticmethod
    def __setup_output_file(filename):
        """ Create program output file to save log. """
        fname = gettempdir() + "\\" + filename
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
        self.logger.debug("running")
        self.device_manager.update()
        self.logger.debug("done")

    def __add_device(self, device):
        """
        Handles when a new device is found by the device manager and added to the program's scope.
        Creates a device type specific graph if needed and connects device specific controller to device graph and
        device manager to let device controller handle device specific messages. Each device gets its own configure tab.
        """
        self.logger.debug("running")
        if not checker.check_device_tuple(device):
            self.logger.warning("expected tuple of two strings, got otherwise")
            return
        if device[0] == "drt":
            self.logger.debug("Got " + device[0] + " " + device[1])
            self.__num_drts += 1
            if not device[0] in self.__graphs:
                self.logger.debug("Making graph for drt")
                if not self.__make_drt_graph():
                    self.__num_drts -= 1
                    self.logger.warning("Failed to make_drt_graph")
                    return
            self.logger.debug("Making controller for drt")
            try:
                device_controller = DRTController(self.tab_box, device, self.device_manager.handle_msg,
                                                  self.add_data_to_graph)
            except Exception as e:
                self.logger.exception("failed to make device_controller for drt" + str(device))
                self.__num_drts -= 1
                self.__check_num_devices()
                return
            self.logger.debug("Made controller for drt")
        elif device[0] == "vog":
            self.logger.debug("Got " + device[0] + " " + device[1])
            self.__num_vogs += 1
            if not device[0] in self.__graphs:
                self.logger.debug("Making graph for vog")
                if not self.__make_vog_graph():
                    self.logger.warning("Failed to make_vog_graph")
                    self.__num_vogs -= 1
                    return
            self.logger.debug("Making controller for vog")
            try:
                device_controller = VOGController(self.tab_box, device, self.device_manager.handle_msg,
                                                  self.add_data_to_graph)
            except Exception as e:
                self.logger.exception("failed to make device_controller for vog" + str(device))
                self.__num_vogs -= 1
                self.__check_num_devices()
                return
            self.logger.debug("Made controller for vog")
        else:
            self.logger.debug("Unknown device in __add_device()")
            return
        self.__graphs[device[0]].get_graph().add_device(device[1])
        self.devices[device] = {}
        self.devices[device]['controller'] = device_controller
        self.tab_box.add_tab(device_controller.get_tab_obj(), device[1])
        self.__make_save_filename_for_device(device)
        if self.__dir_chosen:  # TODO: Is this ever used?
            self.__add_hdr_to_file(device)
        self.logger.debug("done")

    def __remove_device(self, device):
        """ Removes device tab, graph link and device information """
        self.logger.debug("running")
        if not checker.check_device_tuple(device):
            self.logger.warning("expected tuple of two strings, got otherwise")
            return
        self.logger.debug("Removing " + device[0] + " " + device[1])
        if device in self.devices:
            if device[0] == "drt":
                self.__num_drts -= 1
            elif device[0] == "vog":
                self.__num_vogs -= 1
            else:
                self.logger.debug("found a device that is unknown: " + device[0] + " " + device[1])
            self.tab_box.remove_tab(device[1])
            self.__graphs[device[0]].get_graph().remove_device(device[1])
            del self.devices[device]
            self.__check_num_devices()
        self.logger.debug("done")

    def __add_webcam_tab(self):
        self.logger.debug("running")
        try:
            controller = WebcamController(self.tab_box)
        except Exception as e:
            self.logger.exception("Failed to make webcam_controller")
            return
        self.devices["webcams"]["controller"] = controller
        self.logger.debug("done")

    ########################################################################################
    # Other handlers
    ########################################################################################

    def ui_close_event_handler(self):
        """ Shut down all devices before closing the app. """
        self.logger.debug("running")
        if self.exp_running:
            try:
                self.device_manager.end_block_all()
            except Exception as e:
                self.logger.exception("Failed to end_block_all")
        if self.exp_created:
            try:
                self.device_manager.end_exp_all()
            except Exception as e:
                self.logger.exception("Failed to end_exp_all")
        self.logger.debug("done")

    def __about_company(self):
        """ Display company information. """
        self.logger.debug("running")
        self.ui.show_help_window("About Red Scientific", about_RS_text)
        self.logger.debug("done")

    def __about_app(self):
        """ Display app information. """
        self.logger.debug("running")
        self.ui.show_help_window("About Red Scientific Companion App", about_RS_app_text)
        self.logger.debug("done")

    ########################################################################################
    # graph handling
    ########################################################################################

    def __check_num_devices(self):
        self.logger.debug("running")
        if self.__num_drts == 0:
            self.__destroy_drt_graph()
        if self.__num_vogs == 0:
            self.__destroy_vog_graph()
        self.logger.debug("done")

    def __make_drt_graph(self):
        """ Create a drt type graph and add it to the display area. """
        self.logger.debug("running")
        try:
            graph = DRTGraph(self.graph_box)
        except Exception as e:
            self.logger.exception("Failed to make DRTGraph")
            return False
        graph_frame = GraphFrame(self.graph_box, graph)
        self.__graphs["drt"] = graph_frame
        self.graph_box.add_display(graph_frame)
        self.logger.debug("done")
        return True

    def __destroy_drt_graph(self):
        """ Remove the drt graph. Typically called when all drt devices have been disconnected. """
        self.logger.debug("running")
        if "drt" in self.__graphs.keys():
            self.graph_box.remove_display(self.__graphs["drt"])
            del self.__graphs["drt"]
        self.logger.debug("done")

    def __make_vog_graph(self):
        """ Create a vog type graph and add it to the display area. """
        self.logger.debug("running")
        try:
            graph = VOGGraph(self.graph_box)
        except Exception as e:
            self.logger.exception("Failed to make VOGGraph")
            return False
        graph_frame = GraphFrame(self.graph_box, graph)
        graph_frame.set_graph_height(500)
        self.__graphs["vog"] = graph_frame
        self.graph_box.add_display(graph_frame)
        self.logger.debug("done")
        return True

    def __destroy_vog_graph(self):
        """ Remove the vog graph. Typically called when all vog devices have been disconnected. """
        self.logger.debug("running")
        if "vog" in self.__graphs.keys():
            self.graph_box.remove_display(self.__graphs["vog"])
            del self.__graphs["vog"]
        self.logger.debug("done")

    def __refresh_all_graphs(self):
        self.logger.debug("running")
        for graph in self.__graphs:
            self.__graphs[graph].get_graph().refresh_self()
        self.logger.debug("done")

    def add_data_to_graph(self, device, data):
        """ Pass data to device type graph along with specific device id. """
        self.logger.debug("running")
        if not checker.check_device_tuple(device):
            return
        if device[0] not in self.__graphs:
            self.logger.warning("device not found in self.__graphs")
            return
        self.__graphs[device[0]].get_graph().add_data(device[1], data)
        self.logger.debug("done")
