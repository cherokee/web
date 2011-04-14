# -*- coding: utf-8 -*-

import CTK
import Page

class Home:
    def __call__ (self):
        page = Page.Page_Base()
        page += CTK.RawHTML ("testing")
        return page.Render()


CTK.publish ('^/(index)?$', Home)
