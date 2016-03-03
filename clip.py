#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utl
import os

import moviepy
from moviepy.editor import VideoFileClip

USAGE = """
USAGE:
  clip -P PASSWORD [-s START] [-e END] [-H HEIGHT] [-W WIDTH] [--x1 X1] [--x2 X2] [--y1 Y1] [--y2 Y2] INFILE [OUTFILE]
  clip -h|--help

OPTIONS:
  -s START     clip START in the format of "hour,min,sec" or "min,sec" or "sec" [default: 0]
  -e END       clip END [default: end of the input]
  -H HEIGHT    height in pixels or a float representing a scaling factor, like 0.5
  -W WIDTH     width in pixels or a float representing a scaling factor, like 0.5
  --x1 X1      x1, y1 is the lower right corner of the croped region 
  --y1 Y1      x1, y1 is the lower right corner of the croped region 
  --x2 X2      x2, y2 is the lower right corner of the croped region 
  --y2 Y2      x2, y2 is the lower right corner of the croped region 
  -P PASSWORD  password for accessing the application
"""

def num_val(string_val):
    """ Retruns eithe int or float"""

    if string_val is None:
        return None
    else:
        return float(string_val) if '.' in string_val else int(string_val)


def time_stamp(string_val):
    """ Retruns a tuple of either float or int values"""

    if string_val is None:
        return None
    else:
        return tuple((num_val(v) for v in string_val.split(',')))


def clip(infile, outfile=None, **kwargs):

    # remove all 'None' values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    if outfile is None:
        outfile = os.path.splitext(infile)[0] + ".gif"

    cl = VideoFileClip(infile).subclip(
            time_stamp(kwargs.get("-s")),
            time_stamp(kwargs.get("-e")))
    if "-H" in kwargs and "-W" in kwargs:
        cl = cl.resize(num_val(kwargs["-H"]), num_val(kwargs["-W"]))
    elif "-H" in kwargs or "-W" in kwargs:
        val = num_val(kwargs["-H"] if "-H" in kwargs else kwargs["-W"])
        cl = cl.resize(val)
    region = {k[2:]: num_val(kwargs[k]) for k in kwargs if k in ("--x1", "--x2", "--y1", "--x2")}
    if region != {}:
        cl = cl.crop(**region)

    if outfile.upper().endswith(".GIF"):
        cl.write_gif(outfile)
    else:
        cl.write_videofile(outfile)


if __name__ == "__main__":

    o = utl.get_args(USAGE)
    clip(o.get("INFILE"), o.get("OUTFILE"), **o)



