import os
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3_notifications,
    aws_s3 as s3,
)
from constructs import Construct

from lambdas.code.project_lambdas import Lambdas
from s3_cloudfront import S3Deploy
BucketKeyName = "my-1-strands-agents-"
_model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
BucketSampleContent = "image"


class MyAgentCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stk = Stack.of(self)
        _account = stk.account
        _region = stk.region
        _stack_name = stk.stack_name

        s3_deploy = S3Deploy(self, "-image", BucketSampleContent,BucketKeyName)

        Fn  = Lambdas(self,'Lambdas')

        Fn.weather_function.add_to_role_policy(
            iam.PolicyStatement( 
                actions=["bedrock:InvokeAgent","bedrock:InvokeModelWithResponseStream","bedrock:InvokeModel"], 
                resources=[f"*"]
                )
                )
        
        Fn.multimodal_function.add_to_role_policy(
            iam.PolicyStatement( 
                actions=["bedrock:InvokeAgent","bedrock:InvokeModelWithResponseStream","bedrock:InvokeModel"], 
                resources=[f"*"]
                )
                )
        
        s3_deploy.bucket.grant_read(Fn.multimodal_function)

        #s3_deploy.bucket.add_event_notification(s3.EventType.OBJECT_CREATED,
        #                                      aws_s3_notifications.LambdaDestination(Fn.multimodal_function),
        #                                      s3.NotificationKeyFilter(prefix=BucketSampleContent+"/"))
        
        
        Fn.multimodal_function.add_environment("REGION_NAME", _region)

        Fn.multimodal_function.add_environment("MODEL_ID", _model_id)
        


        

        
