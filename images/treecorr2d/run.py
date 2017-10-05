#!/usr/bin/env python
# Make sure this file is executable.
import descpipe

# Get input and output names etc.


class Stage(descpipe.Stage):
    name = "photoz"
    config = {
        "config": "config.yaml"
    }

    inputs = {
        "shear_catalog.fits": "catalog.fits",
    }

    outputs = {
        "correlation_functions.txt": "correlation-functions.txt",
    }


    def run(self):
        # Imports must be in here
        import treecorr

        config_file = self.get_config_path("config")
        input_file = self.get_input_path("shear_catalog")
        output_file = self.get_output_path("correlation_functions")

        config = treecorr.read_config(config_file)
        config['file_name'] = input_file
        config['gg_file_name'] = output_file
        treecorr.corr2(config)



# Always end with this
if __name__ == '__main__':
    Stage.main()
