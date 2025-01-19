from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
)
from constructs import Construct
import os

class LambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define Lambda function
        function = _lambda.Function(
            self,
            "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda_code")),
        )

        # Grant necessary permissions
        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:*"],
                resources=["*"]
            )
        )
