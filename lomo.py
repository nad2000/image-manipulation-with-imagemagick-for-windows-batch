# -*- coding: utf-8 -*-

from pygram import Lomo
import utl

#%%

USAGE = """
USAGE:
	lomo -P PASSWORD INFILE OUTFILE

OPTIONS:
 -P PASSWORD   password for accessing the application
"""


if __name__ == "__main__":

    o = utl.get_args(USAGE)

    f = Lomo(infile=o.get('INFILE'), outfile=o.get('OUTFILE'))
    f.apply()
