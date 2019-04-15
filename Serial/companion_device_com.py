""" Contains a class for detecting changes on the serial/usb port
This class requires that a separate thread be created to call update.
When the target device is plugged in or removed the connect_event or
disconnect_event flags are turned True.
"""

import serial
from serial.tools import list_ports
import Serial.companion_defs as defs


class ControllerSerial:
    def __init__(self, callback, msg_handler):
        # Global
        self.callback = callback
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

    # TODO: format based on type of device
    def handle_msg(self, msg):
        #if msg['device'][0] == "drt":
        #    self.__prepare_msg_for_drt(msg)
        if msg['type'] == "send":
            port = None
            for d in self.devices:
                if msg['device'] == (self.devices[d]['id'], self.devices[d]['port'].name):
                    port = self.devices[d]['port']
            if not port:
                print("Device not found")
                pass
            else:
                if 'arg' in msg.keys():
                    msg_to_send = msg['cmd'] + " " + msg['arg'] + "\n"
                else:
                    msg_to_send = msg['cmd'] + "\n"
                self.__send_msg_on_port(port, msg_to_send)
        else:
            print("Unknown command")

    def __prepare_msg_for_drt(self, msg_dict):
        pass

    def __parse_drt_msg(self, msg, msg_dict):
        if msg[0:4] == "cfg>":
            msg_dict['type'] = "cfg"
            # Check if this is a response to get_config
            if len(msg) > 90:
                # Get relevant values from msg and insert into msg_dict
                for i in range(0, len(defs.drt_config_fields)):
                    index = msg.find(defs.drt_config_fields[i] + ":")
                    index_len = len(defs.drt_config_fields[i])+1
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
            msg_dict['type'] = "trl"
            val_ind_start = 4
            for i in range(0, len(defs.drt_trial_fields)):
                val_ind_end = msg.find(', ', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict[defs.drt_trial_fields[i]] = msg[val_ind_start:val_ind_end]

    def __parse_vog_msg(self, msg, msg_dict):
        pass

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
                        #print("attached {} on {}".format(device, port.device))
                        self.callback((self.devices[port.device]['id'], self.devices[port.device]['port'].name), 1)
                        break
                    else:
                        self.devices[port.device] = {'id': 'unknown'}

        self.devices_known = list(self.devices.keys())

    def __remove_devices(self):

        for e in self.devices_to_remove:
            #print("removed device from {}".format(e))
            if not self.devices[e]['id'] == "unknown":
                self.devices[e]['port'].close()
                self.callback((self.devices[e]['id'], self.devices[e]['port'].name), 0)
            del self.devices[e]

        self.devices_known = list(self.devices.keys())

    def __send_msg_on_port(self, port, msg_to_send):
        port.write(str.encode(msg_to_send))
