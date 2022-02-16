#
#

URL0 = https://github.com/astropy/astroquery
URL1 = https://github.com/teuben/astroquery
URL2 = https://github.com/astropy/pyvo
URL3 = https://github.com/emerge-erc/ALminer

help:
	@echo Targets:
	@echo "   git     pull this and all derived"
	@echo "   git2    associated repos that are needed"

git:
	(cd admit ; git pull)
	(cd QAC   ; git pull)
	git pull

start:
	cat miniconda3/python_start.sh  QAC/casa/casa_start.sh  admit/admit_start.sh  > study7_start.sh
	cat miniconda3/python_start.csh QAC/casa/casa_start.csh admit/admit_start.csh > study7_start.csh


#       needs to source ...
install:
	./install_miniconda3
	./install_qac
	./install_admit


git2: astroquery pyvo

astroquery:
	git clone -b admit $(URL1)
	@echo ""
	@echo "It is recommended to install that using:    pip3 install -e astroquery"
	@echo "but feel free to use your own method"

pyvo:
	git clone $(URL2)
	@echo ""
	@echo "It is recommended to install that using:    pip3 install -e pyvo"
	@echo "but feel free to use your own method"

alminer:
	git clone $(URL3) alminer
	@echo ""
	@echo "It is recommended to install that using:    pip3 install -e alminer"
	@echo "but feel free to use your own method"
