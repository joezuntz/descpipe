# Prototype / Proof-of-concept of Docker-based pipeline

## Overview

This package is a prototype python 3 framework for building pipelines where each stage in the pipeline is built into a Docker container.

The actual pipeline steps are in a companion repository: https://github.com/joezuntz/descpipe-images


We face various issues when building and running pipelines:
- Heterogenous machines & architectures
- Provenance and version tracking
- Ease of use for new people
- Ease of modification and replacement
- Ease of testing

In this framework these issues are addressed by requiring each stage in the pipeline to be built as a docker image which:

- is always launched by running /opt/desc/run.py
- is built on a base image supplying e.g. DM stack and some key libraries (including this package).
- finds all its inputs and outputs using this package to search pre-defined locations (/opt/desc/[inputs|outputs|config])
- can be stored for us on Docker Hub.
- could have their versions and configuration options listed somewhere centrally?

This code currently can currently read a pipeline file and generate a shell script that runs it on a local docker system sequentially.
In future other launchers will submit it to systems like NERSC as well.

An example file in the pipelines directory builds a three-step pipeline (tomographic binning, photometric redshift stacking, correlation functions).  This pipeline requires two input catalog files to run - currently using public DES SV data.


The code runs under python3 and requires pyyaml and pydag, which can be installed with:

```
pip3 install pyyaml py-dag
```

Then you can install and run a test example:

```
# Cloning the code repo and the image builder repo
git clone https://github.com/joezuntz/descpipe
cd descpipe
git clone https://github.com/joezuntz/descpipe-images  images

# Download the input data
wget -o test/inputs/des-sv-annz-pipetest.fits  https://portal.nersc.gov/projecta/lsst/wl/des-sv-annz-pipetest.fits
wget -o test/inputs/des-sv-ngmix-pipetest.fits  https://portal.nersc.gov/projecta/lsst/wl/des-sv-ngmix-pipetest.fits

# Building the images - this runs "docker build" to make the stages.
./bin/descpipe build test/test.yaml

# Generate the script that runs the pipeline
./bin/descpipe local test/pipeline.yaml test.sh

# Run the pipeline
./test.sh

```

On NERSC you would run on the nodes under salloc as well and change "local" to "nersc" and "build" to "pull" above.



## Anatomy of a Stage

A Stage is defined in code stored in a subdirectory of one of the directories specified in the `images` option in the pipeline file.
In that directory there must be at least two files:
 - Dockerfile
 - run.py

As an example, look at `images/tomography`.  As well as these two files it also includes another packaged python module, tomography.py.

### Dockerfile

The Dockerfile tells Docker how to build the image where the code is run.  The example in `tomography` is quite short:
```
FROM joezuntz/desc-pipe-base:1.0
MAINTAINER joezuntz@googlemail.com
RUN bash -lc "pip install fitsio"
USER vagrant
COPY tomography.py /opt/desc/
COPY run.py /opt/desc/run.py
```

Each of these commands tells docker to do another step in building this image.  The file starts with the `FROM` directive, which specifies a base image (shown in the `images/base` directory) that is the foundation of this image.  That base image contains the DM stack, among other things.  We may want to revisit this in future and make slimmer images.

The RUN line installs a dependency of the code, fitsio.  We have to do it under bash in order to use the DM stack.
We can look at changing this in future if we use a different base image (I currently use a DM-supplied one).

The other lines run commands in the image and copy files in from the `tomography` directory.

### run.py

The run.py file, which is the fixed entry point to the pipeline stage, must define exactly one class, called `Stage`, which must inherit from `descpipe.Stage`.  This class must have the the class variables shown in the tomography example - a string name, and three dictionaries: `config, inputs, outputs`.  The config directory maps tags to filenames.  The other two map tags to file types.

Any input required by the code must be specified in the inputs dictionary, and similar for the other two categories.  The parent class knows how to find file paths based on the tag.

The file must also have a method `run`, which is executed when the code is launched.  Any imports that do not come built in with python should only be imported within this method.

The run.py should be a thin layer around other libraries, just finding inputs and outputs for them.
The current design of the treecorr run.py isn't great.


## Notes

### Directions for future work

 - Implementing our pipelines stages as Dockerfiles + run.py
 - Standards for installing packages from github rather than packaging locally
 - Better management of images than just using my name for all of them :-)
 - Singularity support
 - Mode for running whole pipeline under python rather than making shell script?
 - Unifying some aspects of launchers and making them *much* less hacky
 - Adding features to check type of input and output files (using types beyond just specifying output suffix "fits")
 - Adding launcher for Pegasus

### What are Docker images?

- Encapsulate an OS and file system.
- Are a bit like a virtual machine but much less unwieldy.
- Are very easy to share machine images.
- Starting to be possible to run on HPC/HTC.
- Can be created from a very simple file.
- Can interact with several other related systems (shifter, singularity)



### System Components

- Pipeline - reads description file and prepares submission scripts.
- Pipes - Dockerfiles with run.py and Dockerfile.
- Launchers - take the pipeline and turns it into jobs, either local, batch (PBS) or pegasus.
- Stages - specifies input/output files
- I/O?  - common (optional?) interface to standard format(s).
- Image management?  Just dockerhub?  Easier.


### Questions

- How should embarassingly parallel jobs be run?
- How should non-embarassingly parallel jobs be run?
- Could the inputs/outputs dictionary be allowed to specify particular schemas?
- Should we always go via a generated submission script or could we operate the pipeline
- How can we enable users to interactively debug the code on production systems?  Should we?

### Possible base images:

- OSG seems to need these ones: https://github.com/opensciencegrid/osgvo-el7
- NERSC needs things based on certain Ubuntu or Centos versions - has to have the right kernel.
- We want the DM stack - might need to have this built ourselves.
- Could we just install all the needed stuff on one giant on - DM, OSG stuff like CVMFS, etc.?


## Non-trivial features needed in current pipeline steps


### tomography

- tomography for metacalibration samples (for selection bias from redshift cuts)

### pz_stack
- stacking/reconstruction methods (e.g. chippr)
- metadata: area, sigma_e,  n_effective  (variants of these)
- mean shear (and metacalibration variant)
- masks 

### treecorr

- parallelization
- calibration
- ggl & w(theta)
- bins in lens sample
- subtraction of mean shears
- region cuts & selection
- randoms for ggl & w(theta)



## Nuns Fret Not at Their Convent's Narrow Room

```
Nuns fret not at their convent’s narrow room; 
And hermits are contented with their cells; 
And students with their pensive citadels; 
Maids at the wheel, the weaver at his loom, 
Sit blithe and happy; bees that soar for bloom, 
High as the highest Peak of Furness-fells, 
Will murmur by the hour in foxglove bells: 
In truth the prison, into which we doom 
Ourselves, no prison is: and hence for me, 
In sundry moods, ’twas pastime to be bound 
Within the Sonnet’s scanty plot of ground; 
Pleased if some Souls (for such there needs must be) 
Who have felt the weight of too much liberty, 
Should find brief solace there, as I have found.
```

by William Wordsworth
