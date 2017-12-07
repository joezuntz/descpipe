import os
from .. import utils
from .script_launcher import ScriptLauncher
from ..errors import InputError


class NerscSerialLauncher(ScriptLauncher):
    script_template = """#!/bin/sh

    set -e
    {% for script in scripts %}
    {{script}}
    {% endfor %}


    function descpipe_launch {
        mkdir -p {{data_dir}}

        # Main run
        {% for stage_name  in stage_names %}run_{{stage_name}}
        {% endfor %}

        # Pipeline now complete.  Copy out results
        mkdir -p {{output_dir}}
        if [ ! -z "$(ls -A {{data_dir}})" ];
        then
            mv {{data_dir}}/* {{output_dir}}/
        fi
    }

    descpipe_launch


    """

    stage_template = """
    function run_{{stage_name}} {
        echo Running pipeline stage {{stage_name}}

        # Make working directories
        mkdir -p {{input_dir}}
        mkdir -p {{output_dir}}
        mkdir -p {{config_dir}}

        # Make output directory"
        mkdir -p {{host_output_dir}}

        # Hard link config and input files
        {% for path,task_path in input_paths %}cp {{path}}  {{task_path}}
        {% endfor %}

        # Run docker image
        {{cmd}}

        {% for task_path, path in output_paths %}cp {{task_path}}  {{path}}
        {% endfor %}


    }

    """

    def _docker_command(self, stage_name):
        input_dir, output_dir, config_dir = self._task_dirs(stage_name)
        image = self.pipeline.image_name(stage_name)
        input_mount = "-V {}:/opt/input".format(os.path.abspath(input_dir))
        output_mount = "-V {}:/opt/output".format(os.path.abspath(output_dir))
        config_mount = "-V {}:/opt/config".format(os.path.abspath(config_dir))
        flags = [input_mount, output_mount, config_mount]
        cmd = "shifter --image={image} {input_mount} {output_mount} {config_mount} /opt/desc/run.py".format(**locals())
        return cmd
