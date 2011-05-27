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

import re
import os
import CTK
import Page
import Downloads
import Mirror_Sites

MACOSX_TITLE  = N_("Download Cherokee for MacOS X")
LINUX_TITLE   = N_("Download Cherokee for Linux")
SOURCE_TITLE  = N_("Install Cherokee for the Source Code")
WINDOWS_TITLE = N_("Download Cherokee for Window")

URL_BASE      = "/downloads"
URL_MACOSX    = "/downloads/macosx"
URL_MACOSX_2  = "/downloads/macosx/2"
URL_LINUX     = "/downloads/linux"
URL_WINDOWS   = "/downloads/windows"
URL_SOURCE    = "/downloads/source"
URL_VIDEO1    = "/downloads/video/1"

OS_OPTIONS = [
    ('macosx',  N_('MacOS X')),
    ('linux',   N_('Linux')),
    ('windows', N_('Windows')),
    ('source',  N_('Source Code')),
]

DOC_APTGET = 'http://www.cherokee-project.com/doc/basics_installation_unix.html#APT'

class OS_Combo (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self)
        self.os_selected = None

        agent = CTK.request.headers.get ('HTTP_USER_AGENT').lower()

        # Select entry
        combo_props = {'name': 'os_combo'}

        if 'linux' in agent:
            self.os_selected = 'linux'

        if not self.os_selected:
            for key in ('macintosh', 'mac os', 'macos'):
                if key in agent:
                    self.os_selected = 'macosx'
                    break

        if not self.os_selected:
            for key in ('windows', 'net clr'):
                if key in agent:
                    self.os_selected = 'windows'
                    break

        if not self.os_selected:
            for key in ('sunos', 'solaris'):
                if key in agent:
                    self.os_selected = 'source'
                    break

        if not self.os_selected:
            self.os_selected = 'source'

        combo_props['selected'] = self.os_selected
        self.combo = CTK.Combobox (combo_props, OS_OPTIONS)

        # Combo
        self += CTK.RawHTML ("<span>%s: </span>" %(_("Platform")))
        self += self.combo


class Download_MacOSX:
    def __call__ (self):
        # Find the DMG file
        dmg_refs = Downloads.get_latest_macosx_dmg()
        dmg_local, dmg_web = dmg_refs
        dmg_url = "http://www.cherokee-project.com%s"%(dmg_web)

        if os.path.exists (dmg_local):
            mbs = os.path.getsize (dmg_local) / (1024**2)
        else:
            mbs = 0
        ver = re.findall (r'(\d+\.\d+\.\d+)', dmg_web)[0]

        download_button = CTK.Button ('Get Cherokee %s DMG'%(ver)) # — %sMb'%(mbs))
        download_button.bind ('click', CTK.DruidContent__JS_to_goto (download_button.id, URL_MACOSX_2))

        content = CTK.Container()
        content += CTK.RawHTML ('<h3>Binary Package</h3>')
        content += CTK.RawHTML ('<p>%s</p>'%(_("A binary package for MacOS X (Intel) is available for download: %sMb"%(mbs))))
        content += download_button

        return content.Render().toStr()


class Download_MacOSX_2:
    def __call__ (self):
        content = CTK.Box({'id': 'macosx-steps'})
        content += CTK.RawHTML ('<h3>MacOS X (Intel)</h3>')

        # Find the DMG file
        dmg_refs = Downloads.get_latest_macosx_dmg()
        dmg_local, dmg_web = dmg_refs
        dmg_url = "http://www.cherokee-project.com%s"%(dmg_web)
        content += CTK.RawHTML (js='setTimeout(function(){ %s }, 2000);' %(CTK.JS.GotoURL(dmg_url)))

        # Step 1
        box = CTK.Box({'class': 'macosx-step'})
        box += CTK.RawHTML ('<strong>%s</strong>' %(_("Step 1")))
        box += CTK.Image({'src': "/static/images/dmg1.png"})
        box += CTK.RawHTML ('<span>%s</span>' %(_("Save and Open the Cherokee installer")))
        content += box

        # Step 2
        box = CTK.Box({'class': 'macosx-step'})
        box += CTK.RawHTML ('<strong>%s</strong>' %(_("Step 2")))
        box += CTK.Image({'src': "/static/images/dmg2.png"})
        box += CTK.RawHTML ('<span>%s</span>' %(_("Install the package")))
        content += box

        # Step 3
        box = CTK.Box({'class': 'macosx-step'})
        box += CTK.RawHTML ('<strong>%s</strong>' %(_("Step 3")))
        box += CTK.Image({'src': "/static/images/dmg3.png"})
        box += CTK.RawHTML ('<span>%s</span>' %(_("Drag Cherokee Admin to your application folder")))
        content += box

        # Step 4
        box = CTK.Box({'class': 'macosx-step'})
        box += CTK.RawHTML ('<strong>%s</strong>' %(_("Step 4")))
        box += CTK.Image({'src': "/static/images/dmg4.png"})
        box += CTK.RawHTML ('<span>%s</span>' %(_("Open Cherokee Admin")))
        content += box

        return content.Render().toStr()


