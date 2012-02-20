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
import stat
import time
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

def prettySize(size):
    suffixes = [("B",2**10), ("K",2**20), ("M",2**30), ("G",2**40), ("T",2**50)]
    for suf, lim in suffixes:
        if size > lim:
            continue
        else:
            return round(size/float(lim/2**10),2).__str__()+suf


class Index (CTK.Box):
    def __init__ (self, web_path):
        CTK.Box.__init__ (self)

        self += CTK.RawHTML ('<h1 class="download-index-title">Index of %s</h1>'%(web_path or "/"))

        table = CTK.Table({'class': 'download-index-table'})
        table.set_header (row=True, num=1)
        table += [CTK.RawHTML(_("Name")), CTK.RawHTML(_("Last Modification")), CTK.RawHTML(_("Size"))]

        if web_path.count('/') >= 1:
            up_dir = os.path.realpath (URL_BASE + web_path + "/../")
            table += [CTK.Link (up_dir, CTK.RawHTML(_("Parent Directory")))]

        local_path = os.path.join (DOWNLOADS_LOCAL, "."+web_path)

        files = os.listdir (local_path)
        files.sort (sort_files)

        cont = CTK.Container()
        for f in files:
            row       = []
            local_fp  = os.path.join (local_path, f)
            file_stat = os.stat (local_fp)

            link  = os.path.join (URL_BASE, '.'+web_path, f)
            cont += CTK.Link (link, CTK.RawHTML(f))
            row  += cont
            cont.Empty()

            # Date and hour
            date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime (file_stat[stat.ST_MTIME]))
            cont    += CTK.RawHTML(date_str)
            row     += cont
            cont.Empty()

            # Size / <DIR>
            if os.path.isdir(local_fp):
                cont += CTK.RawHTML("&lt;DIR&gt;")
            else:
                size  = prettySize(file_stat[stat.ST_SIZE])
                cont += CTK.RawHTML(size)

            row += cont
            cont.Empty()

            table += row

        self += table


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
