import descpipe
pipeline=descpipe.Pipeline("master-pipeline.yaml")
pipeline.to_local_serial_docker("test.sh")
