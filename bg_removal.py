#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 03 19:10:00 2016

@author: rad.cirskis (nad2000 AT gmail DOT com)
"""

import utl
import re

USAGE = """
USAGE:
 bg_removal -P PWD [-n] [-a] [-r] [-m] [-b BACKGROUND] [-c COLOR] IMAGE FUZZ_OUT FUZZ_IN IMAGE_OUT
 bg_removal -h|-?|-help

OPTIONS:
 -n             Normalize the differences between image and background
 -a             Add the channel differences instead of simply grayscaling
                this will require larger fuzz factor differences)
 -r             use color replacement instead of flood-fill for mask generation
                this lets you find 'holes' within the image object
 -m             Flicker compare (space to swap) the masks found with the original
                image.  Press 'q' to continue processing
                green = object   blue = semi-trans edge  red = transparency
 -b BACKGROUND  use this color for background semi-transparent [default: black]
 -c COLOR       the color or the background image that should be removed
                (by default, if no color or image given, top-left corner pixel color
                of the source image)
 -P PWD         password for accessing the application



Attempt to remove the given background image, given color, or top-left
corner pixel color, from the input image, anti-aliasing the pixels between
the percentage values 'FUZZ_OUT' and 'FUZZ_IN'.

This basically implements a two masked background remove system as detailed
in  http://www.imagemagick.org/Usage/channels/#mask_antialised

The 'FUZZ_OUT' percentage defines the pixels that will be definateally
classed as background (outside the object in the 'IMAGE'.  The lower the
value the better, but too low and the main image may become surrounded by
too many semi-transparent pixels.

The 'FUZZ_IN' percentage defines what pixels should be definatally inside
the object in the image.  Pixels that differ by this much from the
background will be classed as fully-opaque.  If too low you may get halo
effects, while is too big the semi-transparent edging pixels make 'leak'
into the main object.

The program assumes the object in the image as some definate 'threshold'
division between inside and outside.  It will by default color re-color
semi-transparent areas black (shadow), but the -b option lets you change
that.
"""


def process(
        image, fuzz_out, fuzz_in, image_out,
        replace=False,  showmasks=False, additive=False,
        normalize=False, background="black", color=None):

    if color is not None:
        if re.search(r":|/|\.|\ ", color):  # This can't be a color, so use it as a normal image
            bgnd = color
        else:
            bgnd = ("( +clone -sparse-color voronoi 0,0," + color + " )")
    else:
        bgnd = "( +clone -sparse-color voronoi 0,0,%[pixel:p{0,0}] )"
    bgnd = bgnd.split()

    fill = (
        "-opaque black" if replace
        else "-bordercolor black -border 1x1 -floodfill +0+0 black -shave 1x1").split()

    if showmasks:
        showmasks = "( -clone 3,2,4 -combine -clone 0 -write x: -delete 0--1 )".split()
    else:
        showmasks = None

    grayscale = (
        "-separate -compose plus -background black -flatten" if additive else "-colorspace gray").split()

    if normalize:
        grayscale.append(" -normalize")

    utl.run_im(
        image, "(", "-clone", "0", bgnd, "-compose Difference -composite".split(),
        grayscale, "-channel B -evaluate set 0 +channel ) ( -clone 1 -fill blue -fuzz".split(),
        fuzz_out + '%', fill, "-channel B -separate +channel ) ( -clone 1 -fill blue -fuzz".split(),
        fuzz_in + '%', fill,  "-channel B -separate +channel -negate )".split(),
        "( -clone 2,3 -negate -compose multiply -composite )".split(), showmasks,
        "( -clone 0,3 +matte -compose CopyOpacity -composite ) \
        ( -clone 1 -channel R -separate +channel \
        -clone 4 +matte -compose CopyOpacity -composite \
        ( +clone -blur 0x30 +matte ) +swap -compose Over -composite \
        +matte -normalize \
        -clone 4 -compose multiply -composite \
        -background".split(),  background, "-alpha shape \
        -clone 5 -compose over -composite ) -delete 0--2".split(), image_out)


if __name__ == "__main__":

    if utl.os.name == 'nt':
        utl.IM_CMD = utl.find_command('convert', version="6.8.9-3")

    o = utl.get_args(USAGE)

    process(
        image=o.get("IMAGE"), fuzz_out=o.get("FUZZ_OUT"),
        fuzz_in=o.get("FUZZ_IN"), image_out=o.get("IMAGE_OUT"),
        replace=o.get("-r"),  showmasks=o.get("-m"), additive=o.get("-a"),
        normalize=o.get("-n"), background=o.get("-b"), color=o.get("-c"))
