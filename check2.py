#! /usr/bin/env python
#

from astroquery.admit import ADMIT
from astroquery.admit.core import _gen_sql

if True:
    import pickle
    a = pickle.load(open('alma.pickle','rb'))

a = ADMIT()
a.query()
a.check()
payload = { "spw": 123, 
            "velocity": 88.0,
            "transition": 'CO*|H2O',
          }
print("PAYLOAD SQL",_gen_sql(payload))


if False:
    r = a.sql("SELECT * from spw")
    print(len(r),r)
