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
# needs s_region to work.
#           "source_name_resolver": "M16",
            "vlsr": 88.0,
            "formula": 'CO*|H2O',
            "project_abstract": "*YSO* | *young stellar object*",
            "source_snr": ">3",
#            "spatial_resolution": "<10",
          }
a.query(**payload)

# not allowed no keywords
try :
    a.query()
except Exception:
    print("correctly caught no keyword exception")

# Example of using kw that doesn't exist
a.query(foobar="nope")

if False:
    r = a.sql("SELECT * from win")
    print(len(r),r)
