FROM lsstsqre/centos:7-stack-lsst_distrib-v13_0
MAINTAINER joezuntz@googlemail.com
# Other software that we need for DESC that's not in 
#RUN /bin/bash -c "source /opt/lsst/stack/loadLSST.bash && "
USER root
RUN mkdir /opt/desc
COPY run.sh /opt/desc/run.sh
CMD /opt/desc/run.sh

ADD dot-bashprofile /root/.bash_profile
ADD dot-bashrc /root/.bashrc

USER vagrant
ADD dot-bashprofile /home/vagrant/.bash_profile
ADD dot-bashrc /home/vagrant/.bashrc
