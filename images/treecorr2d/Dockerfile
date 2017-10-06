# This is the base we are building off, and is described in 
# the "base" directory.
FROM joezuntz/desc-pipe-base:1.0
MAINTAINER joezuntz@googlemail.com

# Enable root mode, so we can install things more easily
USER root

# Install dependencies
RUN yum install -y libffi-devel

# Commands that need the DM stack set up first require bash -lc "command"
RUN bash -lc "pip install TreeCorr"

# Must always end with these.
# In the base image we told docker that the default command to run 
# should always be "bash -lc /opt/desc/run.py".  We replace what that
# particular file is here.
USER vagrant
COPY run.py /opt/desc/run.py
