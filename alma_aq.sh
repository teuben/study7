#! /bin/bash
#
#    another level of python protection....
#    this assumes -
#         - study7 was symlinked from within ADMIT
#         - there must be an astroquery.alma present via casa's python or the python_start.sh
#         - this script (study7/alma_qa.sh) was copied or symlinked in $ADMIT/bin to 
#     

fits=$1
admit=$2
log=$admit/admit_aq.log

echo "ALMA_AQ: $*"
echo "ADMIT=$ADMIT"

if [ ! -e "$fits" ]; then
    echo "first argument $fits does not exist"
    exit 1
fi

if [ ! -d "$admit" ]; then
    echo "second argument $admit does not exist"
    exit 1
fi

if [ ! -e $log ]; then
    echo "ALMA_AQ: Writing $log"
    source $ADMIT/study7/python_start.sh
    echo "running alma_aq with: $(which python)"
    # prevent our python to see CASA's pythonpath which we use in admit
    PYTHONPATH= $ADMIT/study7/alma_aq.py $fits > $log &
else
    echo "ALMA_AQ: $log already existed, not recreating"
fi
