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

from math import trunc, ceil
from Devices.DRT.View.drt_tab import DRTTab
from Devices.DRT.Model.drt_defs import drtv1_0_intensity_max, drtv1_0_stim_dur_max, drtv1_0_stim_dur_min, drtv1_0_ISI_max,\
    drtv1_0_ISI_min, drtv1_0_output_fields, drtv1_0_file_hdr


class DRTController:
    def __init__(self, tab_parent, device, msg_callback, graph_callback):
        device_name = device[0] + " on " + device[1]
        self.__tab = DRTTab(tab_parent, device_name)
        self.__graph_callback = graph_callback
        self.__device_info = device
        self.__msg_callback = msg_callback
        self.__updating_config = False
        self.__errors = [False, False, False]  # stimDur, upperISI, lowerISI
        self.__changed = [False] * 4  # stimDur, stimIntens, upperISI, lowerISI
        self.__current_vals = [0, 0, 0, 0]  # stimDur, stimIntens, upperISI, lowerISI
        self.__get_vals()
        self.__set_upload_button(False)
        self.__data_types = [["Response Time", 0, True], ["Clicks", 0, True]]
        #self.__add_graph_data_type_buttons()
        #self.__init_graph()
        self.__set_handlers()
        self.__send_output_msg("done with __init__()")

    def update_config(self, msg):
        self.__send_output_msg("update_config()")
        """ Update device configuration display. """
        self.__updating_config = True
        for key in msg:
            self.__set_val(key, msg[key])
        self.__updating_config = False
        self.__send_output_msg("done with update_config()")

    def add_data_to_graph(self, timestamp, data):
        """ Send data from device to graph for display. Separate data types into their own calls. """
        self.__graph_callback(self.__device_info, (self.__data_types[0][0], timestamp, data[drtv1_0_output_fields[3]]))
        self.__graph_callback(self.__device_info, (self.__data_types[1][0], timestamp, data[drtv1_0_output_fields[2]]))

    def get_tab_obj(self):
        return self.__tab

    @staticmethod
    def format_output_for_save_file(msg):
        """ Format and return device output. Typically used for saving data to file. """
        line = ""
        for i in drtv1_0_output_fields:
            line += ", " + str(msg[i])
        line = line.rstrip("\r\n")
        line = line + ", "
        return line

    @staticmethod
    def get_hdr():
        return drtv1_0_file_hdr

    def __set_handlers(self):
        self.__send_output_msg("__set_handlers()")
        self.__tab.add_iso_button_handler(self.__iso)
        self.__tab.add_upload_button_handler(self.__update_device)
        self.__tab.add_stim_dur_entry_changed_handler(self.__stim_dur_entry_changed)
        self.__tab.add_stim_intens_entry_changed_handler(self.__stim_intens_entry_changed)
        self.__tab.add_upper_isi_entry_changed_handler(self.__upper_isi_entry_changed)
        self.__tab.add_lower_isi_entry_changed_handler(self.__lower_isi_entry_changed)
        self.__send_output_msg("done with __set_handlers()")
        #self.__tab.add_graph_button_handler(self.__data_types[0][1], self.__rt_graph_button_handler)
        #self.__tab.add_graph_button_handler(self.__data_types[1][1], self.__clicks_graph_button_handler)

    def __add_graph_data_type_buttons(self):
        """ Depriciated. """
        for i in range(len(self.__data_types)):
            self.__data_types[i][1] = self.__tab.add_graph_button(self.__data_types[i][0])

    def __init_graph(self):
        """ Depriciated. """
        the_list = []
        for data_type in self.__data_types:
            the_list.append(data_type[0])
        self.__graph_callback.add_device(self.__device_info, the_list)

    def __rt_graph_button_handler(self):
        """ Depriciated. """
        self.__data_types[0][2] = not self.__data_types[0][2]
        self.__graph_callback.set_device_data_type_activity(self.__device_info, self.__data_types[0][0],
                                                            self.__data_types[0][2])
        self.__tab.toggle_graph_button(self.__data_types[0][1])

    def __clicks_graph_button_handler(self):
        """ Depriciated. """
        self.__data_types[1][2] = not self.__data_types[1][2]
        self.__graph_callback.set_device_data_type_activity(self.__device_info, self.__data_types[1][0],
                                                            self.__data_types[1][2])
        self.__tab.toggle_graph_button(self.__data_types[1][1])

    def __stim_dur_entry_changed(self):
        """
        Handle when user changes the value in the stim duration field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        if not self.__updating_config:
            self.__check_stim_dur_val()
            self.__set_upload_button(True)

    def __stim_intens_entry_changed(self):
        """
        Handle when user changes the value in the stim intensity field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        if not self.__updating_config:
            self.__check_stim_intens_val()
            self.__set_upload_button(True)

    def __upper_isi_entry_changed(self):
        """
        Handle when user changes the value in the upper isi field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        if not self.__updating_config:
            self.__check_upper_isi_val()
            self.__set_upload_button(True)

    def __lower_isi_entry_changed(self):
        """
        Handle when user changes the value in the lower isi field.
        Make sure it was user that changed the value that it was not changed programmatically.
        If changed by user, check validity of value and then allow user to commit change.
        """
        if not self.__updating_config:
            self.__check_lower_isi_val()
            self.__set_upload_button(True)

    def __check_stim_dur_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.__errors[0] = True
        usr_input = self.__tab.get_stim_dur_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if drtv1_0_stim_dur_max >= usr_input_int >= drtv1_0_stim_dur_min:
                self.__errors[0] = False
                self.__changed[0] = usr_input_int != self.__current_vals[0]
        self.__tab.set_stim_dur_val_error(self.__errors[0])

    def __check_stim_intens_val(self):
        """ Update value with new value from slider. This value will never be out of range due to set slider range. """
        new_val_percent = self.__tab.get_stim_intens_val()
        self.__tab.set_stim_intens_val_label(new_val_percent)
        self.__changed[1] = self.__calc_percent_to_val(new_val_percent) != self.__current_vals[1]

    def __check_upper_isi_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.__errors[1] = True
        usr_input = self.__tab.get_upper_isi_val()
        lower = self.__tab.get_lower_isi_val()
        if usr_input.isdigit() and lower.isdigit():
            usr_input_int = int(usr_input)
            if drtv1_0_ISI_max >= usr_input_int >= int(lower):
                self.__errors[1] = False
                self.__changed[2] = usr_input_int != self.__current_vals[2]
        self.__tab.set_upper_isi_val_error(self.__errors[1])
        if not self.__errors[1] and self.__errors[2]:
            self.__check_lower_isi_val()
        elif self.__errors[1] and not self.__errors[2]:
            self.__check_lower_isi_val()

    def __check_lower_isi_val(self):
        """ Check validity of value, if not valid then set error bool and set visual cue. """
        self.__errors[2] = True
        usr_input = self.__tab.get_lower_isi_val()
        upper = self.__tab.get_upper_isi_val()
        if usr_input.isdigit() and upper.isdigit():
            usr_input_int = int(usr_input)
            if int(upper) >= usr_input_int >= drtv1_0_ISI_min:
                self.__errors[2] = False
                self.__changed[3] = usr_input_int != self.__current_vals[3]
        self.__tab.set_lower_isi_val_error(self.__errors[2])
        if not self.__errors[2] and self.__errors[1]:
            self.__check_upper_isi_val()
        elif self.__errors[2] and not self.__errors[1]:
            self.__check_upper_isi_val()

    def __set_upload_button(self, is_active):
        """ Check to make sure no errors are set and that there are changes to be made. Activate button if needed. """
        if (self.__changed[0] or self.__changed[1] or self.__changed[2] or self.__changed[3])\
                and not (self.__errors[0] or self.__errors[1] or self.__errors[2]):
            self.__tab.set_upload_button_activity(is_active)
        else:
            self.__tab.set_upload_button_activity(False)

    def __update_device(self):
        """ Send updated values to device. Only send uploads if needed, then set as custom and disable upload button """
        if self.__changed[0]:
            self.__set_device_stim_duration(self.__tab.get_stim_dur_val())
        if self.__changed[1]:
            self.__set_device_stim_intensity(self.__tab.get_stim_intens_val())
        if self.__changed[2]:
            self.__set_device_upper_isi(self.__tab.get_upper_isi_val())
        if self.__changed[3]:
            self.__set_device_lower_isi(self.__tab.get_lower_isi_val())
        self.__tab.set_config_val("Custom")
        self.__set_change_bools_false()
        self.__set_upload_button(False)

    def __set_change_bools_false(self):
        for i in self.__changed:
            self.__changed[i] = False

    def __get_vals(self):
        self.__send_output_msg("__get_vals()")
        """ Request current device settings. """
        self.__send_msg({'cmd': "get_config"})
        self.__send_output_msg("done with __get_vals()")

    def __set_val(self, var, val):
        """ Set display value of var to val. """
        self.__send_output_msg("__set_vals()")
        if var == "stimDur":
            self.__current_vals[0] = int(val)
            self.__tab.set_stim_dur_val(val)
            self.__tab.set_stim_dur_val_error(False)
        elif var == "intensity":
            self.__current_vals[1] = int(val)
            self.__tab.set_stim_intens_val(self.__calc_val_to_percent(val))
        elif var == "upperISI":
            self.__current_vals[2] = int(val)
            self.__tab.set_upper_isi_val(val)
            self.__tab.set_upper_isi_val_error(False)
        elif var == "lowerISI":
            self.__current_vals[3] = int(val)
            self.__tab.set_lower_isi_val(val)
            self.__tab.set_lower_isi_val_error(False)
        self.__send_output_msg("done with __set_vals()")

    def __iso(self):
        """ Upload ISO Standards to device. """
        self.__tab.set_config_val("ISO")
        self.__set_device_upper_isi("5000")
        self.__set_device_lower_isi("3000")
        self.__set_device_stim_intensity(100)
        self.__set_device_stim_duration("1000")
        self.__set_upload_button(False)

    def __set_device_stim_duration(self, val):
        """ Upload current setting from user to device. """
        self.__send_msg({'cmd': "set_stimDur", 'arg': str(val)})

    def __set_device_stim_intensity(self, val):
        """ Upload current setting from user to device. """
        self.__send_msg({'cmd': "set_intensity", 'arg': str(self.__calc_percent_to_val(val))})

    def __set_device_upper_isi(self, val):
        """ Upload current setting from user to device. """
        self.__send_msg({'cmd': "set_upperISI", 'arg': str(val)})

    def __set_device_lower_isi(self, val):
        """ Upload current setting from user to device. """
        self.__send_msg({'cmd': "set_lowerISI", 'arg': str(val)})

    def __send_msg(self, msg):
        """ Send message to device. """
        msg['type'] = "send"
        msg['device'] = self.__device_info
        self.__msg_callback(msg)

    def __send_output_msg(self, msg):
        pass
        #self.__msg_callback("From drt_controller.py. msg: " + msg)

    @staticmethod
    def __calc_val_to_percent(val):
        """ Calculate the value of stim intensity from device. """
        return trunc(val / drtv1_0_intensity_max * 100)

    @staticmethod
    def __calc_percent_to_val(val):
        """ Calculate the value of stim intensity for device"""
        return ceil(val / 100 * drtv1_0_intensity_max)

