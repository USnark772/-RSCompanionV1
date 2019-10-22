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

""" Definitions specific to the VOG device """

vog_about = "The Visual Occlusion Glasses have a few different settings available.\n" \
            "-NHTSA\n" \
            "\tWhen NHTSA is applied, the vog will "\
            "-eBlindfold\n" \
            "-Direct Control\n"

vog_note_spacer = ", , , , "

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
