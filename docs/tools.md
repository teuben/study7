# Tools used in this project

## alma_aq.py

This script helped deciphering how to match up a given FITS (cube, mfs, cont) with
the proper record in the ALMA archive.

Typically one would have 4 (# spw's) entries for each OBS_ID. This typically
would result in 9 admit runs:   4 cubes, 4 spw, and one cont. An example of this
is uid://A001/X1288/Xba8, out NGC3504 example.

A counter example is the tiled SMC data, which each have a reference observations,
helping the team in calibration to make a final huge tiled map. So here we have 8
entries per obs_id.  This example can be found in uid://A001/X133f/X196. Also note
these are 7m data.

Typical usage:


    ./alma_aq.py uid://A001/X133f/X196 

you should see the last two lines of output:

    # frequency:    [230.4458578696882, 234.30617855651946, 219.47273691767782, 220.31053258245203, 230.4458473250712, 219.4727268587557, 220.31052250136494, 234.3061677545995]
    # target_name:  ['Tile_001_SMC_SWBar', 'Tile_001_SMC_SWBar', 'Tile_001_SMC_SWBar', 'Tile_001_SMC_SWBar', 'Ref_001_SMC_SWBar', 'Ref_001_SMC_SWBar', 'Ref_001_SMC_SWBar', 'Ref_001_SMC_SWBar']
	
For a given (matching) fits file we can do the same

    ./alma_aq.py member.uid___A001_X133f_X196.Tile_001_SMC_SWBar_sci.spw16.cube.I.pbcor.fits
    ...	
    # Found # 0 with 4.234240407186007e-06 from 230.44586210392862 GHz
	...
	target_name                    Tile_001_SMC_SWBar
	...

and	
	
	./alma_aq.py member.uid___A001_X133f_X196.Ref_001_SMC_SWBar_sci.spw16.cube.I.pbcor.fits
	...
	# Found # 4 with 4.5256672649429674e-06 from 230.44585185073848 GHz
	...
	target_name                    Ref_001_SMC_SWBar
	...
	
but given how ALMA observations are taken, the frequency matching may not be correct, and it needs to be checked
via the target_name.  If you really wanted to ensure a proper match, use the frequency from the list
of 8 printed on the actual archive query.
	
	
## mockdata.py

This converts mockdata.txt into mockdata.db, such that our astroquery.admit modules can query this database.
It was used for narrower tables to get the workflow going. Good for testing.
