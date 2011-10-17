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
import CTK
import Page

URL_BASE = "/screencasts"

DEPRECATED = "Beware: the graphical user interface shown in these videos is obsolete."

EMBED_VIDEO_HTML = """<iframe src="http://player.vimeo.com/video/%(num)s?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=1" width="640" height="480" frameborder="0" webkitAllowFullScreen allowFullScreen></iframe>"""

VIDEOS = [
    ('intro',        "30692102", "Introduction"),
    ('django_flup',  "30691538", "Django with Flup"),
    ('django_uwsgi', "30691738", "Djando with uWSGI"),
    ('php',          "30692492", "PHP"),
    ('rails',        "30692549", "Ruby on Rails"),
    ('streaming',    "30693094", "Media Streaming"),
    ('wordpress',    "30693162", "Wordpress"),
]

JS = """
var urlquery = location.href.split("#");
if (urlquery[1]) {
    window.location = urlquery[0] + '/' + urlquery[1];
}
"""

class PageScreencasts:
    def __call__ (self):
        title = "Screencasts"

        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>"%(title))

        # Sidebar
        page.sidebar += Menu()

        # Redirect the hashtag
        page += CTK.RawHTML (js=JS)

        # Content
        video = None
        tmp = re.findall (r'^%s.*/(.*)$'%(URL_BASE), CTK.request.url, re.I)
        if tmp:
            for v in VIDEOS:
                if v[0] == tmp[0].lower():
                    video = v
                    break
        if not video:
            video = VIDEOS[0]

        box  = CTK.Box ()
        box += CTK.RawHTML ('<h2>%s</h2>' %(video[2]))
        box += CTK.RawHTML (EMBED_VIDEO_HTML%({'num': video[1]}))
        box += CTK.RawHTML ('</br><p><b>%s</b></p>' %(DEPRECATED))

        page += box

        return CTK.HTTP_Cacheable (60, body=page.Render())


class Menu (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self)

        l = CTK.List()
        for v in VIDEOS:
            link = CTK.Link ("%s.html/%s" %(URL_BASE, v[0]))
            link += CTK.RawHTML (v[2])
            l += link

        self += CTK.RawHTML ('<h3>Screencasts</h3>')
        self += l


CTK.publish (URL_BASE, PageScreencasts)
