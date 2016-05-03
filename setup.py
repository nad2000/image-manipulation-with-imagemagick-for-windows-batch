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

from __future__ import print_function

# Configuration settings:
NAME = "EditImageWithIM"
DESCRIPTION = "Image Batch Editing With ImageMagick"
VERSION = "3.03.2"
WEBSITE = "http://www.nowITworks.eu"
PUBLISHER = WEBSITE
REVISION = NAME + " " + VERSION
AUTHOR = "Radomirs Cirskis"
COPYRIGHT ="(c) 2014, 2015, 2016 Radomirs Cirskis",

with open("config.nsh", "w") as nsh:
    print("""
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
        NAME,), file=nsh)

from distutils.core import setup
import os
import py2exe
#import glob
#import shutil
#import sys

#sys.path.insert(0, os.getcwd())

def get_files(dir):
    # dig looking for files
    a= os.walk(dir)
    b = True
    filenames = []

    while (b):
        try:
            (dirpath, dirnames, files) = next(a)
            filenames.append([dirpath, tuple(files)])
        except:
            b = False
    return filenames


print("Compiling as a Windows executable ...")
#setup(console = ["cartoon.py"], options = {"py2exe": {"bundle_files": 1, "compressed": True}})

#NB! FIX/WORKAROUND: with missing DLLs, copy them to C:\Python27\DLLs
setup(
    name = NAME,
    description = DESCRIPTION,
    version = VERSION,
    author = AUTHOR,
    author_email = "nad2000 AT gmail DOT com",
    maintainer = AUTHOR,
    maintainer_email = "nad2000 AT gmail DOT com",
    url = WEBSITE,
    license = "WTFPL",
    console = [
        {"script": "clip.py", "icon_resources": [(1, "app.ico")],},
        {"script": "gotham.py", "icon_resources": [(1, "app.ico")],},
        {"script": "kelvin.py", "icon_resources": [(1, "app.ico")],},
        {"script": "lomo.py", "icon_resources": [(1, "app.ico")],},
        {"script": "nashville.py", "icon_resources": [(1, "app.ico")],},
        {"script": "toaster.py", "icon_resources": [(1, "app.ico")],},
        {"script": "stainedglass.py", "icon_resources": [(1, "app.ico")],},
        {"script": "vintage1.py", "icon_resources": [(1, "app.ico")],},
        {"script": "vintage2.py", "icon_resources": [(1, "app.ico")],},
        {"script": "vintage3.py", "icon_resources": [(1, "app.ico")],},
        {"script": "toycamera.py", "icon_resources": [(1, "app.ico")],},
        {"script": "crossprocess.py", "icon_resources": [(1, "app.ico")],},
        {"script": "sketch.py", "icon_resources": [(1, "app.ico")],},
        {"script": "shapemorph.py", "icon_resources": [(1, "app.ico")],},
        {"script": "thermography.py", "icon_resources": [(1, "app.ico")],},
        {"script": "nightvision.py", "icon_resources": [(1, "app.ico")],},
        {"script": "vignette.py", "icon_resources": [(1, "app.ico")],},
        {"script": "cartoon.py", "icon_resources": [(1, "app.ico")],},
        {"script": "remap.py", "icon_resources": [(1, "app.ico")],},
    ],
    options = {
        "py2exe": {
                "bundle_files": 1,
                #"compressed": True,
                "compressed": False,
                #"xref": True,
                #"optimize": "2",
                "dll_excludes": ["msvcr71.dll"],  # Exclude msvcr71
                "excludes": [
                    "pywin", "pywin.debugger", "pywin.debugger.dbgcon",
                    "pywin.dialogs", "pywin.dialogs.list",
                    "Tkconstants", "Tkinter", "tcl", "tkinter", "PyQt5",
                    "_ssl",  # Exclude _ssl
                    "pyreadline",
                    #"difflib",
                    "doctest",
                    #"locale",
                    "optparse",
                    #"pickle",
                    #"calendar"
                 ],
                "packages": ["moviepy"],
            },
        },
    #zipfile=None,
    zipfile="shared\\shared.lib",
    data_files = [("shared", ["Kelvin.jpg", "Nashville.jpg"])],
)


#setup(
#    name = NAME,
#    description = DESCRIPTION,
#    version = VERSION,
#    console = [{"script": "cartoon.py", "icon_resources": [(1, "app.ico")],}],
#    options = {"py2exe": {"bundle_files": 1, "compressed": True, "optimize": "2"}},
#    zipfile=None)


#setup(
#    name = NAME,
#    description = DESCRIPTION,
#    version = VERSION,
#    console = [{
#        "script": "cartoon.py",
#        "icon_resources": [(1, "app.ico")],
#        #"other_resources": [(u"VERSIONTAG", 1, REVISION)],
#    }],
#    options = {"py2exe": {"bundle_files": 1, "compressed": True}},
#    zipfile=None,
#
##	options = {
##	    "py2exe":{
##		"packages": "encodings",
##		#"includes": "win32com,win32service,win32serviceutil,win32event",
##		"optimize": "2"
##	    },
##	},
#)
