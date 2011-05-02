#!/usr/bin/env python
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

import re
import sys
import time
import cPickle
import pycurl
import cStringIO

from mirrors import main_site, mirror_list

def check_mirror (mirror):
    http = mirror.get('http')

    mirror['status_stamp'] = time.time()
    mirror['up_to_date']   = False
    mirror['latest']       = None
    mirror['error']        = None

    # HTTP request
    res = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(pycurl.URL, http)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.CONNECTTIMEOUT, 15)
    c.setopt(pycurl.TIMEOUT, 25)
    c.setopt(pycurl.NOSIGNAL, 1)
    c.setopt(pycurl.WRITEFUNCTION, res.write)

    try:
        c.perform()
    except:
        mirror['error'] = 'HTTP error'
        return

    # Check latest
    try:
        latest = re.findall (r'LATEST_is_([\d\.]+)', res.getvalue(), re.M)[0]
    except:
        mirror['error'] = 'No LASTEST_is link'
        return

    mirror['latest'] = latest

    # Outdated
    if main_site.get('latest') and \
       main_site.get('latest') != latest:
        return

    # Report version
    mirror['up_to_date'] = True


def check_mirrors():
    global main_site

    # Main site
    check_mirror (main_site)

    # Check mirrors
    results = mirror_list[:]
    for mirror in results:
        # Current mirror
        print mirror['http'],
        sys.stdout.flush()

        # HTTP Request
        response = check_mirror (mirror)

        # Report
        if mirror['error']:
            print mirror['error']
        elif mirror['up_to_date']:
            print mirror['latest'], "OK"
        else:
            print mirror['latest'], "Outdated"

    # Save
    cPickle.dump (results, open("mirrors.pickle", 'w+'))
    os.system ("ls -l mirrors.pickle")


if __name__ == '__main__':
    check_mirrors()
