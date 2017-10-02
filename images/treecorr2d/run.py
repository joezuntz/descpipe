#!/usr/bin/env python
# Make sure this file is executable.
import treecorr
import descpipe

# Get input and output names etc.


class Stage(descpipe.Stage):
    name = "photoz"
    config = {
        "config": "config.yaml"
    }

    inputs = {
        "catalog": "catalog.fits",
    }

    outputs = {
        "catalog": "correlation-functions.txt",
    }


    def run(self):
        config_file = self.get_config_path("config")
        input_file = self.get_input_path("catalog")
        output_file = self.get_output_path("catalog")

        config = treecorr.read_config(config_file)
        config['file_name'] = input_file
        config['gg_file_name'] = output_file
        treecorr.corr2(config)


Stage.main()