# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from View.TabWidget.vog_tab import VOGTab
from Model.defs import vog_max_open_close, vog_min_open_close, vog_debounce_max, vog_debounce_min, vog_button_mode


class VOGConfigureController:
    def __init__(self, parent, device, msg_callback):
        self.tab = VOGTab(parent, device[0])
        self.device_info = device
        self.msg_callback = msg_callback
        self.handling_msg = False
        '''
        self.values = {'buttonControl': self.button_mode_selector,
                       'Debounce': self.debounce_time_line_edit,
                       'MaxClose': self.close_dur_line_edit,
                       'MaxOpen': self.open_dur_line_edit,
                       'ClickMode': 0}
        '''
        self.errors = [False, False, False]  # MaxOpen, MaxClose, Debounce
        self.__set_handlers()
        self.__get_vals()

    def __set_handlers(self):
        self.tab.add_direct_control_button_handler(self.__direct_control)
        self.tab.add_eblind_button_handler(self.__eblind)
        self.tab.add_nhtsa_button_handler(self.__nhtsa)
        self.tab.add_close_inf_handler(self.__toggle_close_inf)
        self.tab.add_open_inf_handler(self.__toggle_open_inf)
        self.tab.add_upload_button_handler(self.__update_device)

    def __update_device(self):
        self.__set_device_open(self.tab.get_open_val())
        self.__set_device_close(self.tab.get_close_val())
        self.__set_device_debounce(self.tab.get_debounce_val())
        self.__set_device_button_control(self.tab.get_button_mode())

    def __get_vals(self):
        self.__send_msg({'cmd': "get_configName"})
        self.__send_msg({'cmd': 'get_configMaxOpen'})
        self.__send_msg({'cmd': 'get_configMaxClose'})
        self.__send_msg({'cmd': 'get_configDebounce'})
        self.__send_msg({'cmd': 'get_configClickMode'})
        self.__send_msg({'cmd': 'get_configButtonControl'})

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

    def handle_msg(self, msg):
        print("Configurator handling msg")
        print(msg)
        for key in msg:
            self.__set_val(key, int(msg[key]))

    def __set_val(self, var, val):
        if var == "Name":
            pass
        elif var == "MaxOpen":
            self.tab.set_open_val(val)
        elif var == "MaxClose":
            self.tab.set_close_val(val)
        elif var == "Debounce":
            self.tab.set_debounce_val(val)
        elif var == "ClickMode":
            self.tab.set_button_mode(val)
        elif var == "ButtonControl":
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
        msg['device'] = self.device_info
        self.msg_callback(msg)
