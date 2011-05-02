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
import os
import CTK
import Page
import time
import stat
import cPickle


CACHE_EXPIRATION = 15 * 60 # 10mins


class Mirrors_Widget (CTK.Box):
    class Mirror_Entry (CTK.Box):
        def __init__ (self, mirror):
            CTK.Box.__init__ (self, {'class': 'mirror-entry'})
            assert (type(mirror) == dict)

            self += CTK.Image({'src': "/static/images/flags/%s.png" %(mirror['code'])})
            self += CTK.LinkWindow (mirror['http'], CTK.RawHTML (mirror['http']))

    def __init__ (self):
        CTK.Box.__init__ (self, {'class': 'mirrors-list'})

        if not os.path.exists ("mirrors.pickle"):
            self += CTK.RawHTML ('<h1>ERROR: Mirrors status file not found</h1>')
            self += CTK.RawHTML ("<p>The <i>mirrors.pickle</i> file was not found. Please, run 'mirrors_checker.py' to create it.</p>")
            return

        mirrors = cPickle.load (open ("mirrors.pickle", 'r'))

        # Mirror List
        l_ok = CTK.List()
        l_no = CTK.List()
        for mirror in mirrors:
            if not mirror['error'] and mirror['up_to_date']:
                l_ok += self.Mirror_Entry (mirror)
            else:
                l_no += self.Mirror_Entry (mirror)

        self += CTK.RawHTML ('<h2>Mirrors</h2>')
        self += l_ok
        self += CTK.RawHTML ('<h3>Outdates mirrors</h3>')
        self += l_no

        # Last Checked
        mtime = os.stat ("mirrors.pickle").st_mtime
        delta = int(time.time() - mtime)

        days    = delta / (60 * 60 * 24)
        hours   = (delta / (60 * 60)) % 24
        minutes = (delta / (60)) % 60
        secs    = delta % 60

        delta_parts = []
        if days:
            delta_parts.append ('%s days'%(days))
        if hours:
            delta_parts.append ('%s hours'%(hours))
        if minutes:
            delta_parts.append ('%s minutes'%(minutes))
        if secs:
            delta_parts.append ('%s seconds'%(secs))

        delta_fmt = ''
        if len(delta_parts) > 1:
            delta_fmt = ', '.join (delta_parts[:-1]) + ' and '
        delta_fmt += delta_parts[-1]

        self += CTK.Box ({'class': 'updated'}, CTK.RawHTML ("Updated %s away" %(delta_fmt)))



#
# Factory and cache
#
latest_widget            = None
latest_widget_expiration = None

def Mirrors():
    global latest_widget
    global latest_widget_expiration

    if not latest_widget or time.time() > latest_widget_expiration:
        latest_widget            = Mirrors_Widget()
        latest_widget_expiration = time.time() + CACHE_EXPIRATION

    return latest_widget
