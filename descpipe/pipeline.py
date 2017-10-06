import yaml
import importlib.util
import os
from .errors import PipelineError

special_keys = ['pipeline', 'runtime']



class Pipeline:

    def __init__(self, input_file):
        self.cfg = self._read(input_file)

        self.info = self.cfg['pipeline']

        self.owner = self.info['owner']
        self.basename = self.info['basename']
        self.version = self.info['version']

        self.stages = {
            name: self.load_stage(name)
            for name in self.info['stages']
        }

    def load_stage(self, name):
        for dirname in self.info['images']:
            dirpath = os.path.join(dirname,name)
            dockerfile_path = os.path.join(dirpath, "Dockerfile")
            run_path = os.path.join(dirpath, "run.py")
            if os.path.isdir(dirpath) and os.path.isfile(dockerfile_path) and os.path.isfile(run_path):
                path = run_path
                break
        else:
            raise PipelineError("""No Stage called {} was found - needs to be in one 
                of the images directories and contain Dockerfile, run.py""".format(name))

        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Stage


    def inputs(self):
        "Return a set of all input tags required by the pipeline and not generated inside it."
        pipeline_inputs = set()
        # Find all the inputs expected by the pipeline
        for stage in self.stages.values():
            pipeline_inputs.update(stage.inputs.keys())
        # Remove any stages that are generated by any step in the pipeline
        for stage in self.stages.values():
            pipeline_inputs.difference_update(stage.outputs.keys())

        return pipeline_inputs




    def _read(self, input_file):
        "Read a YAML file represnting a pipline"
        if not hasattr(input_file, 'read'):
            input_file = open(input_file)
        info = yaml.load(input_file)
        return info



    def image_name(self, name):
        "Return the expected image name for a given stage based on information in the pipeline file"
        return '{}/{}-{}:{}'.format(self.owner,self.basename, name, self.version)


    def serial_sequence(self):
        # for serial systems, choose an ordering for the pipeline
        # TODO: order this
        return self.stages.items()
