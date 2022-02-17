#! /usr/bin/env python
#

from astroquery.admit import ADMIT

a = ADMIT()
a.query()
a.check()


if False:
    r = a.sql("SELECT * from spw")
    print(len(r),r)
