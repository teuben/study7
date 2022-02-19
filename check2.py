#! /usr/bin/env python
#

from astroquery.admit import ADMIT

if True:
    import pickle
    a = pickle.load(open('alma.pickle','rb'))

a = ADMIT()
a.check()
payload = { "spw": 123, 
            "velocity": 88.0,
            "transition": 'CO*|H2O',
          }
a.query(payload)


if False:
    r = a.sql("SELECT * from spw")
    print(len(r),r)
