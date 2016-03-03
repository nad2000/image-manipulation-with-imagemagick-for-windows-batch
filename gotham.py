#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygram import Gotham

import utl

#%%

USAGE = """
USAGE:
	gotham -P PASSWORD INFILE OUTFILE

OPTIONS:
 -P PASSWORD   password for accessing the application
"""


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    f = Gotham(infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
    f.apply()
