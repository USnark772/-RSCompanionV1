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

import logging
from urllib3 import PoolManager
from Model.general_defs import version_url, current_version


class VersionChecker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing")
        self.latest_version = self.get_latest_version()
        self.logger.debug("Initialized")

    def check_version(self):
        """ Compare version numbers. """
        self.logger.debug("running")
        if not self.latest_version:
            self.logger.debug("done")
            return -1
        elif self.latest_version > current_version:
            self.logger.debug("done")
            return 1
        self.logger.debug("done")
        return 0

    def get_latest_version(self):
        """ Connect to site at version_url and retrieve latest version number. """
        self.logger.debug("running")
        mgr = PoolManager()
        try:
            r = mgr.request("GET", version_url)
        except Exception:
            self.logger.exception("failed, could not connect to url")
            return False
        data = str(r.data)
        if "Companion App Version:" in data:
            latest_version = data[data.index(":") + 1:].rstrip("\\n'")
            self.logger.debug("done, found version")
            return float(latest_version)
        self.logger.debug("done, didn't find version")
        return False
