import os
# Use a temporary directory in $SCRATCH as the workspace
# Generate batch scripts
# Make a run directory with all the scripts in also on SCRATCH in the workspace


class NerscShifterLauncher(Launcher):
    def working_dir(self):
        return self.info['working']

    def script_dir(self):
        return os.path.join(self._working_dir(), 'batch')

    def generate(self, script_name):
        self._check_inputs()
        # Maybe do a shifterimg pull command for each step?
        os.mkdirs(self.script_dir())


        lines = ['#!/bin/sh']
        lines.append("mkdir -p {}".format(self._data_dir()))

        for stage_name, stage_class in self.pipeline.sequence():
            self._batch_script_for_stage(stage_name, stage_class)


    def _batch_script_for_stage(stage_name, stage_class):
        processes = self.
        """#!/usr/bin/env bash
#SBATCH
blah blah blah
srun -N {nodes} shifter run {image}
        """        
