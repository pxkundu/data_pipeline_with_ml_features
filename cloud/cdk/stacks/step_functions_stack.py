from aws_cdk import Stack, aws_stepfunctions as sfn, aws_stepfunctions_tasks as tasks
from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_glue as glue
from aws_cdk import aws_s3 as s3
from aws_cdk import Duration


class StepFunctionsStack(Stack):
    def __init__(self, scope: Construct, id: str, glue_job: glue.CfnJob, sagemaker_role: iam.Role, processed_bucket: s3.Bucket, input_path, output_path, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Glue Task
        glue_task = tasks.GlueStartJobRun(
            job_name=glue_job.name,
            arguments={
                '--input_path': input_path,
                '--output_path': output_path
            },
            retry=tasks.Retry(
                max_attempts=3,
                backoff_rate=2
            )
        )
        glue_task = tasks.GlueStartJobRun(
            self, "GlueTask",
            glue_job_name=glue_job.ref,  # Reference Glue job dynamically
            result_path="$.glue_result",
            retry_count=3,
            timeout=Duration.minutes(30)
        )

        # SageMaker Task
        sagemaker_task = tasks.SageMakerCreateTrainingJob(
            self, "SageMakerTrainingTask",
            training_job_name="SimpleTrainingJob",
            algorithm_specification=tasks.AlgorithmSpecification(
                training_image=tasks.DockerImage.from_registry(
                    "382416733822.dkr.ecr.us-east-1.amazonaws.com/linear-learner:latest"
                ),
                training_input_mode=tasks.InputMode.FILE,
            ),
            input_data_config=[
                tasks.Channel(
                    channel_name="training",
                    data_source=tasks.DataSource(
                        s3_data_source=tasks.S3DataSource(
                            s3_uri=f"s3://{processed_bucket.bucket_name}/training-data/",
                            s3_data_type=tasks.S3DataType.S3_PREFIX,
                            s3_data_distribution_type=tasks.S3DataDistributionType.FULLY_REPLICATED,
                        )
                    ),
                    content_type="text/csv",
                )
            ],
            output_data_config=tasks.OutputDataConfig(
                s3_output_path=f"s3://{processed_bucket.bucket_name}/model-output/"
            ),
            resource_config=tasks.ResourceConfig(
                instance_count=1,
                instance_type="ml.m5.large",
                volume_size=10,
            ),
            stopping_condition=tasks.StoppingCondition(
                max_runtime=3600
            ),
            role=sagemaker_role,
        )

        # State Machine
        self.state_machine = sfn.StateMachine(
            self,
            "PipelineStateMachine",
            definition=sfn.Chain(
                glue_task,
                sfn.Choice(
                    self, "Check Glue Task Result",
                    input_path="$.glue_result",
                    choices=[
                        sfn.ChoiceRule(
                            variable="$.glue_result.State",
                            string_equals="SUCCEEDED",
                            next=sagemaker_task
                        ),
                        sfn.ChoiceRule(
                            variable="$.glue_result.State",
                            string_equals="FAILED",
                            next=sfn.Fail(
                                self, "Glue Task Failed",
                                cause="Glue task failed",
                                error="Error occurred during glue task execution"
                            )
                        )
                    ],
                    default=sfn.Fail(
                        self, "Invalid Glue Task Result",
                        cause="Invalid glue task result",
                        error="Error occurred during glue task execution"
                    )
                ),
                sfn.Choice(
                    self, "Check SageMaker Task Result",
                    input_path="$.SageMakerTrainingTask",
                    choices=[
                        sfn.ChoiceRule(
                            variable="$.SageMakerTrainingTask.TrainingJobStatus",
                            string_equals="Completed",
                            next=sfn.Succeed(
                                self, "Pipeline Succeeded",
                                comment="Pipeline execution succeeded"
                            )
                        ),
                        sfn.ChoiceRule(
                            variable="$.SageMakerTrainingTask.TrainingJobStatus",
                            string_equals="Failed",
                            next=sfn.Fail(
                                self, "SageMaker Task Failed",
                                cause="SageMaker task failed",
                                error="Error occurred during SageMaker task execution"
                            )
                        )
                    ],
                    default=sfn.Fail(
                        self, "Invalid SageMaker Task Result",
                        cause="Invalid SageMaker task result",
                        error="Error occurred during SageMaker task execution"
                    )
                )
            )
        )