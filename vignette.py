#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 18:13:46 2014

@author: rad.cirskis
"""

import tempfile
import utl

USAGE = """
USAGE:
    vignette -P PASSWORD [-i INNER] [-o OUTER] [-f FEATHER] [-c COLOR] [-a AMOUNT] INFILE OUTFILE

OPTIONS:
 -i INNER      inner radius of vignette where not darkened;
               integer percent of image dimension [default: 0]
 -o OUTER      outer radius of vignette where darkest;
               integer percent of image dimension; [default: 150]
 -f FEATHER    feathering amount for inner radius; float>=0 [default: 0]
 -c COLOR      vignette color; any IM opaque color. [default: black]
 -a AMOUNT     vignette amount; 0<=integer<=0. [default: 100]
 -P PASSWORD   password for accessing the application
"""

def process(infile, outfile, inner=0, outer=150, feather=0, color='black', amount=100, show=False):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')

    # test input image
    utl.run_im('-quiet', '-regard-warnings', infile, '+repage', tmpA1)

    ww, hh = utl.get_dim(tmpA1)
    wwo, hho = float(outer) * ww / 100, float(outer) * hh / 100
    mwh = float(outer) * min(ww, hh) / 100

    if inner == '0':
        mlevel = []
    else:
        inner = 100 - int(inner)
        mlevel = ['-level', "0x{}%".format(inner)]

    if amount == '100':
        plevel = []
    else:
        amount = 100 - int(amount)
        plevel = ['+level', "{}x100%".format(amount)]

    # setup feathering
    if feather == '0':
        feathering = []
    else:
        feathering = ['-blur', feather + "x65000"]

    utl.run_im(
        '-background', color, tmpA1,
        '(', '-size', "{}x{}".format(mwh, mwh), 'radial-gradient:',
        '-resize',  "{:.0f}x{:.0f}!".format(wwo, hho), '-gravity', 'center',
        '-crop', "{}x{}+0+0".format(ww, hh), '+repage', mlevel, plevel, feathering,
        ')', utl.get_cspace_option(), '-alpha', 'off', '-compose', 'copy_opacity', '-composite',
         '-compose', 'over', '-flatten', outfile)

    utl.delete_tmp_files(tmpA1, tmpB1)

if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        inner=o['-i'], outer=o['-o'], feather=o['-f'], color=o['-c'], amount=o['-a'],
        show=o.get('-s'), infile=o.get('INFILE'), outfile=o.get('OUTFILE'),)
