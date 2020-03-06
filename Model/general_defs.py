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

import cv2

""" General definitions for the app """

""" Change these when building """
image_file_path = '../View/Images/'  # new path should be 'Images/'
version_url = "https://raw.githubusercontent.com/redscientific/CompanionApp/master/Version.txt"
current_version = 1.10  # New version should be incremented.
current_version_str = '1.10'

#################################################################################################################
# general
#################################################################################################################

program_output_hdr = "Timestamp, Author, Location, Message\n"

about_RS_text = "Red Scientific Inc was founded in 2015 by Joel Cooper PhD\n\n" \
                "Contact Information:\n" \
                "joel@redscientific.com\n" \
                "1-801-520-5408"

about_RS_app_text = "- Most things in this app have tooltips. Mouse over different parts to see respective tooltips" \
                    " for more information\n\n" \
                    "Along the top of the app you will find a detachable control bar containing the following:\n" \
                    "- Create button: Create an experiment and choose a location folder for the app to save device" \
                    " data.\n" \
                    "- Play/Pause button: Begin/resume or pause an experiment in progress.\n" \
                    "- Optional condition name: An optional name that will be associated with the newly created" \
                    " experiment.\n\n" \
                    "- Key Flag: Press a letter key at any time to make a quick reference key that will be associated" \
                    " with the data coming in from the devices during an experiment.\n\n" \
                    "- Note: Enter a note into the box and press Post to apply that note to all device data files" \
                    " within the current experiment.\n\n" \
                    "- Information: Displays information in regards to the current experiment.\n\n" \
                    "The lower left section contains the Display area with the following features:\n" \
                    "- Displays data coming in from devices associated with the latest experiment.\n" \
                    "- Clicking on the legend will show/hide device specific data in each graph.\n" \
                    "- Using the control bar under each graph you will be able manipulate the graphs.\n\n" \
                    "The lower right section contains the Device config area where each device will display a" \
                    " configuration menu. In each menu you can alter the settings of how the respective device acts" \
                    " during an experiment.\n"

update_available = "An update is available."

up_to_date = "Your program is up to date."

error_checking_for_update = "There was an unexpected error connecting to the repository. Please check" \
                            " https://github.com/redscientific/CompanionApp manually" \
                            " or contact Red Scientific directly."

device_connection_error = "There was a problem connecting the device, please retry connection."

__compliant_text_color = "rgb(0, 0, 0)"
__error_text_color = "rgb(255, 0, 0)"
__selection_color = "rgb(0, 150, 255)"
__font_size = "12px"
tab_line_edit_compliant_style = "QLineEdit { color: " \
                                + __compliant_text_color \
                                + "; selection-background-color: " \
                                + __selection_color \
                                + "; font: " \
                                + __font_size + "; }"
tab_line_edit_error_style = "QLineEdit { color: " \
                            + __error_text_color \
                            + "; selection-background-color: " \
                            + __selection_color \
                            + "; font: " \
                            + __font_size + "; }"

# "QPushButton:pressed { background-color: rgb(150, 180, 200);
button_pressed_style = "QPushButton:pressed { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, " \
                       "stop: 0 #dadbde, stop: 1 #f6f7fa); font: " + __font_size + "; }"

# "background-color: rgb(230, 230, 230); " \
button_normal_style = "QPushButton { border: 1px solid #8f8f91; background-color: qlineargradient(x1: 0, y1: 0, " \
                      "x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde); min-height: 22px; font: " + __font_size + "; }"

#################################################################################################################
# device list for usb port detection
#################################################################################################################

devices = {'drt': {'probe': "get_name\n\r",
                   'key': 'sDRT',
                   'name': 'sDRT',
                   'pid': 32798,
                   'vid': 9114},
           'vog': {'probe': ">get_deviceName|<<\n",
                   'key': 'deviceName|VOG',
                   'name': 'VOG',
                   'pid': 1155,
                   'vid': 5824}}

#################################################################################################################
# opencv defs
#################################################################################################################

cap_backend = cv2.CAP_DSHOW
cap_temp_codec = cv2.VideoWriter_fourcc(*'mjpg')
cap_codec = cv2.VideoWriter_fourcc(*'MJPG')
