#! /usr/bin/env python
#

from astroquery.admit import ADMIT


a = ADMIT()
a.check()
print("AVAILABLE KEYS ",a.keys)
payload = { 
            "source_name_alma": "NGC3504",
            "vlsr": 88.0,
            "formula": 'CO*|H2O',
            "project_abstract": "*YSO* | *young stellar object*",
            "source_snr": ">3",
            "spatial_resolution": "<10",
          }

#  to note:   there should be no space (or wrong case?) in the source name

p0 = { 
    "source_name_alma": "NGC3504",
    }

p1 = { 
    "source_name_alma": "NGC3504",
    "formula": 'CO',
    "source_snr": ">3",
}

r1 = a.query(**p1)
print(len(r1))
print(r1)
