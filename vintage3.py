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
 vintage3 -P PASSWORD [-H TINTHUE] [-S TINTSATURATION] [-A TINTAMOUNT]
  [-b BRIGHTNESS] [-c CONTRAST] [-s VIGNETTESHAPE] [-r VIGNETTEROUNDING]
  [-l VIGNETTELIGHTEN] [-N NOISEAMOUNT] [-L VERTICALLINES] [-B VERTICALBANDS]
  [-M BACKGROUNDMIX] [-T BORDERTYPE] [-W BORDERWIDTH] [-R BORDERROUNDING]
  [-C BORDERCOLOR] INFILE OUTFILE [BACKGROUNDFILE]
 vintage3 -h|-help

OPTIONS:
 -H TINTHUE           vintage tint hue; 0<=integer<=360; [default: 32]
 -S TINTSATURATION    vintage tint saturation; 0<=integer<=100; [default: 25]
 -A TINTAMOUNT        vintage tint amount; 0<=integer<=100; [default: 100]
 -b BRIGHTNESS        vintage brightness; -100<=integer<=100; [default: 10]
 -c CONTRAST          vintage contrast; -100<=integer<=100; [default: -20]
 -s VIGNETTESHAPE     vignette shape; choices are: roundrectangle,
                      horizontal, vertical or none; [default: roundrectangle]
 -r VIGNETTEROUNDING  vignette rounding percent for roundrectangle only; 0<=integer<=50;
                      default=50 for roundrectangle and default=20 otherwise;
 -l VIGNETTELIGHTEN   vignette ligntening; 0<=integer<=100; [default: 0]
 -N NOISEAMOUNT       noise amount; 0<=integer<=100; [default: 40]
 -L VERTICALLINES     intensity of vertical lines; 0<=integer<=100; [default: 65]
 -B VERTICALBANDS     intensity of vertical bands;  0<=integer<=100; [default: 30]
 -M BACKGROUNDMIX     background mixing; 0<=integer<=100; [default: 100]
 -T BORDERTYPE        border type; choices are: none, torn, rounded; [default: none]
 -W BORDERWIDTH       border width only for bordertype=torn or rounded; integer>=0; [default: 5]
 -R BORDERROUNDING    border rounding percent only for bordertype=rounded; 0<=integer<=50; [default: 10]
 -C BORDERCOLOR       border color; [default: white]
 -P PASSWORD          password for accessing the application
