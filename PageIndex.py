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
import Twitter
import Commits
import Downloads
import MailingList

URL_LEARN_MORE = '/learn_more.html'


class Learn_More:
    def __call__ (self):
        cont = CTK.Container()
        cont += CTK.RawHTML ("This is still WIP")
        return cont.Render().toStr()


class Top_Banner (CTK.Box):
    H1 = "Evolved Web Infrastructure Software"
    P1 = "Cherokee is an innovative, feature rich, and yet easy to configure open source Web Server."

    def __init__ (self):
        CTK.Box.__init__ (self, {'id': 'sprint'})

        dialog = CTK.DialogProxyLazy (URL_LEARN_MORE)

        # Banner body
        box = CTK.Box ({'id': 'mainmsg'})
        box += CTK.RawHTML ('<h1>%s</h1>'%(self.H1))
        box += CTK.RawHTML ('<p>%s</p>'%(self.P1))

        # Download
        link = CTK.Link (None, props={'id': "overview"})
        link += CTK.RawHTML ("Learn More")
        link.bind ('click', dialog.JS_to_show())

        box += link
        self += box
        self += dialog


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

class Sidebox (CTK.Container):
    ELEMENTS = {
        'download': {
                        'icon': '/static/images/download.png',
                        'url': '/downloads.html',
                        'title': 'Download Cherokee %s'%(Downloads.get_latest_version()),
                        'hint': 'Fetch the latest version of Cherokee'
                    },
        'documentation': {
                        'icon': '/static/images/documentation.png',
                        'url': '/doc/index.html',
                        'title': 'Read the Documentation',
                        'hint': 'Tutorials, recipes, etc'
                    },
        'contribute': {
                        'icon': '/static/images/contribute.png',
                        'url': '/contribute.html',
                        'title': 'Contribute to the project',
                        'hint': 'Help us to develop a better server!'
                    }
    }

    class Element (CTK.Container):
        def __init__ (self, url, icon, title, hint):
            CTK.Container.__init__ (self)
            self += CTK.RawHTML ('<img src="%(icon)s" title="%(title)s"><a href="%(url)s">%(title)s</a><br/><span>%(hint)s</span>'%(locals()))

    def __init__ (self):
        CTK.Container.__init__ (self)

        l = CTK.List ()
        for k in self.ELEMENTS:
            url = self.ELEMENTS[k]['url']
            icon = self.ELEMENTS[k]['icon']
            title = self.ELEMENTS[k]['title']
            hint = self.ELEMENTS[k]['hint']
            l += self.Element (url, icon, title, hint)

        box = CTK.Box ({'id': 'main-links'})
        box += l
        self += box



class Home:
    def __call__ (self):
        page = Page.Page_Menu()
        page.banner += Top_Banner()

        main_box  = CTK.Box ({'id': 'index-main'})
        main_box += Highlights()
        page     += main_box

        side_box  = CTK.Box ({'id': 'index-sidebox'})
        side_box += Sidebox()
        page     += side_box

        page += CTK.Box({'class': 'clr'})

        bar3  = CTK.Box ({'class': 'bar3'})
        bar3 += Twitter.Latest_Tweets()
        page += bar3

        bar3  = CTK.Box ({'class': 'bar3'})
        bar3 += Commits.Latest_GIT_Commits()
        page += bar3

        bar3  = CTK.Box ({'class': 'bar3'})
        bar3 += MailingList.Latest_Mailing_List()
        page += bar3

        page += CTK.Box({'class': 'clr'})

        return CTK.HTTP_Cacheable (10, body=page.Render())


CTK.publish ('^/(index)?$',           Home)
CTK.publish ('^%s$'%(URL_LEARN_MORE), Learn_More)
