#! /usr/bin/env python
#
#   get full record for given obs_id.  If mid freq given, the proper spw is returned
#

import sys

key   = 'member_ous_uid'
key   = 'obs_id'

if len(sys.argv) == 1:
    print("Usage: %s obs_id [frequency]")
    sys.exit(0)

val   = sys.argv[1] 
query = "SELECT * FROM ivoa.obscore WHERE %s = '%s'" % (key,val)
url   = "https://almascience.nrao.edu/tap"
mode  = 1

if len(sys.argv) > 2:
    freq = float(sys.argv[2])
else:
    freq = None

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
        
