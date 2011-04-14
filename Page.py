# -*- coding: utf-8 -*-

import os
import CTK

#
# Base classes
#
class Page_Base (CTK.Page):
    def __init__ (self, title=None, body_id='body-cherokee', **kwargs):
        # Load the theme
        srcdir = os.path.dirname (os.path.realpath (__file__))
        theme_file = os.path.join (srcdir, 'theme.html')
        template = CTK.Template (filename=theme_file)

        # Build the page title
        if title:
            full_title = '%s: %s' %(_("Cherokee Project"), title)
        else:
            full_title = _("Cherokee Market")

        template['title'] = full_title
        if body_id:
            template['body_props'] = ' id="%s"'%(body_id)

        # Constructor
        CTK.Page.__init__ (self, template, None, None, **kwargs)
