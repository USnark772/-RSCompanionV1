import logging
from datetime import datetime
from time import sleep
from PySide2.QtCore import QObject, QThread, Signal
from serial import Serial, SerialException
from serial.tools import list_ports
from Model.general_defs import devices as dev_profs


class PortWorkerSig(QObject):
    new_msg_sig = Signal(str, datetime)
    cleanup_sig = Signal((str, str))


class PortWorker(QThread):
    def __init__(self, name, port):
        QThread.__init__(self)
        self.port = port
        self.device_name = name
        self.running = True
        self.signals = PortWorkerSig()

    def run(self):
        while self.running:
            # if not self.port.is_open:
            #     self.signals.disconnect_sig.emit(self.device_name, self.port.name)
            #     break
            self.__check_for_msg()
        self.cleanup()

    def __check_for_msg(self):
        try:
            if self.port.in_waiting > 0:
                the_msg = self.port.readline().decode("utf-8")
                self.signals.new_msg_sig.emit(the_msg, datetime.now())
        except Exception as e:
            self.running = False

    def send_msg(self, msg):
        self.port.write(str.encode(msg))

    def cleanup(self):
        self.running = False
        self.port.close()
        self.signals.cleanup_sig.emit(self.device_name, self.port.name)


class PortScannerSig(QObject):
    new_device_sig = Signal((str, Serial))
    disconnect_sig = Signal((str, str))
    device_connect_fail_sig = Signal()


class PortScanner(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.running = True
        self.signals = PortScannerSig()
        self.known_ports = []

    def run(self):
        while self.running:
            x = list_ports.comports()
            if len(x) > len(self.known_ports):
                self.__try_attach_devices(x)
            elif len(x) < len(self.known_ports):
                self.__check_for_disconnects(x)

    def __try_attach_devices(self, list_of_ports):
        for port in list_of_ports:
            if port not in self.known_ports:
                for profile in dev_profs:
                    if port.vid == dev_profs[profile]['vid'] and port.pid == dev_profs[profile]['pid']:
                        ret_val, new_connection = self.__try_open_port(port)
                        if ret_val:
                            self.signals.new_device_sig.emit(profile, new_connection)
                        else:
                            self.signals.device_connect_fail_sig.emit()
                self.known_ports.append(port)

    def __check_for_disconnects(self, list_of_ports):
        for known_port in self.known_ports:
            if known_port not in list_of_ports:
                self.known_ports.remove(known_port)

    @staticmethod
    def __try_open_port(port):
        new_connection = Serial()
        new_connection.port = port.device
        i = 0
        while not new_connection.is_open and i < 5:  # Make multiple attempts in case device is busy
            i += 1
            try:
                new_connection.open()
            except SerialException as e:
                sleep(1)
        if not new_connection.is_open:  # Failed to connect
            return False, None
        return True, new_connection


class DevConManSig(QObject):
    new_device_sig = Signal((str, str, classmethod))
    disconnect_sig = Signal((str, str))
    failed_con_sig = Signal()


class RSDeviceConnectionManager:
    def __init__(self, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.signals = DevConManSig()
        self.worker_thread_list = []
        self.scanner_thread = PortScanner()
        self.scanner_thread.signals.new_device_sig.connect(self.connect_port_to_thread)
        self.scanner_thread.signals.disconnect_sig.connect(self.remove_device_and_thread)
        self.scanner_thread.signals.device_connect_fail_sig.connect(self.alert_connection_failed)
        self.scanner_thread.start(priority=QThread.LowestPriority)
        self.logger.debug("Initialized")

    def cleanup(self):
        self.logger.debug("running")
        self.scanner_thread.running = False
        self.scanner_thread.wait()
        for worker in self.worker_thread_list:
            worker.running = False
            worker.wait()
        self.logger.debug("done")

    def connect_port_to_thread(self, name, port):
        self.logger.debug("running")
        new_worker = PortWorker(name, port)
        new_worker.signals.cleanup_sig.connect(self.remove_device_and_thread)
        new_worker.start()
        self.worker_thread_list.append(new_worker)
        self.signals.new_device_sig.emit(name, port.name, new_worker)
        self.logger.debug("done")

    def remove_device_and_thread(self, device_name, port_name):
        self.logger.debug("running")
        for worker in self.worker_thread_list:
            if not worker.running:
                self.worker_thread_list.remove(worker)
                worker.wait()
        self.signals.disconnect_sig.emit(device_name, port_name)
        self.logger.debug("done")

    def alert_connection_failed(self):
        self.signals.failed_con_sig.emit()
