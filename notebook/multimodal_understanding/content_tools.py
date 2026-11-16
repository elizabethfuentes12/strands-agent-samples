"""
Content generation tools for Strands Agents (images and videos on Amazon Bedrock).

These custom tools replace the `generate_image`, `nova_reels` and `use_aws` tools that were
removed from `strands-agents-tools` in 0.9.0 (see
https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/).

- Images: Stability AI Stable Image Core via InvokeModel.
  https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-stable-image-core-text-image-request-response.html
- Videos: Luma AI Ray 2 via the asynchronous APIs StartAsyncInvoke / GetAsyncInvoke.
  https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-luma.html
  (Amazon Nova Reel reached end of life on Amazon Bedrock on September 30, 2026.)

Both models are offered in us-west-2; the output S3 bucket for video generation must be in the
same region as the Bedrock endpoint you call.
"""
import base64
import json
import os
import time
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError
from strands import tool

DEFAULT_REGION = os.getenv("CONTENT_TOOLS_REGION", "us-west-2")
IMAGE_MODEL_ID = os.getenv("IMAGE_MODEL_ID", "stability.stable-image-core-v1:1")
VIDEO_MODEL_ID = os.getenv("VIDEO_MODEL_ID", "luma.ray-v2:0")

_IMAGE_ASPECT_RATIOS = {"16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"}
_VIDEO_ASPECT_RATIOS = {"1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"}


