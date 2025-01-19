from aws_cdk import Stack, aws_iam as iam, aws_s3 as s3
from constructs import Construct

class SageMakerStack(Stack):
    def __init__(self, scope: Construct, id: str, processed_bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # SageMaker Role
        self.sagemaker_role = iam.Role(
            self, "SageMakerRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
            ],
        )
