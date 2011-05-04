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
import Ohloh

URL_BASE = "/contribute"

INTRO_P1 = "The Cherokee Project is a diverse community of people from around the world. You don't have to be a networking guru or a skilled C developer to get involved."
INTRO_P2 = "Come join our community, and contribute in any way you like:"

HELP_P1 = 'There are several active communities where you can discuss what is going on in Cherokee and help out other Cherokee users. We have mailing lists, IRC channels and forums. Please have a look at the <a href="/community.html">communication channels</a> for an overview.'
L10N_P1 = 'Get involved by making Cherokee available in your language. You are welcome to contribute with any of the existing translations. The following <a href="/download/trunk/cherokee.pot">Pot file</a> is available for new translations as well.'
CODE_P1 = 'Developers can help Cherokee by adding new features, making our technology faster and making development easier for others.'
MRKT_P1 = 'Help us spread the word about how Cherokee is helping to evolve the Web towards efficiency, scalability, and management simplicity.'
MRKT_P2 = 'Attend FOSS events as part of the Cherokee community. Publicize Cherokee  in media, at fairs and other events, etc. Take part in creating content and coordinating activities for special marketing initiatives.'

DEV_P1 = "Before we can incorporate significant contributions, certain legal requirements must be met."
DEV_P2 = 'We believe it is important to continue distributing Cherokee under a <a href="/license.html">Free Software license</a> and a unified copyright, so both the project and its users are as safe against legal threats.'
DEV_P3 = "Everybody who contributes code to Cherokee is going to be asked to sign a Contribute Agreement. The main to reasons for requiring contributors to sign this document are: First, it protects the project against any legal issue as to the origins and ownership of any particular piece of code contributed."
DEV_P4 = "Second, the Contributor Agreement also ensures that once you have provided a contribution, you cannot try to withdraw permission for its use at a later date. People and companies can therefore use Cherokee, confident that they will not be asked to stop using pieces of the code at a later date."
DEV_P5 = "Please, follow the following steps to submit us your Contributor Agreement:"

DEV_L1 = 'It is available as <a href="/static/doc/Cherokee_Contribution_Agreement_v1.pdf">PDF</a> and <a href="/static/doc/Cherokee_Contribution_Agreement_v1.odt">OpenDocument</a> files.'
DEV_L2 = 'Print out the document and sign it.'
DEV_L3 = 'Scan and email the document to alvaro@alobbs.com'


class PageContribute:
    class ListEntry (CTK.Box):
        def __init__ (self, title, p_list):
            CTK.Box.__init__ (self)
            self += CTK.RawHTML ('<p><b>%s</b>: %s</p>' %(title, p_list[0]))
            for p in p_list[1:]:
                self += CTK.RawHTML ('<p>%s</p>' %(p))

    def __call__ (self):
        title = "Contributing with the Cherokee Project"

        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>"%(title))

        page.sidebar += Ohloh.Cocomo()
        page.sidebar += Ohloh.Languages()

        # Intro
        page += CTK.RawHTML ('<p>%s</p>' %(INTRO_P1))
        page += CTK.RawHTML ('<p>%s</p>' %(INTRO_P2))

        # Ways to contribute
        l = CTK.List()
        l += self.ListEntry ("Helping Users", [HELP_P1])
        l += self.ListEntry ("Localization",  [L10N_P1])
        l += self.ListEntry ("Coding",        [CODE_P1])
        l += self.ListEntry ("Marketing",     [MRKT_P1, MRKT_P2])
        page += l

        # Contributor Agreement
        page += CTK.RawHTML ('<h2>Cherokee Contributor Agreement</h2>')
        page += CTK.RawHTML ('<p>%s</p>' %(DEV_P1))
        page += CTK.RawHTML ('<p>%s</p>' %(DEV_P2))
        page += CTK.RawHTML ('<p>%s</p>' %(DEV_P3))
        page += CTK.RawHTML ('<p>%s</p>' %(DEV_P4))
        page += CTK.RawHTML ('<p>%s</p>' %(DEV_P5))

        l = CTK.List()
        l += self.ListEntry ("Download the Document", [DEV_L1])
        l += self.ListEntry ("Sign it",               [DEV_L2])
        l += self.ListEntry ("Submit it",             [DEV_L3])
        page += l

        # Bug Reports
        page += CTK.RawHTML ('<h2>Report of Issues</h2>')


        return CTK.HTTP_Cacheable (60, body=page.Render())


CTK.publish (URL_BASE, PageContribute)
