import cv2
from sys import argv
from os import remove
from time import sleep
from Model.general_defs import cap_codec


def set_file_playback_speed(from_file_name: str, to_file_name: str, total_secs: float, cleanup: bool) -> bool:
    from_file = cv2.VideoCapture(from_file_name)
    if not from_file.isOpened():
        print("invalid file")
        sleep(3)
        return False
    from_res = (int(from_file.get(cv2.CAP_PROP_FRAME_WIDTH)), int(from_file.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    total_frames = from_file.get(cv2.CAP_PROP_FRAME_COUNT)
    actual_fps = total_frames / total_secs
    to_file = cv2.VideoWriter(to_file_name, cap_codec, actual_fps, from_res)
    to_file.set(cv2.CAP_PROP_FRAME_WIDTH, from_res[0])
    to_file.set(cv2.CAP_PROP_FRAME_HEIGHT, from_res[1])
    try:
        ret, frame = from_file.read()
        while ret and frame is not None:
            to_file.write(frame)
            ret, frame = from_file.read()
    except:
        from_file.release()
        to_file.release()
        remove(to_file_name)
        print('something went wrong.')
        sleep(3)
        return False
    if cleanup:
        remove(from_file_name)
    from_file.release()
    to_file.release()
    print('success')
    sleep(3)
    return True


def main():
    from_file = argv[1]
    to_file = argv[2]
    total_secs = int(argv[3])
    cleanup = eval(argv[4])
    print(from_file, to_file, total_secs, cleanup)
    print(type(from_file), type(to_file), type(total_secs), type(cleanup))
    print(input('please enter a whatever: '))
    # set_file_playback_speed(from_file, to_file, total_secs, cleanup)


if __name__ == '__main__':
    main()
