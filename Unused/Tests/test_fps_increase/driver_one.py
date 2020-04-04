# import the necessary packages
from __future__ import print_function
from Unused.Tests.test_fps_increase.cam_handler import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
from numpy import array_equal


def handle_frame(frame):
    frame = imutils.resize(frame, width=100)
    frame = imutils.resize(frame, width=200)
    frame = imutils.resize(frame, width=300)
    frame = imutils.resize(frame, width=400)
    frame = imutils.resize(frame, width=500)
    return frame


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=900,
                help="# of frames to loop over for FPS test")

ap.add_argument("-d", "--display", type=int, default=1,
                help="Whether or not frames should be displayed")

ap.add_argument("-c", "--cam-index", type=int, default=1,
                help="Index of cam to use")

args = vars(ap.parse_args())

# grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(args['cam_index'], cv2.CAP_DSHOW)
fps = FPS().start()
# loop over some frames
while fps._numFrames < args["num_frames"]:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    (grabbed, frame) = stream.read()
    frame = handle_frame(frame)
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    # update the FPS counter
    fps.__update()
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=args['cam_index']).start()
fps = FPS().start()
prev_frame = vs.read()
num_same = 0
# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    if array_equal(frame, prev_frame):
        # print("same frame")
        # num_same += 1
        continue
    prev_frame = frame
    fps.__update()
    frame = handle_frame(frame)
    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    # update the FPS counter
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
print("[INFO] num same frames: {0}".format(num_same))
# num_new = args['num_frames'] - num_same
# print("[INFO] num new frames: {0}".format(num_new))
# print("[INFO] actual fps: {:.2f}".format(num_new / fps.elapsed()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
