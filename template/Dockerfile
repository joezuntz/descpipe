FROM joezuntz/desc-pipe-test:1.0
MAINTAINER joezuntz@googlemail.com

#Enable root mode
USER root

#Install dependencies
RUN yum install -y libffi-devel
#Commands that need the DM stack set up first require bash -lc "command"
RUN bash -lc "pip install TreeCorr"

# Must always end with these
USER vagrant
COPY run.sh /opt/desc/run.sh




