# Installation and bootstrap

It's easier to live in two universes: one with casa's python (where ADMIT lives) and one
with the queries. If you can manage in one, all the power to you!

## Installing ADMIT/CASA

is covered in other places, though we should summarize that here again.

## Installing astroquery

In your favorite python environment use your favorite installation method via
ya virtual environment of straight inserting it via pip. But we need
the teuben/astroquery repo, not the astropy one

	  git clone https://github.com/teuben/study7
      cd study7
	  make astroquery 
      pip3 install -e astroquery
	  
## Creating alma.pickle


A placeholder for local testing of the big ALMA table (astroquery.alma would query the real one)
is the following 

      ./query_alma.py
	  cp alma.pickle query/
	  
which by default creates a small alma.pickle, that can be copied in the query directory. Is has
20 rows for the galaxy NGC3504, which we've used in some of our tests.


## Testing mockdata

First test making the mockdata.db (from mockdata.txt):

      make mock
      sqlite sqlitebrowser mockdata.db
	  
if you want to test queries using the new astroquery.admit module, this mockdata can be used:

      cp mockdata.db query/admit.db
	  export ADMIT=`pwd`
	  ./check1.py

The $ADMIT may look really weird, but eventually $ADMIT/query will
contain the data. This can then be solved with a symlink.
      

## Testing real (mock) data

Upcoming ...
