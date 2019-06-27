# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

import traceback
from urllib3 import PoolManager
from general_defs import version_url, current_version


class VersionChecker:
    def __init__(self, callback):
        self.callback = callback
        self.latest_version = self.get_latest_version()

    def check_version(self):
        if not self.latest_version:
            return -1
        elif self.latest_version > current_version:
            return 1
        return 0

    def __callback(self, msg):
        self.callback(msg + "\n")

    @staticmethod
    def get_latest_version():
        mgr = PoolManager()
        try:
            r = mgr.request("GET", version_url)
        except Exception:
            with open('logfile.txt', 'w') as f:
                traceback.print_exc(file=f)
            return False
        data = str(r.data)
        if "Companion App Version:" in data:
            latest_version = data[data.index(":") + 1:].rstrip("\\n'")
            return float(latest_version)
        return False
