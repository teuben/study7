# study7

Some tools for 'study7'. This will install self-contained versions of python3, casa (V6 optional),
QAC and admit. Only tested on Linux. 

## Installation

0. get this source code:

        git clone https://github.com/teuben/study7
        cd study7
         
1. bootstrap your OS (ubuntu for now) with system tools we need down the line (useful for AWS or other virgin Ubuntu systems)

        ./bootstrap_ubuntu

2. miniconda3 (or anaconda3) for our controlled python envirment

        ./install_miniconda3       casa6=1
        source python_start.sh
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

## CASA 6

See also https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage



An experimental CASA 6 is now available, which you can install via our
miniconda3 install via the "casa6=1" optional command line argument.

Notes from the CASA team:

Users are welcome to try the new CASA 6 pip install to their own
python environment. This is roughly analogous to using the current
pre-release builds of CASA 5.x as it is coming from the unreleased
master branch of the repository.  Instructions are as follows (from a
RHEL7 terminal window):

    python3 -m venv casa6beta
    
    source casa6beta/bin/activate
    
    pip install --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casatools
    
    pip install --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casatasks

    pip install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casampi



    #sanity check
    
            python
	    
            import casatasks as ct
	    
            help(ct)
	    
            exit()
   
    deactivate

Note that you need python 3.6 installed and may also need
libgfortran3. The use of python3 venv is a simple built-in method of
containerizing the pip install such that multiple versions of CASA 6.x
can be kept on a single machine in different environments.

The first official release of CASA 6, including an all inclusive
environment with python in a tar file, is planned for July 2019. This
will be based on the same science and functionality as the upcoming
CASA 5.6 to be used in ALMA Cycle 7 processing.

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



## Benchmarks




