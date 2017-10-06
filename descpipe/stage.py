import os
import sys
import argparse


class Stage:
    def __init__(self):
        self.config_dir = os.environ['DESC_CONFIG']
        self.input_dir = os.environ['DESC_INPUT']
        self.output_dir = os.environ['DESC_OUTPUT']

    @classmethod
    def main(cls):
        stage = cls()
        stage.run()

    def get_config_path(self, name):
        filename = self.config[name]
        return os.path.join(self.config_dir, filename)

    def get_input_path(self, name):
        filename = self.inputs[name]
        return os.path.join(self.input_dir, filename)

    def get_output_path(self, name):
        filename = self.outputs[name]
        return os.path.join(self.output_dir, filename)

