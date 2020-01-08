import cv2
# If too many usb cameras are on the same usb hub then they won't be able to be used due to power issues


class CameraManager:
    def __init__(self):
        self.cams = []
        self.check_for_cams()

    def check_for_cams(self):
        index = 0
        self.cams = []
        while True:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap is None or not cap.isOpened():
                break
            else:
                self.cams.append((cap, "Camera " + str(index), index))
            index += 1

    # TODO: do this differently.
    # This will not work because it does not know that that index is already used
    # it simply opens a new VideoCapture object and seems to access the same feed.
    # See example in main()
    def check_for_cam_by_index(self, index):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap and cap.isOpened():
            self.cams.append((cap, "Camera " + str(index), index))

    def release_all_cams(self):
        for cam in self.cams:
            self.release_cam(cam)

    @staticmethod
    def release_cam(cam):
        cv2.destroyWindow(cam[1])
        cam[0].release()

    def refresh_all_cams(self):
        released = []
        for b in range(len(self.cams)):
            ret, frame = self.cams[b].read()
            if ret:
                cv2.imshow(self.cams[b][1], frame)
            else:
                self.cams[b].release()
                cv2.destroyWindow('Camera ' + str(b))
                self.cams.remove(self.cams[b])
        return released


def main():
    print(0)
    cam1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print(1)
    cam2 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print(2)
    while True:
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()
        cv2.imshow("Cam1", frame1)
        cv2.imshow("Cam2", frame2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()

    # i = 0
    # cams = check_for_cams(0)
    # while True:
    #     # Capture frame-by-frame
    #     refresh_all_cams(cams)
    #     i += 1
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #     if i == 100:
    #         print("Resetting cams")
    #         release_all_cams(cams)
    #         cams = check_for_cams()
    #         i = 0
    # # When everything done, release the capture
    # release_all_cams(cams)
    # cv2.destroyAllWindows()


main()
