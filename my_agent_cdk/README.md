# AWS CDK Multi-Modal Agent Deployment

## Introduction

This is a Python-based CDK (Cloud Development Kit) project that demonstrates how to deploy serverless Lambda functions implementing the Strands Agent framework. The project includes two Lambda functions:

1. **Weather Forecasting Agent** - A simple agent that provides weather forecasting capabilities
2. **Multi-Modal Processing Agent** - An advanced agent that can process and analyze different types of media (images, documents, videos)

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured
- Python 3.8 or later
- [jq](https://stedolan.github.io/jq/) (optional) for formatting JSON output
- AWS account with Bedrock access

## Project Structure

- `agent_lambda/` - Contains the CDK stack definition in Python
- `app.py` - Main CDK application entry point
- `layers/` - Contains Lambda layers for the Strands Agent framework
  - `package_for_lambda.py` - Python script that packages Lambda code and dependencies into deployment archives
  - `lambda_requirements.txt` - Dependencies for the Lambda functions
- `lambdas/code/` - Contains the Lambda function code
  - `lambda-s-agent/` - Weather forecasting agent Lambda function
  - `lambda-s-multimodal/` - Multi-modal processing agent Lambda function

## Setup and Deployment

1. Create a Python virtual environment and install dependencies:

```bash
# Create a Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install CDK dependencies
pip install -r requirements.txt

# Install Python dependencies for lambda with correct architecture
pip install -r layers/lambda_requirements.txt --python-version 3.12 --platform manylinux2014_aarch64 --target layers/strands/_dependencies --only-binary=:all:
```

2. Package the lambda layers:

```bash
python layers/package_for_lambda.py
```

3. Bootstrap your AWS environment (if not already done):

```bash
cdk bootstrap
```

4. Deploy the stack:

```bash
cdk deploy
```

## Usage

After deployment, you can invoke the Lambda functions using the AWS CLI or AWS Console.

### Weather Forecasting Agent

```bash
aws lambda invoke --function-name AgentSFunction \
      --region us-east-2 \
      --cli-binary-format raw-in-base64-out \
      --payload '{"prompt": "What is the weather in New York?"}' \
      output.json
```

### Multi-Modal Processing Agent

```bash
aws lambda invoke --function-name MultimodalSFunction \
      --region us-east-2 \
      --cli-binary-format raw-in-base64-out \
      --payload '{"prompt": "Analyze this image", "s3object": "s3://your-bucket/path/to/image.jpg"}' \
      output.json
```

If you have jq installed, you can output the response from output.json like so:

```bash
jq -r '.' ./output.json
```

Otherwise, open output.json to view the result.

## Multi-Modal Processing Capabilities

The Multi-Modal Processing Agent can handle various types of media:

- **Images**: PNG, JPEG/JPG, GIF, WebP
- **Documents**: PDF, CSV, DOCX, XLS, XLSX
- **Videos**: MP4, MOV, AVI, MKV, WebM

The agent uses custom tools built with the Strands Agent framework to process and analyze these media types.

## Cleanup

To remove all resources created by this example:

```bash
cdk destroy
```

## Additional Resources

- [AWS CDK Python Documentation](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- [Strands Agent Framework Documentation](https://github.com/aws-samples/strands-framework)