@tool
def generate_image(
    prompt: str,
    output_path: str,
    aspect_ratio: str = "16:9",
    negative_prompt: Optional[str] = None,
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate an image from a text prompt with Stability AI Stable Image Core on Amazon Bedrock
    and save it as a PNG file.

    Args:
        prompt: What you wish to see in the image (up to 10,000 characters). Describe subject,
            lighting, composition and mood.
        output_path: Local file path where the PNG will be written (e.g. "output/barcelona.png").
        aspect_ratio: One of 16:9, 1:1, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21. Default 16:9.
        negative_prompt: Keywords of what you do not want in the image (optional).
        region: AWS region of the Bedrock endpoint (default: us-west-2).

    Returns:
        Dictionary with status, the saved file path and the seed used by the model.
    """
    if aspect_ratio not in _IMAGE_ASPECT_RATIOS:
        return {"status": "error", "content": [{"text": f"❌ Invalid aspect_ratio {aspect_ratio}. Use one of {sorted(_IMAGE_ASPECT_RATIOS)}"}]}

    body: Dict[str, Any] = {
        "prompt": prompt,
        "mode": "text-to-image",
        "aspect_ratio": aspect_ratio,
        "output_format": "png",
    }
    if negative_prompt:
        body["negative_prompt"] = negative_prompt

    try:
        bedrock = boto3.client("bedrock-runtime", region_name=region or DEFAULT_REGION)
        response = bedrock.invoke_model(modelId=IMAGE_MODEL_ID, body=json.dumps(body))
        output = json.loads(response["body"].read())
    except ClientError as e:
        return {"status": "error", "content": [{"text": f"❌ AWS Error: {e.response['Error']['Message']}"}]}

    finish_reason = output.get("finish_reasons", [None])[0]
    if finish_reason:
        return {"status": "error", "content": [{"text": f"❌ Image request was filtered: {finish_reason}"}]}

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(output["images"][0]))

    return {
        "status": "success",
        "content": [{"text": f"✅ Image saved to {output_path} (model {IMAGE_MODEL_ID}, seed {output.get('seeds', [None])[0]})"}],
    }


@tool
def generate_video(
    prompt: str,
    s3_bucket: str,
    s3_prefix: str = "videos/",
    aspect_ratio: str = "16:9",
    duration: str = "5s",
    resolution: str = "540p",
    region: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Start an asynchronous text-to-video generation job with Luma AI Ray 2 on Amazon Bedrock.
    The MP4 is written to the S3 bucket when the job completes; use check_video_status to poll.

    Args:
        prompt: Description of the video (1-5,000 characters and under 300 tokens).
        s3_bucket: Name of an existing S3 bucket in the same region as the Bedrock endpoint.
        s3_prefix: Key prefix inside the bucket for the output (default "videos/").
        aspect_ratio: One of 1:1, 16:9, 9:16, 4:3, 3:4, 21:9, 9:21. Default 16:9.
        duration: "5s" or "9s". Default "5s".
        resolution: "540p" or "720p". Default "540p" (faster; 720p can take much longer).
        region: AWS region of the Bedrock endpoint (default: us-west-2).

    Returns:
        Dictionary with status, the invocation_arn to poll, and the S3 output location.
    """
    if aspect_ratio not in _VIDEO_ASPECT_RATIOS:
        return {"status": "error", "content": [{"text": f"❌ Invalid aspect_ratio {aspect_ratio}. Use one of {sorted(_VIDEO_ASPECT_RATIOS)}"}]}
    if duration not in {"5s", "9s"}:
        return {"status": "error", "content": [{"text": "❌ duration must be '5s' or '9s'"}]}
    if resolution not in {"540p", "720p"}:
        return {"status": "error", "content": [{"text": "❌ resolution must be '540p' or '720p'"}]}

    s3_uri = f"s3://{s3_bucket}/{s3_prefix}"
    try:
        bedrock = boto3.client("bedrock-runtime", region_name=region or DEFAULT_REGION)
        response = bedrock.start_async_invoke(
            modelId=VIDEO_MODEL_ID,
            modelInput={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "loop": False,
                "duration": duration,
                "resolution": resolution,
            },
            outputDataConfig={"s3OutputDataConfig": {"s3Uri": s3_uri}},
        )
    except ClientError as e:
        return {"status": "error", "content": [{"text": f"❌ AWS Error: {e.response['Error']['Message']}"}]}

    arn = response["invocationArn"]
    return {
        "status": "success",
        "content": [{"text": f"✅ Video generation started. invocation_arn={arn} output={s3_uri}. Poll with check_video_status; generation usually takes 2-5 minutes."}],
    }


@tool
def check_video_status(invocation_arn: str, wait_seconds: int = 30, region: Optional[str] = None) -> Dict[str, Any]:
    """
    Check the status of an asynchronous Bedrock video generation job (GetAsyncInvoke).
    Waits `wait_seconds` before checking so you do not poll in a tight loop.

    Args:
        invocation_arn: The invocation ARN returned by generate_video.
        wait_seconds: Seconds to sleep before checking (0-120). Default 30.
        region: AWS region of the Bedrock endpoint (default: us-west-2).

    Returns:
        Dictionary with the job status (InProgress, Completed or Failed) and, when completed,
        the S3 URI of the generated MP4 file.
    """
    time.sleep(max(0, min(int(wait_seconds), 120)))
    try:
        bedrock = boto3.client("bedrock-runtime", region_name=region or DEFAULT_REGION)
        job = bedrock.get_async_invoke(invocationArn=invocation_arn)
    except ClientError as e:
        return {"status": "error", "content": [{"text": f"❌ AWS Error: {e.response['Error']['Message']}"}]}

    status = job["status"]
    if status == "Completed":
        prefix = job["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
        video_uri = _find_mp4(prefix, invocation_arn, region or DEFAULT_REGION)
        return {"status": "success", "content": [{"text": f"✅ Status: Completed. Video: {video_uri}"}]}
    if status == "Failed":
        return {"status": "error", "content": [{"text": f"❌ Status: Failed. {job.get('failureMessage', '')}"}]}
    return {"status": "success", "content": [{"text": f"⏳ Status: {status}. Call check_video_status again (it waits {wait_seconds}s before checking)."}]}


@tool
def download_from_s3(s3_uri: str, local_path: str, region: Optional[str] = None) -> Dict[str, Any]:
    """
    Download an object from Amazon S3 to a local file.

    Args:
        s3_uri: Full S3 URI of the object, e.g. "s3://my-bucket/videos/abc/output.mp4".
        local_path: Local destination path, e.g. "output/barcelona-tour.mp4".
        region: AWS region of the bucket (default: us-west-2).

    Returns:
        Dictionary with status and the local file path.
    """
    if not s3_uri.startswith("s3://"):
        return {"status": "error", "content": [{"text": "❌ s3_uri must start with s3://"}]}
    bucket, _, key = s3_uri[5:].partition("/")
    try:
        os.makedirs(os.path.dirname(os.path.abspath(local_path)), exist_ok=True)
        boto3.client("s3", region_name=region or DEFAULT_REGION).download_file(bucket, key, local_path)
    except ClientError as e:
        return {"status": "error", "content": [{"text": f"❌ AWS Error: {e.response['Error']['Message']}"}]}
    return {"status": "success", "content": [{"text": f"✅ Downloaded {s3_uri} to {local_path}"}]}


def _find_mp4(prefix_uri: str, invocation_arn: str, region: str) -> str:
    """Locate the MP4 written by an async job under the configured S3 prefix."""
    bucket, _, prefix = prefix_uri[5:].partition("/")
    job_id = invocation_arn.rsplit("/", 1)[-1]
    s3 = boto3.client("s3", region_name=region)
    for candidate in (f"{prefix}{job_id}/", prefix):
        page = s3.list_objects_v2(Bucket=bucket, Prefix=candidate)
        for obj in page.get("Contents", []):
            if obj["Key"].endswith(".mp4") and job_id in obj["Key"]:
                return f"s3://{bucket}/{obj['Key']}"
    return f"{prefix_uri}{job_id}/ (mp4 not found yet)"
