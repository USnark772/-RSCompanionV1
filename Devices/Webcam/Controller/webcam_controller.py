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
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

"""
Simply display the contents of the webcam with optional mirroring using OpenCV 
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""

import cv2
from PySide2.QtMultimedia import QCameraInfo, QCamera
from PySide2.QtMultimediaWidgets import QCameraViewfinder


def QCheckCameras():
    info_obj = QCameraInfo.availableCameras()
    return info_obj


# Just takes some time for the usb webcam for some reason.
def show_webcam(cam, mirror=False):
    try:
        cam = cv2.VideoCapture(cam)
        ret_val, img = cam.read()
    except Exception as e:
        print(e)
        cam.release()
        cv2.destroyAllWindows()
        return False
    # Must use ret_val to know if cam is still responding. If cam stops responding then don't try doing anything with
    # image img.
    while ret_val:
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        try:
            ret_val, img = cam.read()
        except Exception as e:
            print(e)
            cam.release()
            cv2.destroyAllWindows()
            return False
    cam.release()
    cv2.destroyAllWindows()
    return True


def find_cams():
    arr = []
    tests = 100
    for i in range(0, tests):
        print("Trying index:", i)
        cap = cv2.VideoCapture(i)
        print("cap is successful")
        if cap.read()[0]:
            arr.append(i)
            cap.release()
        else:
            break
    return arr


def main():
    num_cams = QCheckCameras()
    cams = []
    for cam in num_cams:
        camera = QCamera(cam)
        cams.append(QCamera(cam))
    print(cams)




if __name__ == '__main__':
    main()
