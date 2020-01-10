import cv2
from traceback import print_stack
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues
# Maybe keep track of lowest unplugged cam index then periodically attempt to reconnect from that one up.
# TODO: UI lag when checking for cameras. Need to figure out how to thread that properly.

class CameraManager:
    def __init__(self):
        self.cams = []
        self.num_cams = 0
        self.check_for_cams()

    def check_for_cams(self, index=0):
        self.cams = []
        while True:
            cap = self.__capture_cam(index)
            if cap is None or not cap.isOpened():
                break
            else:
                self.__add_cam_to_list(index, cap)
                self.num_cams += 1
            index += 1

    def reconnect_cams(self):
        self.check_for_cams(self.num_cams)

    def release_all_cams(self):
        for cam in self.cams:
            self.__release_cam(cam)

    def refresh_all_cams(self):
        for cam in self.cams:
            ret, frame = cam[0].read()
            if ret:
                cv2.imshow(cam[1], frame)
            else:
                self.__release_cam(cam)
                self.cams.remove(cam)
                self.num_cams -= 1

    def print_indices(self):
        for cam in self.cams:
            print(cam[2])

    def __add_cam_to_list(self, index, cap):
        self.cams.append((cap, "Camera " + str(index), index))

    def __check_for_cam_by_index(self, index):
        cap = self.__capture_cam(index)
        if cap and cap.isOpened():
            self.__add_cam_to_list(index, cap)

    @staticmethod
    def __capture_cam(index):
        return cv2.VideoCapture(index, cv2.CAP_DSHOW)

    @staticmethod
    def __release_cam(cam):
        cv2.destroyWindow(cam[1])
        cam[0].release()


def main():
    cam_man = CameraManager()
    i = 0
    while True:
        cam_man.refresh_all_cams()
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            break
        if i == 100:
            cam_man.reconnect_cams()
            i = 0
        i += 1
    # When everything done, release the capture
    cam_man.release_all_cams()
    cv2.destroyAllWindows()


main()
