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
