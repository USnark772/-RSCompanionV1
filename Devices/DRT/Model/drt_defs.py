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

""" Definitions specific to the DRT device """

drtv1_0_note_spacer = ", , , , , "

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