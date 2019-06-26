# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from math import trunc, ceil
from View.GraphWidget.graph_obj import GraphObj
from Devices.DRT.View.drt_tab import DRTTab
from Devices.DRT.Model.defs import drtv1_0_intensity_max, drtv1_0_stim_dur_max, drtv1_0_stim_dur_min, drtv1_0_ISI_max,\
    drtv1_0_ISI_min, drtv1_0_output_fields, drtv1_0_file_hdr

from datetime import datetime, timedelta
from random import gauss


# TODO: Pipe data through controller to graph obj
class DRTController:
    def __init__(self, parent, device, msg_callback):
        device_name = device[0] + " on " + device[1]
        self.__tab = DRTTab(parent, device_name)
        self.__graph_obj = GraphObj(device_name, "Timestamp", "Milliseconds")
        self.__device_info = device
        self.__msg_callback = msg_callback
        self.__handling_msg = False
        self.__errors = [False, False, False]  # stimDur, upperISI, lowerISI
        self.__changed = [False] * 4  # stimDur, stimIntens, upperISI, lowerISI
        self.__current_vals = [0, 0, 0, 0]  # stimDur, stimIntens, upperISI, lowerISI
        self.__set_handlers()
        self.__get_vals()
        self.__set_upload_button(False)

        # self.__test_graph_obj()

    def __test_graph_obj(self):
        x = [datetime.now() + timedelta(seconds=i) for i in range(10)]
        y = [i + gauss(0, 1) for i, item in enumerate(x)]
        name = "Response Time"
        self.__graph_obj.add_line(name)
        self.__graph_obj.add_data(name, x, y)

        x2 = [datetime.now() + timedelta(seconds=i) for i in range(10)]
        y2 = [i + gauss(0, 1) for i, item in enumerate(x2)]
        name2 = "other"
        self.__graph_obj.add_line(name2)
        self.__graph_obj.add_data(name2, x2, y2)

        x3 = [datetime.now() + timedelta(seconds=i) for i in range(10)]
        y3 = [i + gauss(0, 1) for i, item in enumerate(x3)]
        name3 = "again"
        self.__graph_obj.add_line(name3)
        self.__graph_obj.add_data(name3, x3, y3)

    def handle_msg(self, msg):
        self.__handling_msg = True
        for key in msg:
            self.__set_val(key, msg[key])
        self.__handling_msg = False

    def get_graph_obj(self):
        return self.__graph_obj

    def set_tab_index(self, index):
        self.__tab.set_index(index)

    def get_tab_index(self):
        return self.__tab.get_index()

    def get_tab_obj(self):
        return self.__tab

    @staticmethod
    def format_output_for_save_file(msg):
        line = ""
        for i in drtv1_0_output_fields:
            line += ", " + str(msg['values'][i])
        line = line.rstrip("\r\n")
        line = line + ", "
        return line

    @staticmethod
    def get_hdr():
        return drtv1_0_file_hdr

    def __set_handlers(self):
        self.__tab.add_iso_button_handler(self.__iso)
        self.__tab.add_upload_button_handler(self.__update_device)
        self.__tab.add_stim_dur_entry_changed_handler(self.__stim_dur_entry_changed)
        self.__tab.add_stim_intens_entry_changed_handler(self.__stim_intens_entry_changed)
        self.__tab.add_upper_isi_entry_changed_handler(self.__upper_isi_entry_changed)
        self.__tab.add_lower_isi_entry_changed_handler(self.__lower_isi_entry_changed)

    def __stim_dur_entry_changed(self):
        if not self.__handling_msg:
            self.__check_stim_dur_val()
            self.__set_upload_button(True)

    def __stim_intens_entry_changed(self):
        if not self.__handling_msg:
            self.__check_stim_intens_val()
            self.__set_upload_button(True)

    def __upper_isi_entry_changed(self):
        if not self.__handling_msg:
            self.__check_upper_isi_val()
            self.__set_upload_button(True)

    def __lower_isi_entry_changed(self):
        if not self.__handling_msg:
            self.__check_lower_isi_val()
            self.__set_upload_button(True)

    def __check_stim_dur_val(self):
        self.__errors[0] = True
        usr_input = self.__tab.get_stim_dur_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if drtv1_0_stim_dur_max >= usr_input_int >= drtv1_0_stim_dur_min:
                self.__errors[0] = False
                self.__changed[0] = usr_input_int != self.__current_vals[0]
        self.__tab.set_stim_dur_val_error(self.__errors[0])

    def __check_stim_intens_val(self):
        new_val_percent = self.__tab.get_stim_intens_val()
        self.__tab.set_stim_intens_val_label(new_val_percent)
        self.__changed[1] = self.__calc_percent_to_val(new_val_percent) != self.__current_vals[1]

    def __check_upper_isi_val(self):
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
        if (self.__changed[0] or self.__changed[1] or self.__changed[2] or self.__changed[3])\
                and not (self.__errors[0] or self.__errors[1] or self.__errors[2]):
            self.__tab.set_upload_button_activity(is_active)
        else:
            self.__tab.set_upload_button_activity(False)

    def __update_device(self):
        # Only send uploads if needed, then set as custom and disable upload button
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
        self.__send_msg({'cmd': "get_config"})

    def __set_val(self, var, val):
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

    def __iso(self):
        self.__tab.set_config_val("ISO")
        self.__set_device_upper_isi("5000")
        self.__set_device_lower_isi("3000")
        self.__set_device_stim_intensity(100)
        self.__set_device_stim_duration("1000")
        self.__set_upload_button(False)

    def __set_device_stim_duration(self, val):
        self.__send_msg({'cmd': "set_stimDur", 'arg': str(val)})

    def __set_device_stim_intensity(self, val):
        self.__send_msg({'cmd': "set_intensity", 'arg': str(self.__calc_percent_to_val(val))})

    def __set_device_upper_isi(self, val):
        self.__send_msg({'cmd': "set_upperISI", 'arg': str(val)})

    def __set_device_lower_isi(self, val):
        self.__send_msg({'cmd': "set_lowerISI", 'arg': str(val)})

    def __send_msg(self, msg):
        msg['type'] = "send"
        msg['device'] = self.__device_info
        self.__msg_callback(msg)

    @staticmethod
    def __calc_val_to_percent(val):
        return trunc(val / drtv1_0_intensity_max * 100)

    @staticmethod
    def __calc_percent_to_val(val):
        return ceil(val / 100 * drtv1_0_intensity_max)
