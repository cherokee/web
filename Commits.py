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
COMMENT_MAX_SIZE   = 52

#
# Internals
#
def get_commit_list (num):
    # Query SVN server
    f = os.popen ("svn log %s --limit %d" %(SVN_QUERY_URL, num))
    cont = f.read()
    try:
        f.close()
    except:
        pass

    # Parse
    parsed = []

    log_entries = cont.split("-"*72)
    for entry in log_entries:
        if not entry.strip():
            continue

        parts = entry.split("\n", 2)[1:]
        parts[0] = parts[0].split(' | ')
        parts[1] = parts[1].strip().replace('\n', ' ')
        parsed.append (parts)

    return parsed


#
# Widget
#
class Latest_SVN_Commits_Widget (CTK.Box):
    def __init__ (self, num=6):
        CTK.Box.__init__ (self, {'id': 'latest-commits'})

        self += CTK.Box({'class': 'bar3-title'}, CTK.RawHTML('<a href="http://svn.cherokee-project.com/log.php?repname=Cherokee&path=%2F&rev=6636&isdir=1" target="_blank">Latest Commits</a>'))

        for commit in get_commit_list (num):
            rev     = commit[0][0]
            user    = commit[0][1]
            month   = commit[0][2].split('(')[1][8:11]
            day     = commit[0][2].split('(')[1][5:7]
            date    = month + " " + day

            comment = commit[1]

            url  = os.path.join (SVN_HTTP_CHANGESET, rev[1:])

            if len(comment) > COMMENT_MAX_SIZE:
                comment = comment[:COMMENT_MAX_SIZE - 3] + "..."

            content_box = CTK.Box({'class': 'commit'})

            date_box = CTK.Box({'class': 'date'})
            date_box += CTK.LinkWindow (url, CTK.RawHTML(date), {'title': rev})
            content_box += date_box

            commit_box = CTK.Box ({'class': 'commit-txt'}, CTK.RawHTML ('%(user)s: %(comment)s'%(locals())))
            content_box += commit_box

            self += content_box

        self += CTK.Box({'class': 'bar3-bottom-link'}, CTK.RawHTML('<a href="http://svn.cherokee-project.com/log.php?repname=Cherokee&path=%2F&rev=6636&isdir=1" target="_blank">View Commits Log &raquo;</a>'))


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
