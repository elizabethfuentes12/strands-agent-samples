#!/usr/bin/env python3
"""
Travel Content Generator Application

Generate complete travel content packages (images, videos, and itineraries)
using Amazon Bedrock and Strands Agents.

Models used:
- Claude Haiku 5.5 (agent reasoning), global cross-region inference profile
- Stability AI Stable Image Core (images) and Luma AI Ray 2 (videos) in us-west-2,
  through the custom tools in content_tools.py
- The itinerary is written with the SDK-vended `write` tool
"""

import os
import sys
import boto3
from strands import Agent
from strands.models import BedrockModel
from strands.vended_tools import write
from content_tools import generate_image, generate_video, check_video_status, download_from_s3


def get_user_input():
    """Get user input for content generation."""
    print("\n" + "="*80)
    print("🌍 Travel Content Generator")
    print("="*80)
    
    # Get destination details
    destination = input("\n📍 Enter destination (e.g., 'Barcelona, Spain'): ").strip()
    if not destination:
        print("❌ Destination is required")
        sys.exit(1)
    
    landmark = input("🏛️  Enter main landmark (e.g., 'Sagrada Familia'): ").strip()
    if not landmark:
        print("❌ Landmark is required")
        sys.exit(1)
    
    # Get trip duration
    while True:
        try:
            duration = int(input("📅 Enter trip duration in days (e.g., 5): ").strip())
            if duration > 0:
                break
            print("❌ Duration must be positive")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Get travel style
    print("\n🎨 Travel styles: cultural, romantic, adventure, modern, historic, luxury")
    style = input("   Enter travel style: ").strip().lower()
    if not style:
        style = "cultural"
    
    # Get season
    print("\n🌤️  Seasons: spring, summer, fall, winter")
    season = input("   Enter season: ").strip().lower()
    if not season:
        season = "summer"
    
    # Get S3 bucket for video generation
    print("\n📦 Video generation requires an S3 bucket in us-west-2 (Bedrock async jobs write the MP4 to S3)")
    print("   Leave empty to skip video generation")
    bucket = input("   Enter S3 bucket name: ").strip()
    
    # Ask if user wants to generate video
    generate_video = False
    if bucket:
        response = input(f"\n🎬 Generate video using bucket '{bucket}'? (y/n): ").strip().lower()
        generate_video = response in ['y', 'yes']
    
    return {
        'destination': destination,
        'landmark': landmark,
        'duration': duration,
        'style': style,
        'season': season,
        'bucket': bucket if generate_video else None,
        'generate_video': generate_video
    }


def create_content_agent(region):
    """Create the content generator agent."""
    # Claude Haiku 5.5 through the global cross-region inference profile
    session = boto3.Session(region_name=region)
    model = BedrockModel(
        model_id=os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5"),
        boto_session=session
    )

    output_dir = os.path.abspath("output")

    # Create content generator agent
    agent = Agent(
        model=model,
        tools=[
            generate_image,
            generate_video,
            check_video_status,
            download_from_s3,
            write
        ],
        system_prompt=f"""You are a professional travel content creator that generates complete content packages.

Your tools:
- generate_image: Create high-quality destination images with Stability AI Stable Image Core on Amazon Bedrock (saves a PNG locally)
- generate_video: Start a promotional video with Luma AI Ray 2 on Amazon Bedrock (saved to S3, asynchronous)
- check_video_status: Poll the video job until it is Completed and get the S3 URI of the MP4
- download_from_s3: Download the finished video from S3 to a local path
- write: Create text files for itineraries (absolute paths)

All files go in the output directory: {output_dir}

When the user provides a destination, you MUST:

1. **Generate Destination Image**:
   - Use generate_image with output_path "{output_dir}/[destination]-[landmark].png" and aspect_ratio 16:9
   - Create a stunning photo of the main landmark at golden hour
   - Include a detailed prompt with: lighting, composition, atmosphere, mood
   - Professional travel photography quality

2. **Generate Tour Video** (only if an S3 bucket is provided):
   - Use generate_video with the s3_bucket provided, duration "5s", aspect_ratio 16:9
   - Create a cinematic tour showing 2-3 iconic locations with smooth camera movement
   - CRITICAL: the prompt MUST be short (under 300 tokens, roughly 2 sentences)
   - Save the invocation_arn from the response
   - Video generation takes 2-5 minutes: call check_video_status repeatedly until the status is "Completed"
   - Only when it is "Completed", call download_from_s3 with the returned S3 URI and local_path "{output_dir}/[destination]-tour.mp4"
   - DO NOT attempt the download before the status is "Completed"

3. **Create Travel Itinerary**:
   - Use the write tool with path "{output_dir}/[destination]-itinerary.txt"
   - Generate a detailed day-by-day itinerary as text
   - Include: activities, restaurants, cultural insights, transportation tips
   - Match the travel style and season provided
   - Format with clear sections: Day 1, Day 2, etc.

Guidelines:
- Be creative and professional
- Use specific location names and landmarks
- Include atmospheric details
- Generate ALL pieces of content automatically

Always execute all available tools when given a destination.
"""
    )

    return agent


