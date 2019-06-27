# Author: Phillip Riskin & Joel Cooper
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

#################################################################################################################
# general
#################################################################################################################

current_version = 1.0

version_url = "https://raw.githubusercontent.com/redscientific/CompanionApp/master/Version.txt"

# TODO: Change this
program_output_hdr = "Timestamp, Author, Location, Message\n"

about_RS_text = "CHANGEME Red Scientific is an awesome company that will do great things in the years to come and " \
                "keep Phillip really happy by paying him lots of money because RS is rich from selling all those " \
                "awesome devices which are made even awesomer by the View that Phillip was instrumental in making " \
                "work. boom."

about_RS_app_text = "CHANGEME The RS Companion App was designed by Joel Cooper and brought to life by Phillip " \
                    "Riskin. It has many functionalities that you might not be aware of so play around with it and " \
                    "see what's going on! Have fun :)"

update_available = "An update is available."

up_to_date = "Your program is up to date."

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
