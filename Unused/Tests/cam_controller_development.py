import cv2
import threading
from CompanionLib.companion_helpers import get_current_time
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues.


class CamObj:
    def __init__(self, cap, name):
        self.cap = cap
        self.name = name
        self.writer = None

    def setup_writer(self, timestamp, save_dir='', vid_ext='.avi', fps=20, frame_size=(640, 480), codec='DIVX'):
        self.writer = cv2.VideoWriter(save_dir + timestamp + self.name + '_output' + vid_ext,
                                      cv2.VideoWriter_fourcc(*codec), fps, frame_size)

    def destroy_writer(self):
        if self.writer:
            self.writer.release()
            self.writer = None

    def get_data(self):
        return self.cap.read()

    def save_data(self, frame):
        if self.writer:
            self.writer.write(frame)

    def release(self):
        self.cap.release()
        self.destroy_writer()
        cv2.destroyWindow(self.name)


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
                self.list.add_cam_to_list(CamObj(cap, "Camera " + str(index)))
            index += 1


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

    def remove_cams(self, cams_to_remove):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            for cam in cams_to_remove:
                self.__remove_cam_from_list(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def empty_cam_list(self):
        self.read_lock.acquire()
        self.write_lock.acquire()
        try:
            for cam in self.__cams:
                self.__remove_cam_from_list(cam)
        finally:
            self.write_lock.release()
            self.read_lock.release()

    def __remove_cam_from_list(self, cam):
        self.__release_cam(cam)
        self.__cams.remove(cam)

    def iterate_cams(self):
        self.read_lock.acquire()
        try:
            for cam in self.__cams:
                yield cam
        finally:
            self.read_lock.release()

    @staticmethod
    def __release_cam(cam):
        cam.release()


class CameraManager:
    def __init__(self):
        self.cam_list = CameraList()
        self.cam_scanner = CamScanner(self.cam_list)
        self.cam_scanner.start()
        self.vid_writer = cv2.VideoWriter()
        self.saving = False

    def setup_savers(self, timestamp, save_dir='', vid_ext='.avi', fps=20, frame_size=(640, 480), codec='DIVX'):
        for cam in self.cam_list.iterate_cams():
            cam.setup_writer(timestamp, save_dir=save_dir, vid_ext=vid_ext, fps=fps, frame_size=frame_size, codec=codec)

    def destroy_savers(self):
        for cam in self.cam_list.iterate_cams():
            cam.destroy_writer()

    def set_saving(self, new_val):
        self.saving = new_val

    def cleanup(self):
        self.cam_list.empty_cam_list()

    def controller_callback(self, cam):
        self.cam_list.remove_cams([cam])

    def refresh_all_cams(self):
        to_remove = []
        for cam in self.cam_list.iterate_cams():
            ret, frame = cam.get_data()
            if ret:
                cv2.imshow(cam.name, frame)
                if self.saving:
                    cam.save_data(frame)
            else:
                to_remove.append(cam)
        if len(to_remove) > 0:
            self.cam_list.remove_cams(to_remove)


def main():
    cam_man = CameraManager()
    save_dir = 'C:/Users/phill/Companion App Save Folder/'
    while True:
        cam_man.refresh_all_cams()
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            break
        elif keypress == ord('s'):
            cam_man.setup_savers(get_current_time(save=True), save_dir=save_dir)
            cam_man.set_saving(True)
        elif keypress == ord('d'):
            cam_man.set_saving(False)
            cam_man.destroy_savers()
    # When everything done, release the capture
    cam_man.cleanup()


main()
