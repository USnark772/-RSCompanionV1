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


def set_file_playback_speed(from_file_name: str, to_file_name: str, total_secs: float, cleanup: bool) -> bool:
    # to_continue('About to create from_file VideoCapture object using file name: ' + str(from_file_name))
    from_file = VideoCapture(from_file_name)
    if not from_file.isOpened():
        # to_continue('Invalid file.')
        return False
    # to_continue('Successful creation of from_file object')
    from_res = (int(from_file.get(CAP_PROP_FRAME_WIDTH)), int(from_file.get(CAP_PROP_FRAME_HEIGHT)))
    total_frames = from_file.get(CAP_PROP_FRAME_COUNT)
    actual_fps = total_frames / total_secs
    # to_continue('About to create to_file VideoWriter object using file name: ' + str(to_file_name) + ', fps: ' + str(actual_fps) + ', screen size: ' + str(from_res))
    to_file = VideoWriter(to_file_name, cap_codec, actual_fps, from_res)
    to_file.set(CAP_PROP_FRAME_WIDTH, from_res[0])
    to_file.set(CAP_PROP_FRAME_HEIGHT, from_res[1])
    # to_continue('Successful creation of to_file object')
    try:
        ret, frame = from_file.read()
        while ret and frame is not None:
            to_file.write(frame)
            ret, frame = from_file.read()
    except Exception as e:
        # to_continue(str(e))
        # to_continue('except statement: releasing from_file and to_file')
        from_file.release()
        to_file.release()
        # to_continue('about to remove(' + str(to_file_name) + ')')
        try:
            remove(to_file_name)
        except Exception as e:
            # to_continue(str(e))
            pass
        # to_continue('done with except statement, about to return.')
        return False
    from_file.release()
    to_file.release()
    if cleanup:
        # to_continue('about to remove(' + str(from_file_name) + ')')
        try:
            remove(from_file_name)
        except Exception as e:
            # to_continue(str(e))
            pass
    # to_continue('Success')
    return True


def to_continue(usr_msg: str = None):
    default = 'Press enter to continue:'
    if usr_msg:
        if not usr_msg.endswith('.'):
            msg = usr_msg + '. ' + default
        else:
            msg = usr_msg + ' ' + default
    else:
        msg = default
    input(msg)


def main():
    from_file: str = ''
    to_file: str = ''
    total_secs: float = 0.0
    cleanup: bool = False
    # to_continue()
    failure = False
    try:
        from_file = argv[1]
    except Exception as e:
        # to_continue(str(e))
        failure = True
    try:
        to_file = argv[2]
    except Exception as e:
        # to_continue(str(e))
        failure = True
    try:
        total_secs = float(argv[3])
    except Exception as e:
        # to_continue(str(e))
        failure = True
    try:
        cleanup = eval(argv[4])
    except Exception as e:
        # to_continue(str(e))
        failure = True
    if failure:
        # to_continue('Failure loading args')
        return
    # to_continue('success loading args')
    print(from_file, '\n', to_file, '\n', total_secs, '\n', cleanup)
    # to_continue()
    print(type(from_file), type(to_file), type(total_secs), type(cleanup))
    # to_continue()
    try:
        set_file_playback_speed(from_file, to_file, total_secs, cleanup)
        # to_continue()
    except Exception as e:
        # to_continue(str(e))
        pass


if __name__ == '__main__':
    main()
