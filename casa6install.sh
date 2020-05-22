#! /bin/bash
#
# Install a python from source - courtesy Felix Stoehr - for casa6
#
# using pip for package management (conda does not seem to be needed for our purposes)
#
#  note:
#  - Python vs. python 
#  - no python in the prefix bin, only python3
#
# Dependencies:  on ubuntu-20 you will need at least:  libssl-dev libsqlite3-dev

INSTALLOCATION=$PWD
PYTHONVERSION=3.6.10
REL=0

# PYTHON
if [ ! -f Python-$PYTHONVERSION.tgz ]; then
    wget https://www.python.org/ftp/python/$PYTHONVERSION/Python-$PYTHONVERSION.tgz
fi
tar -xzvf Python-$PYTHONVERSION.tgz
cd Python-$PYTHONVERSION

prefix=$INSTALLOCATION/python3
./configure --prefix=$prefix
make
make install

# PIP
$prefix/bin/pip3 install --upgrade pip

# IPYTHON
$prefix/bin/pip3 install ipython

# BOKEH
$prefix/bin/pip3 install bokeh phantomjs selenium 

# ASTROPY, NUMPY
$prefix/bin/pip3 install astropy

# CASA release
if [ $REL = 1 ]; then
  $prefix/bin/pip3 install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatools
  $prefix/bin/pip3 install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatasks
else  
  # CASA pre-release
  $prefix/bin/pip3 install --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casatools
  $prefix/bin/pip3 install --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple casatasks
fi  
# Only for development
# ASTROPY PACKAGE TEMPLATE
$prefix/bin/pip3 install cookiecutter gitpython

echo "set path = ($INSTALLOCATION/python3/bin \$path); rehash" >> python_start.csh
echo "export PATH=$INSTALLOCATION/python3/bin:\$PATH"          >> python_start.sh
