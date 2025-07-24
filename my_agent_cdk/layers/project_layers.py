import json
import os
from constructs import Construct

from aws_cdk import (
    aws_lambda

)


class Layers(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define packaging directory path
        packaging_directory = os.path.join(os.path.dirname(__file__), "./strands/")
        
        zip_dependencies = os.path.join(packaging_directory, "dependencies.zip")

        # Create a lambda layer with dependencies to keep the code readable in the Lambda console
        self.strands_layer = aws_lambda.LayerVersion(
            self, "DependenciesStrandsLayer",
            code=aws_lambda.Code.from_asset(zip_dependencies),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_12],
            description="Dependencies needed for Strands agent Lambda"
        )


