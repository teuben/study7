#! /usr/bin/env python
#
# AQ: https://astroquery.readthedocs.io/en/latest/
# VO: https://pyvo.readthedocs.io/en/latest/
#


mode = 1

q1 = "SELECT * FROM ivoa.obscore"
q2 = "SELECT * FROM ivoa.obscore WHERE target_name = 'NGC3504'"
q3 = "NGC3504"

query = q2

url = "https://almascience.nrao.edu/tap"
url = "https://almascience.eso.org/tap"

if mode == 1:
    print("pyvo: ",query)
    
    import pyvo

    service = pyvo.dal.TAPService(url)
    r1 = service.search(query)
    p1 = r1.to_table().to_pandas()
    p1.to_pickle('alma.pickle')
    print('Wrote alma.pickle')
    
elif mode == 2:
    print("astroquery.alma.query_tap:",query)
    
    from astroquery.alma import Alma

    r2 = Alma.query_tap(query)
    p2 = r2.to_table().to_pandas()
    p2.to_pickle('alma.pickle')
    print('Wrote alma.pickle')
    

elif mode == 3:
    print("astroquery.alma.query_object",q3) 

    from astroquery.alma import Alma

    r3 = Alma.query_object(q3)


#



import pickle

a = pickle.load(open('alma.pickle','rb'))
print("read pickle into",type(a),a)
