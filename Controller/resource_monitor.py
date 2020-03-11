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


class WatcherSig(QObject):
    update_sig = Signal(list)


class ResourceWatcher(QThread):
    def __init__(self, ch):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        super().__init__()
        self.signal = WatcherSig()
        self.setPriority(QThread.LowestPriority)
        self.running = True
        self.logger.debug("Initialized")

    def run(self):
        self.logger.debug("running")
        while self.running:
            perc = cpu_percent(percpu=True)
            self.signal.update_sig.emit(perc)
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
        self.watcher = ResourceWatcher(ch)
        self.watcher.signal.update_sig.connect(self.update)
        self.values = []
        for i in range(cpu_count()):
            self.values.append([])
        self.max_values = max_vals
        self.watcher.start()
        self.logger.debug("Initialized")

    def __update_value_array(self, values):
        for b in range(len(values)):
            self.values[b].append(values[b])
            if len(self.values[b]) > self.max_values:
                del(self.values[b][0])

    def update(self, value):
        self.__update_value_array(value)
        ret = []
        for a in range(len(self.values)):
            if len(self.values[a]) > 0:
                val = int(sum(self.values[a]) / len(self.values[a]))
            else:
                val = 0
            ret.append(val)
        self.signal.update_sig.emit(ret)

    def cleanup(self):
        self.watcher.running = False
        self.watcher.wait()
