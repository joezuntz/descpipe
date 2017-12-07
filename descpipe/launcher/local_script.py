import os
from .. import utils
from .script_launcher import ScriptLauncher
from ..errors import InputError

class LocalScriptLauncher(ScriptLauncher):

    script_template = """#!/bin/sh

    set -e
    {% for script in scripts %}
    {{script}}
    {% endfor %}


    function descpipe_launch {
        mkdir -p {{data_dir}}

        # Main run
        {% for stage_name  in stage_names %}
        run_{{stage_name}}
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
        {% for path,task_path in input_paths %}ln -f {{path}}  {{task_path}}
        {% endfor %}

        # Run docker image
        {{cmd}}

        {% for task_path, path in output_paths %}ln -f {{task_path}}  {{path}}
        {% endfor %}


    }

    """
