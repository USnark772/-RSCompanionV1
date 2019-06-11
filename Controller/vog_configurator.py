# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from View.TabWidget.vog_tab import VOGTab
from Model.defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min, vog_button_mode


class VOGConfigureController:
    def __init__(self, parent, device, msg_callback):
        self.tab = VOGTab(parent, device[0] + " on " + device[1])
        self.__device_info = device
        self.__msg_callback = msg_callback
        self.__handling_msg = False
        self.__errors = [False, False, False]  # MaxOpen, MaxClose, Debounce
        self.__current_vals = [0, 0, 0, 0, 0]  # MaxOpen, MaxClose, Debounce, ClickMode, buttonControl
        self.__set_handlers()
        self.__get_vals()

    def handle_msg(self, msg):
        self.__handling_msg = True
        for key in msg:
            self.__set_val(key, msg[key])
        self.__handling_msg = False

    def __set_handlers(self):
        self.tab.add_nhtsa_button_handler(self.__nhtsa)
        self.tab.add_eblind_button_handler(self.__eblind)
        self.tab.add_direct_control_button_handler(self.__direct_control)
        self.tab.add_upload_button_handler(self.__update_device)
        self.tab.add_open_inf_handler(self.__toggle_open_inf)
        self.tab.add_close_inf_handler(self.__toggle_close_inf)
        self.tab.add_open_entry_changed_handler(self.__open_entry_changed)
        self.tab.add_close_entry_changed_handler(self.__close_entry_changed)
        self.tab.add_debounce_entry_changed_handler(self.__debounce_entry_changed)
        self.tab.add_button_mode_entry_changed_handler(self.__button_mode_entry_changed)

    def __open_entry_changed(self):
        self.__check_open_val()
        self.__set_upload_button(True)

    def __close_entry_changed(self):
        self.__check_close_val()
        self.__set_upload_button(True)

    def __debounce_entry_changed(self):
        self.__check_debounce_val()
        self.__set_upload_button(True)

    def __button_mode_entry_changed(self):
        self.__set_upload_button(True)

    def __toggle_open_inf(self, is_checked):
        if is_checked:
            self.__set_device_open(vog_max_open_close)
        else:
            self.__set_device_open(self.tab.get_open_val())
        self.tab.set_open_val_entry_activity(not is_checked)

    def __toggle_close_inf(self, is_checked):
        if is_checked:
            self.__set_device_close(vog_max_open_close)
        else:
            self.__set_device_close(self.tab.get_close_val())
        self.tab.set_close_val_entry_activity(not is_checked)

    def __update_device(self):
        # Only send uploads if needed, then set as custom and disable upload button
        open_val = int(self.tab.get_open_val())
        close_val = int(self.tab.get_close_val())
        debounce_val = int(self.tab.get_debounce_val())
        button_mode = int(self.tab.get_button_mode())
        if open_val != self.__current_vals[0]:
            self.__set_device_open(open_val)
        if close_val != self.__current_vals[1]:
            self.__set_device_close(close_val)
        if debounce_val != self.__current_vals[2]:
            self.__set_device_debounce(debounce_val)
        if button_mode != self.__current_vals[3]:
            self.__set_device_click(button_mode)
        self.tab.set_config_value("Custom")
        self.tab.set_upload_button_activity(False)

    def __get_vals(self):
        self.__send_msg({'cmd': "get_configName"})
        self.__send_msg({'cmd': 'get_configMaxOpen'})
        self.__send_msg({'cmd': 'get_configMaxClose'})
        self.__send_msg({'cmd': 'get_configDebounce'})
        self.__send_msg({'cmd': 'get_configClickMode'})
        self.__send_msg({'cmd': 'get_configButtonControl'})

    def __set_upload_button(self, is_active):
        if self.__errors[0] or self.__errors[1] or self.__errors[2] or self.__handling_msg:
            self.tab.set_upload_button_activity(False)
        else:
            self.tab.set_upload_button_activity(is_active)

    def __check_open_val(self):
        self.__errors[0] = True
        usr_input = self.tab.get_open_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_max_open_close >= usr_input_int >= vog_min_open_close:
                self.__errors[0] = False
        self.tab.set_open_val_error(self.__errors[0])

    def __check_close_val(self):
        self.__errors[1] = True
        usr_input = self.tab.get_close_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_max_open_close >= usr_input_int >= vog_min_open_close:
                self.__errors[1] = False
        self.tab.set_close_val_error(self.__errors[1])

    def __check_debounce_val(self):
        self.__errors[2] = True
        usr_input = self.tab.get_debounce_val()
        if usr_input.isdigit():
            usr_input_int = int(usr_input)
            if vog_debounce_max >= usr_input_int >= vog_debounce_min:
                self.__errors[2] = False
        self.tab.set_debounce_val_error(self.__errors[2])

    def __set_val(self, var, val):
        if var == "Name":
            self.tab.set_config_value(val)
        elif var == "MaxOpen":
            self.tab.set_open_val(val)
        elif var == "MaxClose":
            self.tab.set_close_val(val)
        elif var == "Debounce":
            self.tab.set_debounce_val(val)
        elif var == "ClickMode":
            self.tab.set_button_mode(val)
        elif var == "buttonControl":
            pass

    def __nhtsa(self):
        self.tab.set_open_inf(False)
        self.tab.set_close_inf(False)
        self.__set_device_config("NHTSA")
        self.__set_device_open("1500")
        self.__set_device_close("1500")
        self.__set_device_debounce("20")
        self.__set_device_click("1")
        self.__set_device_button_control("0")

    def __eblind(self):
        self.tab.set_open_inf(False)
        self.tab.set_close_inf(False)
        self.__set_device_config("eBlindfold")
        self.__set_device_open(vog_max_open_close)
        self.__set_device_close("0")
        self.__set_device_debounce("100")
        self.__set_device_click("1")
        self.__set_device_button_control("0")

    def __direct_control(self):
        self.tab.set_open_inf(True)
        self.tab.set_close_inf(True)
        self.__set_device_config("DIRECT CONTROL")
        self.__set_device_open(vog_max_open_close)
        self.__set_device_close("0")
        self.__set_device_debounce("100")
        self.__set_device_click("1")
        self.__set_device_button_control("1")

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
