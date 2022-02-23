# Issues

Things we should clarify or fix.

0. Units Units Units!

1. vmin and vmax are w.r.t. vlsr.

3. LineCube sources missing (MapSources unfinished code)

2. some mom0,1,2 are 0.0 - is that because the line lookup failed due to roundoff?

4. sanitize product tree:   the "iter1" fits files cannot be used. aap.py doesn't skip them. Solution: manually remove the fits files

4. in addition to the 'mfs' and 'cube', the current aap also does 'cont'. do we care?

4. the LineCube "S" has a slightly different coordinate from the CubeSum "S"


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

19. if you ever see a "dummy" entry in the alma table, it means that the "admit_aq" query didn't
    work and/or the fits file wasn't a recent enough ALMA fits file with good headers, and to
	prevent it from failing, just added a dummy entry
	
30. There are some questions for the ALMA db team about some peculiarities of the ALMA columns:
    1. why is there obs_id and member_ous_uid. they seem the same
	2. how come that s_fov < s_resolution
	
	
31. textual searches are case sensitive in abstract etc.   How about NGC vs. ngc in object name?

32. table(s) are not normalized

33. sample3 : how can there be a line, and no source  member.uid___A001_X1288_Xbbe.NGC4414_sci.spw23.cube.I.pbcor.fits

34. Fluxes/Peaks are reported, but they are in noise flat data, thye've not been PB corrected??

## query


1. nrao was down, used eso. in that sense pyvo method is easier to reconfigure
2. astroquery needs some Config method?




https://almascience.eso.org/alma-data/lp/MAPS
2018.1.01055.L   2.3TB
http://alma-maps.info/.
