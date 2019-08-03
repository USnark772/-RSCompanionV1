# Author: Phillip Riskin & Joel Cooper
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

""" General definitions for the app """

#################################################################################################################
# general
#################################################################################################################

current_version = 1.0

version_url = "https://raw.githubusercontent.com/redscientific/CompanionApp/master/Version.txt"

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

image_file_path = "../View/Images/"

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