"""


def process(infile, outfile, tinthue, tintsaturation, tintamount, brightness,
            contrast, vignetteshape, vignetterounding, vignettelighten, noiseamount,
            verticallines, verticalbands, backgroundmix, bordertype, borderwidth,
            borderrounding, bordercolor, backgroundfile):

    # ancillary
    tintlightness = 50
    bandingwidth = 15
    vignettesize = 85
    noiseseed = 100
    vertnoiseseed = 100
    bandseed = 40
    vignettesaturation = 81
    vignettelightness = 34
    torndensity = '1'
    torncurviness = '5'
    tornroughness = '1'
    tornpad = '2'
    tornseed = '100'
    verticalnoiseamt = verticallines
    bandingamt = verticalbands
    backgroundamt = backgroundmix

    if vignetterounding is None:
        vignetterounding = '50' if vignetteshape == 'roundrectangle' else '20'

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')
    tmpA2 = tempfile.mktemp(suffix='.mpc')
    tmpB2 = tempfile.mktemp(suffix='.cache')

    setcspace = utl.get_cspace_option()
    version = utl.get_im_version()

    # no need for setcspace for grayscale or channels after 6.8.5.4
    # but to keep the same look, must use colorspace rec601luma via -intensity, since now colorspace gray is rec709luma
    # also correct for -tint

    if version == "06080504":
        setcspace = ["-intensity", "rec601luma"]
        graycorrect = ["-intensity", "rec601luma"]
    else:
        graycorrect = []

    # test input image
    utl.run_im(['-quiet', '-regard-warnings', infile, '-auto-level', '+repage', tmpA1])

    ww, hh = utl.get_dim(tmpA1)

    if backgroundfile:
        utl.run_im(['-quiet', '-regard-warnings', backgroundfile, '+repage', tmpA2])

    # convert to grayscale
    # note: from vintage1 and vintage2, we need to feed the noise processing a non-linear gray image
    utl.run_im([tmpA1, setcspace, '-colorspace', 'gray', '-set', 'colorspace', 'sRGB', tmpA1])

    # add noise
    if noiseamount != "0":
        noiseamount = round(int(noiseamount) / 100., 4)
        # need to add -set colorspace sRGB at end (not $setcspace as it causes imo results to be grayscale)
        # for the next two sections regarding adding noise and vertical noise to work correctly -- very strange
        # this changed between 6.8.3.8 and 6.8.3.9
        # due to changes in -colorspace gray when -intensity was being introduced and debugged
        utl.run_im([tmpA1, '-seed', str(noiseseed), '-attenuate', str(noiseamount), '+noise', 'gaussian',
                    setcspace, '-colorspace', 'gray', '-set', 'colorspace', 'sRGB', tmpA1])

    # add vertical noise
    if verticalnoiseamt != "0":
        # note need to use non-linear (rather than linear) gray image to avoid
        # (bug driven) lower contrast results from versions 6.8.3.10 through 6.8.4.4
        # could have used gray50, but decided to keep gray(50%) and add -colorspoce sRGB
        # which does not seem to alter results prior to 6.7.7.7
        utl.run_im([tmpA1,
                    '(', '-size', str(ww) + "x1", 'xc:gray(50%)', "-set", "colorspace", "sRGB",
                    "-seed", str(vertnoiseseed), "-attenuate", "15", "+noise", "uniform",
                    setcspace, "-colorspace", "gray", "-resize", "{}x{}!".format(ww, hh),
                    "-alpha", "set", "-channel", "A", "-evaluate", "set", verticalnoiseamt.strip() + '%', "+channel", ')',
                    "-compose", "overlay", "-composite", tmpA1])

    # add banding
    if bandingamt != "0":
        utl.run_im([tmpA1,
                    '(', "-size", str(ww) + "x1", "-seed", str(bandseed), "plasma:fractal",
                    setcspace, "-colorspace", "gray", "-blur", "0x" + str(bandingwidth), "-resize", "{}x{}!".format(ww, hh),
                    "-auto-level", "-alpha", "set", "-channel", 'A', "-evaluate", "set",  bandingamt + '%', "+channel", ')',
                    "-compose", "overlay", "-composite", tmpA1])

    # add background image
    if backgroundfile is not None:

        utl.run_im([tmpA1,
                    '(', tmpA2, "-resize", "{}x{}!".format(ww, hh), "-alpha", "set", "-channel", 'A',
                    "-evaluate", "set", backgroundamt + '%', "+channel", ')',
                    "-compose", "overlay", "-composite", tmpA1])

    # process for color change
    # note tintcolor needs -colorspace sRGB to make imo, im6 and im produce same colors
    tinthue = round(int(tinthue) * 100. / 360, 4)
    tintcolor = utl.hsl_to_srgb(tinthue, tintsaturation, tintlightness)

    utl.run_im([tmpA1, setcspace,
                '(', "-clone", '0', "-fill", tintcolor,  graycorrect, "-tint", "100%",
                "-alpha", "set", "-channel", 'A', "-evaluate", "set", str(tintamount) + '%', "+channel", ')',
                "-compose", "over", "-composite", "-brightness-contrast", brightness + 'x' + contrast, tmpA1])

    # setup vignette
    size_option = ["-size", str(ww) + 'x' + str(hh)]
    if vignetteshape in ["vertical", "horizontal"]:

        utl.run_im([size_option, "xc:black", "-crop",
                    "100x" + vignettesize + "+0+0%" if vignetteshape == "vertical" else vignettesize + "x100+0+0%",
                    "+repage", "-background", "white", "-gravity", "center", "-extent", size_option,
                    "-morphology", "distance", "euclidean:4", "-auto-level", "-negate", tmpA2])

    elif vignetteshape == "roundrectangle":

        xc, yc = ww / 2., hh / 2.
        ww2, hh2 = str(int(vignettesize) * ww / 50.), str(int(vignettesize) * hh / 50.)
        rounding = str(min(ww, hh) * int(vignetterounding) / 100.)

        utl.run_im([size_option, "xc:white", "-fill", "black",
                    "-draw", "translate {},{} roundrectangle -{},-{} {},{} {},{}".format(
                    xc, yc, ww2, hh2, ww2, hh2, rounding, rounding),
                    "-alpha", "off", "-morphology", "Distance", "Euclidean:4", "-auto-level", "-negate", tmpA2])

    # add vignette
    if vignetteshape != "none":
        vignettecolor = utl.hsl_to_cspace(tinthue, vignettesaturation, vignettelightness, utl.get_cspace())
        utl.run_im([tmpA1,
                    '(', tmpA2, "+level-colors", vignettecolor + ",white", "+level", vignettelighten + "x100%", "-blur", "0x5", ')',
                    "-compose", "multiply", "-composite", tmpA1])

    # add border/frame
    if bordertype == "torn":
        psize = borderwidth + tornpad

        utl.run_im([tmpA1,
                    "(", "-clone", "0", "-fill", bordercolor, "-colorize", "100%", ")",
                    "(", "-clone", "0", "-fill", "white", "-colorize", "100%", "-shave",  psize +
                    'x' + psize, "-bordercolor", "black", "-border", psize, ")",
                    "(", "-clone", "0", "-seed", tornseed, "+noise", "Random", "-blur", "0x" + torncurviness,
                    setcspace, "-colorspace", "gray", "-auto-level",
                    "-channel", "R", "-evaluate", "sine", torndensity,
                    "-channel", "G", "-evaluate", "cosine", torndensity,
                    "-channel", "RG", "-separate", "-clone", "2", "-insert", "0",
                    "-define", "compose:args={}x{}".format(borderwidth, borderwidth),
                    "-compose", "displace", "-composite", "-spread", tornroughness,  "-blur", tornroughness + "0x0.7", ")",
                    "-delete", "2", "-swap", "0,1", "-compose", "over", "-composite", "-trim", "+repage",
                    "-gravity", "center", "-background", bordercolor, "-extent", "{}x{}".format(ww, hh), tmpA1])

    elif bordertype in ["round", "rounded"]:

        if version == "06070608":
            aproc = ["+matte", "-channel", "A", "-evaluate", "set", "100%"]
        else:
            aproc = ["-alpha", "set", "-channel", "A"]

        rounding = round(min(ww, hh) * int(borderrounding) / 100., 5)

        utl.run_im([
            tmpA1, "(", "-clone", "0", aproc, "-separate", "+channel",
            "(", "-size", "{0}x{0}".format(rounding), "xc:black", "-draw", "fill white circle {0},{0} {0},0".format(
                rounding), "-alpha", "off", "-write", "mpr:arc", "+delete", ")",
            "(", "mpr:arc", ")", "-gravity", "northwest", "-composite",
            "(", "mpr:arc", "-flip", ")", "-gravity", "southwest", "-composite",
            "(", "mpr:arc", "-flop", ")", "-gravity", "northeast", "-composite",
            "(", "mpr:arc", "-rotate", "180", ")", "-gravity", "southeast", "-composite", ")",
            "-clone", "0", "-clone", "1", "-alpha", "off", "-compose", "copy_opacity", "-composite",
            "-background", bordercolor, "-compose", "over", "-flatten",
            "-bordercolor", bordercolor, "-border", borderwidth, tmpA1])

    utl.run_im([tmpA1, outfile])

    utl.delete_tmp_files(tmpA1, tmpB1, tmpA2, tmpB2)

if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        tinthue=o.get('-H'), tintsaturation=o.get('-S'), tintamount=o.get('-A'),
        brightness=o.get('-b'), contrast=o.get('-c'), vignetteshape=o.get('-s'), vignetterounding=o.get('-r'),
        vignettelighten=o.get('-l'), noiseamount=o.get('-N'), verticallines=o.get('-L'), verticalbands=o.get('-B'),
        backgroundmix=o.get('-M'), bordertype=o.get('-T'), borderwidth=o.get('-W'),  borderrounding=o.get('-R'),
        bordercolor=o.get('-C'), infile=o.get('INFILE'), outfile=o.get('OUTFILE'), backgroundfile=o.get('BACKGROUNDFILE'))
