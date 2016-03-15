#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  18 18:13:46 2014

@author: rad.cirskis
"""

from __future__ import print_function

import tempfile
import utl
from utl import run_im
import random

USAGE = """
USAGE:
 stainedglass -P PASSWORD [-k KIND] [-s SIZE] [-o OFFSET] [-n NCOLORS] [-b BRIGHT]
  [-e ECOLOR] [-t THICK] [-r RSEED] [-a] INFILE OUTFILE
 stainedglass -h|--help

OPTIONS:
 -k KIND      kind of stainedglass cell shape; choices are: square
              (or s),  hexagon (or h), random (or r); [default: random]
 -s SIZE      size of cell; integer>0; [default: 16]
 -o OFFSET    random offset amount; integer>=0; [default: 6];
              only applies to kind=random
 -n NCOLORS   number of desired reduced colors for the output;
              integer>1; default is no color reduction
 -b BRIGHT    brightness value in percent for output image;
              integer>=0; [default: 100]
 -e ECOLOR    color for edge or border around each cell; any valid
              IM color; [default: black]
 -t THICK     thickness for edge or border around each cell;
              integer>=0; ero means no edge or border; [default: 1]
 -r RSEED     random number seed value; integer>=0; if seed provided,
              then image will reproduce; default is no seed, so that
              each image will be randomly different; only applies
              to kind=random
 -a           use average color of cell rather than color at center
              of cell; default is center color
 -P PASSWORD  password for accessing the application

PURPOSE: Applies a stained glass cell effect to an image.

