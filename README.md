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

&