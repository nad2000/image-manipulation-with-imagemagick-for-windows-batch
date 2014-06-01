# -*- coding: utf-8 -*-

from pygram import Nashville
import utl

#%%

USAGE = """
USAGE:
	nashville -P PASSWORD INFILE OUTFILE

OPTIONS:
 -P PASSWORD   password for accessing the application
"""


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    f = Nashville(infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
    f.apply()
