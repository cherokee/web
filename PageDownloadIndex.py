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
from config import *

URL_BASE = "/download"

def sort_files (x, y):
    x_is_dir = os.path.isdir(x)
    y_is_dir = os.path.isdir(y)
    if x_is_dir and not y_is_dir:
        return 1
    elif y_is_dir and not x_is_dir:
        return -1
    elif y_is_dir and x_is_dir:
        return cmp(x,y)
    return cmp(x,y)


class Index (CTK.Box):
    def __init__ (self, web_path):
        CTK.Box.__init__ (self)

        self += CTK.RawHTML ('<h1>Index of %s</h1>'%(web_path or "/"))

        if web_path.count('/') >= 1:
            up_dir = os.path.realpath (URL_BASE + web_path + "/../")
            self += CTK.Link (up_dir, CTK.RawHTML(_("Parent Directory")))
            self += CTK.RawHTML ("<br/>")

        fp = os.path.join (DOWNLOADS_LOCAL, "."+web_path)

        files = os.listdir (fp)
        files.sort (sort_files)

        for f in files:
            link = os.path.join (URL_BASE, '.'+web_path, f)

            self += CTK.Link (link, CTK.RawHTML(f))
            self += CTK.RawHTML ("<br/>")


class Dispatcher:
    def __call__ (self):
        title = _("Cherokee Project Downloads")

        # Page
        page = Page.Page_Menu (title=title)

        # Dispatcher
        tmp = re.findall (r'%s/(.*)$'%(URL_BASE), CTK.request.url)
        if not tmp:
            page += Index('/')
            return page.Render()

        # Check path
        path = tmp[0]
        fp = os.path.realpath (os.path.join (DOWNLOADS_LOCAL, path))
        if not fp.startswith (DOWNLOADS_LOCAL):
            page += CTK.RawHTML ("Nice try")
            return page.Render()

        if not os.path.exists (fp):
            return CTK.HTTP_Response (404)

        # It is a directory
        if os.path.isdir (fp):
            page += Index (fp[len(DOWNLOADS_LOCAL):])
            return page.Render()

        return CTK.HTTP_XSendfile (fp)


CTK.publish (r'^%s'%(URL_BASE), Dispatcher)
