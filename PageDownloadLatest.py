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
import Downloads
from config import *

URL_LATEST  = '/cherokee-latest-tarball'
URL_INSTALL = '/install'

class Redirect_to_Latest_Tarball:
    def __call__ (self):
        tarball_refs = Downloads.get_latest_tarball()
        tar_local, tar_web = tarball_refs
        return CTK.HTTP_Redir (tar_web)

class XSendfile_Installer:
    def __call__ (self):
        fp = os.path.join (GIT_INSTALLER_LOCAL, "install.py")
        return CTK.HTTP_XSendfile (fp)


CTK.publish ('^%s$'%(URL_LATEST),  Redirect_to_Latest_Tarball)
CTK.publish ('^%s$'%(URL_INSTALL), XSendfile_Installer)
