#! /usr/bin/env python
#

from astroquery.admit import ADMIT

if True:
    import pickle
    a = pickle.load(open('alma.pickle','rb'))

a = ADMIT()
a.query()
a.check()


if False:
    r = a.sql("SELECT * from spw")
    print(len(r),r)
