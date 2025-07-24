import sys

from aws_cdk import (
    Duration,
    aws_lambda,
    aws_ssm as ssm,
    Stack,
    aws_iam as iam,

)

from constructs import Construct


LAMBDA_TIMEOUT= 30

BASE_LAMBDA_CONFIG = dict (
    timeout=Duration.seconds(LAMBDA_TIMEOUT),       
    memory_size=256,
    tracing= aws_lambda.Tracing.ACTIVE,
    architecture=aws_lambda.Architecture.ARM_64)

COMMON_LAMBDA_CONF = dict (runtime=aws_lambda.Runtime.PYTHON_3_12, **BASE_LAMBDA_CONFIG)

from layers import Layers


class Lambdas(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Lay = Layers(self, 'Lay')

        # Define the Lambda function
        self.weather_function = aws_lambda.Function(
            self, "AgentSLambda",
            function_name="AgentSFunction",
            description="A function that invokes a weather forecasting agent",
            handler="agent_handler.handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/lambda-s-agent"),
            layers=[Lay.strands_layer],**COMMON_LAMBDA_CONF
        )

        # Define the Lambda function
        self.multimodal_function = aws_lambda.Function(
            self, "StrandsAgentMultimodalLambda",
            function_name="StrandsAgentMultimodalLambda",
            description="A function that invokes a multimodal agent",
            handler="agent_handler.handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/lambda-s-multimodal"),
            layers=[Lay.strands_layer],**COMMON_LAMBDA_CONF
        )
