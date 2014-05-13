#-------------------------------------------------------------------------------
# Name:  setup.py
# Purpose:
#   Image Batch Editing With ImageMagick setup
#
# Author:   Radomirs Cirskis
#
# Created:  2014-05-02
# Licence:  WTFPL
#-------------------------------------------------------------------------------

# Configuration settings:
NAME = 'EditImageWithIM'
DESCRIPTION = 'Image Batch Editing With ImageMagick'
VERSION = '0.04'
WEBSITE = 'http://www.nowITworks.eu'
PUBLISHER = WEBSITE
REVISION = NAME + ' ' + VERSION
AUTHOR = 'Radomirs Cirskis'
COPYRIGHT ="(c) 2014, Radomirs Cirskis",

with open('config.nsh', 'w') as nsh:
    print >>nsh, """
    !define PRODUCT_NAME "%s"
    !define PRODUCT_VERSION "%s"
    !define PRODUCT_PUBLISHER "%s"
    !define PRODUCT_WEB_SITE "%s"
    !define PRODUCT_SHORT_NAME "%s"
    """ % (
        DESCRIPTION,
        VERSION,
        PUBLISHER,
        WEBSITE,
        NAME,)

from distutils.core import setup
import os
import py2exe
#import glob
#import shutil
#import sys

#sys.path.insert(0,os.getcwd())

def get_files(dir):
    # dig looking for files
    a= os.walk(dir)
    b = True
    filenames = []

    while (b):
        try:
            (dirpath, dirnames, files) = a.next()
            filenames.append([dirpath, tuple(files)])
        except:
            b = False
    return filenames

#class Target:
#    def __init__(self,**kw):
#        self.__dict__.update(kw)
#        self.version        = VERSION
#        self.name           = NAME
#        self.description    = DESCRIPTION

#my_com_server_target = Target(
#    description    = DESCRIPTION,
#    service = ["service_module"],
#    modules = ["service_module"],
#    create_exe = True,
#    create_dll = True)

print 'Compiling as a Windows executable ...'
#setup(console = ['cartoon.py'], options = {'py2exe': {'bundle_files': 1, 'compressed': True}})

setup(
    name = NAME,
    description = DESCRIPTION,
    version = VERSION,
    author = AUTHOR,
    author_email = 'nad2000 AT gmail DOT com',
    maintainer = AUTHOR,
    maintainer_email = 'nad2000 AT gmail DOT com',
    url = WEBSITE,
    license = 'WTFPL',
    console = [
        {'script': 'crossprocess.py', 'icon_resources': [(1, 'app.ico')],},
        {'script': 'sketch.py', 'icon_resources': [(1, 'app.ico')],},
        {'script': 'thermography.py', 'icon_resources': [(1, 'app.ico')],},
        {'script': 'nightvision.py', 'icon_resources': [(1, 'app.ico')],},
        {'script': 'vignette.py', 'icon_resources': [(1, 'app.ico')],},
        {'script': 'cartoon.py', 'icon_resources': [(1, 'app.ico')],},
        {'script': 'remap.py', 'icon_resources': [(1, 'app.ico')],},
    ],
    options = {'py2exe': {'bundle_files': 1, 'compressed': True, "optimize": '2'}},
    #zipfile=None
)


#setup(
#    name = NAME,
#    description = DESCRIPTION,
#    version = VERSION,
#    console = [{'script': 'cartoon.py', 'icon_resources': [(1, 'app.ico')],}],
#    options = {'py2exe': {'bundle_files': 1, 'compressed': True, "optimize": '2'}},
#    zipfile=None)


#setup(
#    name = NAME,
#    description = DESCRIPTION,
#    version = VERSION,
#    console = [{
#        'script': 'cartoon.py',
#        'icon_resources': [(1, 'app.ico')],
#        #'other_resources': [(u"VERSIONTAG", 1, REVISION)],
#    }],
#    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
#    zipfile=None,
#
##	options = {
##	    "py2exe":{
##		'packages': 'encodings',
##		#'includes': 'win32com,win32service,win32serviceutil,win32event',
##		"optimize": '2'
##	    },
##	},
#)
