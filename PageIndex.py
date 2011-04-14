# -*- coding: utf-8 -*-

import CTK
import Page

class Top_Banner (CTK.Box):
    H1 = "Evolved Web Infrastructure Software"
    P1 = "Cherokee is an innovative, feature rich, and yet easy to configure open source Web Server."

    def __init__ (self):
        CTK.Box.__init__ (self, {'id': 'sprint'})

        latest_version = "X.Y.Z" # **TEMP**

        # Banner body
        box = CTK.Box ({'id': 'mainmsg'})
        box += CTK.RawHTML ('<h1>%s</h1>'%(self.H1))
        box += CTK.RawHTML ('<p>%s</p>'%(self.P1))

        # Download
        link = CTK.Link ("/cherokee-latest-tarball", props={'id': "download"})
        link += CTK.RawHTML ("<span>Get Cherokee</span><br/>Download Cherokee %(latest_version)s"%(locals()))
        box += link

        self += box


class Home:
    def __call__ (self):
        page = Page.Page_Menu()
        page += Top_Banner()

        return page.Render()


CTK.publish ('^/(index)?$', Home)
