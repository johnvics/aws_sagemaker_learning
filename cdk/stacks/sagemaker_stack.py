from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_sagemaker as sagemaker
)
from constructs import Construct


class SageMakerStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc, private_subnet_id, security_group_id, execution_role_arn, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Optional: create a bucket or refer to one
        bucket = s3.Bucket(self, "SSM-SageMakerDataBucket")

        try:
            domain = sagemaker.CfnDomain(
                self, "Analytics-SageMakerDomain",
                domain_name="analytics-sagemaker-domain",
                auth_mode="IAM",
                vpc_id=vpc.vpc_id,
                subnet_ids=[private_subnet_id],
                default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
                    execution_role=execution_role_arn,
                    security_groups=[security_group_id]
                )
            )
        except Exception as e:
            print("Failed to create SageMaker Domain:", e)
            raise

        sagemaker.CfnUserProfile(
            self, "UserProfile",
            domain_id=domain.attr_domain_id,
            user_profile_name="analytics-poc-admin",
            user_settings=sagemaker.CfnUserProfile.UserSettingsProperty(
                execution_role=execution_role_arn
            )
        )

    @property
    def bucket_name(self) -> str:
        return self.bucket.bucket_name

    @property
    def role_arn(self) -> str:
        return self.sagemaker_role.role_arn

    @property
    def domain_id(self) -> str:
        return self.domain.attr_domain_id
