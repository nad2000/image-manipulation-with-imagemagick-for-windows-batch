#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 18:13:46 2014

@author: rad.cirskis
"""

import tempfile
import utl

USAGE = """
USAGE:
 cartoon -P PASSWORD [-p PATTERN] [-n NUMLEVELS] [-e EDGEAMOUNT] [-b BRIGHTNESS] [-s SATURATION] INFILE OUTFILE
 cartoon -h|--help

OPTIONS:
 -p PATTERN     segmentation pattern (shape); 0<=integer<=100; [default: 70]
 -n NUMLEVELS   number of desired segmentation levels; integer>=2 [default: 6]
 -e EDGEAMOUNT  amount of edges; float>=0; [default: 4]
 -b BRIGHTNESS  brightness of cartoon; integer>=0; [default: 100]
 -s SATURATION  saturation of cartoon; integer>=0; [default: 100]
 -P PASSWORD    password for accessing the application
"""

def cartoon(pattern, numlevels, edgeamount, brightness, saturation, infile, outfile):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')
    tmpA2 = tempfile.mktemp(suffix='.mpc')
    tmpB2 = tempfile.mktemp(suffix='.cache')

    version  = utl.get_im_version()

    edgewidth = 2		# edge width; integer>=0
    edgethresh = 90		# edge threshold; 0<=integer<=100

    if (version < "06070607" or version > "06070707") and version <= "06080504":
        setcspace = ['-set', 'colorspace', 'RGB']
    else:
        setcspace = []

    if version <= "06070707" or version > "06080504":
        proc = ["-gamma", "2.2"]
    else:
        proc = ["-colorspace", "sRGB"]

    if version >= "06060806":
        medproc = ['-statistic', 'median', '3x3']
    else:
        medproc = ['-median', '3']

    utl.run_im([
        '-quiet', '-regard-warnings', infile, '+repage', '-depth', '8',
        '-selective-blur', '0x5+10%', tmpA1])

    # convert to grayscale and posterize to create mask image
    opt = [tmpA1, '-level', '0x'+pattern+'%'] +  setcspace + ['-colorspace', 'gray',
        '-posterize', numlevels, '-depth', '8',] + proc + [tmpA2]
    utl.run_im(opt)


    opt =  [
        tmpA1, '(', tmpA2, '-blur', '0x1', ')',
        '(', '-clone', '0', '-clone', '1', '-compose', 'over',
        '-compose', 'multiply', '-composite', '-modulate', brightness+','+saturation+',100', ')',
        '(', '-clone', '0',] + setcspace + [
        '-colorspace', 'gray', ')',
        '(', '-clone', '3', '-negate', '-blur', '0x'+str(edgewidth), ')',
	  '(', '-clone', '3', '-clone', '4', '-compose', 'over', '-compose', 'colordodge', '-composite',
        '-evaluate', 'pow', edgeamount, '-threshold', str(edgethresh)+'%'] + medproc + [
        ')', '-delete', '0,1,3,4', '-compose', 'over', '-compose', 'multiply', '-composite', outfile]

    utl.run_im(opt)

    utl.delete_tmp_files(tmpA1, tmpA2, tmpB1, tmpB2)


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    cartoon(
        pattern=o['-p'], numlevels=o['-n'], edgeamount=o['-e'],
        brightness=o['-b'], saturation=o['-s'],
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'),)
