#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May  5 18:13:46 2014

@author: rad.cirskis
"""

from docopt import docopt
import tempfile
import os
import sys

import utl
import conf

USAGE = """
USAGE:
    vignette [-i INNER] [-o OUTER] [-f FEATHER] [-c COLOR] [-a AMOUNT] INFILE OUTFILE
    vignette [--help|-h]

OPTIONS:

 -i INNER     inner radius of vignette where not darkened;
              integer percent of image dimension [default: 0]
 -o OUTER     outer radius of vignette where darkest;
              integer percent of image dimension; [default: 150]
 -f FEATHER   feathering amount for inner radius; float>=0 [default: 0]
 -c COLOR     vignette color; any IM opaque color. [default: black]
 -a AMOUNT    vignette amount; 0<=integer<=0. [default: 100]
"""

def vignette(infile, outfile, inner=0, outer=150, feather=0, color='black', amount=100, show=False):

    remap_dir = tempfile.mktemp(suffix='.REMAP')
    os.mkdir(remap_dir)

    tmpA = tempfile.mktemp(suffix='.mpc')
    tmpM = tempfile.mktemp(suffix='.mpc')

#    edgewidth = 2			# edge width; integer>=0
#    edgethresh = 90		# edge threshold; 0<=integer<=100

    # test input image
    utl.run_im([
        '-quiet', '-regard-warnings', infile, '-alpha', 'off', '+repage', '-depth', '8', tmpA])


    # test color table mapfile image
    utl.run_im([
        '-quiet', '-regard-warnings', mapfile, '-alpha', 'off', '+repage', '-depth', '8', tmpM])

    mapcolor_arr = utl.get_colors(tmpM)
    nmapcolors = len(mapcolor_arr)
    numoriginalcolors = utl.color_num(tmpA)

    if show:
        print "number of original colors = {}".format(numoriginalcolors)
        print "number of mapcolors = {}".format(nmapcolors)

    # reduce colors if more than 256 and ncolors not provided
    if not ncolors:
        ncolors = 24 if numoriginalcolors > 256 else numoriginalcolors
    else:
        ncolors = int(ncolors)

    utl.run_im([tmpA, '+dither', '-colors', str(ncolors), '-depth', '8', tmpA])

    # get number of reduced rgb image colors
    color_arr = utl.get_colors(tmpA)
    ncolors = len(color_arr)

    if show:
        print "number of reduced colors =", ncolors

    # output color reduced image for testing
    utl.run_im([tmpA, infile + '_remap_reduced.png'])

    if metric.lower() == "rgb":
        pairlist = [(c, min(mapcolor_arr, key=lambda m: utl.rgb_dist(c, m))) for c in color_arr]
    elif metric.lower() == "rgbl":
        pairlist = [(c, min(mapcolor_arr, key=lambda m: utl.rgbl_dist(c, m))) for c in color_arr]
    else:
        raise Exception("Incorrect color metric value '{}'. Valid values: RGB or RGBL".format(metric))


    #print pairlist

    # do remapping
    if show:
        print "\nRemapping Image"

    tmpO = tempfile.mktemp(suffix='.mpc')

    utl.run_im(['-size', '{}x{}'.format(*utl.get_dim(tmpA)), 'xc:none', '-depth', '8', tmpO])

    for idx, (c, m) in enumerate(pairlist, 1):

        c_rgb, m_rgb = "rgb({},{},{})".format(*c), "rgb({},{},{})".format(*m)
        if show:
            print "{}: {} to {}".format(idx, c_rgb, m_rgb)
        utl.run_im([
            '(', tmpA, '+transparent', c_rgb, '-fill', m_rgb, '-opaque', c_rgb, ')',
            tmpO, '-composite', tmpO])

        utl.run_im([tmpO, outfile])

    if show:
        print "\nFinal colors:"
        final_colors = utl.get_colors(tmpO)
        for c in final_colors:
            print "rgb({},{},{})".format(*c)

        print "number of final colors =", len(final_colors)

    utl.delete_tmp_files(tmpA, tmpM, tmpO)


if __name__ == "__main__":

    if "--verbose" in sys.argv:
        utl.verbose = True
        sys.argv.pop(sys.argv.index("--verbose"))

    o = docopt(USAGE)
    if o['-P'] != conf.PASSWORD:
        raise Exception("Wrong password! Access denied!")

    vignette(
        inner=o['-i'], outer=o['-o'], feather=o['-f'], color=o['-c'], amount=o['-a'],
        show=o['-s'], infile=o.get('INFILE'), outfile=o.get('OUTFILE'),)
