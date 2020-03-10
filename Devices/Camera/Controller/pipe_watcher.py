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

import logging
from multiprocessing.connection import Connection
from PySide2.QtCore import QObject, QThread, Signal
from CompanionLib.companion_helpers import take_a_moment


class PipeWatcherSig(QObject):
    new_msg_sig = Signal()


class PipeWatcher(QThread):
    def __init__(self, pipe: Connection, ch: logging.Handler):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(ch)
        self.logger.debug("Initializing")
        QThread.__init__(self)
        self.setPriority(QThread.LowPriority)
        self.pipe = pipe
        self.signal = PipeWatcherSig()
        self.running = True
        self.logger.debug("Initialized")

    def run(self):
        self.logger.debug("running")
        while self.running:
            take_a_moment()
            try:
                waiting = self.pipe.poll()
                if waiting:
                    self.signal.new_msg_sig.emit()
            except BrokenPipeError as e:
                self.logger.exception("Pipe failed")
                break
        self.logger.debug("done")

    def connect_to_sig(self, func: classmethod):
        self.signal.new_msg_sig.connect(func)

    def send_msg(self, msg):
        self.pipe.send(msg)
