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
# Date: 2020
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html


from multiprocessing.connection import Connection
from PySide2.QtCore import QObject, QThread, Signal


class PipeWatcherSig(QObject):
    new_msg_sig = Signal(tuple)


class PipeWatcher(QThread):
    def __init__(self, pipe: Connection):
        QThread.__init__(self)
        self.setPriority(QThread.LowPriority)
        self.pipe = pipe
        self.signal = PipeWatcherSig()
        self.running = True

    def run(self):
        while self.running:
            waiting = self.pipe.poll()
            if waiting:
                self.signal.new_msg_sig.emit(self.pipe.recv())

    def connect_to_sig(self, func: classmethod):
        self.signal.new_msg_sig.connect(func)
