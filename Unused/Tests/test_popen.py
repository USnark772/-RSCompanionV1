from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE, CREATE_NO_WINDOW


exec_path = 'C:/RSDev/Companion/Unused/Tests/alter_file_fps.py'
from_file = 'C:/Users/phill/Companion App Save Folder/fancy_2020-03-14-17-13-58_CAM_1_output.avi'
to_file = 'C:/Users/phill/Companion App Save Folder/fancy2_2020-03-14-17-13-58_CAM_1_output.avi'
total_secs = 60
cleanup = True


def main():
    Popen(args=[executable, exec_path, from_file, to_file, str(total_secs), str(cleanup)],
          creationflags=CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    main()
