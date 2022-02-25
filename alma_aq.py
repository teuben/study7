#! /usr/bin/env python
#
#   get full record for given obs_id.  If mid freq given, the proper spw is returned
#
#   Problem, for uid___A001_X133f_X196 there appear 2 pairs of 4 spw's
#
import os
import sys

version = '24-feb-2022'

key   = 'member_ous_uid'
key   = 'proposal_id'
key   = 'obs_id'

if len(sys.argv) == 1:
    print("Usage: %s (%s|fits_file) [frequency]" % (sys.argv[0],key))
    print("Examples :")
    print("  uid://A001/X1288/Xba8     NGC3504 - has 4 entries")
    print("  uid://A001/X133f/X196     SMC Ref and Tile - has 8 entries")
    print("This is version %s" % version)
    sys.exit(0)


print("# alma_aq version %s" % version)

val   = sys.argv[1]
freq  = None
if os.path.exists(val):
    from astropy.io import fits    
    hdu = fits.open(val)
    h = hdu[0].header
    # Look for 'uid___A001_X1288_Xba8' in fits header or filename, make it uid://A001/X1288/Xba8
    # Data from 2017.x seem ok
    if 'FILNAM01' not in h:
        print("# No FILNAM01 found in header, not a recent enough ALMA fits file?")
        #   sigh.... try deciphering the file name (<= 2016 projects?)
        #   if e.g. member.uid___A001_X87a_X706.NGC3504_sci.spw25.cube.I.pbcor.fits
        val = val.split('/')[-1]
        if val[0:13] == 'member.uid___':
            uid = val.split('.')[1].split('_')
            spw = val.split('.')[3]
        else:
            print("# %s" % val)
            print("# No 'member.uid___' in filename. Giving up to find the obs_id")
            sys.exit(0)
    else:
        uid = h['FILNAM01'].split('_')
        spw = h['FILNAM04']
    val = 'uid://%s/%s/%s' % (uid[3],uid[4],uid[5])
    # Find the mid frequency
    naxis3 =   int(h['NAXIS3'])
    crpix3 = float(h['CRPIX3'])
    cdelt3 = float(h['CDELT3'])
    crval3 = float(h['CRVAL3'])
    freq = (((naxis3+1)/2.0 - crpix3)*cdelt3 + crval3)/1e9
    print("# obs_id=%s frequency=%.10f" % (val,freq))
    # in case the query fails, we can add these
    a_obs_id = val
    a_target_name = h['OBJECT']
    a_ra = float(h['CRVAL1'])
    a_dec = float(h['CRVAL2'])
    a_frequency = freq
    a_date_obs = h['DATE-OBS']
    print("# <backup> values in case query fails")
    print("obs_id      %s" % a_obs_id)
    print("target_name %s" % a_target_name)
    print("s_ra        %s" % a_ra)
    print("s_dec       %s" % a_dec)
    print("frequency   %s" % a_frequency)
    print("spw         %s" % spw)
    print("date_obs    %s" % a_date_obs)
    print("# </backup>")
else:
    a_obs_id = None
    

query = "SELECT * FROM ivoa.obscore WHERE %s = '%s'" % (key,val)
url   = "https://almascience.nrao.edu/tap"
url   = "https://almascience.eso.org/tap"
mode  = 1

if len(sys.argv) > 2:
    freq = float(sys.argv[2])

query = query + " and science_observation = 'T'"
query = query + " and scan_intent = 'TARGET'"

print("# mode=%d url=%s" % (mode,url))

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
        
