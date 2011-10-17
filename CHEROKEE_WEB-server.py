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

import os
import sys

import CTK
import PageIndex
import PageDownload
import PageDownloadIndex
import PageSVN
import PageDistro
import PageDoc
import PageCommunity
import PageForum
import PageContribute
import PageLicense
import PageMarketing
import PageScreencasts

if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = os.getenv('SCGI_PORT', '8090')

CTK.run (port = int(port))
