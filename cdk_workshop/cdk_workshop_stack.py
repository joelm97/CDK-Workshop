from constructs import Construct
from aws_cdk import (

    Stack,
    aws_lambda as _lambda, #imports lambda module
    aws_apigateway as apigw,
  
)
from .hitcounter import HitCounter
from cdk_dynamo_table_view import TableViewer

#class constructors: self, scope: construct, id (local identity), **kwargs (initliaze arguments)
class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        #hello is file name, handler is function name
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_with_counter._handler, #routes request to hit counter handler to my_lambda function
        )
        TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table,
        )