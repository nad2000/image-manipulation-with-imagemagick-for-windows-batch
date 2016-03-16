#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utl
from utl import num_val

import os
import moviepy
from moviepy.editor import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

USAGE = """
USAGE:
  clip -P PASSWORD [-s START] [-e END] [--speedx SPEEDX] [--fps FPS] [-H HEIGHT] [-W WIDTH] [--x1 X1] [--x2 X2] [--y1 Y1] [--y2 Y2] [--freeze-at AT] [--freeze-x1 FX1] [--freeze-y1 FY1] [--freeze-x2 FX2] [--freeze-y2 FY2] INFILE [OUTFILE]
  clip -h|--help

OPTIONS:
  -s START         clip START in the format of "hour,min,sec" or "min,sec" or "sec" [default: 0]
  -e END           clip END [default: end of the input]
  --speedx SPEEDX  change playback speed by ration SPEEDX, e.g., 0.5
  --fps FPS        output file frame rate (fps)
  -H HEIGHT        height in pixels or a float representing a scaling factor, like 0.5
  -W WIDTH         width in pixels or a float representing a scaling factor, like 0.5
  --x1 X1          x1, y1 is the lower right corner of the croped region 
  --y1 Y1          x1, y1 is the lower right corner of the croped region 
  --x2 X2          x2, y2 is the lower right corner of the croped region 
  --y2 Y2          x2, y2 is the lower right corner of the croped region
  --freeze-at AT   freeze a region at specified time in the format "hour,min,sec" or "min,sec" or "sec" (no spaces)  
  --freeze-x1 FX1  freezing region left X coordinate fraction, e.g., 0.5
  --freeze-y1 FY1  freezing region top Y coordinate fraction, e.g., 0.5
  --freeze-x2 FX2  freezing region right X coordinate fraction, e.g., 0.5
  --freeze-y2 FY2  freezing region bottom Y coordinate fraction, e.g., 0.5
  -P PASSWORD      password for accessing the application 
"""

def time_stamp(string_val):
    """ Retruns a tuple of either float or int values"""

    if string_val is None:
        return None
    else:
        ts = tuple((num_val(v) for v in string_val.split(',')))
        if len(ts) == 1:
            return ts[0]
        else:
            return ts


def clip(infile, outfile=None, **kwargs):

    # remove all 'None' values
    options = {k: v for k, v in kwargs.items() if v is not None}

    if outfile is None:
        outfile = os.path.splitext(infile)[0] + ".gif"

    cl = VideoFileClip(infile).subclip(
            time_stamp(options.get("-s")),
            time_stamp(options.get("-e")))
    if "--speedx" in options:
        cl = cl.speedx(num_val(options["--speedx"]))

    if "-H" in options and "-W" in options:
        cl = cl.resize(num_val(options["-H"]), num_val(options["-W"]))

    elif "-H" in options or "-W" in options:
        val = num_val(options["-H"] if "-H" in options else options["-W"])
        cl = cl.resize(val)

    region = {k[2:]: num_val(options[k]) for k in options if k in ("--x1", "--x2", "--y1", "--x2")}
    if region != {}:
        cl = cl.crop(**region)
        
    # Freeze a region:
    if "--freeze-at" in options:
        region = {k[9:]: num_val(options[k]) for k in options if k in ("--freeze-x1", "--freeze-x2", "--freeze-y1", "--freeze-x2")}
        if region == {}:
            print("*** To freeze a region at leat one region coordinate should be specified!")
        elif not all((v > 0.0 and v <= 1.0 for v in region.values())):
            print("*** The region for freezing should be defined by coordinate fractions!")
        else:
            region = {k: int(round((cl.w if k[0] == 'x' else cl.h) * v)) for k, v in region.items()}
            snapshot = (cl
                .crop(**region)
                .to_ImageClip(num_val(options["--freeze-at"]))
                .set_duration(cl.duration))
            cl = CompositeVideoClip([cl, snapshot])
        
    if outfile.upper().endswith(".GIF"):
        if "--fps" in options:
            cl.write_gif(outfile, fps=num_val(options["--fps"]))
        else:
            cl.write_gif(outfile)
    else:
        cl.write_videofile(outfile)


if __name__ == "__main__":

    o = utl.get_args(USAGE)
    clip(o.get("INFILE"), o.get("OUTFILE"), **o)



