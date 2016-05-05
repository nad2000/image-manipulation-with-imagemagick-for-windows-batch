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
 thermography -P PASSWORD [-l LOWPT] [-H HIGHPT] INFILE OUTFILE
 thermography -h|-?|--help

OPTIONS:
 -l LOWPT     low point value on color table; float; 0<=integer<=100; [default: 0]
 -H HIGHPT    hight point value on color table; float; 0<=integer<=100; [default: 100]
 -P PASSWORD  password for accessing the application
"""

def process(infile, outfile, lowpt='0', highpt='100'):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')

    # test input image
    utl.run_im(
        '-quiet', '-regard-warnings', infile, utl.get_cspace_option(),
        '-colorspace', 'gray', '+repage', tmpA1)

    #convert lowpt and highpt to range and offset
    range_ = int(round(1000 * (int(highpt) - int(lowpt)) / 100., 0))
    offset = int(round(1000 * int(lowpt) / 100., 0))

    # note added $setcspace before -clut to fix bug between 6.8.4.0 and 6.8.4.10
    utl.run_im(
        tmpA1, '(', '-size','1x1', 'xc:blueviolet', 'xc:blue', 'xc:cyan', 'xc:green1', 'xc:yellow', 'xc:orange', 'xc:red',
        '+append', '-filter', 'Cubic', '-resize', '1000x1!', '-crop',
        "{}x{}+{}+0".format(range_, range_, offset), '+repage', '-resize', '1000x1!', ')',
        utl.get_cspace_option(), '-clut', outfile)

    utl.delete_tmp_files(tmpA1, tmpB1)

if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        lowpt=o.get('-l'), highpt=o.get('-H'),
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
