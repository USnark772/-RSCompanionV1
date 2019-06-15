# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from urllib3 import PoolManager
from Model.defs import version_url, current_version


class VersionChecker:
    def __init__(self, callback):
        self.callback = callback
        self.latest_version = self.get_latest_version()
        self.__callback("version_checker init() self.latest_version = " + str(self.latest_version))

    def check_version(self):
        self.__callback("version_checker, check_version() starting")
        if not self.latest_version:
            self.__callback("version_checker, check_version() returning -1")
            return -1
        elif self.latest_version > current_version:
            self.__callback("version_checker, check_version() returning 1")
            return 1
        self.__callback("version_checker, check_version() returning 0")
        return 0

    def get_latest_version(self):
        self.__callback("version_checker, get_latest_version() starting")
        mgr = PoolManager()
        self.__callback("version_checker, get_latest_version() mgr = PoolManager()")
        r = mgr.request("GET", version_url)
        self.__callback("version_checker, get_latest_version() r = mgr.request()")
        data = str(r.data)
        self.__callback("version_checker, get_latest_version() data = str(r.data)")
        if "Companion App Version:" in data:
            self.__callback("version_checker, get_latest_version() found correct file")
            latest_version = data[data.index(":") + 1:].rstrip("\\n'")
            self.__callback("version_checker, get_latest_version() returning with value: " + latest_version)
            return float(latest_version)
        return False

    def __callback(self, msg):
        self.callback(msg + "\n")
