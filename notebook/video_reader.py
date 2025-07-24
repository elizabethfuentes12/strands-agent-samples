from strands import tool
import boto3
import os
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional

@tool
def video_reader(
    video_path: str, 
    text_prompt: str = "Describe what you see in this video",
    #model_id: Optional[str] = None,
    model_id: str = "us.amazon.nova-pro-v1:0",
    region: Optional[str] = None,
    s3_bucket: Optional[str] = None,
    system_prompt: Optional[str] = None,
    agent = None
) -> Dict[str, Any]:
    """
    Analyze video content using AWS Bedrock's Converse API.
    
    This tool processes videos and uses Claude/Nova models to analyze video content 
    through Bedrock's multimodal capabilities, similar to image_reader but for videos.
    
    Args:
        video_path: Path to video file (local path or S3 URI like s3://bucket/video.mp4)
        text_prompt: Question or instruction for analyzing the video
        model_id: Bedrock model ID to use for analysis (if None, uses agent's model)
        region: AWS region for Bedrock client (if None, uses agent's region or us-west-2)
        s3_bucket: S3 bucket name for uploading local videos (defaults to strands-video-analysis)
        system_prompt: Custom system prompt for analysis (if None, uses agent's system_prompt)
        agent: The Strands agent instance (automatically provided by framework)
        
    Returns:
        Dictionary with video analysis results in Converse API format
    """
    try:
        # Get model_id and region from agent if not provided
        if not model_id and agent and hasattr(agent, 'model'):
            if hasattr(agent.model, 'model_id'):
                model_id = agent.model.model_id
            elif hasattr(agent.model, 'model_name'):
                model_id = agent.model.model_name
            else:
                model_id = "us.amazon.nova-pro-v1:0"  # Default fallback
        elif not model_id:
            model_id = "us.amazon.nova-pro-v1:0"  # Default fallback
            
        if not region and agent and hasattr(agent, 'model'):
            if hasattr(agent.model, 'boto_session') and agent.model.boto_session:
                region = agent.model.boto_session.region_name
            elif hasattr(agent.model, 'region'):
                region = agent.model.region
            else:
                region = "us-west-2"  # Default fallback
        elif not region:
            region = "us-west-2"  # Default fallback
            
        # Get system_prompt from agent if not provided
        if not system_prompt and agent and hasattr(agent, 'system_prompt'):
            system_prompt = agent.system_prompt
        elif not system_prompt:
            system_prompt = "Always answer in the same language you are asked."
        
        # Initialize Bedrock client
        session = boto3.Session(region_name=region)
        bedrock_client = session.client('bedrock-runtime')
        
        # Determine video format
        video_format = _get_video_format(video_path)
        if not video_format:
            return {
                "status": "error",
                "content": [{"text": "❌ Unsupported video format. Supported: mp4, mov, avi, mkv, webm"}]
            }
        
        # Handle S3 URI or upload local file
        if video_path.startswith('s3://'):
            s3_uri = video_path
        else:
            # Upload local file to S3
            if not s3_bucket:
                s3_bucket = os.getenv('AWS_S3_BUCKET', 'strands-video-analysis')
            
            s3_uri = _upload_to_s3(video_path, s3_bucket, session)
            if not s3_uri:
                return {
                    "status": "error", 
                    "content": [{"text": "❌ Failed to upload video to S3"}]
                }
        
        # Prepare message for Converse API (similar to your existing code)
        media_content = {
            'video': {
                "format": video_format,
                "source": {
                    's3Location': {
                        'uri': s3_uri
                    }
                }
            }
        }
        
        message = {
            "role": "user",
            "content": [
                {"text": text_prompt},
                media_content
            ]
        }
        
        # Call Bedrock Converse API
        response = bedrock_client.converse(
            modelId=model_id,
            messages=[message],
            system=[{"text": system_prompt}]
        )
        
        # Extract response content
        text_response = response['output']['message']['content'][0]['text']
        
        # Format detailed response with metadata in the text content
        detailed_response = f"""🎥 Video Analysis Results:

**Analysis:** {text_response}

---
**Technical Details:**
- Model Used: {model_id}
- Region: {region}
- Video Path: {video_path}
- S3 URI: {s3_uri}
"""
        
        return {
            "status": "success",
            "content": [{"text": detailed_response}]
        }
        
    except ClientError as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ AWS Error: {e.response['Error']['Message']}"}]
        }
    except Exception as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ Error processing video: {str(e)}"}]
        }


def _get_video_format(file_path: str) -> Optional[str]:
    """Get video format from file extension."""
    formats = {
        '.mp4': 'mp4', '.mov': 'mov', '.avi': 'avi', 
        '.mkv': 'mkv', '.webm': 'webm'
    }
    
    if file_path.startswith('s3://'):
        filename = file_path.split('/')[-1]
    else:
        filename = os.path.basename(file_path)
    
    _, ext = os.path.splitext(filename.lower())
    return formats.get(ext)


def _upload_to_s3(local_path: str, bucket: str, session: boto3.Session) -> Optional[str]:
    """Upload video to S3 and return URI."""
    try:
        s3_client = session.client('s3')
        
        # Create bucket if needed
        try:
            s3_client.head_bucket(Bucket=bucket)
        except ClientError:
            try:
                if session.region_name == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket,
                        CreateBucketConfiguration={'LocationConstraint': session.region_name}
                    )
            except ClientError:
                pass  # Bucket might already exist
        
        # Upload file
        filename = os.path.basename(local_path)
        s3_key = f"videos/{filename}"
        s3_client.upload_file(local_path, bucket, s3_key)
        
        return f"s3://{bucket}/{s3_key}"
        
    except Exception as e:
        print(f"Upload error: {e}")
        return None