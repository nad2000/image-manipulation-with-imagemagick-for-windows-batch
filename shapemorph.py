#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 22:13:46 2015

@author: rad.cirskis
"""

import tempfile
import utl
from subprocess import PIPE

USAGE = """
USAGE:
    shapemorph -P PASSWORD [-f FRAMES] [-d DELAY] [-p PAUSE] [-r] [-m] CONTROLPOINTS INFILE1 INFILE2 OUTFILE
    shapemorph (-h | --help)
 
OPTIONS:
 -h --help         Show this screen.
 -P PASSWORD       Password
 -f FRAMES         Number of frames in animation; frames>1; [default: 20]
 -d DELAY          Delay between frames; delay>0; [default: 10]
 -p PAUSE          Pause delay for two undistorted input images;
                   pause>0; [default: 100]
 -r                Reverse the animation sequence and append it to the end
 -m                Enable progress monitoring of the generation of each frame
 CONTROLPOINTS     Control point location in INFILE1 and INFILE2, respectively;
                   MUST be specified just prior to INFILE1 and OUTFILE1
                   consist of four, comma or space seperated numbers, eg, "x1,y1 x2,y2"

 """
## -F             generate sequence of file instead of animated gif file
 
def process(infile1, infile2, outfile, frames='20', delay='10', pause='100', reverse=False,
        monitor=False, multiple_files=False, coords=None):

    try:
        if int(frames) <= 1:
            raise Exception("Frames=\"{0}\" must be an integer greater than 1".formant(frames))
        if int(delay) < 1:
            raise Exception("Delay=\"{0}\" must be a positive integer".formant(delay))
        if int(pause) < 0:
            raise Exception("Pause=\"{0}\" must be a non-negative integer".formant(pause))
    except ValueError as e:
        raise Exception("Incorrect value: frames='{0}', delay='{1}', pause='{2}'".format(frames, delay, pause))        

    # test that coordinates are specified correctly
    if coords == "":
      raise Exception("--- NO CONTROL POINTS WERE SPECIFIED ---")

    try:
        xx1, yy1, xx2, yy2 = [int(val) for val in coords.replace(',', ' ').split(' ')]
    except:
        raise Exception("Incorrect control points: {0}".format(coords))

    # create the in between frames
    frames_between = (int(frames) - 1)

    tmpA = tempfile.mktemp(suffix='.mpc')
    tmpB = tempfile.mktemp(suffix='.mpc')
    
    utl.run_im('-quiet', '-regard-warnings', '-delay', delay, infile1, '+repage', tmpA)
    utl.run_im('-quiet', '-regard-warnings', '-delay', delay, infile2, '+repage', tmpB)

    aw, ah = utl.get_dim(tmpA)
    bw, bh = utl.get_dim(tmpB)

    if aw == bw and ah == bh:
        ww, hh = aw, ah
    else:
        raise Exception("--- INPUT IMAGES ARE NOT THE SAME SIZE ---")

    # get last pixel in image (for corners)
    wm1 = ww - 1
    hm1 = hh - 1

    # use -distort shepards technique
    # set corner control points as fixed
    corners = "0,0 0,0  {0},0 {0},0  {0},{1} {0},{1}  0,{1} 0,{1}".format(wm1, hm1)
    
    # do geometric warping and intensity blending
    print "Processing {0} Frames:".format(frames)
    
    # initial coord for destination for both images
    cpx, cpy = xx1, yy1

    # increment on current destination coordinates
    dx = round(float(xx2 - xx1) / frames_between, 4)
    dy = round(float(yy2 - yy1) / frames_between, 4)

   
    # reverse and append if desired
    if reverse:
        final_im = utl.open_im("-", "(", "-clone", "-2-1", ")", "-loop", '0', outfile, stdin=PIPE)
    else:
        final_im = utl.open_im("-", "-loop", '0', outfile, stdin=PIPE)

    # add infile1 as first (zeroth) frame
    print "0 (start image)"
    utl.run_im('-delay', pause, tmpA, "miff:-", stdout=final_im.stdin)

    for i in range(1, int(frames)):
        print i
        blend = round((100. * i) / frames_between, 4)
        # new same location for a given iteration used for both images
        cpx += dx
        cpy += dy
        # interate new control point for infile 2 (B)
        cpointsb = corners + "  {0},{1} {2},{3}".format(xx2, yy2, cpx, cpy)

        # interate new control point for infile 1 (A)
        cpointsa = corners + "  {0},{1} {2},{3}".format(xx1, yy1, cpx, cpy)

        im = utl.open_im("-", "-reverse", "-define", "compose:args={0}%".format(blend),
                         "-compose", "blend", "-composite", "miff:-",
                         stdout=final_im.stdin, stdin=PIPE)

        # NOTE: A multi-image miff is just a concatanation of images!
        # transform B to A
        utl.run_im(tmpB, "-distort", "shepards", cpointsb, "miff:-", stdout=im.stdin)
        # transform A to B
        utl.run_im(tmpA, "-distort", "shepards", cpointsa, "miff:-", stdout=im.stdin)

        im.stdin.close()
        im.wait()

    else:
        # add infile2 as last frame
        print i, "(end image)"
        

    utl.run_im("-delay", pause, tmpB,  "miff:-", stdout=final_im.stdin)

    final_im.stdin.close()
    final_im.wait()

    utl.delete_tmp_files(tmpA, tmpB)


if __name__ == "__main__":
    o = utl.get_args(USAGE)
    
    process(
        frames=o.get('-f'), delay=o.get('-d'), pause=o.get('-p'), reverse=o.get('-r'),
        monitor=o.get('-m'), multiple_files=o.get('-F'), coords=o.get('CONTROLPOINTS'),
        infile1=o.get('INFILE1'), infile2=o.get('INFILE2'), outfile=o.get('OUTFILE'))
