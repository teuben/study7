#! /usr/bin/env python
#
#   get full record for given obs_id.  If mid freq given, the proper spw is returned
#
#   Problem, for uid___A001_X133f_X196 there appear 2 pairs of 4 spw's

import os
import sys

key   = 'member_ous_uid'
key   = 'obs_id'

if len(sys.argv) == 1:
    print("Usage: %s (obs_id|fits_file) [frequency]")
    print("Examples :")
    print("  uid://A001/X1288/Xba8     NGC3504 - has 4 entries")
    print("  uid://A001/X133f/X196     SMC Ref and Tile - has 8 entries")
    sys.exit(0)


val   = sys.argv[1]
freq  = None
if os.path.exists(val):
    from astropy.io import fits
    hdu = fits.open(val)
    h = hdu[0].header
    # Look for 'uid___A001_X1288_Xba8' , make it uid://A001/X1288/Xba8
    if 'FILNAM01' not in h:
        print("No FILNAM01 found in header, not an ALMA fits file?")
        sys.exit(0)
    uid = h['FILNAM01'].split('_')
    val = 'uid://%s/%s/%s' % (uid[3],uid[4],uid[5])
    # Find the mid frequency
    naxis3 =   int(h['NAXIS3'])
    crpix3 = float(h['CRPIX3'])
    cdelt3 = float(h['CDELT3'])
    crval3 = float(h['CRVAL3'])
    freq = (((naxis3+1)/2.0 - crpix3)*cdelt3 + crval3)/1e9
    print("# obs_id=%s mid frequency=%.10f" % (val,freq))

query = "SELECT * FROM ivoa.obscore WHERE %s = '%s'" % (key,val)
url   = "https://almascience.nrao.edu/tap"
mode  = 1

if len(sys.argv) > 2:
    freq = float(sys.argv[2])

query = query + " and science_observation = 'T'"
query = query + " and scan_intent = 'TARGET'"

if mode == 1:
    
    import pyvo

    service = pyvo.dal.TAPService(url)
    r = service.search(query)
    p = r.to_table()  #  .to_pandas()
    
elif mode == 2:
    
    from astroquery.alma import Alma

    r = Alma.query_tap(query)
    p = r.to_table()  #  .to_pandas()

else:
    print("# bad mode ",mode)

if len(p) > 0:
    keys = p.keys()
    if freq == None:
        for i in range(len(p)):
            for k in keys:
                print("%2d %-30s %s" % (i,k,p[i][k]))
        freqs = []
        objs  = []
        for i in range(len(p)):
            freqs.append(p[i]['frequency'])
            objs.append(p[i]['target_name'])
        print("# frequency:   ",freqs)
        print("# target_name: ",objs)
    else:
        dfmin = freq
        for i in range(len(p)):
            df = abs(freq - float(p[i]['frequency']))
            if df < dfmin:
                imin = i
                dfmin = df
        print("# Found #",imin,"with",dfmin,"from",freq,"GHz")
        for k in keys:
            print("%-30s %s" % (k,p[imin][k]))
else:
    print("# No records found for %s = %s" % (key,val))
        