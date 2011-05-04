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
import time
import Page
import config
import cPickle

CACHE_EXPIRATION = 15 * 60 # 10mins


DOMAIN_CLICK_JS = """
$(".domain").click (function (event) {
    var domain = $(this).text();

    event.preventDefault();
    event.stopPropagation();
    window.open ("http://" + domain + "/", '_blank');
});
"""

def domain_cmp (x, y):
    if y['page_rank'] == x['page_rank']:
        return cmp (x['domain'], y['domain'])

    return cmp (y['page_rank'], x['page_rank'])


class DomainList_Widget (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self, {'class': 'domain_list'})

        # Load, filter and sort the domain list
        domains = cPickle.load (open (config.PROUD_PICKLE, 'r'))
        domains_clean = filter (lambda d: d['publish'], domains)
        domains_clean.sort (domain_cmp)

        # Render the domain list
        l = CTK.List()
        for domain in domains_clean:
            l += CTK.Box ({'class': 'domain domain-PR%s'%(domain['page_rank'])}, CTK.RawHTML(domain['domain']))

        self += CTK.RawHTML ("<h3>Proud Cherokee Users</h3>")
        self += l
        self += CTK.RawHTML (js = DOMAIN_CLICK_JS)


#
# Factory and cache
#
latest_widget            = None
latest_widget_expiration = None

def DomainList():
    global latest_widget
    global latest_widget_expiration

    if not latest_widget or time.time() > latest_widget_expiration:
        latest_widget            = DomainList_Widget()
        latest_widget_expiration = time.time() + CACHE_EXPIRATION

    return latest_widget
