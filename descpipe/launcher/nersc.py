
# Use a temporary directory in $SCRATCH as the workspace
# Generate batch scripts
# Make a run directory with all the scripts in also on SCRATCH in the workspace


class NerscShifterLauncher(Launcher):

    def generate(self, script_name):
        self._check_inputs()
        # Generate a bash script to run the pipeline locally under docker
        # Assume stages all built already
        lines = ['#!/bin/sh']
        lines.append("mkdir -p {}".format(self._data_dir()))

        for stage_name, stage_class in self.pipeline.serial_sequence():
            lines.append("\n### Run pipeline stage {} ###\n".format(stage_name))
            lines += self._script_for_stage(stage_name, stage_class)


        lines.append("\n### Now pipeline is complete. Copy results out. ###\n".format(stage_name))

        # Final copy out of results
        line = """
if [ ! -z "$(ls -A {data_dir})" ];
then
    mv {data_dir}/* {output_dir}/
fi
    """.format(data_dir=self._data_dir(), output_dir=self.output_dir())
        lines.append(line)
        lines.append("\n")

        with open(script_name, 'w') as script:
            script.write('\n'.join(lines))
        utils.make_user_executable(script_name)


