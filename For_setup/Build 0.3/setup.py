import sys
import os
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os",
                                  "requests",
                                  "queue",
                                  "idna.idnadata",
                                  "urllib3"],
                     "excludes": ["tkinter"]}

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1.dll'),
                 os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1.dll')]

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
    build_exe_options['include_files'] = include_files

setup(name="companion_app",
      version="0.2",
      description="companion app",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
