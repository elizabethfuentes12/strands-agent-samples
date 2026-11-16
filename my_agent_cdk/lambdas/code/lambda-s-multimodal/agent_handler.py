'''

{"prompt": '',
"s3object": ''
}

'''

import boto3
from strands.models import BedrockModel
from strands import Agent
from strands.vended_tools import read  # images and documents (strands_tools image_reader/file_read were removed in 0.9.0)
from video_reader import video_reader
from strands.tools import tool
import os
from file_utils import download_file
from typing import Dict, Any


#os.environ["BYPASS_TOOL_CONSENT"] = "true"
region_name = os.environ["REGION_NAME"]
model_id = os.environ["MODEL_ID"]

# Usar la región de la variable de entorno para todos los clientes
client_s3 = boto3.client('s3', region_name=region_name)
session = boto3.Session(region_name=region_name)
base_path="/tmp/"

# Define a weather-focused system prompt
MULTIMODAL_SYSTEM_PROMPT = """ You are a helpful assistant that can process documents, images, and videos. 
Analyze their contents and provide relevant information.

You can:

1. For PNG, JPEG/JPG, GIF, WebP, PDF, csv, docx, xls or xlsx formats use the `read` tool (absolute file_path)
2. For MP4, MOV, AVI, MKV, WebM formats use `video_reader` to process the file (S3 URI)
3. Just deliver the answer

When displaying responses:
- Format answers data in a human-readable way
- Highlight important information
- Handle errors appropriately
- Convert technical terms to user-friendly language
- Always reply in the original user language

Always reply in the original user language.
"""

def handler(event: Dict[str, Any], _context) -> str:
    print(event)
    try: 
        prompt = event.get('prompt')
        s3object = event.get('s3object')

        # Parse S3 URI
        s3bucket = s3object.split("/")[2]
        s3key = "/".join(s3object.split("/")[3:])
        filename = s3object.split("/")[-1]
        ext = filename.split(".")[-1].lower()  # Convert to lowercase for case-insensitive comparison

        print("s3object: ", s3object)
        print("bucket: ", s3bucket)
        print("key: ", s3key)
        print("filename: ", filename)
        print("ext: ", ext)
        print("region_name: ", region_name)

        # Check if it's a video file
        video_extensions = ['mp4', 'mov', 'avi', 'mkv', 'webm']
        if ext.lower() in video_extensions:
            print("Processing video file")
            final_prompt = f"{prompt}, file_path: {s3object}"
            print("final_prompt: ", final_prompt)
        else:
            # For non-video files, download to /tmp directory
            path_file = base_path + filename
            print(f"Downloading file to {path_file}")
            
            # Download the file
            success = download_file(base_path, s3bucket, s3key, filename)
            if not success:
                raise Exception(f"Failed to download file from s3://{s3bucket}/{s3key}")
                
            # Verify file exists after download
            if not os.path.exists(path_file):
                raise Exception(f"File not found at {path_file} after download")
                
            print(f"File downloaded successfully, size: {os.path.getsize(path_file)} bytes")
            final_prompt = f"{prompt}, file_path: {path_file}"
            print("final_prompt: ", final_prompt)


        bedrock_model = BedrockModel(
            model_id=model_id,
            boto_session=session,
            streaming=False
        )

        # Updated multimodal agent with video support
        multimodal_agent = Agent(
            system_prompt=MULTIMODAL_SYSTEM_PROMPT,
            tools=[read, video_reader],
            model=bedrock_model
        )

        result_agent = multimodal_agent(final_prompt)
        print(result_agent)
        # Claude 4.6+ models can emit a reasoningContent block first, so collect only the text blocks
        return "\n".join(block["text"] for block in result_agent.message["content"] if "text" in block)
    
    except Exception as e:
        import traceback
        error_message = f"Error processing request: {str(e)}\n{traceback.format_exc()}"
        print(error_message)
        return str(f"Error: {str(e)}")
