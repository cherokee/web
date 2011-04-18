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
import Page
import Distro

URL_BASE = "/distribution"


P1 = """The Cherokee Web App Distribution is a worldwide effort to
eases the deployment of Web Applications. Independent contributors and
ISVs from all over the globe are working together in an open,
transparent and friendly manner to bring you this revolutionary way of
deploying Web applications."""

P2 = """It is specially interesting to notice that the project is
driven by its community. Everybody is welcome to join in!"""

MAINTAINERS_P1 = """A number of maintainers already work on this
project in order to brind you these packages. We'd like to take the
opportunity to thank them from these lines:"""


class Distribution:
    def __call__ (self):
        title = _("Web Applications Distribution")

        # Intro
        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>" %(title))
        page += CTK.RawHTML ("<p>%s</p>" %(P1))
        page += CTK.RawHTML ("<p>%s</p>" %(P2))

        # Apps
        page.sidebar += CTK.RawHTML ("<h2>Apps</h2>")
        page.sidebar += Distro.Apps_List()

        # Maintainers
        page += CTK.RawHTML ("<h2>Maintainer</h2>")
        page += CTK.RawHTML ("<p>%s</p>" %(MAINTAINERS_P1))
        page += CTK.RawHTML ("<p>%s</p>" %(MAINTAINERS_P1))
        page += Distro.Authors_List()

        return page.Render()


CTK.publish (r'^%s(\.html)?$'%(URL_BASE), Distribution)


