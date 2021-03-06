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
# Date: 2019 - 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import logging
from typing import Tuple
from tempfile import gettempdir
from datetime import datetime
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QDir, QSize, QSettings, QUrl
from PySide2.QtGui import QKeyEvent, QDesktopServices
from CompanionLib.companion_helpers import get_current_time, check_device_tuple, write_line_to_file
from Model.general_defs import program_output_hdr, about_RS_text, about_RS_app_text, up_to_date, update_available, \
    error_checking_for_update, device_connection_error, current_version_str
from View.MainWindow.main_window import CompanionWindow
from View.DockWidget.control_dock import ControlDock
from View.DockWidget.button_box import ButtonBox
from View.DockWidget.info_box import InfoBox
from View.DockWidget.flag_box import FlagBox
from View.DockWidget.note_box import NoteBox
from View.MenuBarWidget.menu_bar import MenuBar
from View.DisplayWidget.display_container import DisplayContainer
from View.DisplayWidget.graph_frame import GraphFrame
from View.TabWidget.device_tab_container import TabContainer
from View.OutputLog.output_window import OutputWindow
from Controller.version_checker import VersionChecker
from Controller.RS_Device_Manager.rs_device_manager import RSDeviceConnectionManager, PortWorker
from Devices.DRT.Controller.drt_controller import DRTController
from Devices.DRT.View.drt_graph import DRTGraph
from Devices.VOG.Controller.vog_controller import VOGController
from Devices.VOG.View.vog_graph import VOGGraph


