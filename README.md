# study7

Some tools for 'study7'. This will install self-contained versions of python3, casa, QAC and admit. Only tested on Linux.

## Installation

0. get this source code:

        git clone https://github.com/teuben/study7
        cd study7
         

1. bootstrap your OS (ubuntu for now) with system tools we need down the line

        ./bootstrap_ubuntu

2. miniconda3 (mostly for astroquery things)

        ./install_miniconda3
        source python_start.sh
        ./test_alma1

This test will download large amounts of data from the archive. control-C it once it starts, as it can take hours on a slow connection.

3. casa (via QAC)

        ./install_qac
        source casa_start.sh
        ./test_qac1

This test should take a few mins.

4. admit

        ./install_admit
        source admit_start.sh
        ./test_admit1

This test should take a few mins.

## Benchmark




