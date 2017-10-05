STAGES=treecorr2d

OWNER=joezuntz
BASENAME=desc-pipe
VERSION=1.0


LOGS := $(STAGES:%=build/%.log) build/base.log

.DEFAULT_GOAL := $(STAGES)

.PHONY: base $(STAGES) clean

base: build/base.log

$(STAGES): % :  build/%.log

build/base.log: base/Dockerfile
	docker build -t ${OWNER}/${BASENAME}-base:${VERSION} ./base 2>&1 | tee $@

build/%.log :  %/Dockerfile %/run.py build/base.log
	rm -rf $*/descpipe
	cp -r /Users/jaz/src/desc-docker-pipeline/descpipe $*/descpipe
	docker build -t ${OWNER}/${BASENAME}-$*:${VERSION} ./$* 2>&1 | tee $@
	rm -rf $*/descpipe

clean:
	rm -f $(LOGS)
