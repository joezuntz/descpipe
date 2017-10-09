# Prototype / Proof-of-concept of Docker-based pipeline

## Status

Running a test example:
```
# Cloning the code repo and the image builder repo
git clone https://github.com/joezuntz/descpipe
cd descpipe
git clone https://github.com/joezuntz/descpipe-images  images

# Building the images - this runs "docker build" to make the stages.
cd images
make
cd ..

# Generate the script that runs the pipeline
./bin/descpipe local master-pipeline.yaml

# Run the pipeline
./test/sh

```

Requires Python3

Generates a test.sh script that runs a one-step pipeline (catalog->2pt 2D) using packaged Dockerfiles.
Requires a catalog input file to run.

## Some issues we face in pipeline design

Heterogenous machines & architectures
Provenance and version tracking
Ease of use for new people
Easy modification and replacement
Easy testing

## Docker images:

Encapsulate an OS and file system.
Are a bit like a virtual machine but much less unwieldy.
Are very easy to share machine images.
Starting to be possible to run on HPC/HTC.
Can be created from a very simple file.
Can interact with several other related systems (shifter, singularity)

## Proposal: write each step in our (primary?) pipeline as a single Docker image

Built off a base image supplying e.g. DM stack, some key libraries.
Pre-defined mounted input, output, configuration directories.
Can be stored for us on Docker Hub
Versions and their configuration listed somewhere centrally
Accompanied by library to launch them on different systems.
Defined entry point (python script) using the library to find inputs/outputs/config


## Random notes

PIECES:

Translator/Launcher for Cori+shifter - takes the DAGinfo and turns it into cori jobs, just temporarily
    - Or possibly jump straight to pegasus?
IO subsystem
Something to manage the images more carefully?

How should non-embarassingly parallel jobs be run?

Possible base images:
- OSG seems to need these ones: https://github.com/opensciencegrid/osgvo-el7
- NERSC needs things based on certain Ubuntu or Centos versions - has to have the right kernel.
- We want the DM stack - might need to have this built ourselves.
- Could we just install all the needed stuff on one giant on - DM, OSG stuff like CVMFS, etc.?

