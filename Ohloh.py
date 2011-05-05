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

LANGUAGES_HTML = '<script type="text/javascript" src="http://www.ohloh.net/p/3906/widgets/project_languages.js"></script>'
COCOMO_HTML    = '<script type="text/javascript" src="http://www.ohloh.net/p/3906/widgets/project_cocomo.js"></script>'

COCOMO_FIX_JS = """
  /* Come on! $55k? Seriously? It must be a typo.. */
  $('.ohloh-cocomo-box input:text').filter(function() { return $(this).val() == "55000"; }).each(function() {
    $(this).val (90000);
    $(this).trigger ('change');
  });
"""

class Languages (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self, {'class': 'ohloh-languages-box'})
        self += CTK.RawHTML (LANGUAGES_HTML)
        self += CTK.RawHTML (js = COCOMO_FIX_JS)

class Cocomo (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self, {'class': 'ohloh-cocomo-box'})
        self += CTK.RawHTML (COCOMO_HTML)
        self += CTK.RawHTML (js = COCOMO_FIX_JS)


