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
import urllib
import feedparser

ML_RSS_URL       = "http://groups.google.com/group/cherokee-http/feed/atom_v1_0_msgs.xml?num=50"
CACHE_EXPIRATION = 30 * 60  #30mins


#
# Internals
#
def get_mailing_list_subjects():
    # Fetch
    d = feedparser.parse (ML_RSS_URL)

    # Parse
    subjects     = {}
    subject_list = []
    month_link   = ''
    month_page   = ''

    for entry in d['entries']:
        date   = entry['updated'][:10]
        author = entry['author']
        nick   = author.split(' ')[0]
        link   = 'http://lists.octality.com/pipermail/cherokee/%s/thread.html' % (time.strftime("%Y-%B", time.strptime(date, "%Y-%m-%d")))
        if month_link != link:
            month_link = link
            month_page = urllib.urlopen(month_link).read()

        # Clean title
        title = entry['title']
        if title.lower().startswith("re: "):
            title = title[4:]
        if title.lower().startswith("[cherokee] "):
            title = title[11:]
        if len(title) > 45:
            title = title[:45] + " .."

        # Clean author
        n = author.find ('(')
        if n != -1:
            author = author[:n-1]

        if not subjects.has_key(title):
            subjects[title] = {'hits':1}
            subject_list.append(title)
        else:
            subjects[title]['hits'] += 1
        if not subjects[title].has_key('date'):
            subjects[title]['date'] = date
        if not subjects[title].has_key('authors'):
            subjects[title]['authors'] = []
        if not nick in subjects[title]['authors']:
            subjects[title]['authors'] += [nick]
        if not subjects[title].has_key('link'):
            try:
                thread_link = get_thread_link (month_page, title[:45])
                link = link.split('thread.html')[0] + thread_link
            except:
                pass
            subjects[title]['link'] = link

    return (subjects, subject_list)


#
# Widget
#
class Latest_Mailing_List_Widget (CTK.Box):
    def __init__ (self, limit=6):
        CTK.Box.__init__ (self, {'id': 'mailing_list_widget'})

        self += CTK.Box({'class': 'sidetitle'}, CTK.RawHTML('Mailing List'))

        content_box = CTK.Box({'class': 'sidecontent'})


        ret = get_mailing_list_subjects()
        subjects, subject_list = ret

        for s in subject_list[:limit]:
            subject = subjects[s]
            authors = '(%s)'  %(', '.join(subject['authors']))

            box = CTK.Box({'class': 'ml-entry'})
            box += CTK.RawHTML ('%s | %s messages | <b>%s</b>'%(authors, subject['hits'], subject['date']))

            content_box += CTK.LinkWindow (subject['link'], CTK.RawHTML(s))
            content_box += box

        self += content_box


#
# Factory and cache
#
latest_widget            = None
latest_widget_expiration = None

def Latest_Mailing_List():
    global latest_widget
    global latest_widget_expiration

    if not latest_widget or time.time() > latest_widget_expiration:
        latest_widget            = Latest_Mailing_List_Widget()
        latest_widget_expiration = time.time() + CACHE_EXPIRATION

    return latest_widget
