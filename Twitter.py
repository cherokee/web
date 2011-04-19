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
import time
import feedparser

MAX_SZ           = 52
SKIP_SZ          = 11
LIMIT            = 6
TWITTER_URL      = "http://twitter.com/statuses/user_timeline/18079288.rss?count=%d" % (LIMIT)
URL_RE           = '((https?|s?ftp|ssh)://[^"\s\<\>]*[^.,;">\:\s\<\>\)\]\!])'
CACHE_EXPIRATION = 15 * 60 # 10mins


def to_url(url):
    url = url.group(0)
    return '<a href="%s">%s</a>' % (url,url)


#
# Widget
#
class Latest_Tweets_Widget (CTK.Box):
    def __init__ (self, num=6):
        CTK.Box.__init__ (self, {'id': 'latest_tweets'})

        self += CTK.Box({'class': 'sidetitle'}, CTK.RawHTML('Latest Tweets'))

        content_box = CTK.Box({'class': 'sidecontent'})

        # Query
        data = feedparser.parse (TWITTER_URL)
        if data['bozo'] == 1:
            return None

        # Parse
        rc = re.compile(URL_RE)

        for entry in data['entries']:
            link = CTK.util.to_utf8(entry['link'])
            date = CTK.util.to_utf8(entry['updated']).split(', ')[1].split('+')[0]

            # Tidy up (before reformatting URLs).
            text = entry['summary'][SKIP_SZ:]
            if len(text) > MAX_SZ:
                text = text[:MAX_SZ-3] + "..."

            tweet = rc.sub (to_url, text)

            # Layout
            date_box = CTK.Box({'class': 'tweet-date'})
            date_box += CTK.LinkWindow (link, CTK.RawHTML(date))

            content_box += CTK.RawHTML (tweet)
            content_box += date_box
        
        self += content_box


#
# Factory and cache
#
latest_widget            = None
latest_widget_expiration = None

def Latest_Tweets():
    global latest_widget
    global latest_widget_expiration

    if not latest_widget or time.time() > latest_widget_expiration:
        latest_widget            = Latest_Tweets_Widget()
        latest_widget_expiration = time.time() + CACHE_EXPIRATION

    return latest_widget
