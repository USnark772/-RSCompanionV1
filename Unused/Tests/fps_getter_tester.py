import cv2
import time
from sys import platform

small = (640, 480)
big = (1920, 1080)

def show_feeds():
    # Start default camera
    video = cv2.VideoCapture(0)
    size = big
    res1 = video.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
    res2 = video.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    fps = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    print(video.set(cv2.CAP_PROP_FPS, 25.0))
    new_fps = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(new_fps))
    # Number of frames to capture
    num_frames = 120

    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Grab a few frames
    for i in range(0, num_frames):
        ret, frame = video.read()
        pos = video.get(cv2.CAP_PROP_POS_MSEC)
        print(pos)

    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))

    print(video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # Release video
    video.release()


def show_backends():
    backend_ids = cv2.videoio_registry.getBackends()
    for backend in backend_ids:
        print(cv2.videoio_registry.getBackendName(backend))


def show_platform():
    print(platform)


def main():
    # show_feeds()
    # show_backends()
    show_platform()


if __name__ == '__main__':
    main()
