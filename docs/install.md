# Installation and bootstrap

It's easier to live in two universes: one with casa's python (where ADMIT lives) and one
with the queries. If you can manage in one, all the power to you!

## Installing ADMIT/CASA

is covered in other places, though we should summarize that here again.

## Installing query

In your favorite python environment use your favorite installation via
a virtual environment of straight inserting it via pip. But we need
the teuben/astroquery repo, not the astropy one

	  git clone https://github.com/teuben/study7
      cd study7
	  make astroquery
      pip3 install -e astroquery

## Testing mockdata

First test the mockdata:

      make mock
      sqlite sqlitebrowser mockdata.db
	  
if you want to test queries, try this

      cp mockdata.db query/admit.db
	  export ADMIT=`pwd`
	  ./check1.py

The $ADMIT may look really weird, but eventually $ADMIT/query will
contain the data. This can then be solved with a symlink.
      
