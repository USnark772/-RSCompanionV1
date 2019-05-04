# Author: Phillip Riskin & Joel Cooper
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

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

drt_config_fields = ['lowerISI', 'upperISI', 'stimDur', 'intensity']
drt_trial_fields = ['startMillis', 'trial', 'clicks', 'rt']

drt_intensity_max = 255
drt_intensity_min = 0

drt_stim_dur_max = 10
drt_stim_dur_min = 0

drt_ISI_max = 10000
drt_ISI_min = 0

'''
for internal storage:
drt dict keys
device name or type, probe timestamp, time from block start, probe iteration, reaction time, key flag at start, key flag time

vog dict keys
device name or type, setup name, open time, close time, debounce, button mode, total open time, total close time
'''

'''
dict should look like
exp_data
    exp_number entry
        block_number entry
            device_entry (drt for example)
            device_entry
            etc.
        block_number entry
            device_entry
            etc.
    exp_number entry
        block_number entry
            device_entry
            device_entry
            etc.
        block_number entry
            device_entry
            etc.
'''