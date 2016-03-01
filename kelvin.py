#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pygram import Kelvin
import utl

#%%

USAGE = """
USAGE:
	kelvin -P PASSWORD INFILE OUTFILE

OPTIONS:
 -P PASSWORD   password for accessing the application
"""


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    f = Kelvin(infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
    f.apply()
