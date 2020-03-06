""" Licensed under GNU GPL-3.0-or-later """
"""
This file is part of RS Companion.

RS Companion is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RS Companion is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RS Companion.  If not, see <https://www.gnu.org/licenses/>.
"""

# Author: Phillip Riskin
# Date: 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html


import sys
import os
from cx_Freeze import setup, Executable

filepath = 'C:/RSDev'


build_exe_options = {'packages': ['os',
                                  'requests',
                                  'queue',
                                  'idna.idnadata',
                                  'urllib3',
                                  'numpy',
                                  'matplotlib'],
                     'excludes': ['tkinter'],
                     'include_files': [filepath + '/redist/',
                                       filepath + '/Companion/View/Images/',
                                       filepath + '/Companion/readme/']}

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
include_files = [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libcrypto-1_1.dll'),
                 os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'libssl-1_1.dll')]

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    for file in include_files:
        build_exe_options['include_files'].append(file)

setup(name='RS Companion',
      version='1.10',
      description='The companion app to rule all RS Devices',
      options={'build_exe': build_exe_options},
      executables=[Executable('main.py', targetName='Companion.exe', base=base,
                              icon=filepath + '/Companion/View/Images/rs_icon.ico')])
