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
	remap -P PASSWORD [-n NUMCOLORS ] [-m METRIC] [-s] INFILE MAPFILE OUTFILE

OPTIONS:
 -n NUMCOLORS  desired number of colors, if the input image
               has more than 256 unique colors;
               0<integer<=256; default is to use the number
               of input colors if <= 256, otherwise 24
 -m METRIC     colorspace distance metric; choices are:
		    RGB or RGBL (luminance weighted RGB); [default: RGB]
 -s            show/display textual data to the terminal
 -P PASSWORD   password for accessing the application
"""

def process(infile, mapfile, outfile, ncolors=None, metric='RGB', show=False):

    tmpA = tempfile.mktemp(suffix='.mpc')
    tmpM = tempfile.mktemp(suffix='.mpc')

    # test input image
    utl.run_im('-quiet', '-regard-warnings', infile, '-alpha', 'off', '+repage', '-depth', '8', tmpA)

    # test color table mapfile image
    utl.run_im('-quiet', '-regard-warnings', mapfile, '-alpha', 'off', '+repage', '-depth', '8', tmpM)

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

    utl.run_im(tmpA, '+dither', '-colors', str(ncolors), '-depth', '8', tmpA)

    # get number of reduced rgb image colors
    color_arr = utl.get_colors(tmpA)
    ncolors = len(color_arr)

    if show:
        print "number of reduced colors =", ncolors

    # output color reduced image for testing
    utl.run_im(tmpA, infile + '_remap_reduced.png')

    if metric.lower() == "rgb":
        pairlist = [(c, min(mapcolor_arr, key=lambda m: utl.rgb_dist(c, m))) for c in color_arr]
    elif metric.lower() == "rgbl":
        pairlist = [(c, min(mapcolor_arr, key=lambda m: utl.rgbl_dist(c, m))) for c in color_arr]
    else:
        raise Exception("Incorrect color metric value '{}'. Valid values: RGB or RGBL".format(metric))

    # do remapping
    if show:
        print "\nRemapping Image"

    tmpO = tempfile.mktemp(suffix='.mpc')

    utl.run_im('-size', '{}x{}'.format(*utl.get_dim(tmpA)), 'xc:none', '-depth', '8', tmpO)

    for idx, (c, m) in enumerate(pairlist, 1):

        c_rgb, m_rgb = "rgb({},{},{})".format(*c), "rgb({},{},{})".format(*m)
        if show:
            print "{}: {} to {}".format(idx, c_rgb, m_rgb)
        utl.run_im(
            '(', tmpA, '+transparent', c_rgb, '-fill', m_rgb, '-opaque', c_rgb, ')',
            tmpO, '-composite', tmpO)

        utl.run_im(tmpO, outfile)

    if show:
        print "\nFinal colors:"
        final_colors = utl.get_colors(tmpO)
        for c in final_colors:
            print "rgb({},{},{})".format(*c)

        print "number of final colors =", len(final_colors)

    utl.delete_tmp_files(tmpA, tmpM, tmpO)


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        metric=o['-m'], ncolors=o['-n'], show=o['-s'],
        infile=o.get('INFILE'), mapfile=o.get('MAPFILE'), outfile=o.get('OUTFILE'),)
