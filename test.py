#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    print "USAGE:"
    print "  %s /path/to/CTK" %(sys.argv[0])
    raise SystemExit

cwd     = os.getcwd()
ctk_dir = os.path.abspath (sys.argv[1])

# Read
cont = open ('cherokee.conf','r').read()
cont = cont.replace ('python CHEROKEE_WEB-server.py', 'python %s/CHEROKEE_WEB-server.py'%(cwd))
cont = cont.replace ('/change/CTK', '%s/static'%(ctk_dir))
cont = cont.replace ('/change/static', '%s/static'%(cwd))

# Write
open ('cherokee.conf.2', 'w+').write(cont)

# Execute
os.putenv("PYTHONPATH", "%s:%s"%(ctk_dir, os.getenv("PYTHONPATH", '')))
os.system ("cherokee -C cherokee.conf.2")
