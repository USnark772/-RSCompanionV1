# Author: Phillip Riskin & Joel Cooper
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

version = 1.0

# Definitions to use to detect devices

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

drt_file_hdr = "device type: drt\nData: Exp Name, Block Name, Key Flag, Timestamp, Mills from Block Start, Probe #, " \
               "Clicks, Response Time"

drt_config_fields = ['lowerISI', 'upperISI', 'stimDur', 'intensity']
drt_trial_fields = ['startMillis', 'trial', 'clicks', 'rt']
drt_ui_fields = ['Mills from block start', 'probe #', 'clicks', 'response time']

drt_intensity_max = 255
drt_intensity_min = 0

drt_stim_dur_max = 5000
drt_stim_dur_min = 0

drt_ISI_max = 10000
drt_ISI_min = 0

vog_file_hdr = "device type: vog\nData: Exp Name, Block Name, Key Flag, Timestamp, block #, Total Millis Open, " \
               "Total Millis Closed"

vog_config_fields = []
vog_block_field = ['trialCounter', 'millis_openElapsed', 'millis_closeElapsed']
vog_ui_fields = ['block #', 'Total millis open', 'Total millis closed']

vog_max_open_close = 10000
vog_min_open_close = 0

vog_debounce_max = 100
vog_debounce_min = 0

vog_button_mode = 0

block_note_hdr = "Note: Exp Name, Block Name, Key Flag, Timestamp, block note"
com_output_hdr = "timestamp, device, port, device output\n"
