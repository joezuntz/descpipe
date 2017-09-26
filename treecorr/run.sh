#!/usr/bin/env bash

# Most projects will want to initialize further pipeline steps
source /opt/lsst/software/stack/loadLSST.bash

#Run the command. Several directories are pre-defined 
# DESC_CONFIG   DESC_INPUT   DESC_OUTPUT
# maybe DESC_RANK  and DESC_SIZE ??
corr2  $DESC_CONFIG/config.yaml file_name=$DESC_INPUT/catalog.fits gg_file_name=$DESC_OUTPUT/gg.txt

