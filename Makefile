#
#

URL1 = https://github.com/astropy/astroquery
URL2 = https://github.com/astropy/pyvo

help:
	@echo Targets:
	@echo "   git     pull this and all derived"

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

astropy:
	git clone $(URL1)

pyvo:
	git clone $(URL2)

