# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from os.path import dirname, join, exists
import socket
import sys

class VersionChecker:
    def __init__(self):
        self.latest_version = self.get_latest_version()

    def check_version(self):
        current_version = ''
        filename = join(dirname(__file__), 'current_version')
        if not exists(filename):
            with open(filename, 'w+') as f:
                # default to earliest version to prompt update
                f.write('version:1.0')
        f = open(filename, 'r')
        for line in f:
            print("checking line", line)
            if 'version:' in line:
                current_version = float(line[line.index(':')+1:])
                break
        print("current version is:", current_version, " latest version is:", self.latest_version)
        if current_version != self.latest_version:
            print("Update available")
            f.close()
            return True
        else:
            f.close()
            return False

    def update_version(self):
        filename = join(dirname(__file__), 'current_version')
        f = open(filename, 'w')
        f.write('version:' + str(self.latest_version))
        f.close()

    @staticmethod
    def get_latest_version():
        """ Use internet to get latest version from server """
        latest_version = 1.1
        return latest_version
