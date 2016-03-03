#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 18:13:46 2014

@author: rad.cirskis
"""

import tempfile
import utl

USAGE = """
USAGE:
 sketch -P PASSWORD [-k KIND] [-e EDGE] [-c CON] [-s SAT] [-g] INFILE OUTFILE
 sketch -h|--help

OPTIONS:
 -k KIND      kind of grayscale conversion; options are gray(g) or
              desat(d); [default: desat]
 -e EDGE      edge coarseness; integer>0; [default: 4]
 -c CON       percent contrast change; integer>=0; [default: 25]
 -s SAT       percent saturation change; integer>=0; [default: 100]
 -g           output grayscale only
 -P PASSWORD  password for accessing the application
"""

def process(infile, outfile, kind='desat', edge='4', con='25', sat='100', gray=False):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')

    # test input image
    utl.run_im('-quiet', '-regard-warnings', infile, '+repage', tmpA1)

    if kind == "gray" or kind == 'g':
        grayscaling = ["-colorspace", "gray"]
    else:
        grayscaling = ["-modulate", "100,0,100"]

    # convert sat from percent change to absolute value for -modulate
    sat = int(sat) + 100

    # split contrast
    if int(con) <= 100:
        con1, con2 = int(con), 0
    else:
        con1, con2 = 100, int(con) - 100

    setcspace = utl.get_cspace_option()

    opt = [tmpA1,
        '(', '-clone', '0', grayscaling, ')',
        '(', '-clone', '1', '-negate', '-blur', '0x' + edge, ')',
        '(', '-clone', '1', '-clone', '2', setcspace, '-compose', 'color_dodge', '-composite',
          '-level', str(con2) + 'x100%', ')',
        '(', '-clone', '3', '-alpha', 'set', '-channel', 'a', '-evaluate', 'set', str(con1) + '%', '+channel', ')',
        '(', '-clone', '3', '-clone', '4',]

    if gray:
        opt += [setcspace, '-compose', 'multiply', '-composite', ')', '-delete', '0-4', outfile]
    else:
        opt += ['-compose', 'multiply', '-composite', ')',
        '(', '-clone', '0', '-modulate', '100,' + str(sat) + ',100', ')',
        '-delete', '0-4', setcspace, '-compose', 'screen', '-composite', outfile]

    utl.run_im(*opt)

    utl.delete_tmp_files(tmpA1, tmpB1)

if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        kind=o.get('-k', 'desat'), edge=o.get('-e', '4'), con=o.get('-c', '25'),
        sat=o.get('-s', '100'), gray=o.get('-g', False),
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
