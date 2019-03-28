"""The main portal to launch the wireless DRT+ program"""
import rs_device_com as serial
import time
import tkinter as tk


# We provide serial with a list of official RS devices by name. This does not change.'
# This list needs to go into a different file obviously
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

# Serial returns...

class controller:
    def __init__(self):
        self.root = tk.Tk()
        self.bttn = tk.Button(self.root, command=self.start_exp)
        self.bttn.pack()

        self.com = dict()

        self.com = serial.ControllerSerial(devices, self. com_callback)

        self.root.after(5, self.update_com)

        self.root.mainloop()

    def com_callback(self, msg):
        print(msg)

    def update_com(self):
        self.com.update()
        self.root.after(1, self.update_com)

    def start_exp(self):
        for d in self.com.devices:
            if self.com.devices[d]['id'] != 'unknown':
                msg = str.encode("get_name\n")
                self.com.devices[d]['port'].write(msg)
                pass


if __name__ == '__main__':
    controller()
