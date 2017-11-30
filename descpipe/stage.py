import os
import sys
import functools

parallelism_serial = "serial"
parallelism_mpi = "mpi"
parallelism_embarassing = "embarassing"

def at_runtime_only(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.at_runtime:
            raise RuntimeError("Method {} can only be called when pipeline is actually running".format(method.__name__))
        return method(self, *args, **kwargs)
    return wrapper

class Stage:
    def __init__(self):
        self.parallelism = None
        self.at_runtime = False

    def build_paths(self, args):
        paths = {}
        self._input_paths = {}
        self._output_paths = {}
        self._config_paths = {}
        for arg in args:
            name, path = arg.split('=', 1)
            paths[name] = path

        for tag in self.inputs:
            self._input_paths[tag] = paths[tag]

        for tag in self.outputs:
            self._output_paths[tag] = paths[tag]

        for tag in self.config:
            self._config_paths[tag] = paths[tag]

    @classmethod
    def main(cls):
        stage = cls()
        stage.at_runtime = True
        stage.build_paths(sys.argv[1:])
        stage.run()

    def check_inputs():
        pass

    @at_runtime_only
    def get_input_path(self, name):
        "Return the path to an input file from the tag name"
        return self._input_paths[name]

    @at_runtime_only
    def get_output_path(self, name):
        "Return the path to an output file from the tag name"
        return self._output_paths[name]

    @at_runtime_only
    def get_config_path(self, name):
        "Return the complete path to a configuration file from the tag name"
        return self._config_paths[name]

    def _setup_parallel_runtime(self):
        parallelism = os.environ.get("DESC_PARALLEL", parallelism_serial)
        self.parallelism = parallelism
        self._comm = None
        if parallelism == parallelism_serial:
            self._rank = 0
            self._size = 1
        elif parallelism == parallelism_embarassing:
            self._rank = os.environ['DESC_RANK']
            self._size = os.environ['DESC_SIZE']
        elif parallelism == parallelism_mpi:
            from mpi4py.MPI import COMM_WORLD
            self._comm = comm
            self._rank = comm.Get_rank()
            self._size = comm.Get_size()
        else:
            self.parallelism = None
            raise ValueError("Unknown parallelism mode: {}".format(parallelism))

    @at_runtime_only
    def get_comm(self):
        if self.parallelism is None:
            self._setup_parallel_runtime()
        return self._comm

    @at_runtime_only
    def get_rank(self):
        if self.parallelism is None:
            self._setup_parallel_runtime()
        return self._rank

    @at_runtime_only
    def get_size(self):
        if self.parallelism is None:
            self._setup_parallelism()
        return self._size
