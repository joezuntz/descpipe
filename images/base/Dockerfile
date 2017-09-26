# We might have to change this base one, or have several different base versions for
# different systems.  e.g. OSG might require some specific parent image?
FROM lsstsqre/centos:7-stack-lsst_distrib-v13_0
MAINTAINER joezuntz@googlemail.com

USER root
RUN mkdir /opt/desc
COPY run.sh /opt/desc/run.sh
CMD /opt/desc/run.sh

ADD dot-bashprofile /root/.bash_profile
ADD dot-bashrc /root/.bashrc

USER vagrant
ADD dot-bashprofile /home/vagrant/.bash_profile
ADD dot-bashrc /home/vagrant/.bashrc


ENV DESC_INPUT=/opt/input
ENV DESC_OUTPUT=/opt/output
ENV DESC_CONFIG=/opt/config
