#! /bin/bash
#
# Install a python from source - courtesy Felix Stoehr
#
# using pip package management (conda does not seem to be needed for our purposes)
#
#  note:
#  - Python vs. python 
#  - no python in the prefix bin, only python3

INSTALLOCATION=$PWD
PYTHONVERSION=3.6.10

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

# CASA
$prefix/bin/pip3 install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatools
$prefix/bin/pip3 install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatasks

# Only for development
# ASTROPY PACKAGE TEMPLATE
$prefix/bin/pip3 install cookiecutter gitpython

echo "set path = ($INSTALLOCATION/python3/bin \$path); rehash" >> python_start.csh
echo "export PATH=$INSTALLOCATION/python3/bin:\$PATH"          >> python_start.sh
