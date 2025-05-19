from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct


class VPCStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._vpc = ec2.Vpc(
            self, "Analytics-SageMakerVPC",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Analytics-PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Analytics-PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ]
        )

        self._security_group = ec2.SecurityGroup(
            self, "Analytics-SageMakerSG",
            vpc=self._vpc,
            allow_all_outbound=True,
            description="Security group for SageMaker Domain"
        )

        self._s3_endpoint = self._vpc.add_gateway_endpoint(
            "Analytics-S3GatewayEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
            subnets=[
                ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
            ]
        )

    @property
    def vpc(self) -> ec2.Vpc:
        return self._vpc

    # @property
    # def private_subnets(self) -> list:
    #     # Return first private subnet ID (you can generalize to a list if needed)
    #     return self._vpc.private_subnets

    @property
    def private_subnet_id(self) -> str:
        return self._vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnet_ids[0]

    @property
    def security_group_id(self) -> str:
        return self._security_group.security_group_id

    @property
    def s3_endpoint_id(self) -> str:
        return self._s3_endpoint.vpc_endpoint_id
