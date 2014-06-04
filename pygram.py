# -*- coding: utf-8 -*-
"""
Created on Wed May 28 21:00:20 2014

@author: nad2000
"""

import os
import sys
import math
import tempfile

from utl import run_im
import utl

class PyGram():

    def __init__(self, infile, outfile=None):
        self.filename = infile
        self.outfile = infile if outfile is None else outfile


    def colortone(self, color, level, type=0, infile=None, outfile=None):

        if infile is None:
            infile = self.filename
        if outfile is None:
            outfile = self.outfile

        arg0 = level
        arg1 = 100 - level
        if type == 0:
            negate = '-negate'
        else:
            negate = None

        run_im(
            infile, "(", "-clone", "0", "-fill", color, "-colorize", "100%", ")", "(", "-clone", "0", "-colorspace",
            "gray", negate, ")", "-compose", "blend", "-define", "compose:args={},{}".format(arg0, arg1), "-composite", outfile
        )

# Decorations:
class Border(PyGram):

    def border(self, color='black', width=20, infile=None, outfile=None):

        if infile is None:
            infile = self.filename
        if outfile is None:
            outfile = self.outfile

        run_im(infile, "-bordercolor", color, "-border", "{0}x{0}".format(width), outfile)


class Frame(PyGram):
    def frame(self, frame, infile=None, outfile=None):

        if infile is None:
            infile = self.filename
        if outfile is None:
            outfile = self.outfile

        path = os.path.dirname(sys.argv[0])
        ww, _ = utl.get_dim(infile)
        frame=os.path.join(path, frame)
        run_im(infile, '(', frame, "-resize", "{0}x{0}!".format(ww), "-unsharp", "1.5x1.0+1.5+0.02", ')', "-flatten", outfile)


class Vignette(PyGram):
    def vignette(self, color_1='none', color_2='black', crop_factor=1.5, infile=None, outfile=None):

        if infile is None:
            infile = self.filename
        if outfile is None:
            outfile = self.outfile

        ww, hh = utl.get_dim(infile)

        crop_x = math.floor(ww * crop_factor)
        crop_y = math.floor(hh * crop_factor)

        run_im('(', infile, ')', '(',
                   "-size", "{}x{}".format(crop_x, crop_y), "radial-gradient:{}-{}".format(color_1, color_2), "-gravity", "center",
                   "-crop", "{}x{}+0+0".format(ww, hh), "+repage",
               ')', "-compose", "multiply", "-flatten", outfile)


# Filters:
class Toaster(PyGram, Vignette, Border):

    def apply(self):

        tmpA = tempfile.mktemp(suffix='.mpc')

        self.colortone('#330000', 50, 0, outfile=tmpA)
        run_im(tmpA, "-modulate", "150,80,100", "-gamma", "1.2", "-contrast", "-contrast", "-contrast", tmpA)
        self.vignette('none', 'LavenderBlush3', infile=tmpA, outfile=tmpA)
        self.vignette('#ff9966', 'none', infile=tmpA, outfile=tmpA)
        self.border('white', infile=tmpA, outfile=self.outfile)

        utl.delete_tmp_files(tmpA)


class Gotham(PyGram, Border):

    def apply(self):

        tmpA = tempfile.mktemp(suffix='.mpc')
        run_im(self.filename, "-modulate", "120,10,100", "-fill", "#222b6d", "-colorize", "20", "-gamma", "0.5",
               "-contrast", "-contrast", tmpA)
        self.border(infile=tmpA, outfile=self.outfile)

        utl.delete_tmp_files(tmpA)


class Nashville(PyGram, Frame):

    def apply(self):

        tmpA = tempfile.mktemp(suffix='.mpc')

        self.colortone('#222b6d', 50, 0, outfile=tmpA)
        self.colortone('#f7daae', 120, 1, infile=tmpA, outfile=tmpA)
        run_im(tmpA, "-contrast", "-modulate", "100,150,100", "-auto-gamma", tmpA)
        self.frame("Nashville.jpg", infile=tmpA)

        utl.delete_tmp_files(tmpA)


class Lomo(PyGram, Vignette):

    def apply(self):

        tmpA = tempfile.mktemp(suffix='.mpc')

        run_im(self.filename, "-channel", "R", "-level", "33%", "-channel", "G", "-level", "33%", tmpA)
        self.vignette(infile=tmpA)

        utl.delete_tmp_files(tmpA)


class Kelvin(PyGram, Frame):

    def apply(self):

        tmpA = tempfile.mktemp(suffix='.mpc')
        ww, hh = utl.get_dim(self.filename)

        run_im("(", self.filename, "-auto-gamma", "-modulate", "120,50,100", ')', '(', "-size",
               "{}x{}".format(ww, hh), "-fill", "rgba(255,153,0,0.5)", "-draw", "rectangle 0,0 {},{}".format(ww, hh),
               ')', "-compose", "multiply", tmpA)
        self.frame("Kelvin.jpg", infile=tmpA)

        utl.delete_tmp_files(tmpA)
