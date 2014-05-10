# -*- coding: utf-8 -*-

import subprocess
import os
import sys
from docopt import docopt
from cStringIO import StringIO
from math import sqrt

import conf

if os.name == 'nt':
    import distutils.spawn
    IM_CMD = distutils.spawn.find_executable("convert")
else:
    IM_CMD = 'convert'

verbose = False


def get_args(usage):

    global verbose

    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.pop(sys.argv.index("--verbose"))

    o = docopt(usage)
    print o

    if o['-P'] != conf.PASSWORD:
        #raise Exception("Wrong password! Access denied!")
        print "Wrong password! Access denied!"
        exit(-1)

    return o

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


def get_colors(file_name):

    lines = subprocess.check_output([
        IM_CMD, file_name, '-alpha', 'off', '-depth', '8', '-format', '%c',
        '-define','histogram:unique-colors=true','histogram:info:-'])

    return [map(
        int,
        l[l.find('(')+1:l.find(')')].replace(' ', '').split(',')) for l in StringIO(lines) if '(' in l]

#%%


def color_num(file_name):

    return int(subprocess.check_output([IM_CMD, file_name, '-format', '"%k"', 'info:']).strip('"\' \t\n\r'))

def get_dim(file_name):

    return tuple(
        map(int,subprocess.check_output([IM_CMD, file_name, '-format', '"%wx%h"', 'info:']).strip('"\' \t\n\r').split('x')))

def get_cspace_option():
    """
    colorspace RGB and sRGB swapped between 6.7.5.5 and 6.7.6.7
    though probably not resolved until the latter
    then -colorspace gray changed to linear between 6.7.6.7 and 6.7.8.2
    then -separate converted to linear gray channels between 6.7.6.7 and 6.7.8.2,
    though probably not resolved until the latter
    so -colorspace HSL/HSB -separate and -colorspace gray became linear
    but we need to use -set colorspace RGB before using them at appropriate times
    so that results stay as in original script
    The following was determined from various version tests using nightvision.
    with IM 6.7.4.10, 6.7.6.10, 6.8.3.2
    """
    version  = get_im_version()

    if (version < "06070607" or version > "06070707") and version <= "06080504":
        return ['-set', 'colorspace', 'RGB']
    else:
        return []


#%%

def run_im(opt):

    global verbose

    cmd = [IM_CMD]
    cmd += opt
    if verbose:
        print ' '.join(cmd)

    subprocess.call(cmd)


def delete_tmp_files(*files):

    for f in files:
        try:
            os.remove(f)
        except:
            pass


def rgb_dist(c, m):
    return sqrt(sum((_[0]-_[1])**2 for _ in zip(c,m)))


def lum(color):
    R, G, B = color
    return 0.299 * R + 0.587 * G + 0.114 * B


def rgbl_dist(c, m):
    c_R, c_G, c_B = c
    m_R, m_G, m_B = m
    return sqrt(
        (0.299 * ((c_R - m_R) ** 2)
        + 0.587 * ((c_G - m_G) ** 2)
        + 0.114 * ((c_B - m_B) ** 2)) * 0.75
        + (lum(c) - lum(m)) ** 2)
