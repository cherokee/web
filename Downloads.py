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
import glob
import time
import config

DOWNLOADS_WEB = '/download'


class cache (object):
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        now = time.time()

        # Hit
        if self.cache.has_key (args):
            entry = self.cache[args]
            if now < entry['expiration']:
                return entry['ret']

        # Miss
        ret = self.func(*args)
        self.cache[args] = {'ret': ret, 'expiration': now + 10}
        return ret

#
# Util
#
def version_to_num (ver):
    parts = ver.split('.')

    num = 0
    for n in range(1, len(parts)+1):
        num += int(parts[-n]) * (100**(n-1))
    return num

def sort_versions (v1,v2):
    return cmp (version_to_num(v1), version_to_num(v2))

def directory_local_to_web (directory):
    if directory.startswith (config.DOWNLOADS_LOCAL):
        return directory.replace (config.DOWNLOADS_LOCAL, DOWNLOADS_WEB)

    assert False, 'Unhandled case'


#
# Paths
#
@cache
def directory_get_lastest_version (directory):
    dirs = []
    for f in os.listdir(directory):
        if not filter (lambda x: not x in "1234567890.", f):
            dirs.append(f)

    dirs.sort (sort_versions)
    return dirs[-1]

@cache
def get_latest_version():
    major = directory_get_lastest_version (config.DOWNLOADS_LOCAL)
    minor = directory_get_lastest_version (os.path.join (config.DOWNLOADS_LOCAL, major))
    return minor

@cache
def get_latest_version_directory():
    major = directory_get_lastest_version (config.DOWNLOADS_LOCAL)
    minor = directory_get_lastest_version (os.path.join (config.DOWNLOADS_LOCAL, major))
    fullpath = os.path.join (config.DOWNLOADS_LOCAL, major, minor)
    return fullpath

@cache
def get_latest_macosx_dmg():
    latest_dir = get_latest_version_directory()

    for f in os.listdir (latest_dir):
        if 'mac' in f.lower():
            # Check DMG files
            macdir = os.path.join (latest_dir, f)
            dmgs = glob.glob ("%s/*.dmg"%(macdir))
            dmgs.sort()

            # Local & Web references
            dmg_local = dmgs[-1]
            dmg_web   = directory_local_to_web (dmg_local)
            return (dmg_local, dmg_web)


@cache
def get_latest_tarball():
    latest_dir = get_latest_version_directory()

    # Tarballs
    tarballs = glob.glob ("%s/*.tar.gz"%(latest_dir))
    tarballs.sort()

    # Local & Web references
    tar_local = tarballs[-1]
    tar_web   = directory_local_to_web (tar_local)

    return (tar_local, tar_web)


if __name__ == "__main__":
    print "Release", get_latest_version_directory()
    print "DMG    ", get_latest_macosx_dmg()
