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


from PySide2.QtCore import Signal, QObject, QThread
from os import remove
from cv2 import VideoCapture, VideoWriter, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_COUNT
from Model.general_defs import cap_codec


class FileFixerSig(QObject):
    update_sig = Signal(int, int)
    done_sig = Signal(bool)


class FileFixer(QThread):
    def __init__(self, from_file: str, to_file: str, total_seconds: int, cleanup: bool):
        QThread.__init__(self)
        self.signal = FileFixerSig()
        self.from_file = from_file
        self.to_file = to_file
        self.seconds = total_seconds
        self.cleanup = cleanup
        self.running = True

    def run(self):
        self.setPriority(QThread.HighestPriority)
        from_file = VideoCapture(self.from_file)
        if not from_file.isOpened():
            self.signal.done_sig.emit(False)
            return
        from_res = (int(from_file.get(CAP_PROP_FRAME_WIDTH)), int(from_file.get(CAP_PROP_FRAME_HEIGHT)))
        total_frames = from_file.get(CAP_PROP_FRAME_COUNT)
        actual_fps = total_frames / self.seconds
        to_file = VideoWriter(self.to_file, cap_codec, actual_fps, from_res)
        to_file.set(CAP_PROP_FRAME_WIDTH, from_res[0])
        to_file.set(CAP_PROP_FRAME_HEIGHT, from_res[1])
        frames_handled = 0
        if self.running:
            try:
                ret, frame = from_file.read()
                while ret and frame is not None and self.running:
                    to_file.write(frame)
                    frames_handled += 1
                    self.signal.update_sig.emit(frames_handled, total_frames)
                    ret, frame = from_file.read()
            except Exception as e:
                from_file.release()
                to_file.release()
                try:
                    remove(self.to_file)
                except Exception as e:
                    pass
                self.signal.done_sig.emit(False)
                return
        from_file.release()
        to_file.release()
        if not frames_handled == total_frames:
            try:
                remove(self.to_file)
            except Exception as e:
                pass
            self.signal.done_sig.emit(False)
            return
        elif self.cleanup:
            try:
                remove(self.from_file)
            except Exception as e:
                pass
            self.signal.done_sig.emit(True)
            return


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
    frames_handled = 0
    try:
        ret, frame = from_file.read()
        while ret and frame is not None:
            to_file.write(frame)
            frames_handled += 1
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
