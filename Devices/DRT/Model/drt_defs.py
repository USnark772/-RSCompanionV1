# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

""" Definitions specific to the DRT device """

drtv1_0_file_hdr = "Type, Condition, Key Flag, Timestamp, Millisecond counter, Trial counter, Clicks, Response Time,"\
                   " Note"

drtv1_0_config_fields = ['lowerISI', 'upperISI', 'stimDur', 'intensity']
drtv1_0_output_fields = ['startMillis', 'trial', 'clicks', 'rt']
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