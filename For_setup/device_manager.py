""" Contains a class for detecting changes on the serial/usb port
This class requires that a separate thread be created to call update.
When the target device is plugged in or removed the connect_event or
disconnect_event flags are turned True.
"""

import serial
from serial.tools import list_ports
import defs as defs


class DeviceManager:
    def __init__(self, msg_handler):
        # Global
        self.msg_callback = msg_handler
        self.inc_msg = ""

        self.devices_known = []
        self.devices_attached = []
        self.devices_to_add = []
        self.devices_to_remove = []

        # Local
        self.profiles = defs.devices
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
                        msg_dict = {'device': (self.devices[d]['id'], self.devices[d]['port'].name)}
                        if self.devices[d]['id'] == "drt":
                            self.__parse_drt_msg(self.devices[d]['port'].readline().decode("utf-8"), msg_dict)
                        elif self.devices[d]['id'] == "vog":
                            self.__parse_vog_msg(self.devices[d]['port'].readline().decode("utf-8"), msg_dict)
                        else:
                            print("in companion_device_com.update(): couldn't match up device")
                        self.msg_callback(msg_dict)
                except:
                    pass

    def handle_msg(self, msg_dict):
        if msg_dict['type'] == "send":
            port = None
            msg_to_send = None
            for d in self.devices:
                if msg_dict['device'] == (self.devices[d]['id'], self.devices[d]['port'].name):
                    port = self.devices[d]['port']
            if not port:
                print("Device not found")
                pass
            else:
                if msg_dict['device'][0] == "drt":
                    msg_to_send = self.__prepare_drt_msg(msg_dict)
                elif msg_dict['device'][0] == "vog":
                    msg_to_send = self.__prepare_vog_msg(msg_dict)
                self.__send_msg_on_port(port, msg_to_send)
        elif msg_dict['type'] == "start block":
            self.__start_block()
        elif msg_dict['type'] == "stop block":
            self.__end_block()
        elif msg_dict['type'] == "start exp":
            self.__start_exp()
        elif msg_dict['type'] == "stop exp":
            self.__end_exp()
        else:
            print("Unknown command")

    def __start_exp(self):
        for d in self.devices:
            if self.devices[d]['id'] == "vog":
                self.__send_msg_on_port(self.devices[d]['port'], ">do_expStart|<<")

    def __end_exp(self):
        for d in self.devices:
            if self.devices[d]['id'] == "vog":
                self.__send_msg_on_port(self.devices[d]['port'], ">do_expStop|<<")

    def __start_block(self):
        for d in self.devices:
            if self.devices[d]['id'] == "drt":
                self.__send_msg_on_port(self.devices[d]['port'], "exp_start\n")
            elif self.devices[d]['id'] == "vog":
                self.__send_msg_on_port(self.devices[d]['port'], ">do_trialStart|<<")

    def __end_block(self):
        for d in self.devices:
            if self.devices[d]['id'] == "drt":
                self.__send_msg_on_port(self.devices[d]['port'], "exp_stop\n")
            elif self.devices[d]['id'] == "vog":
                self.__send_msg_on_port(self.devices[d]['port'], ">do_trialStop|<<")

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
                        # TODO: Figure out the intermittent issue that comes with plugging in a device
                        # two errors at different times:
                        #   serial.serialutil.SerialException: could not open port 'COM5': FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)
                        # and
                        #   serial.serialutil.SerialException: could not open port 'COM5': PermissionError(13, 'Access is denied.', None, 5)
                        self.devices[port.device] = {'port': serial.Serial(port.device), 'id': device}
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
            msg_to_send = msg_dict['cmd'] + " " + msg_dict['arg'] + "\n"
        else:
            msg_to_send = msg_dict['cmd'] + "\n"
        return msg_to_send

    @staticmethod
    def __parse_drt_msg(msg, msg_dict):
        if msg[0:4] == "cfg>":
            msg_dict['type'] = "settings"
            # Check if this is a response to get_config
            if len(msg) > 90:
                # Get relevant values from msg and insert into msg_dict
                for i in range(0, len(defs.drt_config_fields)):
                    index = msg.find(defs.drt_config_fields[i] + ":")
                    index_len = len(defs.drt_config_fields[i]) + 1
                    val_len = msg.find(', ', index + index_len)
                    if val_len < 0:
                        val_len = None
                    msg_dict[msg[index:index+index_len-1]] = msg[index+index_len:val_len]
            else:
                # Single value update, find which value it is and insert into msg_dict
                for i in range(0, len(defs.drt_config_fields)):
                    index = msg.find(defs.drt_config_fields[i] + ":")
                    if index > 0:
                        index_len = len(defs.drt_config_fields[i])
                        val_ind = index + index_len + 1
                        msg_dict[msg[index:index + index_len]] = msg[val_ind:]
        elif msg[0:4] == "trl>":
            msg_dict['type'] = "data"
            val_ind_start = 4
            for i in range(0, len(defs.drt_trial_fields)):
                val_ind_end = msg.find(', ', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict[defs.drt_trial_fields[i]] = msg[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 2

    # TODO: test this
    @staticmethod
    def __prepare_vog_msg(msg_dict):
        if 'arg' in msg_dict.keys():
            msg_to_send = ">" + msg_dict['cmd'] + "|" + msg_dict['arg'] + "<<\n"
        else:
            msg_to_send = ">" + msg_dict['cmd'] + "|" + "<<\n"
        return msg_to_send

    # TODO: Fill this in
    @staticmethod
    def __parse_vog_msg(msg, msg_dict):
        if msg[0:5] == "data|":
            msg_dict['type'] = "data"
            val_ind_start = 5
            for i in range(len(defs.vog_block_field)):
                val_ind_end = msg.find(',', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict[defs.vog_block_field[i]] = msg[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 1
        elif msg[0:6] == "config":
            msg_dict['type'] = "settings"
            bar_ind = msg.find('|', 6)
            if msg[6:bar_ind] == "Name":
                msg_dict['Name'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "MaxOpen":
                msg_dict['MaxOpen'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "MaxClose":
                msg_dict['MaxClose'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "Debounce":
                msg_dict['Debounce'] = msg[bar_ind + 1: len(msg)]
            elif msg[6:bar_ind] == "ClickMode":
                msg_dict['ClickMode'] = msg[bar_ind + 1: len(msg)]
