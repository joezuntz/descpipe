import argparse
import sys

from .pipeline import Pipeline
from .launcher import LocalDockerLauncher

parser = argparse.ArgumentParser(description="Manage, build, and launch DESC pipelines")
subparsers = parser.add_subparsers(help="What to do with the pipeline", dest='task')


parser_local = subparsers.add_parser('local', help='Make a bash script to the pipeline locally under docker')
parser_local.add_argument('pipe_file', type=str, help='Input pipeline file to draw')
parser_local.add_argument('script_file', type=str, help='Output bash script to generate')

def local(args):
    pipeline=Pipeline(args.pipe_file)
    launcher=LocalDockerLauncher(pipeline)
    launcher.generate(args.script_file)

def main():
    args = parser.parse_args()
    if not args.task:
        parser.print_help()
    if args.task=='local':
        local(args)
    else:
        sys.stderr.write("Unknown command {}\n".format(args.task))

if __name__ == '__main__':
    status = main()
    sys.exit(status)

