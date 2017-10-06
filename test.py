import descpipe
pipeline=descpipe.Pipeline("master-pipeline.yaml")
launcher=descpipe.LocalDockerLauncher(pipeline)
launcher.generate("test.sh")