class CompanionController:
    """
    Main controller driving the companion app
        Controls UI and experiments
        Handles errors
        Creates device controllers
        Formats and saves device and experiment data to a file
    """
    def __init__(self) -> None:
        """
        Create elements of View and Controller
        :return None:
        """

        # initialize logging for app
        self.log_output = OutputWindow()
        self.settings = QSettings("Red Scientific", "Companion")

        self.settings.beginGroup("logging")
        if not self.settings.contains("loglevel"):
            self.settings.setValue("loglevel", "DEBUG")
        logginglevel = eval('logging.' + self.settings.value('loglevel'))
        self.settings.endGroup()

        logging.basicConfig(filename=self.__setup_log_output_file("companion_app_log.txt"), filemode='w',
                            level=logginglevel, format='%(levelname)s - %(name)s - %(funcName)s: %(message)s')
        self.logger = logging.getLogger(__name__)

        self.formatter = logging.Formatter('%(levelname)s - %(name)s - %(funcName)s: %(message)s')
        self.ch = logging.StreamHandler(self.log_output)
        self.ch.setLevel(logginglevel)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)

        self.logger.info("RS Companion app version: " + current_version_str)
        self.logger.debug("Initializing")

        # set up ui
        ui_min_size = QSize(950, 740)
        dock_size = QSize(850, 160)
        button_box_size = QSize(205, 120)
        info_box_size = QSize(230, 120)
        flag_box_size = QSize(80, 120)
        note_box_size = QSize(250, 120)
        tab_box_width_range = (350, 320)
        self.ui = CompanionWindow(ui_min_size, self.ch)
        self.menu_bar = MenuBar(self.ui, self.ch)
        self.control_dock = ControlDock(self.ui, dock_size, self.ch)
        self.button_box = ButtonBox(self.control_dock, button_box_size, self.ch)
        self.info_box = InfoBox(self.control_dock, info_box_size, self.ch)
        self.flag_box = FlagBox(self.control_dock, flag_box_size, self.ch)
        self.note_box = NoteBox(self.control_dock, note_box_size, self.ch)
        self.graph_box = DisplayContainer(self.ui, self.__refresh_all_graphs, self.ch)
        self.tab_box = TabContainer(self.ui, tab_box_width_range, self.ch)
        self.file_dialog = QFileDialog(self.ui)

        self.dev_con_manager = RSDeviceConnectionManager(self.ch)
        self.__setup_managers()
        self.settings.endGroup()
        # Initialize storage and state
        self.__controller_classes = dict()
        self.__controller_inits = dict()
        self.__graph_inits = dict()
        self.__populate_func_dicts()
        self.__graphs = dict()
        self.__exp_created = False
        self.__exp_running = False
        self.__num_drts = 0
        self.__num_vogs = 0
        self.__current_cond_name = ""
        self.__device_controllers = dict()
        self.__save_file_name = ""
        self.__save_dir = QDir().homePath()
        self.__device_spacers = dict()
        self.__devices_to_add = dict()

        # Assemble View objects
        self.__initialize_view()
        self.__init_controller_classes()

        self.logger.debug("Initialized")

    ########################################################################################
    # public functions
    ########################################################################################

    # TODO: Figure out how to show device added but not allow use until next experiment
    def add_device(self, device_name: str, port_name: str, thread: PortWorker) -> None:
        """
        Handles an RS device being added during runtime
        If no experiment running, device added
        If experiment running, device put in a queue to add after experiment
        :param device_name: Type of RS device
        :param port_name: Specific device number
        :param thread: Device communication thread
        :return None:
        """

        self.logger.debug("running")
        if not self.__exp_created:
            self.__add_device((device_name, port_name), thread)
        else:
            self.__devices_to_add[(device_name, port_name)] = thread
        self.logger.debug("done")

    def remove_device(self, device_name: str, port_name: str) -> None:
        """
        Handles an RS device being removed during runtime
        :param device_name: Type of RS device
        :param port_name: Specific device number
        :return None:
        """

        self.logger.debug("running")
        if (device_name, port_name) in self.__devices_to_add:
            del self.__devices_to_add[(device_name, port_name)]
        self.__remove_device((device_name, port_name))
        self.logger.debug("done")

    def alert_device_connection_failure(self) -> None:
        """
        Handles a connection failure with a device
        Alerts user to connection failure
        :return None:

        """

        self.logger.debug("running")
        self.ui.show_help_window("Error", device_connection_error)
        self.logger.debug("done")

    def save_device_data(self, device_name: Tuple[str, str], device_line: str = '', timestamp: datetime = None) -> None:
        """
        Saves experiment data from a device to a file
        :param device_name: Type of device and specific device number
        :param device_line: Data from device
        :param timestamp: Time of data received
        :return None:
        """

        self.logger.debug("running")
        if not timestamp:
            timestamp = get_current_time(device=True)
        spacer = ", "
        time = timestamp.strftime("%H:%M:%S.%f")
        date = timestamp.strftime("%Y-%m-%d")
        block_num = self.info_box.get_block_num()
        cond_name = self.button_box.get_condition_name()
        flag = self.flag_box.get_flag()
        main_block = time + spacer + date + spacer + block_num + spacer + cond_name + spacer + flag
        if device_name[0] == "Note":
            line = device_name[0] + spacer + main_block + spacer
            line = self.__get_device_note_spacers(line)
            line += device_line
        elif device_name[0] == "Keyflag":
            line = device_name[0] + spacer + main_block
            line = self.__get_device_note_spacers(line)
        else:
            line = device_name[0] + device_name[1] + spacer + main_block
            for key in self.__controller_classes:
                if device_name[0] == key:
                    line += device_line
                elif self.__controller_classes[key][1] > 0:
                    line += self.__controller_classes[key][0].get_note_spacer()
        write_line_to_file(self.__save_file_name, line)
        self.logger.debug("done")

    def __get_device_note_spacers(self, line: str):
        for val in self.__controller_classes.values():
            if val[1] > 0:
                line += val[0].get_note_spacer()
        return line

    ########################################################################################
    # initial setup
    ########################################################################################

    def __setup_managers(self) -> None:
        """
        Sets up device connection managers
        :return None:
        """

        self.logger.debug("running")
        self.dev_con_manager.signals.new_device_sig.connect(self.add_device)
        self.dev_con_manager.signals.disconnect_sig.connect(self.remove_device)
        self.dev_con_manager.signals.failed_con_sig.connect(self.alert_device_connection_failure)
        self.logger.debug("done")

    def __initialize_view(self) -> None:
        """
        Assembles the different View objects into a window. Initializes some handlers and controller functions
        :return None:
        """

        self.logger.debug("running")
        self.__setup_file_dialog()
        self.__setup_handlers()
        # self.__start_update_timer()
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

    # TODO: Add device controller destructors?
    def __populate_func_dicts(self) -> None:
        """
        creates dictionaries containing device controllers and device graphs functions
        :return None:
        """

        self.logger.debug("running")
        self.__controller_inits['drt'] = dict()
        self.__controller_inits['vog'] = dict()
        self.__graph_inits['drt'] = dict()
        self.__graph_inits['vog'] = dict()
        self.__controller_inits['drt']['creator'] = self.__create_drt_controller
        self.__controller_inits['vog']['creator'] = self.__create_vog_controller
        self.__graph_inits['drt']['creator'] = self.__make_drt_graph
        self.__graph_inits['drt']['destructor'] = self.__destroy_drt_graph
        self.__graph_inits['vog']['creator'] = self.__make_vog_graph
        self.__graph_inits['vog']['destructor'] = self.__destroy_vog_graph
        self.logger.debug("done")

    # TODO: move functionality to model, keep track of device count elsewhere
    def __init_controller_classes(self) -> None:
        """
        Creates a dictionary for static method references, and device count
        :return:
        """

        self.logger.debug("running")
        self.__controller_classes["DRT"] = [DRTController, 0]
        self.__controller_classes["VOG"] = [VOGController, 0]
        self.logger.debug("done")

    def __setup_file_dialog(self) -> None:
        """
        Sets up a file dialog for 1. saving data from experiments and 2. opening previous experiments.
        2. not implemented yet
        :return None:
        """

        self.logger.debug("running")
        # self.file_dialog.setViewMode(QFileDialog.Detail)
        self.file_dialog.setDirectory(QDir().homePath())
        # self.file_dialog.setFileMode(QFileDialog.Directory)
        self.logger.debug("done")

    def __setup_handlers(self) -> None:
        """
        Wire up buttons etc. in the view.
        :return None:
        """

        self.logger.debug("running")
        self.button_box.add_create_button_handler(self.__create_end_exp)
        self.button_box.add_start_button_handler(self.__start_stop_exp)
        self.note_box.add_note_box_changed_handler(self.__check_toggle_post_button)
        self.note_box.add_post_handler(self.__post_handler)
        self.menu_bar.add_open_last_save_dir_handler(self.__open_last_save_dir)
        self.menu_bar.add_about_app_handler(self.__about_app)
        self.menu_bar.add_about_company_handler(self.__about_company)
        self.menu_bar.add_update_handler(self.__check_for_updates_handler)
        self.menu_bar.add_log_window_handler(self.__log_window_handler)
        self.ui.keyPressEvent = self.__key_press_handler
        self.ui.add_close_handler(self.ui_close_event_handler)
        self.logger.debug("done")

    ########################################################################################
    # Experiment handling
    ########################################################################################

    def __create_end_exp(self) -> None:
        """
        Either begin or end an experiment. If beginning an experiment then get a dir path from the user to save
        experiment data and check output files. Path is required to continue.
        :return None:
        """

        self.logger.debug("running")
        if not self.__exp_created:
            self.logger.debug("creating experiment")
            if not self.__get_save_file_name():
                self.logger.debug("no save directory selected, done running __create_end_exp()")
                return
            self.__create_exp()
            self.logger.debug("done")
        else:
            self.logger.debug("ending experiment")
            self.__end_exp()
            self.__save_file_name = ""
        self.logger.debug("done")

    def __create_exp(self) -> None:
        """
        Creates an experiment and updates the save file
        :return None:
        """

        self.logger.debug("running")
        date_time = get_current_time(device=True)
        self.__exp_created = True
        self.button_box.toggle_create_button()
        self.__add_hdr_to_output()
        devices_running = list()
        try:
            for controller in self.__device_controllers.values():
                if controller.active:
                    controller.start_exp()
                    devices_running.append(controller)
        except Exception as e:
            self.logger.exception("Failed trying to start_exp_all")
            self.button_box.toggle_create_button()
            self.__exp_created = False
            for controller in devices_running:
                controller.end_exp()
            return
        self.__check_toggle_post_button()
        self.info_box.set_start_time(get_current_time(time=True, date_time=date_time))
        self.logger.debug("done")

    def __end_exp(self) -> None:
        """
        Ends an experiment, and checks device backlog
        :return None:
        """

        self.logger.debug("running")
        self.__exp_created = False
        self.button_box.toggle_create_button()
        try:
            for controller in self.__device_controllers.values():
                controller.end_exp()
        except Exception as e:
            self.logger.exception("Failed trying to end_exp_all")
        self.__check_toggle_post_button()
        self.info_box.set_block_num(0)
        self.__check_device_backlog()
        self.logger.debug("done")

    def __start_stop_exp(self) -> None:
        """
        Handler method to either start or stop an experiment.
        :return None:
        """

        self.logger.debug("running")
        if self.__exp_running:
            self.logger.debug("stopping experiment")
            self.__stop_exp()
        else:
            self.logger.debug("starting experiment")
            self.__start_exp()
        self.logger.debug("done")

    def __start_exp(self) -> None:
        """
        Starts an experiment
        :return None:
        """

        self.logger.debug("running")
        self.__exp_running = True
        devices_running = list()
        try:
            for controller in self.__device_controllers.values():
                if controller.active:
                    controller.start_block()
                    devices_running.append(controller)
        except Exception as e:
            self.logger.exception("Failed trying to start_block_all")
            self.__exp_running = False
            for controller in devices_running:
                controller.end_exp()
            return
        self.info_box.set_block_num(str(int(self.info_box.get_block_num()) + 1))
        self.__current_cond_name = self.button_box.get_condition_name()
        self.__add_break_in_graph_lines()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self.logger.debug("done")

    def __stop_exp(self) -> None:
        """
        Stops an experiment
        :return None:
        """

        self.logger.debug("running")
        self.__exp_running = False
        try:
            for controller in self.__device_controllers.values():
                controller.end_block()
        except Exception as e:
            self.logger.exception("Failed trying to end_block_all")
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self.logger.debug("done")

    # Depreciated
    def __add_vert_lines_to_graphs(self) -> None:
        """
        Adds to the Y-axis of a graph based on the current time
        :return None:
        """

        time = get_current_time(graph=True)
        for device_type in self.__graphs.values():
            device_type['frame'].get_graph().add_vert_lines(time)

    def __add_break_in_graph_lines(self) -> None:
        """
        Creates a break between times when the pause button is pressed
        :return None:
        """

        time = get_current_time(graph=True)
        for device_type in self.__graphs.values():
            device_type['frame'].get_graph().add_empty_point(time)

    def __check_toggle_post_button(self) -> None:
        """
        If an experiment is created and running and there is a note then allow user access to post button.
        :return None:
        """

        self.logger.debug("running")
        if self.__exp_created and len(self.note_box.get_note()) > 0:  # and self.__exp_running:
            self.logger.debug("button = true")
            self.note_box.toggle_post_button(True)
        else:
            self.logger.debug("button = false")
            self.note_box.toggle_post_button(False)
        self.logger.debug("done")

    ########################################################################################
    # Data saving
    ########################################################################################

    def __key_press_handler(self, event: QKeyEvent) -> None:
        """
        Only act on alphabetical key presses
        :return None:
        """

        self.logger.debug("running")
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.flag_box.set_flag(chr(event.key()))
                if self.__exp_created:
                    self.save_device_data(('Keyflag', ''))
            event.accept()
        else:
            event.ignore()
        self.logger.debug("done")

    def __post_handler(self) -> None:
        """
        Write a given user note to all device output files.
        :return None:
        """

        self.logger.debug("running")
        note = self.note_box.get_note()
        self.note_box.clear_note()
        self.save_device_data(("Note", ''), note)
        self.logger.debug("done")

    def __get_save_file_name(self) -> bool:
        """
        Saves a save directory from a given file
        :return bool: True if the file name is longer than 1 character
        """

        self.logger.debug("running")
        self.__save_file_name = self.file_dialog.getSaveFileName(filter="*.txt")[0]
        self.logger.debug("1")
        valid = len(self.__save_file_name) > 1
        self.logger.debug("2")
        if valid:
            self.__save_dir = self.__get_save_dir_from_file_name(self.__save_file_name)
        self.logger.debug("done")
        return valid

    @staticmethod
    def __get_save_dir_from_file_name(file_name: str) -> str:
        """
        Returns the directory for where a file is saved
        :param file_name: Full file directory including file name
        :return str: Directory to the file
        """

        # possibly use for get last used directory
        end_index = file_name.rfind('/')
        dir_name = file_name[:end_index + 1]
        return dir_name

    def __check_for_updates_handler(self) -> None:
        """
        Ask VersionChecker if there is an update then alert user to result.
        :return None:
        """

        self.logger.debug("running")
        vc = VersionChecker()
        is_available = vc.check_version()
        if is_available == 1:
            self.ui.show_help_window("Update", update_available)
        elif is_available == 0:
            self.ui.show_help_window("Update", up_to_date)
        elif is_available == -1:
            self.ui.show_help_window("Error", error_checking_for_update)
        self.logger.debug("done")

    def __log_window_handler(self) -> None:
        """
        Handler for the output log
        :return None:
        """

        self.log_output.show()

    def __add_hdr_to_output(self) -> None:
        """
        Adds the header line to the output file
        :return None:
        """

        line = 'Device ID, Time, Date, Block, Condition, Key Flag, '
        for key in self.__controller_classes:
            if self.__controller_classes[key][1] > 0:
                line += self.__controller_classes[key][0].get_save_file_hdr()
        line += 'Note'
        write_line_to_file(self.__save_file_name, line, new=True)

    @staticmethod
    def __setup_log_output_file(file_name: str) -> str:
        """
        Create program output file to save log.
        :param file_name: Name of the save log
        :return str: full directory to the save log, including the save log name
        """

        fname = gettempdir() + "\\" + file_name
        with open(fname, "w") as temp:
            temp.write(program_output_hdr)
        return fname

    ########################################################################################
    # generic device handling
    ########################################################################################

    def __check_device_backlog(self) -> None:
        """
        Adds device backlog to devices
        :return None:
        """

        for device in self.__devices_to_add:
            self.__add_device(device, self.__devices_to_add[device])

    def __add_device(self, device: Tuple[str, str], thread: PortWorker) -> None:
        """
        Handles when a new device is found by the device manager and added to the program's scope.
        Creates a device type specific graph if needed and connects device specific controller to device graph and
        device manager to let device controller handle device specific messages.
        Each device gets its own configure tab.
        :param device: Device to add, tuple of device type and name as strings
        :param thread: Device communication thread
        :return None:
        """

        self.logger.debug("running")
        if not check_device_tuple(device):
            self.logger.warning("expected tuple of two strings, got otherwise")
            return
        if device[0] not in self.__controller_inits.keys():
            self.logger.warning("Unknown device")
            return
        if not self.__controller_inits[device[0]]['creator'](device, thread):
            self.logger.debug("Failed to make controller")
            return
        self.__graphs[device[0]]['frame'].get_graph().add_device(device[1][3:])
        self.tab_box.add_tab(self.__device_controllers[device].get_tab_obj())
        self.__controller_classes[device[0].upper()][1] += 1
        self.logger.debug("done")

    def __remove_device(self, device: Tuple[str, str]) -> None:
        """
        Removes device tab, graph link and device information
        :param device: Device to be removed, tuple of device type and name as strings
        :return None:
        """

        self.logger.debug("running")
        if not check_device_tuple(device):
            self.logger.warning("expected tuple of two strings, got otherwise")
            return
        self.logger.debug("Removing " + device[0] + " " + device[1])
        if device in self.__device_controllers:
            self.__graphs[device[0]]['num_devices'] -= 1
        else:
            self.logger.debug("Unknown device or already disconnected: " + device[0] + " " + device[1])
            return
        self.tab_box.remove_tab(self.__device_controllers[device].get_tab_obj().get_name())
        self.__graphs[device[0]]['frame'].get_graph().remove_device(device[1][3:])
        del self.__device_controllers[device]
        self.__check_num_devices()
        self.__controller_classes[device[0].upper()][1] -= 1
        self.logger.debug("done")

    # TODO: This and create drt controller functions could be merged. Perhaps different functions for the
    #  try except block.
    def __create_drt_controller(self, device: Tuple[str, str], thread: PortWorker) -> bool:
        """
        Creates a controller for a DRT device
        :param device: Device to create a controller for, tuple of device type and name as strings
        :param thread: Device communication thread
        :return bool: Returns true if a DRT controller is created
        """


        self.logger.debug("running")
        self.logger.debug("Got " + device[0] + " " + device[1])
        if not device[0] in self.__graphs:
            self.logger.debug("Making graph for drt")
            if not self.__make_drt_graph():
                self.logger.warning("Failed to make_drt_graph")
                return False
        self.logger.debug("Making controller for drt")
        try:
            device_controller = DRTController(device, thread, self.add_data_to_graph, self.ch,
                                              self.save_device_data)
            device_controller.get_tab_obj().setParent(self.tab_box)
        except Exception as e:
            self.logger.exception("failed to make device_controller for drt" + str(device))
            self.__check_num_devices()
            return False
        self.logger.debug("Made controller for drt")
        self.__device_controllers[device] = device_controller
        self.__graphs[device[0]]['num_devices'] += 1
        self.logger.debug("done")
        return True

    def __create_vog_controller(self, device: Tuple[str, str], thread: PortWorker) -> bool:
        """
        Creates a controller for a VOG device
        :param device: Device to create a controller for, tuple of device type and name as strings
        :param thread: Device communication thread
        :return bool: Returns true if a VOG controller is created
        """


        self.logger.debug("running")
        self.logger.debug("Got " + device[0] + " " + device[1])
        if not device[0] in self.__graphs:
            self.logger.debug("Making graph for vog")
            if not self.__make_vog_graph():
                self.logger.warning("Failed to make_vog_graph")
                return False
        self.logger.debug("Making controller for vog")
        try:
            device_controller = VOGController(device, thread, self.add_data_to_graph, self.ch,
                                              self.save_device_data)
            device_controller.get_tab_obj().setParent(self.tab_box)
        except Exception as e:
            self.logger.exception("failed to make device_controller for vog" + str(device))
            self.__check_num_devices()
            return False
        self.logger.debug("Made controller for vog")
        self.__device_controllers[device] = device_controller
        self.__graphs[device[0]]['num_devices'] += 1
        self.logger.debug("done")
        return True

    ########################################################################################
    # Other handlers
    ########################################################################################

    # TODO: Figure out why closing right after running app causes error.
    def ui_close_event_handler(self):
        """
        Shut down all devices before closing the app.
        :return:
        """

        self.logger.debug("running")
        self.dev_con_manager.cleanup()
        for controller in self.__device_controllers.values():
            controller.cleanup()
        self.log_output.close()
        self.logger.debug("done")

    def __open_last_save_dir(self):
        """
        Opens native file manager to the last directory used for an experiment.
        If no experiment has been performed, opens default home path.
        :return:
        """

        self.logger.debug("running")
        if self.__save_dir == "":
            QDesktopServices.openUrl(QUrl.fromLocalFile(QDir().homePath()))
        else:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.__save_dir))
        self.logger.debug("done")

    def __about_company(self):
        """ Display company information. """
        self.logger.debug("running")
        self.ui.show_help_window("About Red Scientific", about_RS_text)
        self.logger.debug("done")

    def __about_app(self):
        """ Display app information. """
        self.logger.debug("running")
        self.ui.show_help_window("About Red Scientific Companion App", about_RS_app_text + "\n\n Version: "
                                 + current_version_str)
        self.logger.debug("done")

    ########################################################################################
    # graph handling
    ########################################################################################

    def __check_num_devices(self):
        self.logger.debug("running")
        to_remove = list()
        for device_type in self.__graphs:
            if self.__graphs[device_type]['num_devices'] == 0:
                to_remove.append(device_type)
        for item in to_remove:
            self.__graph_inits[item]['destructor']()
        self.logger.debug("done")

    def __make_drt_graph(self):
        """ Create a drt type graph and add it to the display area. """
        self.logger.debug("running")
        try:
            graph = DRTGraph(self.graph_box, self.ch)
        except Exception as e:
            self.logger.exception("Failed to make DRTGraph")
            return False
        graph_frame = GraphFrame(self.graph_box, graph)
        self.__graphs["drt"] = dict()
        self.__graphs["drt"]["frame"] = graph_frame
        self.__graphs["drt"]["num_devices"] = 0
        self.graph_box.add_display(graph_frame)
        self.logger.debug("done")
        return True

    def __destroy_drt_graph(self):
        """ Remove the drt graph. Typically called when all drt devices have been disconnected. """
        self.logger.debug("running")
        if "drt" in self.__graphs.keys():
            self.graph_box.remove_display(self.__graphs["drt"]['frame'])
            del self.__graphs["drt"]
        self.logger.debug("done")

    def __make_vog_graph(self):
        """ Create a vog type graph and add it to the display area. """
        self.logger.debug("running")
        try:
            graph = VOGGraph(self.graph_box, self.ch)
        except Exception as e:
            self.logger.exception("Failed to make VOGGraph")
            return False
        graph_frame = GraphFrame(self.graph_box, graph)
        graph_frame.set_graph_height(500)
        self.__graphs["vog"] = dict()
        self.__graphs["vog"]["frame"] = graph_frame
        self.__graphs["vog"]["num_devices"] = 0
        self.graph_box.add_display(graph_frame)
        self.logger.debug("done")
        return True

    def __destroy_vog_graph(self):
        """ Remove the vog graph. Typically called when all vog devices have been disconnected. """
        self.logger.debug("running")
        if "vog" in self.__graphs.keys():
            self.graph_box.remove_display(self.__graphs["vog"]['frame'])
            del self.__graphs["vog"]
        self.logger.debug("done")

    def __refresh_all_graphs(self):
        self.logger.debug("running")
        for device_type in self.__graphs:
            self.__graphs[device_type]['frame'].get_graph().refresh_self()
        self.logger.debug("done")

    def add_data_to_graph(self, device, data):
        """ Pass data to device type graph along with specific device id. """
        self.logger.debug("running")
        if not check_device_tuple(device):
            return
        if device[0] not in self.__graphs:
            self.logger.warning("device not found in self.__graphs")
            return
        self.__graphs[device[0]]['frame'].get_graph().add_data(device[1][3:], data)
        self.logger.debug("done")
