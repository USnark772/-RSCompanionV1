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
# Date: 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

""" 
Contains a class for detecting changes on the serial/usb port
This class requires that a separate thread be created to call update.
When the target device is plugged in or removed the connect_event or
disconnect_event flags are turned True.
"""

import queue
from time import sleep
from datetime import datetime
import logging
import threading
from PySide2.QtCore import QTimer
from serial import Serial, SerialException
from serial.tools import list_ports
from Model.general_defs import devices


# TODO: Try threading each device connection. Maybe use signals to add/remove devices and get data from devices instead
#  of a timer.
class PortMonitor(threading.Thread):
    def __init__(self, port, devices_list, lock):
        threading.Thread.__init__(self, daemon=True)
        self.devices_list = devices_list
        self.lock = lock
        self.port = port
        self.timer = QTimer()
        self.going = True

    def run(self):
        while self.going:
            sleep(1)
            self.check_port()

    def check_port(self):
        if not self.port.is_open:
            self.lock.aquire_write()
            self.devices_list.remove_port(self.port)
            self.lock.release_write()
            self.going = False


class PortScanner(threading.Thread):
    def __init__(self, the_queue):
        threading.Thread.__init__(self, daemon=True)
        self.queue = the_queue

    def run(self):
        while True:
            x = list_ports.comports()
            self.queue.put(x)


class DeviceManager:
    def __init__(self, msg_handler, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")

        self.msg_callback = msg_handler

        self.devices_known = []
        self.devices_attached = []
        self.devices_to_add = []
        self.devices_to_remove = []
        self.num_comports = 0
        self.profiles = devices
        self.devices_map = dict()
        self.check_for_updates = True
        self.logger.debug("Initialized")
        self.comports_queue = queue.Queue(maxsize=1)
        self.scanner_thread = PortScanner(self.comports_queue)
        self.scanner_thread.start()

    def check_for_msgs(self):
        #self.logger.debug("running")
        need_update = False
        for d in self.devices_map:
            the_message = None
            device_info = None
            device = self.devices_map[d]
            try:
                if 'port' in self.devices_map[d].keys() and device['port'].in_waiting > 0:
                    the_message = device['port'].readline().decode("utf-8")
                    self.logger.info(str(device['id'] + ", " + device['port'].name + ", " + the_message))
                    device_info = (device['id'], device['port'].name)
            except SerialException as se:
                # self.logger.exception("Trouble with port")
                need_update = True
                continue
            except Exception as e:
                self.logger.exception("Failed try catch in check_for_msgs() for loop.")
                continue

            if the_message and device_info:
                self.logger.debug("msg_callback(1, the_message, device_info) msg_dict: " + the_message)
                self.msg_callback(1, the_message, datetime.now(), device_info)
        if need_update:
            self.update_devices(True)
            sleep(.1)
        #self.logger.debug("done")

    def update_devices(self, override=False):
        #self.logger.debug("running")
        if not override and not self.check_for_updates:
            return
        self.__scan_ports()

        if len(self.devices_to_add) != 0:
            self.__attach_devices()
        elif len(self.devices_to_remove) != 0:
            self.__remove_devices()
        #self.logger.debug("done")

    def handle_msg(self, device=None, msg=None):
        """ Parse message from controller and attempt to pass to device specified in dictionary. If error do nothing."""
        self.logger.debug("running")
        port = None
        if not type(device) == tuple or not type(msg) == str:
            self.logger.error("function called without proper args. type(device): " + str(type(device))
                              + " expected tuple. type(msg): " + str(type(msg)) + " expected string")
        else:
            for d in self.devices_map:
                if 'port' in self.devices_map[d].keys() and device == \
                        (self.devices_map[d]['id'], self.devices_map[d]['port'].name):
                    port = self.devices_map[d]['port']
                    self.logger.debug("Have port")
            if not port:
                self.logger.debug("Device not found")
            else:
                self.__send_msg_on_port(port, msg)
        self.logger.debug("done")

    def set_check_for_updates(self, check_bool):
        self.check_for_updates = check_bool

    def __scan_ports(self):
        """ Go through list of ports and get set of attached devices. """
        #self.logger.debug("running")
        devices_known = list(self.devices_map.keys())

        self.devices_to_add = []
        self.devices_to_remove = []
        self.devices_attached = []

        try:
            x = self.comports_queue.get(block=False)
        except Exception as e:
            x = []
        for port in x:
            self.devices_attached.append(port.device)

        if len(devices_known) == 0:
            self.devices_to_add = self.devices_attached
        elif len(devices_known) < len(self.devices_attached):
            self.devices_to_add = list(set(self.devices_attached) - set(devices_known))
        elif len(devices_known) > len(self.devices_attached):
            self.devices_to_remove = list(set(devices_known) - set(self.devices_attached))
        #self.logger.debug("done")

    def __attach_devices(self):
        """ Go through list of attached devices and attach each device to app if it is known. """
        self.logger.debug("running")
        for port in list_ports.comports():
            if port.device in self.devices_to_add:
                for device in self.profiles:
                    if port.vid == self.profiles[device]['vid'] and port.pid == self.profiles[device]['pid']:
                        the_port = Serial()
                        the_port.port = port.device
                        i = 0
                        while not the_port.is_open and i < 5:  # Make multiple attempts in case device is busy
                            self.logger.debug("Attempt " + str(i + 1) + " of 5 to connect to device: " + device)
                            i += 1
                            try:
                                the_port.open()
                            except SerialException as e:
                                sleep(1)
                        if not the_port.is_open:
                            self.logger.debug("Failed to connect to device")
                            self.msg_callback(4)
                            break
                        self.devices_map[port.device] = {'port': the_port, 'id': device}
                        #msg_dict = {'type': "add", 'device': (self.devices_map[port.device]['id'], self.devices_map[port.device]['port'].name)}
                        self.logger.debug("done, known device")
                        self.msg_callback(2, device=(self.devices_map[port.device]['id'], self.devices_map[port.device]['port'].name))
                        break
                    else:
                        self.logger.debug("done, unknown device")
                        self.devices_map[port.device] = {'id': 'unknown'}
        self.logger.debug("done")

    def __remove_devices(self):
        """ Go through list of attached devices and alert controller of devices that have been unplugged. """
        self.logger.debug("running")
        for e in self.devices_to_remove:
            if not self.devices_map[e]['id'] == "unknown":
                self.devices_map[e]['port'].close()
                #msg_dict = {'type': "remove", 'device': (self.devices_map[e]['id'], self.devices_map[e]['port'].name)}
                self.msg_callback(3, device=(self.devices_map[e]['id'], self.devices_map[e]['port'].name))
            del self.devices_map[e]
        self.logger.debug("done")

    def __send_msg_on_port(self, port, msg_to_send):
        self.logger.debug("running")
        port.write(str.encode(msg_to_send))
        self.logger.debug("done")
