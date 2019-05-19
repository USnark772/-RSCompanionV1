# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import View.device_tab as tab
import View.Devices.drt_tab_contents as DRT
import View.Devices.vog_tab_contents as VOG


class RSDevice:
    def __init__(self, device_id, msg_callback, tab_parent):
        self.device_id = device_id
        self.device_name = self.device_id[0] + " on " + self.device_id[1]
        self.tab_parent = tab_parent
        self.msg_callback = msg_callback
        self.device_tab = tab.Tab(self.device_id, self.callback)

        if self.device_id[0] == "drt":
            self.tab_contents = DRT.TabContents(self.device_tab.scroll_area_contents, self.device_name, self.callback)

        elif self.device_id[0] == "vog":
            self.tab_contents = VOG.TabContents(self.device_tab.scroll_area_contents, self.device_name, self.callback)

        self.tab_parent.setUpdatesEnabled(False)
        index = self.tab_parent.addTab(self.device_tab, "")
        self.tab_parent.setUpdatesEnabled(True)
        self.tab_parent.setTabText(index, self.device_name)

    def handle_msg(self, msg):
        # print("device.handle_msg()")
        self.tab_contents.handle_msg(msg)

    def remove_self(self):
        self.tab_parent.removeTab(self.tab_parent.indexOf(self.device_tab))
        # self.configure_widget.deleteLater()
        self.device_tab.deleteLater()

    def callback(self, msg_dict):
        msg_dict['type'] = "send"
        msg_dict['device'] = self.device_id
        self.msg_callback(msg_dict)