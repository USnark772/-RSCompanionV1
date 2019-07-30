# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from Devices.VOG.View.vog_tab import VOGTab
from Devices.VOG.Model.vog_defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min, \
    vog_output_field, vog_file_hdr


class VOGController:
    def __init__(self, parent, device, msg_callback, graph_callback):
        device_name = device[0] + " on " + device[1]
        self.__tab = VOGTab(parent, device_name)
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
        self.__lens_open = False
        # bools: tried array but had bugs when setting bools[0] to true, bools must be separate.
        self.__prev_vals = ["", ""]  # MaxOpen, MaxClose
        self.__get_vals()
        self.__set_upload_button(False)
        self.__data_types = [["Time Open", 0, True], ["Time Closed", 0, True]]
        #self.__add_graph_data_type_buttons()
        #self.__init_graph()
        self.__set_handlers()

    def update_config(self, msg):
        self.__updating_config = True
        for key in msg:
            self.__set_val(key, msg[key])
        self.__updating_config = False

    def add_data_to_graph(self, timestamp, data):
        print("vog_controller.py add_data_to_graph()")
        self.__graph_callback(self.__device_info, (timestamp, int(data[vog_output_field[1]]), int(data[vog_output_field[2]])))

    def get_tab_obj(self):
        return self.__tab

    @staticmethod
    def format_output_for_save_file(msg):
        line = ""
        for i in vog_output_field:
            line += ", " + str(msg[i])
        line = line.rstrip("\r\n")
        line = line + ", "
        return line

    @staticmethod
    def get_hdr():
        return vog_file_hdr

    def __set_handlers(self):
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
        self.__tab.add_manual_control_handler(self.__toggle_lens)
        #self.__tab.add_graph_button_handler(self.__data_types[0][1], self.__time_open_graph_button_handler)
        #self.__tab.add_graph_button_handler(self.__data_types[1][1], self.__time_closed_graph_button_handler)

    def __add_graph_data_type_buttons(self):
        for i in range(len(self.__data_types)):
            self.__data_types[i][1] = self.__tab.add_graph_button(self.__data_types[i][0])

    def __init_graph(self):
        the_list = []
        for data_type in self.__data_types:
            the_list.append(data_type[0])
        self.__graph_obj.add_device(self.__device_info, the_list)

    def __time_open_graph_button_handler(self):
        self.__data_types[0][2] = not self.__data_types[0][2]
        self.__graph_obj.set_device_data_type_activity(self.__device_info, self.__data_types[0][0],
                                                       self.__data_types[0][2])
        self.__tab.toggle_graph_button(self.__data_types[0][1])

    def __time_closed_graph_button_handler(self):
        self.__data_types[1][2] = not self.__data_types[1][2]
        self.__graph_obj.set_device_data_type_activity(self.__device_info, self.__data_types[1][0],
                                                       self.__data_types[1][2])
        self.__tab.toggle_graph_button(self.__data_types[1][1])

    def __open_entry_changed(self):
        if not self.__updating_config:
            self.__check_open_val()
            self.__set_upload_button(True)

    def __close_entry_changed(self):
        if not self.__updating_config:
            self.__check_close_val()
            self.__set_upload_button(True)

    def __debounce_entry_changed(self):
        if not self.__updating_config:
            self.__check_debounce_val()
            self.__set_upload_button(True)

    def __button_mode_entry_changed(self):
        if not self.__updating_config:
            self.__check_button_mode_val()
            self.__set_upload_button(True)

    def __toggle_open_inf(self, is_checked):
        if is_checked:
            self.__prev_vals[0] = self.__tab.get_open_val()
            self.__tab.set_open_val(str(vog_max_open_close))
        else:
            self.__tab.set_open_val(self.__prev_vals[0])
        self.__tab.set_open_val_entry_activity(not is_checked)

    def __toggle_close_inf(self, is_checked):
        if is_checked:
            self.__prev_vals[1] = self.__tab.get_close_val()
            self.__tab.set_close_val(str(vog_max_open_close))
        else:
            self.__tab.set_close_val(self.__prev_vals[1])
        self.__tab.set_close_val_entry_activity(not is_checked)

    def __update_device(self):
        # Only send uploads if needed, then set as custom and disable upload button
        if self.__open_changed:
            self.__set_device_open(self.__tab.get_open_val())
        if self.__closed_changed:
            self.__set_device_close(self.__tab.get_close_val())
        if self.__debounce_changed:
            self.__set_device_debounce(self.__tab.get_debounce_val())
        if self.__mode_changed:
            self.__set_device_click(self.__tab.get_button_mode())
        self.__tab.set_config_value("Custom")
        self.__set_changed_bools_false()
        self.__set_upload_button(False)

    def __set_changed_bools_false(self):
        self.__open_changed = False
        self.__closed_changed = False
        self.__debounce_changed = False
        self.__mode_changed = False

    def __get_vals(self):
        self.__send_msg({'cmd': "get_configName"})
        self.__send_msg({'cmd': 'get_configMaxOpen'})
        self.__send_msg({'cmd': 'get_configMaxClose'})
        self.__send_msg({'cmd': 'get_configDebounce'})
        self.__send_msg({'cmd': 'get_configClickMode'})
        self.__send_msg({'cmd': 'get_configButtonControl'})

    def __set_upload_button(self, is_active):
        if (self.__open_changed or self.__closed_changed or self.__debounce_changed or self.__mode_changed)\
                and not (self.__errors[0] or self.__errors[1] or self.__errors[2]):
            self.__tab.set_upload_button_activity(is_active)
        else:
            self.__tab.set_upload_button_activity(False)

    def __check_open_val(self):
        self.__errors[0] = True
        usr_input = self.__tab.get_open_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_max_open_close >= usr_input_int >= vog_min_open_close:
                self.__errors[0] = False
                self.__open_changed = usr_input_int != self.__current_vals[0]
        self.__tab.set_open_val_error(self.__errors[0])

    def __check_close_val(self):
        self.__errors[1] = True
        usr_input = self.__tab.get_close_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_max_open_close >= usr_input_int >= vog_min_open_close:
                self.__errors[1] = False
                self.__closed_changed = usr_input_int != self.__current_vals[1]
        self.__tab.set_close_val_error(self.__errors[1])

    def __check_debounce_val(self):
        self.__errors[2] = True
        usr_input = self.__tab.get_debounce_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_debounce_max >= usr_input_int >= vog_debounce_min:
                self.__errors[2] = False
                self.__debounce_changed = usr_input_int != self.__current_vals[2]
        self.__tab.set_debounce_val_error(self.__errors[2])

    def __check_button_mode_val(self):
        self.__mode_changed = self.__tab.get_button_mode() != self.__current_vals[3]

    def __set_val(self, var, val):
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

    def __toggle_lens(self):
        if self.__lens_open:
            self.__send_msg({'cmd': "do_peekClose"})
        else:
            self.__send_msg({'cmd': "do_peekOpen"})

    def __nhtsa(self):
        self.__tab.set_open_inf(False)
        self.__tab.set_close_inf(False)
        self.__set_device_config("NHTSA")
        self.__set_device_open("1500")
        self.__set_device_close("1500")
        self.__set_device_debounce("20")
        self.__set_device_click("1")
        self.__set_device_button_control("0")
        self.__set_upload_button(False)

    def __eblind(self):
        self.__tab.set_open_inf(True)
        self.__tab.set_close_inf(False)
        self.__set_device_config("eBlindfold")
        self.__set_device_open(vog_max_open_close)
        self.__set_device_close("0")
        self.__set_device_debounce("100")
        self.__set_device_click("1")
        self.__set_device_button_control("0")
        self.__set_upload_button(False)

    def __direct_control(self):
        self.__tab.set_open_inf(True)
        self.__tab.set_close_inf(True)
        self.__set_device_config("DIRECT CONTROL")
        self.__set_device_open(vog_max_open_close)
        self.__set_device_close("0")
        self.__set_device_debounce("100")
        self.__set_device_click("0")
        self.__set_device_button_control("1")
        self.__set_upload_button(False)

    def __set_device_config(self, val):
        self.__send_msg({'cmd': "set_configName", 'arg': str(val)})

    def __set_device_open(self, val):
        self.__send_msg({'cmd': "set_configMaxOpen", 'arg': str(val)})

    def __set_device_close(self, val):
        self.__send_msg({'cmd': "set_configMaxClose", 'arg': str(val)})

    def __set_device_debounce(self, val):
        self.__send_msg({'cmd': "set_configDebounce", 'arg': str(val)})

    def __set_device_click(self, val):
        self.__send_msg({'cmd': "set_configClickMode", 'arg': str(val)})

    def __set_device_button_control(self, val):
        self.__send_msg({'cmd': "set_configButtonControl", 'arg': str(val)})

    def __send_msg(self, msg):
        msg['type'] = "send"
        msg['device'] = self.__device_info
        self.__msg_callback(msg)