class Download_Source:
    def __call__ (self):
        tarball_refs = Downloads.get_latest_tarball()
        tar_local, tar_web = tarball_refs

        # Automatic
        content = CTK.Container()
        content += CTK.RawHTML ("<h3>%s</h3>" %(_("Option 1: Automatic installation")))

        box  = CTK.Box()
        box += CTK.RawHTML ('<p>%s</p>' %(_('Open a terminal and enter:')))
        box += CTK.RawHTML ('<pre class="terminal">wget http://cherokee-project.com/install && python install</pre>')
        box += CTK.RawHTML ('<p>%s</p>' %(_('or')))
        box += CTK.RawHTML ('<pre class="terminal">curl -LO http://cherokee-project.com/install && python install</pre>')
        box += CTK.RawHTML ('<p>%s</p>' %(_('This will download and install Cherokee under /opt/cherokee')))
        content += box

        # By hand
        content += CTK.RawHTML ("<h3>%s</h2>" %(_("Option 2: Compile it by hand")))

        sources  = CTK.Box()
        sources += CTK.RawHTML ('%s '%(_("Download")))
        sources += CTK.Link (tar_web, CTK.RawHTML (_("latest source code package")))
        sources += CTK.RawHTML (', and install it by hand doing the configure, make, make install dance')
        sources += CTK.RawHTML ('<pre class="terminal">configure --prefix=/usr --localstatedir=/var --sysconfdir=/etc<br/>make && sudo make install</pre>')
        content += sources

        return content.Render().toStr()


class Download_Windows:
    def __call__ (self):
        content = CTK.Container()
        content += CTK.RawHTML ("<h3>%s</h3>" %(_("Windows packages coming soon...")))
        content += CTK.RawHTML ('<p>%s<br/>%s</p>' %(_('We are working really hard to provide native Windows packages soon.'),
                                                     _('Native Windows installers are expected by Summer 2011.')))
        return content.Render().toStr()


class Download_Linux:
    def __call__ (self):
        content = CTK.Container()

        # Ubuntu
        box = CTK.Box({'class': 'platform', 'id': 'platform-ubuntu'})
        box += CTK.RawHTML ('<h3>Ubuntu</h3>')
        box += CTK.RawHTML ('Open a terminal and enter:')
        box += CTK.RawHTML ('<pre class="terminal">sudo add-apt-repository ppa:cherokee-webserver/ppa</pre>')
        box += CTK.RawHTML ('After that, you should tell your system to pull down the latest list of software from each archive it knows about, including the PPA you just added:')
        box += CTK.RawHTML ('<pre class="terminal">sudo apt-get update</pre>')
        box += CTK.RawHTML ("Now you're ready to install Cherokee from the PPA:")
        box += CTK.RawHTML ('<pre class="terminal">sudo apt-get install cherokee cherokee-admin</pre>')
        content += box

        # Debian
        box = CTK.Box({'class': 'platform', 'id': 'platform-debian'})
        box += CTK.RawHTML ('<h3>Debian</h3>')
        box += CTK.RawHTML ('Install Cherokee from the apt repository')
        box += CTK.RawHTML ('<pre class="terminal">apt-get install cherokee cherokee-admin</pre>')
        details = CTK.Box({'class': 'platform-details'})
        details += CTK.RawHTML ('%s '%(_('Please, check the documentation for further')))
        details += CTK.LinkWindow (DOC_APTGET, CTK.RawHTML(_('details')))
        details += CTK.RawHTML ('.')

        box += details
        content += box
        return content.Render().toStr()

class Development_Version (CTK.Box):
    def __init__ (self):
        CTK.Box.__init__ (self, {'class': 'download-svn-box'})
        self += CTK.RawHTML ('<h2>%s</h2>' %("Development Snapshots"))
        self += CTK.RawHTML ("You can also retrieve the current development sources ")
        self += CTK.Link ("/svn.html", CTK.RawHTML ("using SVN"))
        self += CTK.RawHTML (" or downloading the ")
        self += CTK.Link ("/download/trunk/cherokee-latest-svn.tar.gz", CTK.RawHTML ("latest SVN snapshot"))
        self += CTK.RawHTML (".")


class QuickStart:
    def __call__ (self):
        title = _("Quickstart Guide")

        # Install Cherokee
        os_combo = OS_Combo()
        druid    = CTK.Druid (CTK.RefreshableURL ('%s/%s'%(URL_BASE, os_combo.os_selected)))

        box  = CTK.Box ({'id': 'platform-box'})
        box += os_combo

        step1  = CTK.Box({'id': 'qs-step-1', 'class': 'qs-step'})
        step1 += box
        step1 += CTK.RawHTML ('<h2>%s</h2>' %(_("Install Cherokee")))
        step1 += druid
        os_combo.bind ('change', druid.JS_to_goto('"%s/"+$("#%s").val()' %(URL_BASE, os_combo.combo.id)))

        # Page
        page = Page.Page_Menu_Side (title=title)
        page += CTK.RawHTML ("<h1>%s</h1>" %(title))
        page  += step1

        # Development version
        page.sidebar += Development_Version()

        # Mirros
        mirrors = Mirror_Sites.Mirrors()
        page.sidebar += mirrors

        # This page cannot be cached. It'd break the OS detection.
        return page.Render()


CTK.publish (r'^%s(\.html)?$'%(URL_BASE), QuickStart)
CTK.publish (r'^%s'  %(URL_MACOSX),       Download_MacOSX)
CTK.publish (r'^%s/2'%(URL_MACOSX),       Download_MacOSX_2)
CTK.publish (r'^%s'  %(URL_LINUX),        Download_Linux)
CTK.publish (r'^%s'  %(URL_SOURCE),       Download_Source)
CTK.publish (r'^%s'  %(URL_WINDOWS),      Download_Windows)
