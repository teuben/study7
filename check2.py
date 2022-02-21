#! /usr/bin/env python
#

from astroquery.admit import ADMIT

if True:
    import pickle
    a = pickle.load(open('alma.pickle','rb'))

a = ADMIT()
a.check()
print("AVAILABLE KEYS ",a.keys)
payload = { 
            "source_name_alma": "NGC 123",
            "source_name_resolver": "M16",
            "velocity": 88.0,
            "transition": 'CO*|H2O',
            "pub_abstract": "*YSO* | *young stellar object*",
            "snr": ">3",
            "spatial_resolution": "<10",
          }
a.query(**payload)
try :
    a.query()
except Exception:
    print("correctly caught no keyword exception")

a.query(foobar="nope")

if False:
    r = a.sql("SELECT * from win")
    print(len(r),r)
