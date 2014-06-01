# -*- coding: utf-8 -*-

from pygram import Toaster
import utl

#%%

USAGE = """
USAGE:
	toaster -P PASSWORD INFILE OUTFILE

OPTIONS:
 -P PASSWORD   password for accessing the application
"""


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    f = Toaster(infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
    f.apply()
