import cv2
import time

if __name__ == '__main__':

    # Start default camera
    video = cv2.VideoCapture(0)
    x = 1920
    y = 1080
    res1 = video.set(cv2.CAP_PROP_FRAME_WIDTH, x)
    res2 = video.set(cv2.CAP_PROP_FRAME_HEIGHT, y)

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    fps = video.get(cv2.CAP_PROP_FPS)
    print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Number of frames to capture
    num_frames = 120

    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Grab a few frames
    for i in range(0, num_frames):
        ret, frame = video.read()

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
