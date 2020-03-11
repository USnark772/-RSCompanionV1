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

import logging
from psutil import cpu_percent, cpu_count
from PySide2.QtCore import QThread, Signal, QObject
from CompanionLib.companion_helpers import take_a_moment


class CPUWatcherSig(QObject):
    update_sig = Signal(list)


class CPUWatcher(QThread):
    def __init__(self, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__()
        self.signal = CPUWatcherSig()
        self.setPriority(QThread.LowestPriority)
        self.running = True
        self.logger.debug("Initialized")

    def run(self):
        self.logger.debug("running")
        while self.running:
            perc_list = cpu_percent(percpu=True)
            perc_list.append(cpu_percent())
            self.signal.update_sig.emit(perc_list)
            take_a_moment(.2)
        self.logger.debug("done")


class DiskWatcherSig(QObject):
    update_sig = Signal(list)


class DiskWatcher(QThread):
    def __init__(self, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__()
        self.signal = DiskWatcherSig()
        self.setPriority(QThread.LowestPriority)
        self.running = True
        self.logger.debug("Initialized")

    def run(self):
        self.logger.debug("running")
        while self.running:
            # TODO: Replace with disk_io_counters()
            # perc = cpu_percent(percpu=True)
            # perc.append(cpu_percent())
            self.signal.update_sig.emit(perc_lst)
            take_a_moment(.2)
        self.logger.debug("done")


class MonitorSig(QObject):
    update_sig = Signal(list)


class ResourceMonitor:
    def __init__(self, ch, max_vals: int = 20):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        self.signal = MonitorSig()
        self.cpu_watcher = CPUWatcher(ch)
        self.cpu_watcher.signal.update_sig.connect(self.update_cpu_values)
        self.values = []
        for i in range(cpu_count() + 1):
            self.values.append([])
        self.max_values = max_vals
        self.cpu_watcher.start()
        self.logger.debug("Initialized")

    def __update_cpu_value_array(self, values):
        for b in range(len(values)):
            self.values[b].append(values[b])
            if len(self.values[b]) > self.max_values:
                del(self.values[b][0])

    def update_cpu_values(self, values):
        self.__update_cpu_value_array(values)
        ret = []
        for a in range(len(self.values) - 1):
            if len(self.values[a]) > 0:
                val = int(sum(self.values[a]) / len(self.values[a]))
            else:
                val = 0
            ret.append(val)
        j = len(self.values) - 1
        ret.append(sum(self.values[j]) / len(self.values[j]))
        self.signal.update_sig.emit(ret)

    def cleanup(self):
        self.cpu_watcher.running = False
        self.cpu_watcher.wait()
