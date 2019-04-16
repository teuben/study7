#
#


help:
	@echo Targets:
	@echo "   git     pull this and all derived"

git:
	(cd admit ; git pull)
	(cd QAC   ; git pull)
	git pull


#       needs to source ...
install:
	./install_miniconda3
	./install_qac
	./install_admit