DESCRIPTION: STAINEDGLASS applies a stained glass cell effect to an image. The
choices of cell shapes are hexagon, square and randomized square. The cell
size and border around the cell can be specified.
"""


def process(
        infile, outfile, kind, size, offset, ncolors, bright, ecolor, thick, rseed, average):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')
    tmpA2 = tempfile.mktemp(suffix='.mpc')
    tmpB2 = tempfile.mktemp(suffix='.cache')
    tmpA3 = tempfile.mktemp(suffix='.mpc')
    tmpB3 = tempfile.mktemp(suffix='.cache')
    tmpC = tempfile.mktemp(suffix='_C.txt')
    tmpG = tempfile.mktemp(suffix='_G.txt')
    tmpC2 = tempfile.mktemp(suffix='_C2.txt')



    setcspace = utl.get_cspace_option()
    version = utl.get_im_version()

    if version > "06080504":
        cspace2 = cspace1 = ""
    else:
        cspace1 = "sRGB" if version >= "06070606" else "RGB"
        cspace2 = cspace1 + 'A'


    colorspace = utl.get_file_colorspace(infile)

    reduce_color = ["-monitor", "+dither", "-colors", ncolors, "+monitor"] if ncolors is not None and ncolors.strip() != "" else []

    # set up for modulate
    # note there seems to be a change in -modulate (for HSL) between IM 6.8.4.6 and 6.8.4.7 that is noticeable in the output
    if bright != "100":
        if colorspace == "CMYK":
            modulation = ["-colorspace", cspace1, "-modulate", bright + ",100,100", "-colorspace", "cmyk"]
        elif colorspace == "CMYKA":
            modulation = ["-colorspace", cspace2, "-modulate", bright + ",100,100", "-colorspace", "cmyka"]
        else:
            modulation = ["-modulate", bright + ",100,100"]
    else:
        modulation = []

    # test input image
    run_im('-quiet', '-regard-warnings', infile, reduce_color, modulation, '+repage', tmpA1)

    ww, hh = utl.get_dim(tmpA1)

    # preprocess for average color
    if average:
        if version >= "06050900":
            if kind == "square":
                dim = str(round((size - 1.) / 2., 0))
                run_im(tmpA1, "-define", "convolve:scale=!", "-morphology", "convolve", "square:" + dim, tmpA1)
            else:
                dim = str(round((size - 1.) / 2., 0) + 0.5)
                run_im(tmpA1, "-define", "convolve:scale=!", "-morphology", "convolve", "disk:" + dim, tmpA1)
        else:
            dim = str(round((size - 1.) / 2., 0))
            run_im(tmpA1, "-blur", dim + "x65000", tmpA1)

    ww1, hh1 = ww - 1, hh - 1
    ww2, hh2 = round(ww1 + int(size) / 2., 0), round(hh1 + int(size) / 2., 0)

    qrange = int(utl.run_im("xc:", "-format", "%[fx:quantumrange]", "info:"))

    if rseed is not None and rseed.strip() != "":
        random.seed(int(rseed))

    size = int(size)
    offset = int(offset)

    with open(tmpC, 'w') as cf, open(tmpG, 'w') as gf:

        print("# ImageMagick pixel enumeration: {},{},255,rgb".format(ww, hh), file=cf)

        if kind in ["random", "r"]:
            y = k = 0
            offset += 1

            while y < hh2:

                x = 0
                while x < ww2:

                    if x > ww1: x = ww1
                    if y > hh1: y = hh1

                    xx = x + int((-1 if random.random() < 0.5 else 1) * random.random() * offset)

                    if xx < 0: xx = 0
                    if xx > ww1: xx = ww1

                    yy = y + int((-1 if random.random() < 0.5 else 1) * random.random() * offset)

                    if yy < 0: yy = 0
                    if yy > hh1: yy = hh1

                    g = round(100.0 * k / qrange, 8)

                    print("{},{}: (255,255,255)\t#FFFFFF\trgb(255,255,255)".format(xx, yy), file=cf)
                    print("{} {} gray({}%)".format(xx, yy, g), file=gf)
                    x += size
                    k += 1

                y += size

        elif kind in ["hexagon", "h"]:
            y = k = j = 0

            while y < hh2:

                x = int((size + 0.5) / 2) if j % 2 == 0 else 0

                while x < ww2:

                    if x > ww1: x = ww1
                    if y > hh1: y = hh1

                    g = round(100.0 * k / qrange, 8)

                    print("{},{}: (255,255,255)\t#FFFFFF\trgb(255,255,255)".format(x, y), file=cf)
                    print("{} {} gray({}%)".format(x, y, g), file=gf)
                    x += size
                    k += 1

                y += size
                j += 1


        elif kind in ["square", "s"]:
            y = k = 0

            while y < hh2:

                x = 0

                while x < ww2:

                    if x > ww1: x = ww1
                    if y > hh1: y = hh1

                    g = round(100.0 * k / qrange, 8)

                    print("{},{}: (255,255,255)\t#FFFFFF\trgb(255,255,255)".format(x, y), file=cf)
                    print("{} {} gray({}%)".format(x, y, g), file=gf)
                    x += size
                    k += 1

                y += size


    if thick == "0":
        utl.make_pached(tmpA1, outfile, tmpC)

    else:
        utl.make_pached(tmpA1, tmpA2, tmpC)

        run_im("-size", "{}x{}".format(ww, hh), "xc:", "-sparse-color", "voronoi", "@" + tmpG, "-auto-level",
               "-morphology", "edge", "diamond:" + thick, "-threshold", "0", "-negate", tmpA3)

        run_im(tmpA2, tmpA3, "-alpha", "off", "-compose", "copy_opacity", "-composite",
               "-compose", "over", "-background", ecolor, "-flatten", outfile)

    #utl.delete_tmp_files(tmpA1, tmpB1, tmpA2, tmpB2, tmpA3, tmpB3, tmpC, tmpG, tmpC2)


if __name__ == "__main__":

    if utl.os.name == 'nt':
        utl.IM_CMD = utl.find_command('convert', version="6.8.9-3")

    o = utl.get_args(USAGE)

    process(
        kind=o.get('-k'), size=o.get('-s'), offset=o.get('-o'), ncolors=o.get('-n'), bright=o.get('-b'),
        ecolor=o.get('-e'), thick=o.get('-t'), rseed=o.get('-r'), average=o.get('-a'),
        infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
