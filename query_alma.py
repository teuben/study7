#! /usr/bin/env python
#
# AQ: https://astroquery.readthedocs.io/en/latest/
# VO: https://pyvo.readthedocs.io/en/latest/
#


mode = 1

q1 = "SELECT * FROM ivoa.obscore"
q2 = "SELECT * FROM ivoa.obscore WHERE target_name = 'NGC3504'"
q3 = "NGC3504"

query = q1

if mode == 1:
    
    import pyvo

    service = pyvo.dal.TAPService("https://almascience.nrao.edu/tap") 
    r1 = service.search(query)
    p1 = r1.to_table().to_pandas()
    p1.to_pickle('alma.pickle')
    print('Wrote alma.pickle')
    
elif mode == 2:
    
    from astroquery.alma import Alma

    r2 = Alma.query_tap(query)
    p2 = r2.to_table().to_pandas()
    p2.to_pickle('alma.pickle')
    print('Wrote alma.pickle')
    

elif mode == 3:

    r3 = Alma.query_object(q3)
