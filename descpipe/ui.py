import argparse
import sys

from .pipeline import Pipeline
from .launcher import LocalDockerLauncher

parser = argparse.ArgumentParser(description="Manage, build, and launch DESC pipelines")
subparsers = parser.add_subparsers(help="What to do with the pipeline", dest='task')


parser_local = subparsers.add_parser('local', help='Make a bash script to the pipeline locally under docker')
parser_local.add_argument('pipe_file', type=str, help='Input pipeline file to generate a script for')
parser_local.add_argument('script_file', type=str, help='Output bash script to generate')
parser_local.add_argument('-b', "--build",  action='store_true', help='Run "make" in the pipe directories before running')

parser_local = subparsers.add_parser('build', help='Run "make" in the pipe directories')
parser_local.add_argument('pipe_file', type=str, help='Input pipeline file to build')

parser_local = subparsers.add_parser('push', help='Run "make push" in the pipe directories')
parser_local.add_argument('pipe_file', type=str, help='Input pipeline file to push')

def build(args):
    pipeline=Pipeline(args.pipe_file)
    pipeline.build()

def push(args):
    pipeline=Pipeline(args.pipe_file)
    pipeline.push()


def local(args):
    pipeline=Pipeline(args.pipe_file)
    if args.build:
        pipeline.build()
    launcher=LocalDockerLauncher(pipeline)
    launcher.generate(args.script_file)

def main():
    args = parser.parse_args()
    if not args.task:
        parser.print_help()
    if args.task=='local':
        local(args)
    elif args.task=='build':
        build(args)
    elif args.task=='push':
        push(args)
    else:
        sys.stderr.write("Unknown command {}\n".format(args.task))

if __name__ == '__main__':
    status = main()
    sys.exit(status)

