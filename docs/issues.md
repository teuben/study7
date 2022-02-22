# Issues

Things we should clarify or fix.

1.  vmin and vmax are w.r.t. vlsr.

3. LineCube sources missing (MapSources unfinished code)

2.  some mom0,1,2 are 0.0 - is that because the line lookup failed due to roundoff?

4. the "iter1" fits files cannot be used. aap.py doesn't skip them. Solution: manually remove the fits files

5. there is an admit failure in the _ph and _bp calibration files.  are they useful for another experiment, e.g.
   flux(time) ?   but we haven't saved alma::t_min

6. We only store a few of the 63 variables in the alma:: table

7. fix the vlsr=0 for continuum windows? (but we often use VLSRc)

8. add "peak" to win:: table ?

9. (@todo?) edge tables

11. is the units of bmaj/bmin/smaj/smin really degrees?

12. example cone searching in an area around ra/dec

13. sources only have 2D information;  no <vmean> and sigma and shape

14. the two python universe

15. ascii ingest from admit results, written using logging.study7()

16. archive might change the names of e.g. "spw19" to include "104.5GHz" its center

17. snr is not in the SourceList 

## query


1. nrao was down, used eso. in that sense pyvo method is easier to reconfige
2. astroquery needs some Config method?

# example

2017.1.00964.S/science_goal.uid___A001_X1288_Xba4/group.uid___A001_X1288_Xba5/member.uid___A001_X1288_Xba8/product/
member.uid___A001_X1288_Xba8.NGC3504_sci.spw25.mfs.I.pbcor.fits
member.uid___A001_X1288_Xba8.NGC3504_sci.spw25.cube.I.pbcor.fits
member.uid___A001_X1288_Xba8.NGC3504_sci.spw19_21_23_25.cont.I.pbcor.fits


uid://A001/X1288/Xba6  86GB
uid://A001/X1288/Xba8  40GB


https://almascience.nrao.edu/dataPortal/member.uid___A001_X1288_Xba6.README.txt.tar

https://almascience.nrao.edu/aq/?result_view=observation&mous=uid://A001/X1288/Xba6
https://almascience.nrao.edu/aq/?result_view=observation&mous=uid://A001/X1288/Xba8

both of these MOUSE have the same GOUS root, and under a SOUS, and under project 2017.1.00964.S

This project has seven (7) SOUS
N3049 (2)
N3504 (2)
N3593 (1)
N4402 (1)
N4414 (2)
N5253 (2)
N377  (2)



