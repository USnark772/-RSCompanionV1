# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from os import path
from datetime import datetime
from sys import argv
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QTimer, QDir, QSize
from PySide2.QtGui import QKeyEvent
from Model.general_defs import program_output_hdr, about_RS_text, about_RS_app_text, up_to_date, update_available, \
    device_connection_error
from View.MainWindow.main_window import CompanionWindow
from View.DockWidget.control_dock import ControlDock
from View.DockWidget.button_box import ButtonBox
from View.DockWidget.info_box import InfoBox
from View.DockWidget.flag_box import FlagBox
from View.DockWidget.note_box import NoteBox
from View.MenuBarWidget.menu_bar import MenuBar
from View.GraphWidget.graph_container import GraphContainer
from View.TabWidget.device_tab import TabContainer
from Controller.version_checker import VersionChecker
from Controller.device_manager import DeviceManager
from Devices.DRT.Controller.drt_controller import DRTController
from Devices.VOG.Controller.vog_controller import VOGController


class CompanionController:
    def __init__(self):
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
        self.graph_box = GraphContainer(self.ui)
        self.tab_box = TabContainer(self.ui, tab_box_width_range)
        self.file_dialog = QFileDialog(self.ui)

        self.device_manager = DeviceManager(self.receive_msg_from_device_manager)

        self.exp_created = False
        self.exp_running = False
        self.__dir_chosen = False
        self.current_cond_name = ""
        self.program_output_save_file = self.__setup_output_file()
        self.devices = {}

        self.__initialize_view()

    ########################################################################################
    # public functions
    ########################################################################################

    def receive_msg_from_device_manager(self, msg):
        msg_type = msg['type']
        if msg_type == "data":
            self.__update_save(msg)
            self.devices[msg['device']]['controller'].add_data_to_graph(self.__get_current_time(graph=True),
                                                                        msg['values'])
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
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.__device_update)
        self.update_timer.start(1)

    ########################################################################################
    # Experiment handling
    ########################################################################################

    def __create_end_exp(self):
        """Begin an experiment. Get a directory to save to, """
        if not self.exp_created:
            if not self.__get_save_dir_path():
                return
            self.__update_device_filenames()
            self.__check_save_file_hdrs()
            self.__create_exp()
        else:
            self.__end_exp()

    def __create_exp(self):
        self.button_box.toggle_create_button()
        self.device_manager.start_exp_all()
        self.info_box.set_start_time(self.__get_current_time(time=True))
        self.exp_created = True

    def __end_exp(self):
        self.button_box.toggle_create_button()
        self.device_manager.end_exp_all()
        self.exp_created = False

    def __start_stop_exp(self):
        if self.exp_running:
            self.__stop_exp()
        else:
            self.__start_exp()

    def __start_exp(self):
        self.device_manager.start_block_all()
        self.current_cond_name = self.button_box.get_condition_name()
        self.__check_toggle_post_button()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self.exp_running = True

    def __stop_exp(self):
        self.device_manager.end_block_all()
        self.__check_toggle_post_button()
        self.button_box.toggle_start_button()
        self.button_box.toggle_condition_name_box()
        self.exp_running = False

    def __check_toggle_post_button(self):
        if self.exp_created and self.exp_running and len(self.note_box.get_note()) > 0:
            self.note_box.toggle_post_button(True)
        else:
            self.note_box.toggle_post_button(False)

    ########################################################################################
    # Data saving
    ########################################################################################

    def __key_press_handler(self, event):
        if type(event) == QKeyEvent:
            if 0x41 <= event.key() <= 0x5a:
                self.flag_box.set_flag(chr(event.key()))
            event.accept()
        else:
            event.ignore()

    def __save_output_msg(self, msg):
        line = str(self.__get_current_time(save=True)) + ", " + msg
        with open(self.program_output_save_file, 'a+') as file:
            file.write(line)

    def __post_handler(self):
        note = self.note_box.get_note()
        self.note_box.clear_note()
        flag = self.flag_box.get_flag()
        time = self.__get_current_time(True, True, True)
        name = self.current_cond_name
        for device in self.devices:
            spacer = self.__make_note_spacer(device[0])
            self.__write_line_to_file(self.devices[device]['fn'],
                                      "note, " + name + ", " + flag + ", " + time + spacer + ", " + note)

    def __get_save_dir_path(self):
        return self.file_dialog.exec_()

    def __write_line_to_file(self, fname, line):
        line = line + "\n"
        filepath = path.join(self.file_dialog.directory().path(), fname)
        filepath += ".txt"
        with open(filepath, 'a+') as file:
            file.write(line)

    def __check_for_updates_handler(self):
        vc = VersionChecker(self.__save_output_msg)
        is_available = vc.check_version()
        if is_available == 1:
            self.ui.show_help_window("Update", update_available)
        elif is_available == 0:
            self.ui.show_help_window("Update", up_to_date)
        elif is_available == -1:
            self.ui.show_help_window("Error", "There was an unexpected error connecting to the repository")

    def __update_save(self, msg):
        device = msg['device']
        cond_name = self.current_cond_name
        flag = self.flag_box.get_flag()
        time = self.__get_current_time(True, True, True)
        prepend = device[0] + ", " + cond_name + ", " + flag + ", " + time
        line = self.devices[device]['controller'].format_output_for_save_file(msg['values'])
        self.__write_line_to_file(self.devices[device]['fn'], prepend + line)

    def __check_save_file_hdrs(self):
        for device in self.devices:
            if not self.devices[device]['hdr_bool']:
                self.__add_hdr_to_file(device)

    def __make_save_filename_for_device(self, device):
        self.devices[device]['fn'] = device[0] + " on " + device[1] + " " + self.__get_current_time(save=True)
        self.devices[device]['hdr_bool'] = False

    def __update_device_filenames(self):
        for device in self.devices:
            self.__make_save_filename_for_device(device)

    def __add_hdr_to_file(self, device):
        self.__write_line_to_file(self.devices[device]['fn'], self.devices[device]['controller'].get_hdr())
        self.devices[device]['hdr_bool'] = True

    @staticmethod
    def __setup_output_file():
        fname = path.dirname(argv[0]) + "\\program_output.txt"
        if path.exists(fname):
            with open(fname, "w") as temp:
                temp.write(program_output_hdr)
        return fname

    @staticmethod
    def __make_note_spacer(device):
        if device == "drt":
            return ", , "
        elif device == "vog":
            return ", , , , "

    ########################################################################################
    # generic device handling
    ########################################################################################

    def __device_update(self):
        self.device_manager.update()

    def __add_device(self, device):
        if device[0] == "drt":
            controller = DRTController(self.tab_box, device, self.device_manager.handle_msg)
        elif device[0] == "vog":
            controller = VOGController(self.tab_box, device, self.device_manager.handle_msg)
        else:
            return
        self.devices[device] = {}
        self.devices[device]['controller'] = controller
        controller.set_tab_index(self.tab_box.add_tab(controller.get_tab_obj()))
        self.graph_box.add_graph(controller.get_graph_obj())
        self.__make_save_filename_for_device(device)
        if self.__dir_chosen:
            self.__add_hdr_to_file(device)

    def __remove_device(self, device):
        if device in self.devices:
            self.tab_box.remove_tab(self.devices[device]['controller'].get_tab_index())
            self.graph_box.remove_graph(self.devices[device]['controller'].get_graph_obj())
            del self.devices[device]

    ########################################################################################
    # Other handlers
    ########################################################################################

    def ui_close_event_handler(self):
        self.device_manager.end_block_all()
        self.device_manager.end_exp_all()

    def __about_company(self):
        self.ui.show_help_window("About Red Scientific", about_RS_text)

    def __about_app(self):
        self.ui.show_help_window("About Red Scientific Companion App", about_RS_app_text)

    @staticmethod
    def __get_current_time(day=False, time=False, mil=False, save=False, graph=False):
        date_time = datetime.now()
        if day and time and mil:
            return date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        elif day and time and not mil:
            return date_time.strftime("%Y-%m-%d %H:%M:%S")
        elif day and not time and not mil:
            return date_time.strftime("%Y-%m-%d")
        elif not day and time and not mil:
            return date_time.strftime("%H:%M:%S")
        elif not day and time and mil:
            return date_time.strftime("%H:%M:%S.%f")
        elif save:
            return date_time.strftime("%Y-%m-%d-%H-%M-%S")
        elif graph:
            return date_time
