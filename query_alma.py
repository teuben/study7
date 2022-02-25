#! /usr/bin/env python
#
# AQ: https://astroquery.readthedocs.io/en/latest/
# VO: https://pyvo.readthedocs.io/en/latest/
#

import os
import sys

db_name = 'alma.db'
p_name = 'alma.pickle'

url = "https://almascience.nrao.edu/tap"
url = "https://almascience.eso.org/tap"

q1 = "SELECT * FROM ivoa.obscore"
q2 = "SELECT * FROM ivoa.obscore WHERE target_name = 'NGC3504'"
q3 = "NGC3504"

#         1=pyvo   2=astroquery
mode = 2
query = q1



if os.path.exists(db_name):
    print("%s already exists" % db_name)
    sys.exit(0)




if mode == 1:
    print("pyvo: ",query)
    print("url:  ",url)
    
    import pyvo

    service = pyvo.dal.TAPService(url)
    r1 = service.search(query)
    p1 = r1.to_table().to_pandas()
    p1.to_pickle(p_name)
    print('Wrote ',p_name)
    
elif mode == 2:
    print("astroquery.alma.query_tap:",query)
    
    from astroquery.alma import Alma

    r2 = Alma.query_tap(query)
    p2 = r2.to_table().to_pandas()
    p2.to_pickle(p_name)
    print('Wrote ',p_name)
    

elif mode == 3:
    # why is this failing?
    print("astroquery.alma.query_object",q3) 

    from astroquery.alma import Alma

    r3 = Alma.query_object(q3)


    
#


import pickle

a = pickle.load(open('alma.pickle','rb'))
print("read pickle into",type(a),a)

#   rm alma.db 
import sqlite3
conn = sqlite3.connect('alma.db')
a.to_sql('alma', conn)


# to query e.g.
# a1 = pd.read_sql('SELECT * FROM alma', conn)
