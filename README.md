# STUDY7

These are tools for 'study7'. This will install self-contained versions of python3, casa (V6 optional),
QAC and admit. Only tested on Linux.

## Branches:

The master branch of ADMIT is still the classic python2 version that should work with casa 5.x.
The python3 branch of ADMIT will work with casa 5.x, and is working with a pip installed version of CASA6.
Very soon an official version of 

## Installation

0. get this source code:

        git clone https://github.com/teuben/study7
        cd study7
         
1. bootstrap your OS (ubuntu for now) with system tools we need down the line (useful for AWS or other virgin Ubuntu systems)

        ./bootstrap_ubuntu

2. miniconda3 (or anaconda3) for our controlled python envirment

        ./install_miniconda3       casa6=1
        ./test_alma1
        ./test_casa6

This test will download large amounts of data from the archive. control-C it once it starts, as it can take
hours on a slow connection. These data are downloaded in the data subdirectory. Remove these, since it can
go fast on a good connection.

If you are brave and want to try out CASA6, add the "casa6=1" argument to the install_miniconda3 script.


2b. Development of astroquery (optional)

        git clone https://github.com/teuben/astroquery
        pip install -e astroquery

3. casa (via QAC)

        ./install_qac
        source casa_start.sh
        ./test_qac1

This test should take a few mins.  Note that this casa is (should be) orthogonal to the casa installed in the classic way.

4. admit

        ./install_admit
        source admit_start.sh
        ./test_admit1

This test should take a few mins.

## CASA 6: currently a moving target

See also https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage


An experimental CASA 6 is now available, which you can install via our
miniconda3 install via the "casa6=1" optional command line argument.

Within study7 we have experimented with several python3 environments:

* miniconda3
* anaconda3
* raw python3 build
* virtual environment (the CASA team recommended way)

The important constraint is that Python 3.6 is needed, as well
as libgfortran3.

The first official release of CASA 6, including an all inclusive
environment with python in a tar file, is planned for July 2019. This
will be based on the same science and functionality as the upcoming
CASA 5.6 to be used in ALMA Cycle 7 processing.  CASA 6.1 is a more
full traditional environment, and will be available June/July 2020.

### Shared Libraries

This install worked for me in Ubuntu 18, because they happen to overlap version
of the shared libraries with the CASA6 developers.   In Ubuntu 20 this failed for
me because they got updated (now libgfortran3 became libgfortran5 and libtinfo5 became
libtinfo6). I happen to have both mounted, so this did the trick for me (YMMV):

      sudo cp -a  /a6/usr/lib/x86_64-linux-gnu/libgfortran.so.3* /usr/lib/x86_64-linux-gnu/
      sudo cp -a  /a6/lib/x86_64-linux-gnu/libtinfo.so.5* /lib/x86_64-linux-gnu

### ipython profiles

The command

      ipython profile create casa6

will create a **casa6** profile, so you can simplify calling casa using

      ipython --profile=casa6

where files in ~/.ipython/profile_casa6/startup are executed before
the command prompt appears. This is where you can place some conventient
import commands, to make casa6 look like casa.

Mine are in ~/.ipython/profile_casa6/startup/10-import.py

     import numpy as np
     import os
     import sys

and ~/.ipython/profile_casa6/startup/60-casa.py

## Testing different versions of ADMIT

Best is to look at the redo_\* scripts, and pick your poison. Each, for sanity, will work within a fresh admitNNN directory.
The **wgetc** script referenced is useful to keep a cache, otherwise replace it with **wgetc**


* redo_2 - classic admit w/ casa5
* redo_35 - new admit3 w/ casa6
* redo_36 - new admit3 w/ anaconda3
* redo_360 - new admit3 w/ python 3.6.10 and casa60
* redo_361 - new admit3 w/ python 3.6.10 and casa61


