import os
from .. import utils
from .launcher import Launcher
from ..errors import InputError
import shutil

class CWLLauncher(Launcher):

    def workflow_inputs(self):
        inputs = {}
        for tag in self.pipeline.input_tags():
            inputs[tag] = "File"
        return inputs

    def _generate_stage_tool(self, dirname, stage_name, stage_class):
        import yaml
        tool = {}
        tool['class'] = "CommandLineTool"
        tool['cwlVersion'] = 'v1.0'
        tool['stderr'] = '{}-stderr.txt'.format(stage_name)
        tool['stdout'] = '{}-stdout.txt'.format(stage_name)

        image = self.pipeline.image_name(stage_name)
        tool['requirements'] = {'DockerRequirement':{'dockerPull':image}}

        position = 1
        inputs = {}
        for tag in stage_class.inputs:
            binding = {'prefix':'{}='.format(tag), 'separate':False, 'position':position}
            inputs[tag] = {'type':'File', 'inputBinding':binding}
            position += 1

        tool['inputs'] = inputs
        
        outputs = {}
        arguments = []
        for tag,file_type in stage_class.outputs.items():
            output_filename = '{}.{}'.format(tag, file_type)
            outputs[tag] = {'type':'File', 'outputBinding':{'glob':output_filename}}
            arguments.append("{}={}".format(tag,output_filename))
        tool['outputs'] = outputs
        tool['arguments'] = arguments

        tool['baseCommand'] = 'bash -lc /opt/desc/run.py'.split()

        filename = self._tool_filename(dirname, stage_name)
        tool_file = open(filename, 'w')
        tool_file.write("#!/usr/bin/env cwl-runner\n")
        yaml.dump(tool, tool_file)
        tool_file.close()

            

    def _tool_filename(self, dirname, stage_name):
        filename = os.path.join(dirname, stage_name+'.tool')
        return filename


    def generate(self, dirname):
        import yaml
        workflow = {}
        workflow['class'] = "Workflow"
        workflow['cwlVersion'] = 'v1.0'

        steps = {}
        overall_inputs = {}
        overall_outputs = {}
        workflow['inputs'] = overall_inputs
        workflow['outputs'] = overall_outputs
        workflow['steps'] = steps

        # Record where inputs come from for later stages
        # this information should be in the pipeline object I think
        input_sources = {}
        

        # Overall inputs for the whole pipeline
        for tag in self.pipeline.input_tags():
            overall_inputs[tag] = {'type':'File'}

        # All the stages in the pipeline
        for stage_name, stage_class in self.pipeline.sequence():

            # Each stage needs a separate CWL file as well as this main one
            self._generate_stage_tool(dirname, stage_name, stage_class)

            stage = {}
            stage['run'] = stage_name + '.tool'

            # Outputs.  We do two things:
            # Record for the overall pipeline that this is an output
            # Record that it is an output for this particular stage,
            # So that later stages can find it.
            output_tags = list(stage_class.outputs.keys())
            stage['out'] = output_tags
            for tag in output_tags:
                overall_outputs[tag] = {'type':'File', 'outputSource':"{}/{}".format(stage_name,tag)}
                input_sources[tag] = stage_name

            # Inputs - two cases, either overall inputs to the whole pipeline
            # or from a previous stage
            inputs = {}
            for tag in stage_class.inputs:
                if tag in input_sources:
                    inputs[tag] = '{}/{}'.format(input_sources[tag], tag)
                else:
                    inputs[tag] = tag
            stage['in'] = inputs

            steps[stage_name] = stage

        filename = os.path.join(dirname, 'workflow.cwl')
        workflow_file = open(filename, 'w')
        workflow_file.write("#!/usr/bin/env cwl-runner\n")
        yaml.dump(workflow, workflow_file)

        # We also need the job.yml which defines inputs for this particular run
        job = {}
        for tag in overall_inputs:
            path = self.info['inputs'].get(tag)
            path = os.path.abspath(path)
            job[tag] = {'class':'File', 'path':path}

        filename = os.path.join(dirname, 'job.yml')
        job_file = open(filename, 'w')
        yaml.dump(job, job_file)





