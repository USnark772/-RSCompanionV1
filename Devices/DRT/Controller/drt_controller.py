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

from math import trunc, ceil
import logging
from PySide2.QtCore import QObject, Signal
from Devices.DRT.View.drt_tab import DRTTab
from Devices.DRT.Model.drt_defs import drtv1_0_intensity_max, drtv1_0_stim_dur_max, drtv1_0_stim_dur_min, \
    drtv1_0_ISI_max, drtv1_0_ISI_min, drtv1_0_output_fields, drtv1_0_file_hdr, drtv1_0_config_fields, \
    drtv1_0_note_spacer, drtv1_0_save_fields
from Devices.abc_device_controller import ABCDeviceController


class DRTSig(QObject):
    send_device_msg_sig = Signal(str)


class DRTController(ABCDeviceController):
    def __init__(self, tab_parent, device, graph_callback, ch, save_callback):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.signals = DRTSig()
        self.device_name = device[0].upper(), "_" + device[1][3:]
        super().__init__(DRTTab(tab_parent, self.device_name[0] + self.device_name[1], ch))
        self.__graph_callback = graph_callback
        self.__device_info = device
        self.__save_callback = save_callback
        self.__updating_config = False
        self.__errors = [False, False, False]  # stimDur, upperISI, lowerISI
        self.__changed = [False] * 4  # stimDur, stimIntens, upperISI, lowerISI
        self.__current_vals = [0, 0, 0, 0]  # stimDur, stimIntens, upperISI, lowerISI
        self.__set_upload_button(False)
        self.__data_types = [["Response Time", 0, True], ["Clicks", 0, True]]
        self.save_file = str()
        self.__set_handlers()
        self.logger.debug("Initialized")

    def get_tab_obj(self):
        return self.tab

    def handle_msg(self, msg_string, timestamp):
        msg_dict = self.__parse_msg(msg_string)
        msg_type = msg_dict['type']
        if msg_type == "data":
            self.__add_data_to_graph(msg_dict['values'], timestamp)
            self.__save_data(msg_dict['values'], timestamp)
        elif msg_type == "settings":
            self.__update_config(msg_dict['values'])

    def cleanup(self):
        self.end_block()

    def start_block(self):
        self.__send_msg(self.__prepare_msg("exp_start"))

    def end_block(self):
        self.__send_msg(self.__prepare_msg("exp_stop"))

    def init_values(self):
        self.logger.debug("running")
        """ Request current device settings. """
        self.__send_msg(self.__prepare_msg("get_config"))
        self.logger.debug("done")

    @staticmethod
    def get_save_file_hdr():
        return drtv1_0_file_hdr

    @staticmethod
    def get_note_spacer():
        return drtv1_0_note_spacer

    def __save_data(self, values, timestamp):
        line = self.__format_output_for_save_file(values)
        self.__save_callback(self.device_name, line, timestamp)

    def __add_data_to_graph(self, data, timestamp):
        """ Send data from device to graph for display. Separate data types into their own calls. """
        self.logger.debug("running")
        self.__graph_callback(self.__device_info, (self.__data_types[0][0], timestamp, data[drtv1_0_output_fields[3]]))
        self.__graph_callback(self.__device_info, (self.__data_types[1][0], timestamp, data[drtv1_0_output_fields[2]]))
        self.logger.debug("done")

    def __update_config(self, msg):
        self.logger.debug("running")
        """ Update device configuration display. """
        self.__updating_config = True
        for key in msg:
            self.__set_val(key, msg[key])
        self.__updating_config = False
        self.logger.debug("done")

    def __set_handlers(self):
        self.logger.debug("running")
        self.tab.add_iso_button_handler(self.__iso)
        self.tab.add_upload_button_handler(self.__update_device)
        self.tab.add_stim_dur_entry_changed_handler(self.__stim_dur_entry_changed)
        self.tab.add_stim_intens_entry_changed_handler(self.__stim_intens_entry_changed)
        self.tab.add_upper_isi_entry_changed_handler(self.__upper_isi_entry_changed)
        self.tab.add_lower_isi_entry_changed_handler(self.__lower_isi_entry_changed)
        self.logger.debug("done")

    def __stim_dur_entry_changed(self):
        """
        Handle when user changes the value in the stim duration field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_stim_dur_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __stim_intens_entry_changed(self):
        """
        Handle when user changes the value in the stim intensity field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_stim_intens_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __upper_isi_entry_changed(self):
        """
        Handle when user changes the value in the upper isi field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_upper_isi_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __lower_isi_entry_changed(self):
        """
        Handle when user changes the value in the lower isi field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        self.logger.debug("running")
        if not self.__updating_config:
            self.__check_lower_isi_val()
            self.__set_upload_button(True)
        self.logger.debug("done")

    def __check_stim_dur_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.logger.debug("running")
        self.__errors[0] = True
        usr_input = self.tab.get_stim_dur_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if drtv1_0_stim_dur_max >= usr_input_int >= drtv1_0_stim_dur_min:
                self.__errors[0] = False
                self.__changed[0] = usr_input_int != self.__current_vals[0]
        self.tab.set_stim_dur_val_error(self.__errors[0])
        self.logger.debug("done")

    def __check_stim_intens_val(self):
        """ Update value with new value from slider. This value will never be out of range due to set slider range. """
        self.logger.debug("running")
        new_val_percent = self.tab.get_stim_intens_val()
        self.tab.set_stim_intens_val_label(new_val_percent)
        self.__changed[1] = self.__calc_percent_to_val(new_val_percent) != self.__current_vals[1]
        self.logger.debug("done")

    def __check_upper_isi_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.logger.debug("running")
        self.__errors[1] = True
        usr_input = self.tab.get_upper_isi_val()
        lower = self.tab.get_lower_isi_val()
        if usr_input.isdigit() and lower.isdigit():
            usr_input_int = int(usr_input)
            if drtv1_0_ISI_max >= usr_input_int >= int(lower):
                self.__errors[1] = False
                self.__changed[2] = usr_input_int != self.__current_vals[2]
        self.tab.set_upper_isi_val_error(self.__errors[1])
        if not self.__errors[1] and self.__errors[2]:
            self.__check_lower_isi_val()
        elif self.__errors[1] and not self.__errors[2]:
            self.__check_lower_isi_val()
        self.logger.debug("done")

    def __check_lower_isi_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.logger.debug("running")
        self.__errors[2] = True
        usr_input = self.tab.get_lower_isi_val()
        upper = self.tab.get_upper_isi_val()
        if usr_input.isdigit() and upper.isdigit():
            usr_input_int = int(usr_input)
            if int(upper) >= usr_input_int >= drtv1_0_ISI_min:
                self.__errors[2] = False
                self.__changed[3] = usr_input_int != self.__current_vals[3]
        self.tab.set_lower_isi_val_error(self.__errors[2])
        if not self.__errors[2] and self.__errors[1]:
            self.__check_upper_isi_val()
        elif self.__errors[2] and not self.__errors[1]:
            self.__check_upper_isi_val()
        self.logger.debug("done")

    def __set_upload_button(self, is_active):
        """ Check to make sure no errors are set and that there are changes to be made. Activate button if needed. """
        self.logger.debug("running")
        if (self.__changed[0] or self.__changed[1] or self.__changed[2] or self.__changed[3])\
                and not (self.__errors[0] or self.__errors[1] or self.__errors[2]):
            self.tab.set_upload_button_activity(is_active)
        else:
            self.tab.set_upload_button_activity(False)
        self.logger.debug("done")

    def __update_device(self):
        """ Send updated values to device. Only send uploads if needed, then set as custom and disable upload button """
        self.logger.debug("running")
        if self.__changed[0]:
            self.__set_device_stim_duration(self.tab.get_stim_dur_val())
        if self.__changed[1]:
            self.__set_device_stim_intensity(self.tab.get_stim_intens_val())
        if self.__changed[2]:
            self.__set_device_upper_isi(self.tab.get_upper_isi_val())
        if self.__changed[3]:
            self.__set_device_lower_isi(self.tab.get_lower_isi_val())
        self.tab.set_config_val("Custom")
        self.__set_change_bools_false()
        self.__set_upload_button(False)
        self.logger.debug("done")

    def __set_change_bools_false(self):
        self.logger.debug("running")
        for i in self.__changed:
            self.__changed[i] = False
        self.logger.debug("done")

    def __set_val(self, var, val):
        """ Set display value of var to val. """
        self.logger.debug("running")
        if var == "stimDur":
            self.__current_vals[0] = int(val)
            self.tab.set_stim_dur_val(val)
            self.tab.set_stim_dur_val_error(False)
        elif var == "intensity":
            self.__current_vals[1] = int(val)
            self.tab.set_stim_intens_val(self.__calc_val_to_percent(val))
        elif var == "upperISI":
            self.__current_vals[2] = int(val)
            self.tab.set_upper_isi_val(val)
            self.tab.set_upper_isi_val_error(False)
        elif var == "lowerISI":
            self.__current_vals[3] = int(val)
            self.tab.set_lower_isi_val(val)
            self.tab.set_lower_isi_val_error(False)
        self.logger.debug("done")

    def __iso(self):
        """ Upload ISO Standards to device. """
        self.logger.debug("running")
        self.tab.set_config_val("ISO")
        self.__set_device_upper_isi("5000")
        self.__set_device_lower_isi("3000")
        self.__set_device_stim_intensity(100)
        self.__set_device_stim_duration("1000")
        self.__set_upload_button(False)
        self.logger.debug("done")

    def __set_device_stim_duration(self, val):
        """ Upload current setting from user to device. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_stimDur", str(val)))
        self.logger.debug("done")

    def __set_device_stim_intensity(self, val):
        """ Upload current setting from user to device. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_intensity", str(self.__calc_percent_to_val(val))))
        self.logger.debug("done")

    def __set_device_upper_isi(self, val):
        """ Upload current setting from user to device. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_upperISI", str(val)))
        self.logger.debug("done")

    def __set_device_lower_isi(self, val):
        """ Upload current setting from user to device. """
        self.logger.debug("running")
        self.__send_msg(self.__prepare_msg("set_lowerISI", str(val)))
        self.logger.debug("done")

    def __send_msg(self, msg):
        """ Send message to device. """
        self.logger.debug("running")
        self.signals.send_device_msg_sig.emit(msg)
        self.logger.debug("done")

    @staticmethod
    def __calc_val_to_percent(val):
        """ Calculate the value of stim intensity from device. """
        return trunc(val / drtv1_0_intensity_max * 100)

    @staticmethod
    def __calc_percent_to_val(val):
        """ Calculate the value of stim intensity for device"""
        return ceil(val / 100 * drtv1_0_intensity_max)

    @staticmethod
    def __parse_msg(msg_string):
        ret = dict()
        ret['values'] = {}
        if msg_string[0:4] == "cfg>":
            ret['type'] = "settings"
            # Check if this is a response to get_config
            if len(msg_string) > 90:
                # Get relevant values from msg and insert into ret
                for i in drtv1_0_config_fields:
                    index = msg_string.find(i + ":")
                    index_len = len(i) + 1
                    val_len = msg_string.find(', ', index + index_len)
                    if val_len < 0:
                        val_len = None
                    ret['values'][msg_string[index:index+index_len-1]] = int(msg_string[index+index_len:val_len])
            else:
                # Single value update, find which value it is and insert into ret
                for i in drtv1_0_config_fields:
                    index = msg_string.find(i + ":")
                    if index > 0:
                        index_len = len(i)
                        val_ind = index + index_len + 1
                        ret['values'][msg_string[index:index + index_len]] = int(msg_string[val_ind:])
        elif msg_string[0:4] == "trl>":
            ret['type'] = "data"
            val_ind_start = 4
            for i in drtv1_0_output_fields:
                val_ind_end = msg_string.find(', ', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                ret['values'][i] = int(msg_string[val_ind_start:val_ind_end])
                if val_ind_end:
                    val_ind_start = val_ind_end + 2
        return ret

    @staticmethod
    def __prepare_msg(cmd, arg=None):
        """ Create string using drt syntax. """
        if arg:
            msg_to_send = cmd + " " + arg + "\n"
        else:
            msg_to_send = cmd + "\n"
        return msg_to_send

    @staticmethod
    def __format_output_for_save_file(msg):
        """ Format and return device output. Typically used for saving data to file. """
        line = ""
        for i in drtv1_0_save_fields:
            line += ", " + str(msg[i])
        line = line.rstrip("\r\n")
        line = line + ", "
        return line
