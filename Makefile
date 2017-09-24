STAGES=treecorr
OWNER=joezuntz
BASENAME=desc-pipe
VERSION=1.0


.DEFAULT_GOAL := $(STAGES)

.PHONY: base $(STAGES)

base: base/docker-build.log

$(STAGES): % :  %/docker-build.log

base/docker-build.log: base/Dockerfile
	@echo [triggered by changes in $?]
	cd base; docker build -t ${OWNER}/${BASENAME}-base:${VERSION} . 2>&1 | tee docker-build.log

%/docker-build.log :  %/Dockerfile %/run.sh base/docker-build.log
	@echo [$* triggered by changes in $?]
	cd $*; docker build -t ${OWNER}/${BASENAME}-$*:${VERSION} . 2>&1 | tee docker-build.log

