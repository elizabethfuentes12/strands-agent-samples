from strands import tool
import boto3
import os
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional

@tool
def video_reader(
    video_path: str, 
    text_prompt: str = "Describe what you see in this video",
    model_id: str = "us.amazon.nova-pro-v1:0",
    region: Optional[str] = None,
    system_prompt: Optional[str] = None,
    agent = None
) -> Dict[str, Any]:
    """
    Analyze video content using AWS Bedrock's Converse API.
    
    This tool processes videos and uses Claude/Nova models to analyze video content 
    through Bedrock's multimodal capabilities, similar to image_reader but for videos.
    
    Args:
        video_path: Path to video file (S3 URI like s3://bucket/video.mp4)
        text_prompt: Question or instruction for analyzing the video
        model_id: Bedrock model ID to use for analysis (if None, uses agent's model)
        region: AWS region for Bedrock client (if None, uses environment variable REGION_NAME)
        system_prompt: Custom system prompt for analysis (if None, uses agent's system_prompt)
        agent: The Strands agent instance (automatically provided by framework)
        
    Returns:
        Dictionary with video analysis results in Converse API format
    """
    try:
        # Always use the region from environment variable
        env_region = os.environ.get("REGION_NAME")
        
        # Get model_id from agent if not provided
        if not model_id and agent and hasattr(agent, 'model'):
            if hasattr(agent.model, 'model_id'):
                model_id = agent.model.model_id
            elif hasattr(agent.model, 'model_name'):
                model_id = agent.model.model_name
            else:
                model_id = "us.amazon.nova-pro-v1:0"  # Default fallback
        elif not model_id:
            model_id = "us.amazon.nova-pro-v1:0"  # Default fallback
            
        # Always prioritize the environment variable for region
        if env_region:
            region = env_region
        elif not region and agent and hasattr(agent, 'model'):
            if hasattr(agent.model, 'boto_session') and agent.model.boto_session:
                region = agent.model.boto_session.region_name
            elif hasattr(agent.model, 'region'):
                region = agent.model.region
        
        # If region is still not set, log an error
        if not region:
            print("ERROR: No region specified and REGION_NAME environment variable not set")
            return {
                "status": "error",
                "content": [{"text": "❌ No region specified. Please set the REGION_NAME environment variable."}]
            }
            
        # Get system_prompt from agent if not provided
        if not system_prompt and agent and hasattr(agent, 'system_prompt'):
            system_prompt = agent.system_prompt
        elif not system_prompt:
            system_prompt = "Always answer in the same language you are asked."
        
        # Initialize Bedrock client with the determined region
        print(f"Using region: {region} for Bedrock client")
        session = boto3.Session(region_name=region)
        bedrock_client = session.client('bedrock-runtime')
        
        # Determine video format
        video_format = _get_video_format(video_path)
        if not video_format:
            return {
                "status": "error",
                "content": [{"text": "❌ Unsupported video format. Supported: mp4, mov, avi, mkv, webm"}]
            }
        
        # Verify that the path is an S3 URI
        if not video_path.startswith('s3://'):
            return {
                "status": "error",
                "content": [{"text": "❌ Video path must be an S3 URI (s3://bucket/path/to/video.mp4)"}]
            }
        
        # Use the S3 URI directly with Converse API
        s3_uri = video_path
        print(f"Using S3 URI: {s3_uri} in region {region}")
        
        # Prepare message for Converse API
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
        print(f"Calling Bedrock Converse API with model {model_id} in region {region}")
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
"""
        
        return {
            "status": "success",
            "content": [{"text": detailed_response}]
        }
        
    except ClientError as e:
        error_message = f"❌ AWS Error: {e.response['Error']['Message']}"
        print(f"ClientError: {error_message}")
        return {
            "status": "error",
            "content": [{"text": error_message}]
        }
    except Exception as e:
        error_message = f"❌ Error processing video: {str(e)}"
        print(f"Exception: {error_message}")
        return {
            "status": "error",
            "content": [{"text": error_message}]
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
