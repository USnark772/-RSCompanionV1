import cv2
import threading
import queue
from traceback import print_stack
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues
# Maybe keep track of lowest unplugged cam index then periodically attempt to reconnect from that one up.
# TODO: UI lag when checking for cameras. Need to figure out how to thread that properly.
#  Likely need to use a lock around a shared resource.


class CamScanner(threading.Thread):
    def __init__(self, the_list):
        threading.Thread.__init__(self, daemon=True)
        self.list = the_list

    # Try to connect new cam from latest index and up
    def run(self):
        while True:
            i = self.list.get_num_cams()
            self.check_for_cams(i)

    def check_for_cams(self, index=0):
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap is None or not cap.isOpened():
                break
            else:
                self.list.add_cam_to_list((cap, "Camera " + str(index), index))
            index += 1


# TODO: Fix the deadlocking between iterating and add/remove cams.
class CameraList:
    def __init__(self):
        print("making read and write locks")
        self.write_lock = threading.Lock()
        self.read_lock = threading.Lock()
        self.__cams = []

    def get_num_cams(self):
        self.read_lock.acquire()
        try:
            return len(self.__cams)
        finally:
            self.read_lock.release()

    def add_cam_to_list(self, cam):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            self.__cams.append(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def remove_cam_from_list(self, cam):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            self.__release_cam(cam)
            self.__cams.remove(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def iterate_cams(self):
        self.read_lock.acquire()
        try:
            for cam in self.__cams:
                yield cam
        finally:
            self.read_lock.release()

    @staticmethod
    def __release_cam(cam):
        cv2.destroyWindow(cam[1])
        cam[0].release()


class CameraManager:
    def __init__(self):
        self.cam_list = CameraList()
        self.cam_scanner = CamScanner(self.cam_list)
        self.cam_scanner.start()

    def release_all_cams(self):
        for cam in self.cam_list.iterate_cams():
            self.cam_list.remove_cam_from_list(cam)

    def refresh_all_cams(self):
        for cam in self.cam_list.iterate_cams():
            ret, frame = cam[0].read()
            if ret:
                cv2.imshow(cam[1], frame)
            else:
                self.cam_list.remove_cam_from_list(cam)


def main():
    cam_man = CameraManager()
    while True:
        cam_man.refresh_all_cams()
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            break
    # When everything done, release the capture
    cam_man.release_all_cams()


main()
