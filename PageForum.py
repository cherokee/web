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

URL_BASE = "/forums"

FORUM_EMBEDDABLE_HTML = """
<a id="nabblelink" href="http://cherokee-web-server-general.1049476.n5.nabble.com/">Cherokee Web Server - General</a>
<script src="http://cherokee-web-server-general.1049476.n5.nabble.com/embed/f4369600"></script>
"""

class PageForum:
    def __call__ (self):
        title = "Forums"

        page = Page.Page_Menu (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>"%(title))
        page += CTK.RawHTML (FORUM_EMBEDDABLE_HTML)

        return CTK.HTTP_Cacheable (60, body=page.Render())


CTK.publish (URL_BASE, PageForum)

