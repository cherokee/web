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
import Page
import config

URL_BASE = "/marketing"


CLARIFICATION_TEXT = [
'As far as we can tell, the project is not affiliated, related to, or endorsed in any manner by the <a href="http://en.wikipedia.org/wiki/Cherokee" rel="nofollow" target="_blank">Cherokee Nation</a> (Tsálăgĭ/Tsárăgĭ).',
'The project was named at its inception following the tradition in Hacker Culture to name Web servers after Native American Nations, and of course nor is -or ever was- meant to be disrespectful in any way.',
'Being a project with World-wide scope, the Community of users and developers of the Cherokee Project is multicultural and multiethnical in nature. As such, no cultural discrimination or disrespect is acceptable or will be tolerated within the project. It is our whole hearted sentiment that both the name and logo of the project fully comply with the above-mentioned directives, and if anything, should be understood as a humble token of our appreciation for these values.',
'The Cherokee Project logo represents a smiling kid, running fast, trying to emulate a plane. Its aim is to represent a few of the most wonderful things in life: youth, happiness, and fun. There is nothing to read in between lines, but we acknowledge that it is hardly possible to please everyone. Native Americans are deservedly proud of their heritage. The Cherokee Project does not represent the Cherokee Nation in any manner, and as such we can not accept any recognition addressed to them.'
]


class Clarification (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self)

        self += CTK.RawHTML ('<h2>Regarding the name and logo for the Cherokee Project</h2>')
        for l in CLARIFICATION_TEXT:
            self += CTK.RawHTML ('<p>%s</p>'%(l))


class Logo (CTK.Box):
    def __init__ (self, image_name, comments):
        CTK.Box.__init__ (self)

        c1 = CTK.Container()
        c1 += CTK.Link("/download/misc/logos/%s.png"%(image_name), CTK.RawHTML("PNG Image"))
        c1 += CTK.RawHTML (": %s" %(comments[0]))

        c2 = CTK.Container()
        c2 += CTK.Link("/download/misc/logos/%s.svg"%(image_name), CTK.RawHTML("SVG Graphic"))
        c2 += CTK.RawHTML (": %s" %(comments[1]))

        l = CTK.List()
        l += c1
        l += c2

        self += CTK.Image ({'src': '/static/images/%s-mini.png'%(image_name)})
        self += l

class PageMarketing:
    def __call__ (self):
        title = "Marketing and Branding"

        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>"%(title))

        # Logos
        page += CTK.RawHTML ('<h2>Logos</h2>')
        page += Logo("cherokee",        ["8000 x 3109px, 460Kb", "Vectorial, 27Kb"])
        page += Logo("cherokee-border", ["8000 x 5333px, 721Kb", "Vectorial, 102Kb"])

        # Clarification
        page += Clarification()

        return CTK.HTTP_Cacheable (60, body=page.Render())


CTK.publish (URL_BASE, PageMarketing)
