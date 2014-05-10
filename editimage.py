# -*- coding: utf-8 -*-
"""
Created on Mon May  5 18:13:46 2014

@author: rad.cirskis
"""

from docopt import docopt

USAGE = """
USAGE:
 editimage cartoon [-p PATTERN] [-n NUMLEVELS] [-e EDGEAMOUNT] [-b BRIGHTNESS] [-s SATURATION] INFILE OUTFILE
 editimage -h,--help

OPTIONS:
 -p PATTERN     segmentation pattern (shape); 0<=integer<=100;
                default=70
 -n NUMLEVELS   number of desired segmentation levels; integer>=2;
                default=6
 -e EDGEAMOUNT  amount of edges; float>=0; default=4
 -b BRIGHTNESS  brightness of cartoon; integer>=0; default=100
 -s SATURATION  saturation of cartoon; integer>=0; default=100


 """
#%%
