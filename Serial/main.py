"""The main portal to launch the wireless DRT+ program"""
import controller_serial as serial
import time
import tkinter as tk

# We provide serial with a list of official RS devices by name. This does not change.

drt = {'probe': "get_name\n\r",
       'key': 'sDRT',
       'name': 'sDRT'}
vog = {'probe': ">get_deviceName|<<\n",
       'key': 'deviceName|VOG',
       'name': 'VOG'}

# Serial returns...

class controller:
    def __init__(self):
        self.root = tk.Tk()

        self.DRT = serial.ControllerSerial(drt, self.drt_callback)
        self.VOG = serial.ControllerSerial(vog, self.vog_callback)
        self.DRT2 = serial.ControllerSerial(drt, self.drt_callback)

        self.root.after(5, self.update_com)

        self.root.mainloop()

    def drt_callback(self, msg):
        print(msg)

    def vog_callback(self, msg):
        print(msg)


    def update_com(self):
        self.DRT.update()
        self.VOG.update()
        self.DRT2.update()
        self.root.after(1, self.update_com)


if __name__ == '__main__':
    controller()
