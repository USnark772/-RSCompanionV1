# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import View.drt_view as DRT


# TODO: Make different subwindows etc. for each type of device and then build based on device type
class RSDevice:
    def __init__(self, device_id, msg_callback, tab_parent):
        self.device_id = device_id
        self.device_name = self.device_id[0] + " on " + self.device_id[1]
        self.tab_parent = tab_parent
        self.msg_callback = msg_callback

        if self.device_id[0] == "drt":
            self.configure_widget = DRT.ConfigureWidget(self.device_name, self.callback)
            self.device_tab = DRT.Tab(self.device_id, self.callback, self.show_hide_configure_widget_handler)

        elif self.device_id[0] == "vog":
            self.device_tab = DRT.Tab(self.device_id, self.callback, self.show_hide_configure_widget_handler)

        self.tab_parent.setUpdatesEnabled(False)
        index = self.tab_parent.addTab(self.device_tab, "")
        self.tab_parent.setUpdatesEnabled(True)
        self.tab_parent.setTabText(index, self.device_name)

    def show_hide_configure_widget_handler(self):
        if self.configure_widget.isVisible():
            self.configure_widget.hide()
        else:
            self.configure_widget.show()

    def handle_msg(self, msg):
        self.configure_widget.handle_msg(msg)

    def remove_self(self):
        self.tab_parent.removeTab(self.tab_parent.indexOf(self.device_tab))
        self.device_tab.deleteLater()

    def callback(self, msg_dict):
        msg_dict['type'] = "send"
        msg_dict['device'] = self.device_id
        self.msg_callback(msg_dict)