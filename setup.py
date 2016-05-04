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
VERSION = "3.04.0"
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

MANIFEST_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="*"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="%(level)s"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.30729.4918"
            processorArchitecture="X86"
            publicKeyToken="1fc8b3b9a1e18e3b"
            language="*"
        />
    </dependentAssembly>
    <!-- dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="*"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly -->
  </dependency>
</assembly>
'''

RT_BITMAP = 2
RT_MANIFEST = 24

def manifesest(prog_name):
    return (
        RT_MANIFEST, 1,
        (MANIFEST_TEMPLATE % 
            dict(prog="stainedglass", level="asInvoker")).encode("utf-8")
    )

    
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
        dict(
            script=prog_name + ".py",
            company_name="nowITworks (http://www.nowitworks.eu)",
            copyright=u"Radomirs Cirskis © 2014, 2015, 2016",
            legal_copyright=u"Radomirs Cirskis © 2014, 2015, 2016",
            legal_trademark="Radomirs Cirskis (rad AT nowitworks DOT eu)",
            product_version=VERSION,
            product_name=DESCRIPTION,
            icon_resources=[(1, "app.ico")],
            other_resources=[
                manifesest(prog_name),
                # for bitmap resources, the first 14 bytes must be skipped when reading the file:
                # (RT_BITMAP, 1, open("bitmap.bmp", "rb").read()[14:]),
                (u"VERSIONTAG", 1, VERSION)
            ]
        ) for prog_name in ["bg_removal", "clip", "gotham", "kelvin", "lomo", "nashville", "toaster", "stainedglass", "vintage1", "vintage2", "vintage3", "toycamera", "crossprocess", "sketch", "shapemorph", "thermography", "nightvision", "vignette", "cartoon", "remap",]
    ],
    options = {
        "py2exe": {
                "bundle_files": 1,
                #"compressed": True,
                "compressed": False,
                #"xref": True,
                #"optimize": "2",
                "dll_excludes": ["msvcr71.dll", "msvcp90.dll", "numpy-atlas.dll"],  # Exclude msvcr71
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
