#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 20:13:46 2014

@author: rad.cirskis (nad2000 AT gmail DOT com)
"""

import tempfile
import utl

USAGE = """
USAGE:
 toycamera -P PASSWORD [-g] [-i INNER] [-o OUTER] [-d DARK] [-f FEATHER]
  [-b BRI] [-s SAT] [-H HUE] [-c CONTR] [-t TINT] [-a AMOUNT]
  [-S SHARP] [-I IBLUR] [-O OBLUR] [-B BARREL] [-D double]
  INFILE OUTFILE
 toycamera [-help]

OPTIONS:
 -g           convert image to grayscale
 -i INNER     inner radius of vignette where not darkened;
              integer percent of image dimension; [default: 0]
 -o OUTER     outer radius of vignette where darkest;
              integer percent of image dimension; [default: 150]
 -d DARK      graylevel of darkest part of vignette in integer
              range 0 to 100; [default: 0]
 -f FEATHER   feathering amount for inner radius; float>=0; [default: 0]
 -b BRI       modulation brightness change percent; integer; [default: 0]
 -s SAT       modulation saturation change percent; integer; [default: 0]
 -H HUE       modulation hue change percent; integer; [default: 0]
 -c CONTR     contrast change percent; integer; [default: 0]
 -t TINT      tint color; any IM opaque color; [default: no tint]
 -a AMOUNT    tint amount; integer>=0; [default: 0]
 -S SHARP     sharpening amount; float>=0; [default: 0]
 -I IBLUR     inner blurring amount; float>=0; [default: 0]
 -O OBLUR     outer blurring amount; float>=0; [default: 0]
 -B BARREL    barrel distortion; float>=0; [default: 0]
 -D DOUBLE    doubling distortion spacing; integer>=0; [default: +0,+0]
 -P PASSWORD  password for accessing the application
 """


def process(infile, outfile, inner='0', outer='150', dark='0', feather='0', bri='0', sat='0', hue='0',
        contr='0', tint='no tint', amount='0', sharp='0', iblur='0', oblur='0', barrel='0', gray=False, double='0'):

    tmpA1 = tempfile.mktemp(suffix='.mpc')
    tmpB1 = tempfile.mktemp(suffix='.cache')

    # test input image
    utl.run_im('-quiet', '-regard-warnings', infile, '+repage', tmpA1)

    ww, hh = utl.get_dim(tmpA1)
    wwo, hho = round(float(outer) * ww / 100, 4), round(float(outer) * hh / 100, 4)
    mwh = round(float(outer) * min(ww, hh) / 100, 4)

    setcspace = utl.get_cspace_option()
    grayish = setcspace + ["-colorspace", "gray"] if gray else []
    mlevel = ["-level", "0x{}%".format(100 - int(inner))] if int(inner) != '0' else []
    plevel = ["+level", dark + "x100%"] if dark != '0' else []
    iblurring = ["-blur", "0x" + iblur] if iblur != "0" else []
    oblurring = ["-blur", "0x" + oblur] if oblur != "0" else []
    feathering = ["-blur", feather + "x65000"] if feather != '0' else []
    sharpening = ["-sharpen", "0x" + sharp] if sharp != '0' else []
    contrasting = ["-brightness-contrast", "0," + contr] if contr != '' else []
    if bri == "0" and sat == "0" and hue == "0":
        modulation = []
    else:
        modulation = [
            "-modulate",
            "{},{},{}".format(int(bri) + 100, int(sat) + 100, int(hue) + 100)]

    if barrel == '0':
        distorting = []
    else:
        distort = round(int(barrel) / 100., 4)
        distorting = ["-distort", "barrel", "{},0,0,{}".format(distort, 1 + 2 * (distort if distort < 0 else -distort))]

    tinting = setcspace + ["-fill", tint, "-colorize", amount + "%"] if tint != "no tint" and amount != '0' else []

    if double in ["+0,+0", "-0,-0"]:
        rolling1 = rolling2 = rolling3 = []
    else:
        xroll, yroll = double.split(',')
        rolling1 = ["+clone", "-roll", xroll + yroll]
        rolling2 = setcspace + ["-compose", "blend", "-define", "compose:args=50,50", "-composite", "-compose", "over"]
        axroll, ayroll = abs(int(xroll)), abs(int(yroll))
        rolling3 = ["-shave", "{}x{}".format(axroll, ayroll)]
        utl.run_im(
            tmpA1, '-channel', color, ('+' if amt < 0 else '-') + 'sigmoidal-contrast',
            "{},50%".format(amt_), '+channel', tmpA1)

    utl.run_im(
        '(' , tmpA1, '(', rolling1, ')', rolling2, contrasting, iblurring, sharpening, distorting, ')',
        '(', "+clone", oblurring, ')', '(', '-size', "{}x{}".format(mwh, mwh), "radial-gradient:", "-resize",
        "{}x{}!".format(wwo, hho), "-gravity", "center", "-crop", "{}x{}+0+0".format(ww, hh), "+repage", ')',
        '(', "+clone", mlevel, plevel, "-clamp", feathering, tinting, ')',
        '(', "-clone", '1', "-clone", '0', "-clone", '2', setcspace, "-clamp", "-compose", "over", "-composite", modulation, ')',
        "-delete", "0-2", "+swap", "-compose", "multiply", "-composite", rolling3, outfile)

    utl.delete_tmp_files(tmpA1, tmpB1)

if __name__ == "__main__":

    o = utl.get_args(USAGE)

    process(
        inner=o.get('-i', '0'), outer=o.get('-o', '150'), dark=o.get('-d', '0'), feather=o.get('-f', '0'),
        bri=o.get('-b', '0'), sat=o.get('-s', '0'), hue=o.get('-H', '0'), contr=o.get('-c', '0'),
        tint=o.get('-t', 'no tint'), amount=o.get('-a', '0'), sharp=o.get('-S', '0'),
        iblur=o.get('-I', '0'), oblur=o.get('-O', '0'), barrel=o.get('-B', '0'), gray=False,
        double=o.get('-D', '0'), infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
