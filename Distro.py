# -*- Mode: python; coding: utf-8 -*-

#
# Cherokee Web Site
#
# Authors:
#      Alvaro Lopez Ortega <alvaro@alobbs.com>
#
# Copyright (C) 2001-2011 Alvaro Lopez Ortega
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 2 of the GNU General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import os
import re
import CTK
import gzip
import time
import config

CACHE_EXPIRATION = 2 * 60 * 60


#
# Index file
#
def parse_distro_index():
    distro_root  = os.path.join (config.DOWNLOADS_LOCAL, "distribution")
    distro_index = os.path.join (distro_root, "index.py.gz")

    # Read
    f = gzip.open (distro_index, 'rb')
    content = f.read()
    f.close()

    # Parse
    return CTK.util.data_eval (content)


latest_info            = None
latest_info_expiration = None

def Distro_Info():
    global latest_info
    global latest_info_expiration

    if not latest_info or time.time() > latest_widget_expiration:
        latest_info            = parse_distro_index()
        latest_info_expiration = time.time() + CACHE_EXPIRATION

    return latest_info


#
# Authors
#
class Authors_List (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self)

        # Collect Authors
        info  = Distro_Info()
        pkgs  = info.get('packages', {})
        names = {}

        for pkg_name in pkgs:
            pkg = pkgs[pkg_name]
            maintainer = pkg.get('maintainer', {})
            name = maintainer.get('name')

            if name and not names.keys():
                names[name] = maintainer.get('email')

        # Build Widget
        l = CTK.List()
        for name in names:
            entry = CTK.Box()
            entry += CTK.RawHTML (name)
            entry += CTK.RawHTML (names[name] or '')
            l += entry

        self += l


latest_auth_wid            = None
latest_auth_wid_expiration = None

def Latest_Tweets():
    global latest_auth_wid
    global latest_auth_wid_expiration

    if not latest_auth_wid or time.time() > latest_widget_expiration:
        latest_auth_wid            = Authors_List()
        latest_auth_wid_expiration = time.time() + CACHE_EXPIRATION

    return latest_auth_wid
