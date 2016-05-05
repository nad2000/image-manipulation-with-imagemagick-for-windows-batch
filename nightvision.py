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
    nightvision -P PASSWORD [-b BRIGHTNESS] [-d DIAMETER] [-r ROLLOFF] [-n NOISE] [-s SEED] [-B] [-T THRESHOLD] INFILE OUTFILE
    nightvision -h|-?|--help

OPTIONS:
 -b BRIGHTNESS  brightness of night view; 0<=integer<=200; [default: 100]
 -d DIAMETER    vignette diameter expressed as a percent of the image
                dimensions; 0<=integer<=100; [default: 60]
 -r ROLLOFF     vignette ramp rolloff; -100<=integer<=100;
                larger values lengthen the ramp and shorter values
                shorten the ramp; default=0 is linear ramp to most
                distant image point. [default: 0]
 -n NOISE       noise amount; float>=0; [default: 2]
 -s SEED        seed value for noise; integer>=0; [default: 100]
 -B             include blooming effect;
 -T THRESHOLD   blooming threshold; 0<=float<=100; [default: 5]
 -P PASSWORD    password for accessing the application
 """

def process(infile, outfile, brightness='100', diameter='60', rolloff='0',
             noise='2', seed='100', blooming='no', threshold='5'):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')
    tmpA2 = tempfile.mktemp(suffix='.mpc')
    tmpB2 = tempfile.mktemp(suffix='.cache')

    setcspace = utl.get_cspace_option()

    # test input image
    utl.run_im('-quiet', '-regard-warnings', infile, '+repage', tmpA1)

    ww, hh = utl.get_dim(tmpA1)
    # compute half and get centre
    xc, yc =  round(int(ww) / 2., 2), round(int(hh) / 2., 2)
    # get size of ellipse to draw
    ww2 = round(int(ww) * int(diameter) / 200., 2)
    hh2 = round(int(hh) * int(diameter) / 200., 2)

    # set ellipse args (center at 0,0 because will use translate to xc,yc)
    args = "0,0 {},{} 0,360".format(ww2,hh2)

    # set up outer ramp leveling
    rampval = 100 - abs(int(rolloff))
    leveling = ["-level" if int(rolloff) < 0 else "+level", '0x' + str(rampval) + '%']

    # convert brightness from percent to fraction
    if int(brightness) > 100:
        gain = float(brightness) / 100
        lighten = ["-evaluate", "multiply", "{:.2f}".format(gain)]
        brightness = 100
    else:
        lighten = []

    utl.run_im('(', tmpA1, lighten, '-attenuate', noise, '-seed', seed, '+noise', 'gaussian',
        setcspace, '-colorspace', 'gray', ')',
        '(', '-clone', '0', '-fill', 'green1', '-colorize', str(brightness) + '%', ')',
        '-compose', 'multiply', '-composite',
        '(', '-clone', '0', '-fill', 'white', '-colorize', '100%', '-fill', 'black',
        '-draw', "translate {},{} ellipse ".format(xc, yc) + args, '-alpha', 'off', '-morphology',
        'Distance', 'Euclidean:4', '-auto-level', leveling, ')',
        '(', '-clone','0', '-fill', 'black', '-colorize', '100%', ')',
        '+swap', '-compose', 'over', '-composite', tmpA2)

    if blooming:
        # get mask of top percent brightness
        # blur mask
        # apply as mask to overlay white
        utl.run_im(tmpA1, tmpA2,
            '(', '-clone', '0', '-fill', 'white', '-colorize', '100%', ')',
            '(', '-clone', '0', '-colorspace', 'HSB', '-channel', 'B', '-separate', '+channel',
                '-contrast-stretch', '0,' + threshold + '%',
                '-fill', 'black', '+opaque', 'white', '-blur', '0x2', ')',
                '-delete', '0', '-compose', 'over', '-composite', outfile)
    else:
        utl.run_im(tmpA2, outfile)

    utl.delete_tmp_files(tmpA1, tmpB1, tmpA2, tmpB2)


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        brightness=o.get('-b'), diameter=o.get('-d'), rolloff=o.get('-r'), noise=o.get('-n'),
        seed=o.get('-s'), blooming=o.get('-B'), threshold=o.get('-T'),
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
