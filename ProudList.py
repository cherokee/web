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
import xmlrpclib

URL_NEW_SUBMIT = '/proud/apply'

CACHE_EXPIRATION = 15 * 60 # 10mins
URL_OPEN         = 'http://www.octality.com/api/v2/open/proud'

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
        try:
            domains = cPickle.load (open (config.PROUD_PICKLE, 'r'))
        except (IOError, EOFError) as e: # This exception means a corrupt pickle failed to load
            # log the exception and assume an empty list
			sys.stderr.write("Error: Can't unpickle proud domain list.\n%s\n"%(e,))
            domains = []

        domains_clean = filter (lambda d: d['publish'], domains)
        domains_clean.sort (domain_cmp)
        if not domains_clean: # puke in the napkin, politely
            domains_clean = [{'domain':'Sorry: list broken!', 'page_rank':0}]

        # Render the domain list
        l = CTK.List()
        for domain in domains_clean:
            l += CTK.Box ({'class': 'domain domain-PR%s'%(domain['page_rank'])}, CTK.RawHTML(domain['domain']))

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


class Add_New_Domain (CTK.Box):
    P1 = """Submit the form and if your site is running Cherokee it
    will be listed. Sites are sorted by popularity and, among sites in
    the same league, are listed in alphabetical order."""

    REPORT_OK_JS = """
    $('#%s').html ($('#%s').val() + " added succesfully.");
    """

    REPORT_FAIL_JS = """
    $('#%s').html ("Couldn't add " + $('#%s').val());
    """

    class Apply:
        def __call__ (self):
            domain = CTK.post.get_val('new_domain')

            xmlrpc = xmlrpclib.ServerProxy (URL_OPEN)
            try:
                reply = xmlrpc.add_domain (domain)
            except xmlrpclib.Fault, err:
                return {'ret':'error', 'errors': {'new_domain': err.faultString}}
            except Exception, e:
                return {'ret':'error', 'errors': {'new_domain': str(e)}}

            return CTK.cfg_reply_ajax_ok()

    def __init__ (self):
        CTK.Box.__init__ (self, {'class': 'add_new_domain'})

        # Dialog
        field  = CTK.TextField ({'name': 'new_domain', 'class': 'noauto'})
        add    = CTK.SubmitterButton ("Add")
        report = CTK.Box()

        box = CTK.Box()
        box += field
        box += add
        box += report

        submit = CTK.Submitter (URL_NEW_SUBMIT)
        submit += box
        submit.bind ('submit_success',
                     self.REPORT_OK_JS%(report.id, field.id) +
                     field.JS_to_clean())
        submit.bind ('submit_fail',
                     self.REPORT_FAIL_JS%(report.id, field.id))

        coll = CTK.CollapsibleEasy (('Add your domain…','Add your domain…'))
        coll += CTK.RawHTML ('<p>%s</p>' %(self.P1))
        coll += submit

        self += coll


CTK.publish ('^%s$'%(URL_NEW_SUBMIT), Add_New_Domain.Apply, method="POST")
