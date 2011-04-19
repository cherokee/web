# -*- coding: utf-8 -*-

import os
import CTK

#
# Widgets
#
class MenuBar (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self, {'id': 'bar'})

        link = CTK.Link ("/", CTK.Image({'src': "/static/images/logo.png"}))
        self += CTK.Box ({'id': 'logo'}, link)

        nav =  CTK.Box ({'id': 'nav'})

        l = CTK.List()
        l += CTK.Link ("/downloads.html",  CTK.RawHTML("Download"))
        l += CTK.Link ("/doc/",            CTK.RawHTML("Documentation"))
        l += CTK.Link ("/community.html",  CTK.RawHTML("Community"))
        l += CTK.Link ("/Contribute.html", CTK.RawHTML("Contribute"))
        nav += l

        self += nav

class Footer (CTK.Box):
    ALVARO_URL = "http://www.linkedin.com/profile/view?id=19919180"

    def __init__ (self):
        CTK.Box.__init__ (self, {'id': 'footer'})

        box  = CTK.Box ({'id': 'footer-inner'})
        box += CTK.RawHTML ('Obviously powered by Cherokee!<br/>')
        box += CTK.RawHTML ('&copy; 2001-2010 ')
        box += CTK.LinkWindow (self.ALVARO_URL, CTK.RawHTML('Alvaro Lopez Ortega'))
        self += box


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
            full_title = _("Cherokee Web Server")

        template['title'] = full_title
        if body_id:
            template['body_props'] = ' id="%s"'%(body_id)

        # Constructor
        CTK.Page.__init__ (self, template, None, None, **kwargs)

#
# Pages
#
class Page_Menu (Page_Base):
    def __init__ (self, *args, **kwargs):
        Page_Base.__init__ (self, *args, **kwargs)

        # Add MenuBar
        Page_Base.__iadd__ (self, MenuBar())

        # Main Container (tricky)
        self.container = CTK.Box ({'id': 'container'})
        Page_Base.__iadd__ (self, self.container)

    def __iadd__ (self, widget):
        self.container += widget
        return self

    def Render (self):
        Page_Base.__iadd__ (self, Footer())
        return Page_Base.Render (self)


#
# Pages Sidebar
#
class Page_Menu_Side (Page_Menu):
    def __init__ (self, *args, **kwargs):
        Page_Menu.__init__ (self, *args, **kwargs)
        self.main    = CTK.Box({'id': 'main_area'})
        self.sidebar = CTK.Box({'id': 'sidebar'})

        Page_Menu.__iadd__ (self, self.sidebar)
        Page_Menu.__iadd__ (self, self.main)

    def __iadd__ (self, widget):
        self.main += widget
        return self