def generate_content(config):
    """Generate travel content based on configuration."""
    # Get AWS region from session
    session = boto3.Session()
    region = session.region_name or 'us-east-1'
    
    print(f"\n🌐 Using AWS region: {region}")
    
    # Create agent
    print("🤖 Creating content generator agent...")
    agent = create_content_agent(region)
    
    # Extract city from destination
    city = config['destination'].split(',')[0].strip()
    country = config['destination'].split(',')[1].strip() if ',' in config['destination'] else ""
    
    # Check if video generation is possible
    skip_video = not config['generate_video'] or not config['bucket']
    video_instruction = "Skip video generation (disabled or no S3 bucket configured)." if skip_video else f"Generate video using S3 bucket: {config['bucket']}"
    
    print("\n" + "="*80)
    print("🎨 Generating Content...")
    print("="*80)
    print(f"📍 Destination: {config['destination']}")
    print(f"🏛️  Landmark: {config['landmark']}")
    print(f"📅 Duration: {config['duration']} days")
    print(f"🎨 Style: {config['style']}")
    print(f"🌤️  Season: {config['season']}")
    if config['generate_video']:
        print(f"🎬 Video: Yes (bucket: {config['bucket']})")
    else:
        print("🎬 Video: No")
    print("="*80 + "\n")
    
    # Generate content
    prompt = f"""
Generate a complete travel content package for:

Destination: {config['destination']}
City: {city}
Country: {country}
Main Landmark: {config['landmark']}
Trip Duration: {config['duration']} days
Travel Style: {config['style']}
Season: {config['season']}

Video generation: {video_instruction}
{'S3 Bucket: ' + config['bucket'] if not skip_video else ''}

Create {'image and itinerary' if skip_video else 'all three pieces of content (image, video, and itinerary)'}.
Use the exact parameters provided above.

For video generation:
1. Use generate_video to start the job (the MP4 will be saved to S3)
2. IMPORTANT: Keep calling check_video_status until it shows "Completed" (takes 2-5 minutes)
3. Only after status is "Completed", use download_from_s3 to save the video in output/
4. Do NOT skip the waiting period - the video must be fully generated before download
"""
    
    response = agent(prompt)
    
    print("\n" + "="*80)
    print("✅ Content Generation Complete")
    print("="*80)
    print(response)
    print()


def verify_content():
    """Verify generated content."""
    from pathlib import Path
    
    output_dir = Path("output")
    
    print("\n" + "="*80)
    print("📁 Generated Content")
    print("="*80)
    
    if output_dir.exists():
        # Images
        images = list(output_dir.glob("*.jpg")) + list(output_dir.glob("*.png"))
        if images:
            print("\n🖼️  Images:")
            for img in images:
                size_mb = img.stat().st_size / (1024 * 1024)
                print(f"  • {img.name} ({size_mb:.2f} MB)")
        
        # Videos
        videos = list(output_dir.glob("*.mp4"))
        if videos:
            print("\n🎬 Videos:")
            for vid in videos:
                size_mb = vid.stat().st_size / (1024 * 1024)
                print(f"  • {vid.name} ({size_mb:.2f} MB)")
        
        # Itineraries
        itineraries = list(output_dir.glob("*.txt"))
        if itineraries:
            print("\n📄 Itineraries:")
            for txt in itineraries:
                size_kb = txt.stat().st_size / 1024
                print(f"  • {txt.name} ({size_kb:.2f} KB)")
        
        total_files = len(list(output_dir.glob("*")))
        print(f"\n✅ Total files: {total_files}")
    else:
        print("\n❌ No content directory found")
    
    print("="*80 + "\n")


def main():
    """Main application entry point."""
    try:
        # Get user input
        config = get_user_input()
        
        # Generate content
        generate_content(config)
        
        # Verify generated content
        verify_content()
        
        print("🎉 All done! Your travel content is ready.\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
