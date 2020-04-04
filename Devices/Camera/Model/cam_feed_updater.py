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


from PySide2.QtCore import QThread, QObject, Signal
from multiprocessing.connection import Connection
from numpy import ndarray
from Model.app_helpers import take_a_moment


class FeedUpdaterSig(QObject):
    new_frame_sig = Signal(ndarray)


class FeedUpdater(QThread):
    def __init__(self, pipe: Connection):
        QThread.__init__(self)
        self.signal = FeedUpdaterSig()
        self.running = False
        self.pipe = pipe

    def run(self):
        # self.setPriority(QThread.LowPriority)
        while self.running:
            if self.pipe.poll():
                self.signal.new_frame_sig.emit(self.pipe.recv())
            else:
                take_a_moment()
