#! /usr/bin/env python
#

from astroquery.admit import ADMIT


a = ADMIT('admit_maps.db')
a.check()

p = a.query(nchan='>0')
s = p['target_name'].unique()
print(len(s),' unique sources: ',s)

p = a.query(nchan='>2',mom0flux='>0')
print(len(p))
f=p['formula'].unique()
print(len(f),'unique lines: ',f)

