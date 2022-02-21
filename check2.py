#! /usr/bin/env python
#

from astroquery.admit import ADMIT

if True:
    import pickle
    a = pickle.load(open('alma.pickle','rb'))

a = ADMIT()
a.check()
payload = { 
            "source_name_alma": "NGC 123",
            "source_name_resolver": "M16",
            "velocity": 88.0,
            "transition": 'CO*|H2O',
            "pub_abstract": "*YSO* | *young stellar object*",
            "snr": ">3",
            "spatial_resolution": "<10",
          }
a.query(payload)


if False:
    r = a.sql("SELECT * from spw")
    print(len(r),r)
