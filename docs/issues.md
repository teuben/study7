# Issues

Things we should clarify or fix.

1.  vmin and vmax are w.r.t. vlsr.

3. LineCube sources missing (MapSources unfinished code)

2.  some mom0,1,2 are 0.0 - is that because the line lookup failed due to roundoff?

4. sanitize product tree:   the "iter1" fits files cannot be used. aap.py doesn't skip them. Solution: manually remove the fits files

4. in addition to the 'mfs' and 'cube', the current aap also does 'cont'. do we care?


5. there is an admit failure in the _ph and _bp calibration files.  are they useful for another experiment, e.g.
   flux(time) since we have t_min in the alma table

6. We only store a few of the 63 variables in the alma:: table.  no need to re-run admit if we need them, they can be
   ingested with a new version of admit_study7.py

7. fix the vlsr=0 for continuum windows? (but we often use VLSRc)

8. add "peak" to win:: table ?

9. (@todo?) edge tables

11. is the units of bmaj/bmin/smaj/smin really degrees?

12. example cone searching in an area around ra/dec

13. sources only have 2D information;  no <vmean> and sigma and shape

14. the two python universe

15. ascii ingest from admit results, written using logging.study7()

16. archive might change the names of e.g. "spw19" to include "104.5GHz" its center

17. snr is not in the SourceList ;  do we need nppb? (i did flux = peak * smaj * smin / nppb)

18. need to do a sanity check on the rms in the cube, and the one used in SFind2D

## query


1. nrao was down, used eso. in that sense pyvo method is easier to reconfigure
2. astroquery needs some Config method?


