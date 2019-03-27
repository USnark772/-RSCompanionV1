""" Contains a class for detecting changes on the serial/usb port
This class requires that a separate thread be created to call update.
When the target device is plugged in or removed the connect_event or
disconnect_event flags are turned True.
"""

import serial
from serial.tools import list_ports
import time
import configparser

CONNECT_MESSAGE = 'connect'
DISCONNECT_MESSAGE = 'disconnect'

class ControllerSerial:
    def __init__(self, name, callback):
        # Load config
        self.config = configparser.ConfigParser()
        self.config.read('serial_config.ini')

        self.port_timeout = float(self.config['DEFAULT']['PORT_TIMEOUT'])
        self.wait_send = float(self.config['DEFAULT']['WAIT_SEND'])
        self.wait_reply = float(self.config['DEFAULT']['WAIT_REPLY'])

        # Global
        self.callback = callback
        self.inc_msg = ""

        # Local
        self.name = name

        # Port object
        self.port = serial.Serial()
        self.port.timeout = self.port_timeout
        self.ports_old = []


    def update(self):

        """ This needs to be called from an external loop that also controls the port
         All serial related functions must be on a single thread to avoid cross talk """
        plug_event, unplug_event = self.__connect_events()  # probe plug/unplug events

        # if device was unplugged, was it the one we care about?
        if plug_event:
            ours = self.__ours_inserted()
            if ours:
                self.callback('{} {} on {}'.format(CONNECT_MESSAGE, self.name['name'], self.port.name))

        # device unplugged, was it ours?
        if unplug_event:
            ours = self.__ours_removed()
            if ours:
                self.callback('{} {}'.format(DISCONNECT_MESSAGE, self.name['name']))


    def __connect_events(self):
        """ Uses the ports_list to look for changes in status over time"""
        plug_event = False
        unplug_event = False

        ports_new = list_ports.comports()
        change = self.ports_old != ports_new
        plug_in = len(self.ports_old) < len(ports_new)

        if change and plug_in:
            plug_event = True
        elif change and not plug_in:
            unplug_event = True

        self.ports_old = ports_new

        return plug_event, unplug_event

    def __ours_inserted(self):
        """ Checks to see if the device that was just connected is a target device"""
        device_inserted = False

        if self.port.port is None:  # If there is no active device, look for it
            for port in list_ports.comports():
                try:

                    self.port.setPort(port[0])  # set up the port
                    msg = str.encode(self.name['probe'])

                    self.port.open()
                    time.sleep(self.wait_send)
                    self.port.write(msg)
                    time.sleep(self.wait_reply)
                    self.inc_msg = self.port.readline()

                    if self.name['key'] in str(self.inc_msg):  # if the reply fits our key, the we found a device!
                        device_inserted = True
                        break
                    else:
                        pass
                        self.__close_port()
                except:
                    self.inc_msg = ""

        return device_inserted

    def __ours_removed(self):
        """This method is called if an unplug event has been detected in the main loop"""
        device_removed = True

        if self.port.port is not None:  # If the device was/is attached
            if not list_ports.comports():  # If nothing is currently plugged in
                self.__close_port()
            else:  # if something is still plugged in, check to see if it is our device
                for port in list_ports.comports():
                    if self.port.port == port[0]:
                        device_removed = False  # our device was found
                if device_removed:
                    self.__close_port()
        return device_removed

    def __close_port(self):
        self.port.close()
        self.port.setPort(None)

