# Author: Phillip Riskin
# Date: Spring 2019
# Project: Companion App
# Company: Red Scientific
# https://redscientific.com/index.html

from os.path import dirname, join, exists
from requests import get


class VersionChecker:
    def __init__(self):
        version_url = "https://raw.githubusercontent.com/redscientific/Companion/master/" \
              "Version.txt?token=AH5QIBO7ADV5FWFR2AXOYSK5AAF3C"
        self.latest_version = self.get_latest_version(version_url)

    def check_version(self):
        current_version = ''
        filename = join(dirname(__file__), 'current_version')
        if not exists(filename):
            with open(filename, 'w+') as f:
                # default to earliest version to prompt update
                f.write('version:1.0')
        f = open(filename, 'r')
        for line in f:
            if 'version:' in line:
                current_version = float(line[line.index(':')+1:])
                break
        print("current version is:", current_version, " latest version is:", self.latest_version)
        if current_version != self.latest_version:
            print("New app version", self.latest_version, " available")
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
    def get_latest_version(url):
        """ Use internet to get latest version from server """
        r = get(url)
        if "Companion App Version:" in r.text:
            return r.text[r.text.index(":") + 1:]
        else:
            print("Error getting latest version number")
