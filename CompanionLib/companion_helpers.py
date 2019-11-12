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
from datetime import datetime, timedelta
from PySide2.QtWidgets import QFrame

logger = logging.getLogger(__name__)


def write_line_to_file(fname, line):
    logger.debug("running")
    if not line.endswith("\n"):
        line = line + "\n"
    with open(fname, 'a+') as file:
        file.write(line)
    logger.debug("done")


def check_device_tuple(device):
    return type(device[0]) == str and type(device[1]) == str


def check_dict(msg):
    return type(msg) == dict


def round_time(dt=None, round_to=60):
    """ Rounds a datetime object to the nearest round_to interval. Default round_to rounds to the nearest second"""
    logger.debug("running")
    if dt is None:
        dt = datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+round_to/2) // round_to * round_to
    logger.debug("done")
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)


def get_current_time(day=False, time=False, mil=False, save=False, graph=False, device=False):
    """
    Returns a datetime string with day, time, and milliseconds options. Also available, save is formatted for when
    colons are not acceptable and graph is for the graphing utility which requires a datetime object
    """
    logger.debug("running")
    date_time = datetime.now()
    if day and time and mil:
        logger.debug("day, time, mil. done")
        return date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    elif day and time and not mil:
        logger.debug("day, time. done")
        return date_time.strftime("%Y-%m-%d %H:%M:%S")
    elif day and not time and not mil:
        logger.debug("day. done")
        return date_time.strftime("%Y-%m-%d")
    elif not day and time and not mil:
        logger.debug("time, done")
        return date_time.strftime("%H:%M:%S")
    elif not day and time and mil:
        logger.debug("time, mil. done")
        return date_time.strftime("%H:%M:%S.%f")
    elif save:
        logger.debug("save. done")
        return date_time.strftime("%Y-%m-%d-%H-%M-%S")
    elif graph or device:
        logger.debug("graph or device. done")
        return date_time


class MyFrame(QFrame):
    """ Creates a frame for display purposes depending on bools. """
    def __init__(self, line=False, vert=False):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        super().__init__()
        if line:
            if vert:
                self.setFrameShape(QFrame.VLine)
            else:
                self.setFrameShape(QFrame.HLine)
            self.setFrameShadow(QFrame.Sunken)
        else:
            self.setFrameShape(QFrame.StyledPanel)
            self.setFrameShadow(QFrame.Raised)
        self.logger.debug("Initialized")
