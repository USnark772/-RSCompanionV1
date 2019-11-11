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

import logging
from CompanionLib.companion_helpers import write_line_to_file
from Devices.VOG.View.vog_tab import VOGTab
from Devices.VOG.Model.vog_defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min, \
    vog_output_field, vog_file_hdr, vog_note_spacer


class VOGController:
    def __init__(self, tab_parent, device, msg_callback, graph_callback, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        device_name = device[0] + " on " + device[1]
        self.__tab = VOGTab(tab_parent, device_name, ch)
        self.__graph_callback = graph_callback
        self.__device_info = device
        self.__msg_callback = msg_callback
        self.__updating_config = False
        self.__errors = [False] * 3
        self.__current_vals = [0] * 5  # MaxOpen, MaxClose, Debounce, ClickMode, buttonControl
        self.__open_changed = False
        self.__closed_changed = False
        self.__debounce_changed = False
        self.__mode_changed = False
        self.__config_val_changed = False
        self.__lens_open = False
        # bools: tried array but had bugs when setting bools[0] to true, bools must be separate.
        self.__prev_vals = ["", ""]  # MaxOpen, MaxClose
        self.__get_vals()
        self.__set_upload_button(False)
        self.__data_types = [["Time Open", 0, True], ["Time Closed", 0, True]]
        self.save_file = str()
        self.__set_handlers()
        self.logger.debug("Initialized")

    def get_tab_obj(self):
        return self.__tab

    def handle_msg(self, msg_string, ui_info):
        msg_dict = self.__parse_msg(msg_string)
        if 'type' in msg_dict.keys():
            msg_type = msg_dict['type']
            if msg_type == "data":
                self.__add_data_to_graph(msg_dict['values'], ui_info[2])
                self.__save_data(msg_dict['values'], ui_info)
            elif msg_type == "settings":
                self.__update_config(msg_dict['values'])

    def create_new_save_file(self, new_filename):
        self.save_file = new_filename
        self.add_save_file_hdr()

    def add_save_file_hdr(self):
        write_line_to_file(self.save_file, vog_file_hdr)

    def start_exp(self):
        self.__send_msg(self.__prepare_msg("do_expStart"))

    def end_exp(self):
        self.__send_msg(self.__prepare_msg("do_expStop"))

    def start_block(self):
        self.__send_msg(self.__prepare_msg("do_trialStart"))

    def end_block(self):
        self.__send_msg(self.__prepare_msg("do_trialStop"))

    def __save_data(self, values, ui_info):
        prepend = self.__device_info[0] + ", " + ui_info[1] + ", " + ui_info[2] + ", " + \
                  ui_info[2].strftime("%Y-%m-%d-%H-%M-%S")
        line = self.__format_output_for_save_file(values)
        write_line_to_file(self.save_file, prepend + line)

    def __add_data_to_graph(self, data, timestamp):
        """ Send data from device to graph for display. """
        self.logger.debug("running")
        self.__graph_callback(self.__device_info, (timestamp, int(data[vog_output_field[1]]), int(data[vog_output_field[2]])))
        self.logger.debug("done")

    def __update_config(self, msg):
        """ Update device configuration display. """
        self.logger.debug("running")
        self.__updating_config = True
        for key in msg:
            self.__set_val(key, msg[key])
        self.__updating_config = False
        self.logger.debug("done")

    def __set_handlers(self):
        self.logger.debug("running")
        self.__tab.add_nhtsa_button_handler(self.__nhtsa)
        self.__tab.add_eblind_button_handler(self.__eblind)
        self.__tab.add_direct_control_button_handler(self.__direct_control)
        self.__tab.add_upload_button_handler(self.__update_device)
        self.__tab.add_open_inf_handler(self.__toggle_open_inf)
        self.__tab.add_close_inf_handler(self.__toggle_close_inf)
        self.__tab.add_open_entry_changed_handler(self.__open_entry_changed)
        self.__tab.add_close_entry_changed_handler(self.__close_entry_changed)
        self.__tab.add_debounce_entry_changed_handler(self.__debounce_entry_changed)
        self.__tab.add_button_mode_entry_changed_handler(self.__button_mode_entry_changed)
        self.__tab.add_config_val_changed_handler(self.__config_val_entry_changed)
        self.__tab.add_manual_control_handler(self.__toggle_lens)
        self.logger.debug("done")

    def __open_entry_changed(self):
        """
        Handle when user changes the value in the time open field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_open_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __close_entry_changed(self):
        """
        Handle when user changes the value in the time closed field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_close_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __debounce_entry_changed(self):
        """
        Handle when user changes the value in the debounce field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_debounce_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __button_mode_entry_changed(self):
        """
        Handle when user changes the value in the button mode field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_button_mode_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __config_val_entry_changed(self):
        """
        Handle when user changes the value in the time open field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__config_val_changed = True
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __toggle_open_inf(self, is_checked):
        """
        Handle when open inf checkbox is checked.
        Save value of time open field and change display to reflect new setting.
        Else: replace with previously saved value.
        """
        self.logger.debug("running")
        if is_checked:
            self.__prev_vals[0] = self.__tab.get_open_val()
            self.__tab.set_open_val(str(vog_max_open_close))
        else:
            self.__tab.set_open_val(self.__prev_vals[0])
        self.__tab.set_open_val_entry_activity(not is_checked)
        self.logger.debug("done")

    def __toggle_close_inf(self, is_checked):
        """
        Handle when close inf checkbox is checked.
        Save value of time open field and change display to reflect new setting.
        Else: replace with previously saved value.
        """
        self.logger.debug("running")
        if is_checked:
            self.__prev_vals[1] = self.__tab.get_close_val()
            self.__tab.set_close_val(str(vog_max_open_close))
        else:
            self.__tab.set_close_val(self.__prev_vals[1])
        self.__tab.set_close_val_entry_activity(not is_checked)
        self.logger.debug("done")

    # TODO: Check that config value is working properly
    def __update_device(self):
        """ Send updated values to device. Only send uploads if needed, then set as custom and disable upload button """
        self.logger.debug("running")
        if self.__open_changed:
            self.__set_device_open(self.__tab.get_open_val())
        if self.__closed_changed:
            self.__set_device_close(self.__tab.get_close_val())
        if self.__debounce_changed:
            self.__set_device_debounce(self.__tab.get_debounce_val())
        if self.__mode_changed:
            self.__set_device_click(self.__tab.get_button_mode())
        if self.__config_val_changed:
            self.__set_device_config(self.__tab.get_config_value())
        self.__set_changed_bools_false()
        self.__set_upload_button(False)
        self.logger.debug("done")

    def __set_changed_bools_false(self):
        self.logger.debug("running")
        self.__open_changed = False
        self.__closed_changed = False
        self.__debounce_changed = False
        self.__mode_changed = False
        self.__config_val_changed = False
        self.logger.debug("done")

    def __get_vals(self):
        """ Request current device settings. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("get_configName"))
        self.__send_msg(self.__prepare_msg("get_configMaxOpen"))
        self.__send_msg(self.__prepare_msg("get_configMaxClose"))
        self.__send_msg(self.__prepare_msg("get_configDebounce"))
        self.__send_msg(self.__prepare_msg("get_configClickMode"))
        self.__send_msg(self.__prepare_msg("get_configButtonControl"))
        self.logger.debug("done")

    def __set_upload_button(self, is_active):
        """ Check to make sure no errors are set and that there are changes to be made. Activate button if needed. """
        self.logger.debug("running")
        if (self.__open_changed or self.__closed_changed or self.__debounce_changed or self.__mode_changed)\
                and not (self.__errors[0] or self.__errors[1] or self.__errors[2]):
            self.__tab.set_upload_button_activity(is_active)
        else:
            self.__tab.set_upload_button_activity(False)
        self.logger.debug("done")

    def __check_open_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.logger.debug("running")
        self.__errors[0] = True
        usr_input = self.__tab.get_open_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_max_open_close >= usr_input_int >= vog_min_open_close:
                self.__errors[0] = False
                self.__open_changed = usr_input_int != self.__current_vals[0]
        self.__tab.set_open_val_error(self.__errors[0])
        self.logger.debug("done")

    def __check_close_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.logger.debug("running")
        self.__errors[1] = True
        usr_input = self.__tab.get_close_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_max_open_close >= usr_input_int >= vog_min_open_close:
                self.__errors[1] = False
                self.__closed_changed = usr_input_int != self.__current_vals[1]
        self.__tab.set_close_val_error(self.__errors[1])
        self.logger.debug("done")

    def __check_debounce_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.logger.debug("running")
        self.__errors[2] = True
        usr_input = self.__tab.get_debounce_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_debounce_max >= usr_input_int >= vog_debounce_min:
                self.__errors[2] = False
                self.__debounce_changed = usr_input_int != self.__current_vals[2]
        self.__tab.set_debounce_val_error(self.__errors[2])
        self.logger.debug("done")

    def __check_button_mode_val(self):
        """ Set button mode changed bool. """
        self.logger.debug("running")
        self.__mode_changed = self.__tab.get_button_mode() != self.__current_vals[3]
        self.logger.debug("done")

    def __set_val(self, var, val):
        """ Set display value of var to val. """
        self.logger.debug("running")
        if var == "Name":
            self.__tab.set_config_value(val)
        elif var == "MaxOpen":
            self.__current_vals[0] = int(val)
            self.__tab.set_open_val(val)
            self.__tab.set_open_val_error(False)
        elif var == "MaxClose":
            self.__current_vals[1] = int(val)
            self.__tab.set_close_val_error(False)
            self.__tab.set_close_val(val)
        elif var == "Debounce":
            self.__current_vals[2] = int(val)
            self.__tab.set_debounce_val(val)
            self.__tab.set_debounce_val_error(False)
        elif var == "ClickMode":
            self.__current_vals[3] = int(val)
            self.__tab.set_button_mode(val)
        elif var == "buttonControl":
            self.__current_vals[4] = int(val)
        elif var == "lensState":
            if val == "peekOpen":
                self.__lens_open = True
            else:
                self.__lens_open = False
        self.logger.debug("done")

    def __toggle_lens(self):
        """ Tell device to toggle lens. """
        self.logger.debug("running")
        if self.__lens_open:
            self.__send_msg(self.__prepare_msg("do_peekClose"))
        else:
            self.__send_msg(self.__prepare_msg("do_peekOpen"))
        self.logger.debug("done")

    def __nhtsa(self):
        """ Set device and display to nhtsa defaults. """
        self.logger.debug("running")
        self.__tab.set_open_inf(False)
        self.__tab.set_close_inf(False)
        self.__set_device_config("NHTSA")
        self.__set_device_open("1500")
        self.__set_device_close("1500")
        self.__set_device_debounce("20")
        self.__set_device_click("1")
        self.__set_device_button_control("0")
        self.__set_upload_button(False)
        self.logger.debug("done")

    def __eblind(self):
        """ Set device and display to eblind mode. """
        self.logger.debug("running")
        self.__tab.set_open_inf(True)
        self.__tab.set_close_inf(False)
        self.__set_device_config("eBlindfold")
        self.__set_device_open(vog_max_open_close)
        self.__set_device_close("0")
        self.__set_device_debounce("100")
        self.__set_device_click("1")
        self.__set_device_button_control("0")
        self.__set_upload_button(False)
        self.logger.debug("done")

    def __direct_control(self):
        """ Set device and display to direct control mode. """
        self.logger.debug("running")
        self.__tab.set_open_inf(True)
        self.__tab.set_close_inf(True)
        self.__set_device_config("DIRECT CONTROL")
        self.__set_device_open(vog_max_open_close)
        self.__set_device_close("0")
        self.__set_device_debounce("100")
        self.__set_device_click("0")
        self.__set_device_button_control("1")
        self.__set_upload_button(False)
        self.logger.debug("done")

    def __set_device_config(self, val):
        """ Set device config.txt setting. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_configName", str(val)))
        self.logger.debug("done")

    def __set_device_open(self, val):
        """ Set device time open setting. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_configMaxOpen", str(val)))
        self.logger.debug("done")

    def __set_device_close(self, val):
        """ Set device time close setting. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_configMaxClose", str(val)))
        self.logger.debug("done")

    def __set_device_debounce(self, val):
        """ Set device debounce setting. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_configDebounce", str(val)))
        self.logger.debug("done")

    def __set_device_click(self, val):
        """ Set device click mode setting. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_configClickMode", str(val)))
        self.logger.debug("done")

    def __set_device_button_control(self, val):
        """ Set device button control setting. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_configButtonControl", str(val)))
        self.logger.debug("done")

    def __send_msg(self, msg):
        """ Send message to device. """
        self.logger.debug("running")
        msg['type'] = "send"
        msg['device'] = self.__device_info
        self.__msg_callback(msg)
        self.logger.debug("done")

    @staticmethod
    def __parse_msg(msg_string):
        ret = dict()
        ret['values'] = {}
        if msg_string[0:5] == "data|":
            ret['type'] = "data"
            val_ind_start = 5
            for i in range(len(vog_output_field)):
                val_ind_end = msg_string.find(',', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                ret['values'][vog_output_field[i]] = msg_string[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 1
        elif "config" in msg_string:
            ret['type'] = "settings"
            bar_ind = msg_string.find('|', 6)
            if msg_string[6:bar_ind] == "Name":
                ret['values']['Name'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "MaxOpen":
                ret['values']['MaxOpen'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "MaxClose":
                ret['values']['MaxClose'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "Debounce":
                ret['values']['Debounce'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
            elif msg_string[6:bar_ind] == "ClickMode":
                ret['values']['ClickMode'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
        elif "Click" in msg_string:
            ret['action'] = "Click"
        elif "buttonControl" in msg_string:
            ret['type'] = "settings"
            bar_ind = msg_string.find('|')
            ret['values'] = {}
            ret['values']['buttonControl'] = msg_string[bar_ind + 1: len(msg_string)].rstrip("\r\n")
        elif "peek" in msg_string:
            ret['type'] = "settings"
            ret['values'] = {}
            ret['values']['lensState'] = msg_string.rstrip("\r\n")
        return ret

    @staticmethod
    def __prepare_msg(cmd, arg=None):
        """ Create string using vog syntax. """
        if arg:
            msg_to_send = ">" + cmd + "|" + arg + "<<\n"
        else:
            msg_to_send = ">" + cmd + "|" + "<<\n"
        return msg_to_send

    @staticmethod
    def __format_output_for_save_file(msg):
        """ Format and return device output. Typically used for saving data to file. """
        line = ""
        for i in vog_output_field:
            line += ", " + str(msg[i])
        line = line.rstrip("\r\n")
        line = line + ", "
        return line
