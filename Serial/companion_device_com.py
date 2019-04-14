""" Contains a class for detecting changes on the serial/usb port
This class requires that a separate thread be created to call update.
When the target device is plugged in or removed the connect_event or
disconnect_event flags are turned True.
"""

import serial
from serial.tools import list_ports


class ControllerSerial:
    def __init__(self, devices, callback, msg_handler):
        # Global
        self.callback = callback
        self.msg_callback = msg_handler
        self.inc_msg = ""

        self.devices_known = []
        self.devices_attached = []
        self.devices_to_add = []
        self.devices_to_remove = []

        # Local
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
                        msg_dict = {'device': (self.devices[d]['id'], self.devices[d]['port'].name)}
                        msg_dict['msg'] = self.devices[d]['port'].readline().decode("utf-8")
                        self.msg_callback(msg_dict)
                except:
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
                        self.devices[port.device] = {'port': serial.Serial(port.device), 'id': device}
                        print("attached {} on {}".format(device, port.device))
                        self.callback((self.devices[port.device]['id'], self.devices[port.device]['port'].name), 1)
                        break
                    else:
                        self.devices[port.device] = {'id': 'unknown'}

        self.devices_known = list(self.devices.keys())

    def __remove_devices(self):

        for e in self.devices_to_remove:
            print("removed device from {}".format(e))
            if not self.devices[e]['id'] == "unknown":
                self.devices[e]['port'].close()
                self.callback((self.devices[e]['id'], self.devices[e]['port'].name), 0)
            del self.devices[e]

        self.devices_known = list(self.devices.keys())

    # TODO: format based on type of device
    def handle_msg(self, msg):
        if msg['action'] == "send":
            port = None
            for d in self.devices:
                if msg['device'] == (self.devices[d]['id'], self.devices[d]['port'].name):
                    port = self.devices[d]['port']
            if not port:
                print("Device not found")
                pass
            else:
                msg_to_send = msg['cmd'] + " " + msg['arg'] + "\n"
                print(msg_to_send)
                self.__send_msg_on_port(port, msg_to_send)
        else:
            print("Unknown command")

    def __send_msg_on_port(self, port, msg_to_send):
        port.write(str.encode(msg_to_send))
