#! /usr/bin/env python
#
#    summarize an admit.db database
#

import sys

from astroquery.admit import ADMIT


if len(sys.argv) == 1:
    print("Usage: %s admit.db" % sys.argv[0])
    print("Will summarize data ")
    sys.exit(0)

db = sys.argv[1]


a = ADMIT(db)
a.check()

p = a.query(nchan='>0')
s = p['target_name'].unique()
print(len(s),' unique sources: ',s)

p = a.query(nchan='>2',mom0flux='>0')
print(len(p))
f=p['formula'].unique()
print(len(f),'unique lines: ',f)

# number of spectral cubes and cont maps
pl=a.query(nchan='>2')
pc=a.query(nchan=1)

#  various orphans: lines with no sources, sources with no lines
ps0=a.query(nchan='>2',nlines='>1',nsources=0)
ps1=a.query(nchan='>2',nlines='>1')
pl0=a.query(nchan='>2',nlines=0,nsources='>1')

print("Continuum maps:                      ",len(pc))
print('Spectral Line Cube:                  ',len(pl))
print('  w/ Line detections:                ',len(ps1))
print('  w/ Line detections with no sources:',len(ps0))
print('  w/ Source detections with no lines:',len(pl0))
