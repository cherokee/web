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
import config

CACHE_EXPIRATION = 10 * 60 # 10mins
COMMENT_MAX_SIZE = 60

def run (cmd):
    f = os.popen ("cd '%s'; %s" %(config.GIT_CHEROKEE_LOCAL, cmd))
    cont = f.read()
    try:
        f.close()
    except:
        pass
    return cont

#
# Internals
#
def get_commit_list (num):
    # Update
    run ('git pull')

    # Query SVN server
    cont = run ('git log --branches --pretty=format:"%an||%ar||%s||%H" -'+str(num))

    # Parse
    parsed = []

    for line in cont.split('\n'):
        parts = line.split("||")
        if len(parts) != 4:
            continue

        parsed.append (parts)

    return parsed


#
# Widget
#
class Latest_GIT_Commits_Widget (CTK.Box):
    def __init__ (self, num=7):
        CTK.Box.__init__ (self, {'id': 'latest-commits'})

        self += CTK.Box({'class': 'bar3-title'}, CTK.RawHTML('<a href="https://github.com/cherokee/webserver/commits/dev" target="_blank">Latest Commits</a>'))

        for commit in get_commit_list (num):
            user    = commit[0]
            date    = commit[1]
            comment = commit[2]
            rev     = commit[3]

            if len(comment) > COMMENT_MAX_SIZE:
                comment = comment[:COMMENT_MAX_SIZE - 3] + "..."

            url = "https://github.com/cherokee/webserver/commit/" + rev
            content_box = CTK.Box({'class': 'commit'})

            date_box = CTK.Box({'class': 'date'})
            date_box += CTK.LinkWindow (url, CTK.RawHTML(date), {'title': rev})
            content_box += date_box

            commit_box = CTK.Box ({'class': 'commit-txt'}, CTK.RawHTML ('%(user)s: %(comment)s'%(locals())))
            content_box += commit_box

            self += content_box

        self += CTK.Box({'class': 'bar3-bottom-link'}, CTK.RawHTML('<a href="https://github.com/cherokee/webserver/commits/dev" target="_blank">View Commits Log &raquo;</a>'))


#
# Factory and cache
#
latest_widget            = None
latest_widget_expiration = None

def Latest_GIT_Commits():
    global latest_widget
    global latest_widget_expiration

    if not latest_widget or time.time() > latest_widget_expiration:
        latest_widget            = Latest_GIT_Commits_Widget()
        latest_widget_expiration = time.time() + CACHE_EXPIRATION

    return latest_widget
