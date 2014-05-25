#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 18:13:46 2014

@author: rad.cirskis (nad2000 AT gmail DOT com)
"""

import tempfile
import utl

USAGE = """
USAGE:
 crossprocess -P PASSWORD [-r RAMT] [-g GAMT] [-b BAMT] [-B BRIGHT] [-C CONTRAST] INFILE OUTFILE
 crossprocess -h|-help

OPTIONS:
 -r RAMT      red sigmoidal-contrast amount; -100<=integer<=100; [default: 0] (no change)
 -g GAMT      green sigmoidal-contrast amount; -100<=integer<=100; [default: 0] (no change)
 -b BAMT      blue sigmoidal-contrast amount; -100<=integer<=100; [default: 0] (no change)
 -B BRIGHT    post process brightness adjust; -100<=integer<=100; [default: 0] (no change)
 -C CONTRAST  post process contrast adjust; -100<=integer<=100; [default: 0] (no change)
 -P PASSWORD  password for accessing the application
"""


def process(infile, outfile, ramt='0', gamt='0', bamt='0', bright='0', contrast='0'):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')

    # scaling factor for contrast amounts
    div = 5

    # test input image
    utl.run_im('-quiet', '-regard-warnings', infile, '+repage', tmpA1)

    for color, amt in dict(R=int(ramt), G=int(gamt), B=int(bamt)).iteritems():
        if amt == 0:
            continue

        amt_ = round(abs(amt) / div, 4)

        utl.run_im(
            tmpA1, '-channel', color, ('+' if amt < 0 else '-') + 'sigmoidal-contrast',
            "{},50%".format(amt_), '+channel', tmpA1)

    utl.run_im(tmpA1, '-brightness-contrast', "{},{}".format(bright, contrast), outfile)

    utl.delete_tmp_files(tmpA1, tmpB1)

if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        ramt=o.get('-r', '0'), gamt=o.get('-g', '0'), bamt=o.get('-b', '0'),
        bright=o.get('-B', '0'), contrast=o.get('-C', '0'),
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
