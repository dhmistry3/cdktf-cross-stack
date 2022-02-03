# standard
import getpass
from typing import Union

#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import AwsProvider, AwsProviderDefaultTags
from imports.aws.datasources import DataAwsCallerIdentity, DataAwsRegion
from imports.aws.sqs import SqsQueue
from imports.aws.lambdafunction import LambdaFunction, LambdaFunctionEnvironment

ROLE=''

class GeneralStack(TerraformStack):
    """
    Base stack to use for other stacks
    """
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        AwsProvider(
            self,
            "Aws",
            region='us-east-2',
            default_tags=AwsProviderDefaultTags(
                tags={
                    "deployment": "terraform",
                    "deployer": getpass.getuser(),
                }
            ),
        )
        
        caller = DataAwsCallerIdentity(self, "caller_id")
        region = DataAwsRegion(self, "current_region")

class SqsStack(GeneralStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        
        # define resources here
        sqs_queue = SqsQueue(
                self,
                "dm-test-sqs",
                name = "dm-test-sqs",
            )
        
        self.sqs_arn = sqs_queue.arn

class MyStack(GeneralStack):
    def __init__(self, scope: Construct, ns: str, sqs: str):
        super().__init__(scope, ns)

        # define resources here
        LambdaFunction(
            self,
            'dm-test-lambda',
            filename='./lambda_function.zip',
            function_name='dm-test-lambda',
            role = ROLE,
            handler='lambda_function.lambda_handler',
            runtime='python3.8',
            environment=LambdaFunctionEnvironment(variables={
                'sqs': sqs
            })
        )

app = App()
sqs_stack = SqsStack(app, 'sqs_stack')
MyStack(app, 'lambda_stack', sqs_stack.sqs_arn)

app.synth()
