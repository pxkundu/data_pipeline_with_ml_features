#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.s3_stack import S3Stack
from stacks.glue_stack import GlueStack

app = cdk.App()

# Create S3 Stack
s3_stack = S3Stack(app, "S3Stack")

# Create Glue Stack with references to the S3 buckets
glue_stack = GlueStack(
    app,
    "GlueStack",
    raw_bucket=s3_stack.raw_bucket,
    processed_bucket=s3_stack.processed_bucket
)

app.synth()
