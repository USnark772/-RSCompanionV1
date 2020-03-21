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


from sys import argv
from os import remove
from cv2 import VideoCapture, VideoWriter, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_COUNT
from Model.general_defs import cap_codec


# TODO: If app is closed during this, check with user if they really want to close and then just cut.
#  Else if no, then finish work and leave open
#  Else if end exp, show progress of this.
def set_file_playback_speed(from_file_name: str, to_file_name: str, total_secs: float, cleanup: bool) -> bool:
    from_file = VideoCapture(from_file_name)
    if not from_file.isOpened():
        return False
    from_res = (int(from_file.get(CAP_PROP_FRAME_WIDTH)), int(from_file.get(CAP_PROP_FRAME_HEIGHT)))
    total_frames = from_file.get(CAP_PROP_FRAME_COUNT)
    actual_fps = total_frames / total_secs
    to_file = VideoWriter(to_file_name, cap_codec, actual_fps, from_res)
    to_file.set(CAP_PROP_FRAME_WIDTH, from_res[0])
    to_file.set(CAP_PROP_FRAME_HEIGHT, from_res[1])
    try:
        ret, frame = from_file.read()
        while ret and frame is not None:
            to_file.write(frame)
            ret, frame = from_file.read()
    except Exception as e:
        from_file.release()
        to_file.release()
        try:
            remove(to_file_name)
        except Exception as e:
            pass
        return False
    from_file.release()
    to_file.release()
    if cleanup:
        try:
            remove(from_file_name)
        except Exception as e:
            pass
    return True


def main():
    from_file: str = ''
    to_file: str = ''
    total_secs: float = 0.0
    cleanup: bool = False
    if len(argv) == 5:
        try:
            from_file = argv[1]
            to_file = argv[2]
            total_secs = float(argv[3])
            cleanup = eval(argv[4])
        except Exception as e:
            return
    try:
        set_file_playback_speed(from_file, to_file, total_secs, cleanup)
    except Exception as e:
        pass


if __name__ == '__main__':
    main()
