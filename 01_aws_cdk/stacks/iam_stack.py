from aws_cdk import (
    Stack,
    aws_iam as iam
)
from constructs import Construct


class IAMStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Execution role for SageMaker users
        self.sagemaker_execution_role = iam.Role(
            self, "Analytics-SageMakerExecutionRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            description="Execution role for SageMaker Studio users",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess")
            ]
        )

    @property
    def execution_role_arn(self) -> str:
        return self.sagemaker_execution_role.role_arn
    2