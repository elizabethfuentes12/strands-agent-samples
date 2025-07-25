import aws_cdk as core
import aws_cdk.assertions as assertions

from my_agent_cdk.my_agent_cdk_stack import MyAgentCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_agent_cdk/my_agent_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyAgentCdkStack(app, "my-agent-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
