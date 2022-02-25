#
#

URL0 = https://github.com/astropy/astroquery
URL1 = https://github.com/teuben/astroquery
URL2 = https://github.com/astropy/pyvo
URL3 = https://github.com/emerge-erc/ALminer
URL4 = https://github.com/astroumd/admit

REPOS = astroquery pyvo alminer

help:
	@echo Targets:
	@echo "   git     clone repos needed"
	@echo "   pull    pull the needed repos"
	@echo "   mock    make new mockdata"

git2:
	(cd admit ; git pull)
	(cd QAC   ; git pull)
	git pull

start2:
	cat miniconda3/python_start.sh  QAC/casa/casa_start.sh  admit/admit_start.sh  > study7_start.sh
	cat miniconda3/python_start.csh QAC/casa/casa_start.csh admit/admit_start.csh > study7_start.csh


#       optionals
install2:
	./install_miniconda3
	./install_qac
	./install_admit


git: $(REPOS)

pull:
	for r in . $(REPOS); do\
	   (cd $$r; git pull);\
	done

status:
	for r in . $(REPOS); do\
	   (cd $$r; git status -uno);\
	done


push:
	for r in . $(REPOS); do\
	   (cd $$r; git push);\
	done

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

# not required here, but you could
admit7:
	git clone -b study7 $(URL4) admit7


# a few often used tests


mock:
	rm -f mockdata.db
	python mockdata.py


alma:
	./query_alma.py
	cp alma.pickle query/

# create a new admit.db with the A-W-L-S tables

NEW = admit_cal.db admit.db admit.tar.gz
new:
	rm -f $(NEW)
	$(MAKE) $(NEW)

admit.db:
	./admit_study7.py -d admit.db    data/product_member*latest/*sci*cube*admit      data/product_member*latest/*sci*mfs*admit

admit_cal.db:
	./admit_study7.py -c -d admit_cal.db    data/product_member*latest/*_ph*mfs*admit      data/product_member*latest/*_bp*mfs*admit

admit.tar.gz:
	tar zcf admit.tar.gz data/product_member*latest/*admit/*.log data/product_member*latest/*admit/*.log

admit_maps.db:
	./admit_study7.py -d admit_maps.db    data/MAPS/product_member*latest/*sci*cube*admit      data/MAPS/product_member*latest/*sci*mfs*admit
