import descpipe
pipeline=descpipe.Pipeline("master-pipeline.yaml")
translator=descpipe.LocalDockerTranslator(pipeline)
translator.generate("test.sh")
