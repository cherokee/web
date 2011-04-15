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
import CTK
import time

SVN_QUERY_URL      = "svn://cherokee-project.com/"
SVN_HTTP_CHANGESET = "http://svn.cherokee-project.com/changeset"
CACHE_EXPIRATION   = 10 * 60 # 10mins


#
# Internals
#
def get_commit_list (num):
    # Query SVN server
    f = os.popen ("svn log %s --limit %d" %(SVN_QUERY_URL, num))
    lines = [x.strip() for x in f.readlines()]
    f.close()

    # Parse
    lines = filter(lambda x: x and x[0]=='r' and ' | ' in x, lines)
    lines = [x.split(' | ') for x in lines]
    return lines


#
# Widget
#
class Latest_SVN_Commits_Widget (CTK.Box):
    def __init__ (self, num=6):
        CTK.Box.__init__ (self, {'id': 'latest_svn_commit'})

        for commit in get_commit_list (num):
            rev  = commit[0]
            user = commit[1]
            date = commit[2].split('(')[1][:-1]
            url  = os.path.join (SVN_HTTP_CHANGESET, rev[1:])

            self += CTK.LinkWindow (url, CTK.RawHTML(rev))
            self += CTK.Box ({'class': 'details'}, CTK.RawHTML ('%(user)s | <b>%(date)s</b>'%(locals())))


#
# Factory and cache
#
latest_widget            = None
latest_widget_expiration = None

def Latest_SVN_Commits():
    global latest_widget
    global latest_widget_expiration

    if not latest_widget or time.time() > latest_widget_expiration:
        latest_widget            = Latest_SVN_Commits_Widget()
        latest_widget_expiration = time.time() + CACHE_EXPIRATION

    return latest_widget
