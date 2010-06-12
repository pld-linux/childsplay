#!/usr/bin/python

import os.path
import sys
import Version
import distutils
from distutils.core import setup
from distutils.sysconfig import get_python_lib
import os, glob, shutil


PREFIX = '/usr'

modulepaths = {'ALPHABETDIR':os.path.join(PREFIX, 'share', 'childsplay', 'alphabetsounds')}
modulepaths['BASEDIR'] = os.path.join(PREFIX, 'childsplay_sp')
modulepaths['SHARELIBDATADIR'] = "/usr/share/childsplay"
modulepaths['LOCALEDIR'] = "/usr/share/locale"
modulepaths['PYTHONCPDIR'] = os.path.join(get_python_lib(), 'childsplay_sp')

module = 'SPBasePaths.py'

filelines = ["# AUTO-GENERATED MODULE, DON'T EDIT", \
"# This module holds all the paths needed for childsplay.\n"]
for k, v in modulepaths.items():
	filelines.append("%s = '%s'" % (k, v))
f = open(module, 'w')
f.write("\n".join(filelines))
f.close()
sys.argv.insert(1, '--quiet')

DESCRIPTION = """childsplay is a collection of educational activities and
comes with extensive data collecting and multi user support."""
VERSION = Version.version
setup(name="childsplay_sp",
        version=VERSION,
        license="GPL",
        url="http://schoolsplay.sf.net",
        author="Stas Zytkiewicz",
        author_email="stas.zytkiewicz@gmail.com",
        description="Collection of educational activities",
        long_description=DESCRIPTION,
        packages=['childsplay_sp', 'childsplay_sp.gui', 'childsplay_sp.lib', \
            'childsplay_sp.ocempgui', \
            'childsplay_sp.ocempgui.access', 'childsplay_sp.ocempgui.draw', \
            'childsplay_sp.ocempgui.events', 'childsplay_sp.ocempgui.object', \
            'childsplay_sp.ocempgui.widgets', \
            'childsplay_sp.ocempgui.widgets.components', \
            'childsplay_sp.ocempgui.widgets.images', \
            'childsplay_sp.ocempgui.widgets.themes', \
            'childsplay_sp.ocempgui.widgets.themes.default'],
        package_dir={'childsplay_sp':''}
        )
