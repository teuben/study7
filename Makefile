#
#


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
