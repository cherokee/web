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

URL_BASE = "/doc"

class Index (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self)

        local_file = os.path.join (config.DOC_LOCAL, "index.txt")
        lines = open(local_file,'r').readlines()

        n = 0
        while n < len(lines):
            line = lines[n].strip()

            if not line:
                n += 1
                continue
            elif line.startswith("=="):
                n += 1
                continue
            elif line.startswith("*"*10):
                # *********************************
                # link:basics.html[Getting started]: Cherokee basics
                # *********************************
                n += 1
                line = lines[n].strip()

                tmp = re.findall (r'link:(\S+)\[(.+)\](.*)$', line)
                if tmp:
                    self += CTK.RawHTML ('<h3><a href="%s">%s</a>%s</h3>' %(tmp[0][0], tmp[0][1], tmp[0][2]))
                else:
                    self += CTK.RawHTML ('<h3>%s</h3>' %(line))

                n += 2
                continue
            elif line.startswith(". "):
                #
                # . link:dev_quickstart.html[Quickstart]: Where to start?.
                # . link:dev_debug.html[Debugging]: Resources available to debug Cherokee.
                #
                l = CTK.List()
                self += l

                while True:
                    tmp = re.findall (r'link:(\S+)\[(.+)\](.*)$', line)
                    l += CTK.RawHTML ('<a href="%s">%s</a>%s' %(tmp[0][0], tmp[0][1], tmp[0][2]))
                    n += 1

                    if lines[n].startswith(". "):
                        line = lines[n].strip()
                        continue
                    else:
                        break
            else:
                n+= 1


        self += CTK.RawHTML ("index")


class PageDoc:
    def __call__ (self):
        # Handle request
        if CTK.request.url in ('/doc', '/doc/', '/doc/index', '/doc/index.html'):
            request = "/doc/index.html"
            sidebar = False
        else:
            request = CTK.request.url
            sidebar = True

        tmp = re.findall (r'^%s/(.+\.html)'%(URL_BASE), request)
        if not tmp:
            return CTK.HTTP_Response (404)
        help_file = tmp[0]

        # Title
        title = help_file.replace ('_', ' ').replace('.html', '') + ": Documentation"
        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>Documentation</h1>")

        # Security check
        local_file = os.path.abspath (os.path.join (config.DOC_LOCAL, help_file))
        if not local_file.startswith (config.DOC_LOCAL):
            page += CTK.RawHTML ('no way')
            return page.Render()

        if not os.path.exists(local_file):
            return CTK.HTTP_Response (404)

        # Read it
        html = open(local_file, 'r').read()
        body = html [html.find ('<body>')+6 : html.find('</body>')]

        # Layout
        if sidebar:
            page.sidebar += Index()

        page += CTK.RawHTML (body)
        return CTK.HTTP_Cacheable (60, body=page.Render())


class PageMedia:
    def __call__ (self):
        tmp = re.findall (r'^%s(/media/.*)$'%(URL_BASE), CTK.request.url)
        if not tmp:
            return HTTP_Error (404)

        local_file = config.DOC_LOCAL + tmp[0]
        return CTK.HTTP_XSendfile (local_file)


CTK.publish (URL_BASE,              PageDoc)
CTK.publish ('^%s/media'%(URL_BASE), PageMedia)
