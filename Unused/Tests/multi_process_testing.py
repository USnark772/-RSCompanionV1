from multiprocessing import Process
import cv2


def show_feed(index):
    x = 1920
    y = 1080
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)
    while True:
        ret, frame = cap.read()
        if frame is None or not ret:
            break
        try:
            cv2.imshow("Cam", frame)
        except Exception as e:
            break
        keypress = cv2.waitKey(1) % 0xFF
        if keypress == ord('q'):
            break


if __name__ == '__main__':
    i = 0
    p1 = Process(target=show_feed, args=(i,))
    i += 1
    p2 = Process(target=show_feed, args=(i,))
    i += 1
    p3 = Process(target=show_feed, args=(i,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
