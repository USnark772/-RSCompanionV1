# Author: Phillip Riskin & Joel Cooper
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

#################################################################################################################
# general
#################################################################################################################

version = 1.0

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


compliant_text_color = "rgb(0, 0, 0)"
error_text_color = "rgb(255, 0, 0)"
selection_color = "rgb(0, 150, 255)"
font_size = "10px"
tab_line_edit_compliant_style = "QLineEdit { color: "\
                                + compliant_text_color\
                                + "; selection-background-color: "\
                                + selection_color \
                                + "; font: " \
                                + font_size + "; }"
tab_line_edit_error_style = "QLineEdit { color: "\
                            + error_text_color\
                            + "; selection-background-color: "\
                            + selection_color \
                            + "; font: " \
                            + font_size + "; }"

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
# drt specific
#################################################################################################################

drtv1_0_file_hdr = "Type, Condition, Key Flag, Timestamp, Millisecond counter, trial counter, Clicks, Response Time,"\
                   " Note"

drtv1_0_config_fields = ['lowerISI', 'upperISI', 'stimDur', 'intensity']
drtv1_0_trial_fields = ['startMillis', 'trial', 'clicks', 'rt']
drtv1_0_ui_fields = ['Mills from block start', 'probe #', 'clicks', 'response time']

drtv1_0_iso_standards = {'upperISI': 5000, 'lowerISI': 3000, 'intensity': 255, 'stimDur': 1000}

# drt v1.0 uses uint16_t for drt value storage
drtv1_0_max_val = 65535
# All the following drt values must be between 0 and drt_max_val
drtv1_0_intensity_max = 255
drtv1_0_intensity_min = 0

drtv1_0_stim_dur_max = drtv1_0_max_val
drtv1_0_stim_dur_min = 0

drtv1_0_ISI_max = drtv1_0_max_val
drtv1_0_ISI_min = 0

#################################################################################################################
# vog specific
#################################################################################################################

# TODO: Change this
vog_file_hdr = "Type, Condition, Key Flag, Timestamp, Trial #, Millis Open, Millis Closed, Note"

vog_config_fields = []
vog_block_field = ['trialCounter', 'millis_openElapsed', 'millis_closeElapsed']
vog_ui_fields = ['block #', 'Total millis open', 'Total millis closed']

vog_max_val = 2147483647

vog_max_open_close = vog_max_val
vog_min_open_close = 0

vog_debounce_max = 100
vog_debounce_min = 0

vog_button_mode = 0
