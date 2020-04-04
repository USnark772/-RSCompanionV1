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

from enum import Enum, auto
from cv2 import CAP_DSHOW, VideoWriter_fourcc


cap_backend = CAP_DSHOW
cap_temp_codec = VideoWriter_fourcc(*'mjpg')
cap_codec = VideoWriter_fourcc(*'MJPG')


list_of_common_sizes = \
    [
        (640.0, 480.0),
        (640.0, 640.0),
        (800.0, 600.0),
        (960.0, 720.0),
        (1024.0, 768.0),
        (1248.0, 1536.0),
        (1280.0, 720.0),
        (1280.0, 960.0),
        (1440.0, 1080.0),
        (1600.0, 900.0),
        (1600.0, 1200.0),
        (1920.0, 1080.0),
        # (2048.0, 1536.0),
        # (2560.0, 1440.0),
        # (3840.0, 2160.0),
    ]


class CEnum(Enum):
    WORKER_MAX_TRIES = auto()
    WORKER_STATUS_UPDATE = auto()
    WORKER_DONE = auto()
    SAVE_STATUS_UPDATE = auto()
    CAM_FAILED = auto()
    OPEN_SETTINGS = auto()
    GET_RESOLUTION = auto()
    SET_RESOLUTION = auto()
    GET_FPS = auto()
    SET_FPS = auto()
    FPS_UPDATE = auto()
    GET_BW = auto()
    SET_BW = auto()
    GET_ROTATION = auto()
    SET_ROTATION = auto()
    ACTIVATE_CAM = auto()
    DEACTIVATE_CAM = auto()
    SHOW_FEED = auto()
    HIDE_FEED = auto()
    START_SAVING = auto()
    STOP_SAVING = auto()
    NEW_FRAME = auto()
    TOTAL_SECONDS = auto()
    CLEANUP = auto()

