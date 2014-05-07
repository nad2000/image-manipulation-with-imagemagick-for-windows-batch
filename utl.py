# -*- coding: utf-8 -*-


import subprocess
import os

if os.name == 'nt':
    import distutils.spawn
    IM_CMD = distutils.spawn.find_executable("convert")
else:
    IM_CMD = 'convert'

#%%
im_version = None

def get_im_version():
    global im_version
    if im_version is None:
        version = subprocess.check_output([IM_CMD, '-list', 'configure'])
        version = version[version.find('LIB_VERSION_NUMBER'):]
        version = version[:version.find('\n')]
        version = version.split()[1]
        version = ''.join(['0'+n if len(n) == 1 else n for n in version.split(',')])
        im_version = version
    return im_version

#%%

# docopt(USAGE, ['-b', '123', '-P', 'p4sw0rd', 'IF', 'OF' ])

def run_im(opt):
    cmd = [IM_CMD]
    cmd += opt
    print ' '.join(cmd)
    subprocess.call(cmd)
