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
./bin/descpipe local master-pipeline.yaml test.sh

# Run the pipeline
./test.sh

```

Requires Python3

Generates a test.sh script that runs a one-step pipeline (catalog->2pt 2D) using packaged Dockerfiles.
Requires a catalog input file to run.

## Some issues we face in pipeline design

- Heterogenous machines & architectures
- Provenance and version tracking
- Ease of use for new people
- Easy modification and replacement
- Easy testing


## Proposal: write each step in our (primary?) pipeline as a single Docker image

- Built off a base image supplying e.g. DM stack, some key libraries.
- Pre-defined mounted input, output, configuration directories.
- Can be stored for us on Docker Hub
- Versions and their configuration listed somewhere centrally
- Accompanied by library to launch them on different systems.
- Defined entry point (python script) using the library to find inputs/outputs/config


## Docker images:

- Encapsulate an OS and file system.
- Are a bit like a virtual machine but much less unwieldy.
- Are very easy to share machine images.
- Starting to be possible to run on HPC/HTC.
- Can be created from a very simple file.
- Can interact with several other related systems (shifter, singularity)


## Random notes

### Components

- Pipeline - reads description file and prepares submission scripts
- Pipes - Dockerfiles with run.py and Dockerfile
- Launchers - take the pipeline and turns it into jobs, either local, batch (PBS) or pegasus
- Pathfinder - communicates paths to input/output files
- I/O?  - common (optional?) interface to standard format(s).
- Image management?  Just dockerhub?


How should non-embarassingly parallel jobs be run?

Possible base images:
- OSG seems to need these ones: https://github.com/opensciencegrid/osgvo-el7
- NERSC needs things based on certain Ubuntu or Centos versions - has to have the right kernel.
- We want the DM stack - might need to have this built ourselves.
- Could we just install all the needed stuff on one giant on - DM, OSG stuff like CVMFS, etc.?

