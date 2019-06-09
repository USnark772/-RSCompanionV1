""" Contains a class for detecting changes on the serial/usb port
This class requires that a separate thread be created to call update.
When the target device is plugged in or removed the connect_event or
disconnect_event flags are turned True.
"""

from serial import Serial, SerialException
from serial.tools import list_ports
from Model.defs import devices, drt_config_fields, drt_trial_fields, vog_block_field


class DeviceManager:
    def __init__(self, msg_handler):
        self.msg_callback = msg_handler

        self.devices_known = []
        self.devices_attached = []
        self.devices_to_add = []
        self.devices_to_remove = []

        self.profiles = devices
        self.devices = dict()

    def update(self):
        self.devices_known = list(self.devices.keys())
        self.__scan_ports()  # probe plug/unplug events

        if len(self.devices_to_add) != 0:
            self.__attach_devices()
        elif len(self.devices_to_remove) != 0:
            self.__remove_devices()

        for d in self.devices:
            if self.devices[d]['id'] != 'unknown':
                try:
                    if self.devices[d]['port'].in_waiting > 0:
                        the_message = self.devices[d]['port'].readline().decode("utf-8")
                        print(the_message)
                        self.msg_callback({'type': "save",
                                           'msg': str(self.devices[d]['id']
                                                      + ", " + self.devices[d]['port'].name
                                                      + ", " + the_message)})
                        msg_dict = {'device': (self.devices[d]['id'], self.devices[d]['port'].name)}
                        if self.devices[d]['id'] == "drt":
                            self.__parse_drt_msg(the_message, msg_dict)
                        elif self.devices[d]['id'] == "vog":
                            self.__parse_vog_msg(the_message, msg_dict)
                        else:
                            self.msg_callback({'type': "save", 'msg': "Debug, DeviceManager.update(), couldn't "
                                                                      "match up device" + str(self.devices[d]['id'])})
                        self.msg_callback(msg_dict)
                except:
                    pass

    def handle_msg(self, msg_dict):
        msg_type = msg_dict['type']
        if msg_type == "send":
            port = None
            msg_to_send = None
            for d in self.devices:
                if msg_dict['device'] == (self.devices[d]['id'], self.devices[d]['port'].name):
                    port = self.devices[d]['port']
            if not port:
                self.msg_callback({'type': "save", 'msg': "Debug, DeviceManager.handle_msg(), Device not found"})
                pass
            else:
                if msg_dict['device'][0] == "drt":
                    msg_to_send = self.__prepare_drt_msg(msg_dict)
                elif msg_dict['device'][0] == "vog":
                    msg_to_send = self.__prepare_vog_msg(msg_dict)
                self.__send_msg_on_port(port, msg_to_send)
        else:
            self.msg_callback({'type': "save", 'msg': "Debug, DeviceManager.handle_msg(), Unknown command"})

    def start_exp_all(self):
        for d in self.devices:
            self.__start_exp(self.devices[d]['id'], self.devices[d]['port'])

    def end_exp_all(self):
        for d in self.devices:
            self.__end_exp(self.devices[d]['id'], self.devices[d]['port'])

    def start_block_all(self):
        for d in self.devices:
            self.__start_block(self.devices[d]['id'], self.devices[d]['port'])

    def end_block_all(self):
        for d in self.devices:
            self.__end_block(self.devices[d]['id'], self.devices[d]['port'])

    def __start_exp(self, device, port):
        if device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_expStart"}))

    def __end_exp(self, device, port):
        if device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_expStop"}))

    def __start_block(self, device, port):
        if device == "drt":
            self.__send_msg_on_port(port, self.__prepare_drt_msg({'cmd': "exp_start"}))
        elif device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_trialStart"}))

    def __end_block(self, device, port):
        if device == "drt":
            self.__send_msg_on_port(port, self.__prepare_drt_msg({'cmd': "exp_stop"}))
        elif device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_trialStop"}))

    def __scan_ports(self):
        self.devices_to_add = []
        self.devices_to_remove = []
        self.devices_attached = []

        if len(list_ports.comports()) != 0:
            for i in list_ports.comports():
                self.devices_attached.append(i.device)

        if len(self.devices_known) == 0:
            self.devices_to_add = self.devices_attached
        elif len(self.devices_known) < len(self.devices_attached):
            self.devices_to_add = list(set(self.devices_attached) - set(self.devices_known))
        elif len(self.devices_known) > len(self.devices_attached):
            self.devices_to_remove = list(set(self.devices_known) - set(self.devices_attached))

    def __attach_devices(self):
        for port in list_ports.comports():
            if port.device in self.devices_to_add:
                for device in self.profiles:
                    if port.vid == self.profiles[device]['vid'] and port.pid == self.profiles[device]['pid']:
                        try:
                            the_port = Serial(port.device)
                        except SerialException:
                            self.msg_callback({'type': "error", 'msg': "Connection error, please reconnect device"})
                            del port
                            return
                        self.devices[port.device] = {'port': the_port, 'id': device}
                        msg_dict = {'type': "add", 'device': (self.devices[port.device]['id'], self.devices[port.device]['port'].name)}
                        self.msg_callback(msg_dict)
                        break
                    else:
                        self.devices[port.device] = {'id': 'unknown'}

        self.devices_known = list(self.devices.keys())

    def __remove_devices(self):
        for e in self.devices_to_remove:
            if not self.devices[e]['id'] == "unknown":
                self.devices[e]['port'].close()
                msg_dict = {'type': "remove", 'device': (self.devices[e]['id'], self.devices[e]['port'].name)}
                self.msg_callback(msg_dict)
            del self.devices[e]

        self.devices_known = list(self.devices.keys())

    @staticmethod
    def __send_msg_on_port(port, msg_to_send):
        port.write(str.encode(msg_to_send))

    @staticmethod
    def __prepare_drt_msg(msg_dict):
        if 'arg' in msg_dict.keys():
            msg_to_send = msg_dict['cmd'] + " " + str(msg_dict['arg']) + "\n"
        else:
            msg_to_send = msg_dict['cmd'] + "\n"
        return msg_to_send

    # TODO: Clean this up
    @staticmethod
    def __parse_drt_msg(msg, msg_dict):
        if msg[0:4] == "cfg>":
            msg_dict['type'] = "settings"
            msg_dict['values'] = {}
            # Check if this is a response to get_config
            if len(msg) > 90:
                # Get relevant values from msg and insert into msg_dict
                for i in range(0, len(drt_config_fields)):
                    index = msg.find(drt_config_fields[i] + ":")
                    index_len = len(drt_config_fields[i]) + 1
                    val_len = msg.find(', ', index + index_len)
                    if val_len < 0:
                        val_len = None
                    msg_dict['values'][msg[index:index+index_len-1]] = int(msg[index+index_len:val_len])
            else:
                # Single value update, find which value it is and insert into msg_dict
                for i in range(0, len(drt_config_fields)):
                    index = msg.find(drt_config_fields[i] + ":")
                    if index > 0:
                        index_len = len(drt_config_fields[i])
                        val_ind = index + index_len + 1
                        msg_dict['values'][msg[index:index + index_len]] = int(msg[val_ind:])
        elif msg[0:4] == "trl>":
            msg_dict['type'] = "data"
            val_ind_start = 4
            for i in range(0, len(drt_trial_fields)):
                val_ind_end = msg.find(', ', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict[drt_trial_fields[i]] = int(msg[val_ind_start:val_ind_end])
                if val_ind_end:
                    val_ind_start = val_ind_end + 2

    @staticmethod
    def __prepare_vog_msg(msg_dict):
        if 'arg' in msg_dict.keys():
            msg_to_send = ">" + msg_dict['cmd'] + "|" + str(msg_dict['arg']) + "<<\n"
        else:
            msg_to_send = ">" + msg_dict['cmd'] + "|" + "<<\n"
        return msg_to_send

    # TODO: Clean this up
    @staticmethod
    def __parse_vog_msg(msg, msg_dict):
        if msg[0:5] == "data|":
            msg_dict['type'] = "data"
            val_ind_start = 5
            for i in range(len(vog_block_field)):
                val_ind_end = msg.find(',', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict[vog_block_field[i]] = msg[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 1
        elif msg[0:6] == "config":
            msg_dict['type'] = "settings"
            bar_ind = msg.find('|', 6)
            msg_dict['values'] = {}
            if msg[6:bar_ind] == "Name":
                msg_dict['values']['Name'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "MaxOpen":
                msg_dict['values']['MaxOpen'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "MaxClose":
                msg_dict['values']['MaxClose'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "Debounce":
                msg_dict['values']['Debounce'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "ClickMode":
                msg_dict['values']['ClickMode'] = msg[bar_ind + 1: len(msg)]
        elif "Click" in msg:
            msg_dict['action'] = "Click"
