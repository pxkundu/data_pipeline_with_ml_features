from aws_cdk import Stack, aws_glue as glue, aws_iam as iam, aws_s3 as s3
from constructs import Construct

class GlueStack(Stack):
    def __init__(self, scope: Construct, id: str, raw_bucket: s3.Bucket, processed_bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Glue Role
        glue_role = iam.Role(
            self, "GlueRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
            ],
        )

        # Glue Job
        self.glue_job = glue.CfnJob(
            self, "ETLJob",
            role=glue_role.role_arn,
            command={
                "name": "glueetl",
                "scriptLocation": f"s3://{raw_bucket.bucket_name}/scripts/etl_job.py",
                "pythonVersion": "3",
            },
            default_arguments={
                "--RAW_BUCKET": raw_bucket.bucket_name,
                "--PROCESSED_BUCKET": processed_bucket.bucket_name,
                "--TEMP_DIR": f"s3://{processed_bucket.bucket_name}/temp/",
                "--job-bookmark-option": "job-bookmark-enable"
            },
            glue_version="3.0"
        )
