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
import ProudList

URL_BASE = "/community"

MAILING_P1 = 'The primary discussion forum for Cherokee community members is the <a href="http://lists.octality.com/">Cherokee Project\'s mailing lists</a>.'
MAILING_P2 = 'If you prefer a forums interface, you can interact with other Cherokee users and developers through the <a href="/forums.html">Forums interface</a> to our mailing lists.'
IRC_P1     = 'The Cherokee developers, as well as many members of the Cherokee user community, can be found online in the <a href="irc://irc.freenode.net/cherokee">#cherokee</a> IRC channel on the FreeNode IRC Network (servers: irc.freenode.net).'
SOCIAL_P1  = 'The Cherokee project has also presence in the following social networks. Please, do not hesitate to join us!'

class PageCommunity:
    def __call__ (self):
        title = "Community"

        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>"%(title))

        # Proud Cherokee Users List
        page.sidebar += CTK.RawHTML ('<h3>Proud Cherokee Users</h3>')
        page.sidebar += ProudList.Add_New_Domain()
        page.sidebar += ProudList.DomainList()

        # Content
        box  = CTK.Box ({'class': 'community-lists'})
        box += CTK.RawHTML ('<h2>Mailing Lists / Forums</h2>')
        box += CTK.RawHTML ('<p>%s</p>' %(MAILING_P1))
        box += CTK.RawHTML ('<p>%s</p>' %(MAILING_P2))
        page += box

        box  = CTK.Box ({'class': 'community-chat'})
        box += CTK.RawHTML ('<h2>IRC / Chat</h2>')
        box += CTK.RawHTML ('<p>%s</p>' %(IRC_P1))
        page += box

        box  = CTK.Box ({'class': 'community-social'})
        box += CTK.RawHTML ('<h2>Social Networks</h2>')
        l = CTK.List()
        l += CTK.LinkWindow ("http://www.github.com/cherokee", CTK.RawHTML("Github"), {'class': 'github-link'})
        l += CTK.LinkWindow ("http://www.twitter.com/webserver", CTK.RawHTML("Twitter"), {'class': 'twitter-link'})
        l += CTK.LinkWindow ("http://www.linkedin.com/groups/Cherokee-Web-Server-1819726", CTK.RawHTML("LinkedIn"), {'class': 'linkedin-link'})
        l += CTK.LinkWindow ("http://www.facebook.com/cherokee.project", CTK.RawHTML("Facebook"), {'class': 'fb-link'})
        box += CTK.RawHTML ('<p>%s</p>' %(SOCIAL_P1))
        box += l
        page += box

        return CTK.HTTP_Cacheable (60, body=page.Render())


CTK.publish (URL_BASE, PageCommunity)
