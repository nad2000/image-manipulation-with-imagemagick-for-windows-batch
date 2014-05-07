#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 18:13:46 2014

@author: rad.cirskis
"""

from docopt import docopt
import subprocess
import tempfile
import os

USAGE = """
USAGE:
 cartoon [-p PATTERN] [-n NUMLEVELS] [-e EDGEAMOUNT] [-b BRIGHTNESS] [-s SATURATION] -P PASSWORD INFILE OUTFILE
 cartoon -h,--help

OPTIONS:
 -p PATTERN     segmentation pattern (shape); 0<=integer<=100; [default: 70]
 -n NUMLEVELS   number of desired segmentation levels; integer>=2 [default: 6]
 -e EDGEAMOUNT  amount of edges; float>=0; [default: 4]
 -b BRIGHTNESS  brightness of cartoon; integer>=0; [default: 100]
 -s SATURATION  saturation of cartoon; integer>=0; [default: 100]
 -P PASSWORD    password for accessing the application
 """

PASSWORD = "p4s5w0rd"

if os.name == 'nt':
    IM_CMD = r'C:\Program Files (x86)\ImageMagick-6.8.9-Q16\convert.exe'
else:
    IM_CMD = 'convert'

#%%

def get_im_version():
    version = subprocess.check_output([IM_CMD, '-list', 'configure'])
    version = version[version.find('LIB_VERSION_NUMBER'):]
    version = version[:version.find('\n')]
    version = version.split()[1]
    version = ''.join(['0'+n if len(n) == 1 else n for n in version.split(',')])
    return version

#%%

# docopt(USAGE, ['-b', '123', '-P', 'p4sw0rd', 'IF', 'OF' ])

def run_im(opt):
    cmd = [IM_CMD]
    cmd += opt
    print ' '.join(cmd)
    subprocess.call(cmd)


def cartoon(pattern, numlevels, edgeamount, brightness, saturation, infile, outfile):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')
    tmpA2 = tempfile.mktemp(suffix='.mpc')
    tmpB2 = tempfile.mktemp(suffix='.cache')

    version  = get_im_version()

    edgewidth = 2			# edge width; integer>=0
    edgethresh = 90		# edge threshold; 0<=integer<=100

    run_im([
        '-quiet', '-regard-warnings', infile, '+repage', '-depth', '8',
        '-selective-blur', '0x5+10%', tmpA1])

    # convert to grayscale and posterize to create mask image
    run_im([tmpA1, '-level', '0x'+pattern+'%', '-colorspace', 'gray',
           '-posterize', numlevels, '-depth', '8', tmpA2])

    run_im([
        tmpA1, '-level', '0x'+pattern+'%', '-colorspace', 'gray', '-posterize', numlevels,
        '-depth', '8', tmpA2])

    opt =  [
        tmpA1, '(', tmpA2, '-blur', '0x1', ')',
        '(', '-clone', '0', '-clone', '1', '-compose', 'over',
        '-compose', 'multiply', '-composite', '-modulate', brightness+','+saturation+',100', ')',
        '(', '-clone', '0', '-colorspace', 'gray', ')',
        '(', '-clone', '3', '-negate', '-blur', '0x'+str(edgewidth), ')',
	  '(', '-clone', '3', '-clone', '4', '-compose', 'over', '-compose', 'colordodge', '-composite',
        '-evaluate', 'pow', edgeamount, '-threshold', str(edgethresh)+'%']

    if version >= "06060806":
        opt += ['-statistic', 'median', '3x3']
    else:
        opt += ['-median', '3']

    opt += [')', '-delete', '0,1,3,4', '-compose', 'over', '-compose', 'multiply', '-composite', outfile]

    run_im(opt)


if __name__ == "__main__":

    o = docopt(USAGE)
    #if o['-P'] != PASSWORD:
    #    raise Exception("Wrong password! Access denied!")

    cartoon(
        pattern=o['-p'], numlevels=o['-n'], edgeamount=o['-e'],
        brightness=o['-b'], saturation=o['-s'],
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'),)

