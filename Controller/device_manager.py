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

from time import sleep
import logging
import threading
from PySide2.QtCore import QTimer
import CompanionLib.checkers as checker
from serial import Serial, SerialException
from serial.tools import list_ports
from Model.general_defs import devices
from Devices.DRT.Model.drt_defs import drtv1_0_config_fields, drtv1_0_output_fields
from Devices.VOG.Model.vog_defs import vog_output_field


class ReadWriteLock:
    """ A lock object that allows many simultaneous "read locks", but
    only one "write lock." """
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release()


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


class PortMap:
    def __init__(self):
        self.devices = dict()

    def add_device(self, key, port):
        self.devices[key] = port

    def remove_device(self, key, port):
        del self.devices[key]


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
        self.rs_devices = dict()
        self.logger.debug("Initialized")

    def check_for_msgs(self):
        #self.logger.debug("running")
        need_update = False
        the_message = None
        msg_dict = None
        for d in self.devices_map:
            device = self.devices_map[d]
            try:
                if device['port'].in_waiting > 0:
                    the_message = device['port'].readline().decode("utf-8")
                    self.logger.info(str(device['id'] + ", " + device['port'].name + ", " + the_message))
                    msg_dict = {'device': (device['id'], device['port'].name)}
            except SerialException as se:
                # self.logger.exception("Trouble with port")
                need_update = True
                continue
            except Exception as e:
                self.logger.exception("Failed try catch in update() for loop.")
                continue

            if the_message:
                if self.devices_map[d]['id'] == "drt":
                    self.__parse_drt_msg(the_message, msg_dict)
                elif self.devices_map[d]['id'] == "vog":
                    self.__parse_vog_msg(the_message, msg_dict)
                else:
                    self.logger.info("couldn't match up device" + str(self.devices_map[d]['id']))
                self.logger.debug("msg_callback(msg_dict) msg_dict: " + str(msg_dict))
                self.msg_callback(msg_dict)
        if need_update:
            self.update_devices()
        #self.logger.debug("done")

    def update_devices(self):
        #self.logger.debug("running")
        self.__scan_ports()

        if len(self.devices_to_add) != 0:
            self.__attach_devices()
        elif len(self.devices_to_remove) != 0:
            self.__remove_devices()
        #self.logger.debug("done")

    def handle_msg(self, msg_dict):
        """ Parse message from controller and attempt to pass to device specified in dictionary. If error do nothing."""
        self.logger.debug("running")
        if not checker.check_dict(msg_dict):
            self.logger.warning("expected dictionary, got: " + str(type(msg_dict)))
            return
        if 'type' not in msg_dict.keys():
            self.logger.warning("'type' not found in keys")
            return
        if 'device' not in msg_dict.keys():
            self.logger.warning("'device' not found in keys")
            return
        msg_type = msg_dict['type']
        if msg_type == "send":
            port = None
            msg_to_send = None
            for d in self.devices_map:
                if 'port' in self.devices_map[d].keys() and msg_dict['device'] == \
                        (self.devices_map[d]['id'], self.devices_map[d]['port'].name):
                    port = self.devices_map[d]['port']
                    self.logger.debug("Have port")
            if not port:
                self.logger.debug("Device not found")
                pass
            else:
                if msg_dict['device'][0] == "drt":
                    msg_to_send = self.__prepare_drt_msg(msg_dict)
                elif msg_dict['device'][0] == "vog":
                    msg_to_send = self.__prepare_vog_msg(msg_dict)
                self.logger.info("Sending message " + msg_to_send)
                self.__send_msg_on_port(port, msg_to_send)
        else:
            self.logger.debug("Unknown command")
        self.logger.debug("done")

    def start_exp_all(self):
        """ Send start experiment messages to all devices. """
        self.logger.debug("running")
        for d in self.devices_map:

            # Com1 has no device attribute 'port' - This error fails
            # Rather than asking if the device is a VOG, each device should have an experiment start command.
            # If there is no experiment start command then nothing should happen
            if 'port' in self.devices_map[d].keys():
                self.__start_exp(self.devices_map[d]['id'], self.devices_map[d]['port'])

        self.logger.debug("done")

    def end_exp_all(self):
        """ Send end experiment messages to all devices. """
        self.logger.debug("running")
        for d in self.devices_map:
            if 'port' in self.devices_map[d].keys():
                self.__end_exp(self.devices_map[d]['id'], self.devices_map[d]['port'])
        self.logger.debug("done")

    def start_block_all(self):
        """ Send start block messages to all devices. """
        self.logger.debug("running")
        for d in self.devices_map:
            #print("Checking device: ", self.devices[d]['id'])
            if 'port' in self.devices_map[d].keys():
                #print("calling start block for: ", self.devices[d]['id'])
                self.__start_block(self.devices_map[d]['id'], self.devices_map[d]['port'])
        self.logger.debug("done")

    def end_block_all(self):
        """ Send end block messages to all devices. """
        self.logger.debug("running")
        for d in self.devices_map:
            if 'port' in self.devices_map[d].keys():
                self.__end_block(self.devices_map[d]['id'], self.devices_map[d]['port'])
        self.logger.debug("done")

    def __start_exp(self, device, port):
        """ If device needs a start experiment message, send it. """
        self.logger.debug("running")
        if device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_expStart"}))
        self.logger.debug("done")

    def __end_exp(self, device, port):
        """ If device needs a stop experiment message, send it. """
        self.logger.debug("running")
        if device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_expStop"}))
        self.logger.debug("done")

    def __start_block(self, device, port):
        """ If device needs a start block message, send it. """
        self.logger.debug("running")
        if device == "drt":
            self.__send_msg_on_port(port, self.__prepare_drt_msg({'cmd': "exp_start"}))
        elif device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_trialStart"}))
        self.logger.debug("done")

    def __end_block(self, device, port):
        """ If device needs a stop block message, send it. """
        self.logger.debug("running")
        if device == "drt":
            self.__send_msg_on_port(port, self.__prepare_drt_msg({'cmd': "exp_stop"}))
        elif device == "vog":
            self.__send_msg_on_port(port, self.__prepare_vog_msg({'cmd': "do_trialStop"}))
        self.logger.debug("done")

    def __scan_ports(self):
        """ Go through list of ports and get set of attached devices. """
        #self.logger.debug("running")
        devices_known = list(self.devices_map.keys())
        self.devices_to_add = []
        self.devices_to_remove = []
        self.devices_attached = []

        for port in list_ports.comports():
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
                            i += 1
                            try:
                                the_port.open()
                            except SerialException as e:
                                sleep(1)
                        if not the_port.is_open:
                            self.logger.debug("Failed to connect to device")
                            self.msg_callback({'type': "error"})
                            break
                        self.devices_map[port.device] = {'port': the_port, 'id': device}
                        msg_dict = {'type': "add", 'device': (self.devices_map[port.device]['id'], self.devices_map[port.device]['port'].name)}
                        self.logger.debug("done, known device")
                        self.msg_callback(msg_dict)
                        break
                    else:
                        self.logger.debug("done, unkown device")
                        self.devices_map[port.device] = {'id': 'unknown'}
        self.logger.debug("done")

    def __remove_devices(self):
        """ Go through list of attached devices and alert controller of devices that have been unplugged. """
        self.logger.debug("running")
        for e in self.devices_to_remove:
            if not self.devices_map[e]['id'] == "unknown":
                self.devices_map[e]['port'].close()
                msg_dict = {'type': "remove", 'device': (self.devices_map[e]['id'], self.devices_map[e]['port'].name)}
                self.msg_callback(msg_dict)
            del self.devices_map[e]
        self.logger.debug("done")

    def __send_msg_on_port(self, port, msg_to_send):
        self.logger.debug("running")
        port.write(str.encode(msg_to_send))
        self.logger.debug("done")

    def __prepare_drt_msg(self, msg_dict):
        """ Create string using drt syntax. """
        self.logger.debug("running")
        if 'arg' in msg_dict.keys():
            msg_to_send = msg_dict['cmd'] + " " + str(msg_dict['arg']) + "\n"
        else:
            msg_to_send = msg_dict['cmd'] + "\n"
        self.logger.debug("done, returning: " + msg_to_send)
        return msg_to_send

    # TODO: Clean this up
    def __parse_drt_msg(self, msg, msg_dict):
        self.logger.debug("running")
        msg_dict['values'] = {}
        if msg[0:4] == "cfg>":
            msg_dict['type'] = "settings"
            # Check if this is a response to get_config
            if len(msg) > 90:
                # Get relevant values from msg and insert into msg_dict
                for i in drtv1_0_config_fields:
                    index = msg.find(i + ":")
                    index_len = len(i) + 1
                    val_len = msg.find(', ', index + index_len)
                    if val_len < 0:
                        val_len = None
                    msg_dict['values'][msg[index:index+index_len-1]] = int(msg[index+index_len:val_len])
            else:
                # Single value update, find which value it is and insert into msg_dict
                for i in drtv1_0_config_fields:
                    index = msg.find(i + ":")
                    if index > 0:
                        index_len = len(i)
                        val_ind = index + index_len + 1
                        msg_dict['values'][msg[index:index + index_len]] = int(msg[val_ind:])
        elif msg[0:4] == "trl>":
            msg_dict['type'] = "data"
            val_ind_start = 4
            for i in drtv1_0_output_fields:
                val_ind_end = msg.find(', ', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict['values'][i] = int(msg[val_ind_start:val_ind_end])
                if val_ind_end:
                    val_ind_start = val_ind_end + 2
        self.logger.debug("done")

    def __prepare_vog_msg(self, msg_dict):
        """ Create string using vog syntax. """
        if 'arg' in msg_dict.keys():
            msg_to_send = ">" + msg_dict['cmd'] + "|" + str(msg_dict['arg']) + "<<\n"
        else:
            msg_to_send = ">" + msg_dict['cmd'] + "|" + "<<\n"
        self.logger.debug("done, returning: " + msg_to_send)
        return msg_to_send

    # TODO: Clean this up
    def __parse_vog_msg(self, msg, msg_dict):
        self.logger.debug("running")
        #print("in parse_vog_msg", msg, msg_dict)
        msg_dict['values'] = {}
        if msg[0:5] == "data|":
            msg_dict['type'] = "data"
            val_ind_start = 5
            for i in range(len(vog_output_field)):
                val_ind_end = msg.find(',', val_ind_start + 1)
                if val_ind_end < 0:
                    val_ind_end = None
                msg_dict['values'][vog_output_field[i]] = msg[val_ind_start:val_ind_end]
                if val_ind_end:
                    val_ind_start = val_ind_end + 1
        elif "config" in msg:
            msg_dict['type'] = "settings"
            bar_ind = msg.find('|', 6)
            if msg[6:bar_ind] == "Name":
                msg_dict['values']['Name'] = msg[bar_ind + 1: len(msg)].rstrip("\r\n")
            elif msg[6:bar_ind] == "MaxOpen":
                msg_dict['values']['MaxOpen'] = msg[bar_ind + 1: len(msg)].rstrip("\r\n")
            elif msg[6:bar_ind] == "MaxClose":
                msg_dict['values']['MaxClose'] = msg[bar_ind + 1: len(msg)].rstrip("\r\n")
            elif msg[6:bar_ind] == "Debounce":
                msg_dict['values']['Debounce'] = msg[bar_ind + 1: len(msg)].rstrip("\r\n")
            elif msg[6:bar_ind] == "ClickMode":
                msg_dict['values']['ClickMode'] = msg[bar_ind + 1: len(msg)].rstrip("\r\n")
        elif "Click" in msg:
            msg_dict['action'] = "Click"
        elif "buttonControl" in msg:
            msg_dict['type'] = "settings"
            bar_ind = msg.find('|')
            msg_dict['values'] = {}
            msg_dict['values']['buttonControl'] = msg[bar_ind + 1: len(msg)].rstrip("\r\n")
        elif "peek" in msg:
            msg_dict['type'] = "settings"
            msg_dict['values'] = {}
            msg_dict['values']['lensState'] = msg.rstrip("\r\n")
        #print("at end of parse_vog_msg.", msg_dict, "\n")
        self.logger.debug("done")
