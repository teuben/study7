#! /usr/bin/env python
#

from astroquery.admit import ADMIT

if True:
    import pickle
    a = pickle.load(open('alma.pickle','rb'))

a = ADMIT()
a.query(source_name_alma="NGC3504")
a.check()


if False:
    r = a.sql("SELECT * from win")
    print(len(r),r)

if False:
    q1 = 'SELECT * from  spw, sources WHERE sources.flux > 9 and sources.spw_id = spw.id and sources.lines_id = 0;'
    r1 = a.sql(q1)
    print('Should find the 1 CubeSum source, 10 Jy')
    print(r1)
    q2 = 'SELECT * from  spw, sources, lines WHERE sources.flux > 7 AND sources.spw_id = spw.id  and sources.lines_id = lines.id and lines.spw_id = spw.id;'
    r2 = a.sql(q2)
    print('Should find the 1 CO LineCube source, 8 Jy')    
    print(r2)
    
