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




