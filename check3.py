#! /usr/bin/env python
#

from astroquery.admit import ADMIT


a = ADMIT()
a.check()
print("AVAILABLE KEYS ",a.keys)
payload = { 
            "source_name_alma": "NGC3504",
            "source_name_resolver": "M16",
            "velocity": 88.0,
            "formula": 'CO*|H2O',
            "pub_abstract": "*YSO* | *young stellar object*",
            "source_snr": ">3",
            "spatial_resolution": "<10",
          }

p1 = { 
    "source_name_alma": "NGC3504",
    "formula": 'CO',
    "source_snr": ">3",
}

r1 = a.query(**p1)
print(len(r1))
print(r1)
