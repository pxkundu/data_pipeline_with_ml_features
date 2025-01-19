from aws_cdk import Stack, aws_s3 as s3, RemovalPolicy
from constructs import Construct

class S3Stack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 bucket for raw data
        self.raw_bucket = s3.Bucket(
            self,
            "RawDataBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # S3 bucket for processed data
        self.processed_bucket = s3.Bucket(
            self,
            "ProcessedDataBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )
