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

import CTK
import Page
import Downloads

class Top_Banner (CTK.Box):
    H1 = "Evolved Web Infrastructure Software"
    P1 = "Cherokee is an innovative, feature rich, and yet easy to configure open source Web Server."

    def __init__ (self):
        CTK.Box.__init__ (self, {'id': 'sprint'})

        latest_version = Downloads.get_latest_version()

        # Banner body
        box = CTK.Box ({'id': 'mainmsg'})
        box += CTK.RawHTML ('<h1>%s</h1>'%(self.H1))
        box += CTK.RawHTML ('<p>%s</p>'%(self.P1))

        # Download
        link = CTK.Link ("/downloads.html", props={'id': "download"})
        link += CTK.RawHTML ("<span>Get Cherokee</span><br/>Download Cherokee %(latest_version)s"%(locals()))
        box += link

        self += box


class Highlights (CTK.Container):
    H2 = "Features Highlights"

    FEATURES = {
        'Modern Technologies': "Cherokee supports the most widespread Web technologies: FastCGI, SCGI, PHP, uWSGI, SSI, CGI, LDAP, TLS/SSL, HTTP proxying, Video streaming, Content caching, Traffic Shaping, etc.",
        'Cross Platform':      "Cherokee runs on Linux, MacOS X, Solaris, and BSD. A native Windows port is on the works.",
        'User friendly':       "All the configuration is done through Cherokee-Admin, a beautiful and powerful Web interface.",
        'Web Apps repository': "Cherokee allows to deploy Web Apps optimally, in seconds, with just a few mouse clicks."
    }

    class Feature (CTK.Container):
        def __init__ (self, name, description):
            CTK.Container.__init__ (self)
            self += CTK.RawHTML ('<strong>%(name)s</strong><br/><span>%(description)s</span>'%(locals()))

    def __init__ (self):
        CTK.Container.__init__ (self)
        self += CTK.RawHTML('<h2>%s</h2>' %(self.H2))

        l = CTK.List ({'class': 'list'})
        for k in self.FEATURES:
            l += self.Feature (k, self.FEATURES[k])

        box = CTK.Box ({'id': 'features'})
        box += l
        self += box


class Home:
    def __call__ (self):
        page = Page.Page_Menu()
        page += Top_Banner()
        page += Highlights()
        return page.Render()


CTK.publish ('^/(index)?$', Home)
