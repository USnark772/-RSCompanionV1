# Author: Phillip Riskin & Joel Cooper
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

""" Definitions specific to the VOG device """

vog_about = "The Visual Occlusion Glasses have a few different settings available.\n" \
            "-NHTSA\n" \
            "\tWhen NHTSA is applied, the vog will "\
            "-eBlindfold\n" \
            "-Direct Control\n"

# TODO: Change this
vog_file_hdr = "Type, Condition, Key Flag, Timestamp, Trial counter, Millis Open, Millis Closed, Note"

vog_config_fields = []
vog_output_field = ['trialCounter', 'millis_openElapsed', 'millis_closeElapsed']
vog_ui_fields = ['block #', 'Total millis open', 'Total millis closed']

vog_max_val = 2147483647

vog_max_open_close = vog_max_val
vog_min_open_close = 0

vog_debounce_max = 100
vog_debounce_min = 0

vog_button_mode = 0
