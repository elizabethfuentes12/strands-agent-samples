# Multimodal AI with Strands Agents

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/AWS-Bedrock-orange.svg" alt="AWS Bedrock">
  <img src="https://img.shields.io/badge/Code-10--35_lines-green.svg" alt="10-35 lines">
</p>

Build production-ready multimodal AI systems in **minutes, not hours**. Process images, documents, and videos with just a few lines of code using [Strands Agents](https://strandsagents.com/) built-in tools—no custom code required.

**Why Strands Agents?**

✅ **Built-in tools** - `generate_image`, `generate_video`, `nova_reels`, `use_aws` ready to use  
✅ **Minimal code** - Complete agents in 10-35 lines  
✅ **No boilerplate** - Focus on logic, not infrastructure  
✅ **AWS-native** - Seamless integration with Bedrock, S3, and more

---

## 🚀 Quick Start

**Prerequisites:** AWS account with [Amazon Bedrock](https://aws.amazon.com/bedrock/) access, Python 3.9+

```bash
# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

### Code Simplicity Example

**Traditional approach:** 100+ lines of custom code for video processing

**Strands Agents approach:** 10 lines with built-in tools

```python
from strands import Agent
from strands.models import BedrockModel
from strands_tools import generate_image, generate_video, nova_reels

# Create agent with built-in tools (no custom code needed!)
agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0"),
    tools=[generate_image, generate_video, nova_reels]  # Ready to use!
)

# Generate content with a simple prompt
response = agent("Generate a travel image of Paris and a 6-second video tour")
```

**That's it!** No custom video processing, no S3 upload logic, no frame extraction code. Strands provides everything.

---

## 📚 Tutorials

Six progressive tutorials from basic multimodal processing to production-ready AI systems.

| Tutorial | Notebook | Built-in Tools | Code | What You Build | Key Learning |
|----------|----------|----------------|------|----------------|--------------|
| **01** | [Image & Document Analysis](01-multimodal-basic.ipynb) | `image_reader`, `file_read` | ~15 lines | Multimodal content processing | Claude Sonnet multimodal API |
| **02** | [Video Analysis & MCP](02-multimodal-with-mcp.ipynb) | `video_reader`, MCP | ~20 lines | Video processing + external tools | Amazon Nova Pro, MCP integration |
| **03** | [Local Memory with FAISS](03-multimodal-with-faiss.ipynb) | `mem0_memory` | ~25 lines | Vector storage & semantic search | Context retention, FAISS vectors |
| **04** | [Production Memory with S3](04-multimodal-with-s3-vectors.ipynb) | `s3_vector_memory` | ~25 lines | AWS-native vector storage | S3 Vectors, user isolation |
| **05** | [AI Content Generation](05-travel-content-generator.ipynb) | `generate_image`, `nova_reels`, `use_aws`, `file_write` | ~30 lines | Generate images & videos | Nova Canvas, Nova Reel |
| **06** | [Intelligent Travel Assistant](06-travel-assistant-demo.ipynb) | All tools combined | ~35 lines | Complete AI assistant | End-to-end multimodal system |

---

**Related Resources:**
- **Tutorial 03 Article:** [Multi-Modal Content Processing with FAISS Memory](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-faiss-memory-39hg)
- **Tutorial 04 Docs:** [Amazon S3 Vectors Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
- **Tutorial 05 App:** `travel_content_generator.py` (standalone content generator)

## Tools & Files

| File | Purpose | Used In |
|------|---------|---------|
| `video_reader.py` | Process videos with S3 upload | Chapters 2-6 |
| `video_reader_local.py` | Process videos locally (no S3) | Chapters 2-6 |
| `s3_memory.py` | AWS-native memory with S3 Vectors | Chapter 4 |
| `travel_content_generator.py` | Standalone content generator app | Chapter 5 |
| `requirements.txt` | Python dependencies | All chapters |

## Skills You'll Gain

**Multimodal AI**
- Process images, documents, and videos
- Generate visual and video content
- Build cross-modal intelligence

**Memory Systems**
- Implement vector storage (FAISS, S3 Vectors)
- Manage user-specific memory
- Deploy production-ready memory

**AWS Services**
- Amazon Bedrock (Claude, Nova models)
- Amazon S3 Vectors (vector storage)
- Amazon Transcribe (audio processing)

**Production Patterns**
- Stateless → Stateful → Distributed
- Local development → Cloud deployment
- Prototype → Production

## Real-World Applications

**Content Creation**
- Automated travel content generation
- Marketing material production
- Multi-format content pipelines

**Intelligent Assistants**
- Travel planning with memory
- Customer support with context
- Research assistants

**Enterprise Solutions**
- Content moderation at scale
- Document intelligence
- Knowledge management systems

## AWS Services Used

| Service | Purpose | Cost |
|---------|---------|------|
| [Amazon Bedrock](https://aws.amazon.com/bedrock/) | Model inference (Claude, Nova) | Pay per request |
| [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) | Vector storage | Pay per GB stored |
| [Amazon S3](https://aws.amazon.com/s3/) | Media file storage | Pay per GB stored |

**Cost optimization:** Use FAISS (Chapter 3) for development, S3 Vectors (Chapter 4) for production.

## Documentation

**Strands Agents**
- [Official Documentation](https://strandsagents.com/)
- [SDK Repository](https://github.com/strands-agents/sdk-python)
- [Tools Package](https://github.com/strands-agents/tools)

**AWS Services**
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Amazon S3 Vectors Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
- [Amazon Nova Models](https://docs.aws.amazon.com/nova/latest/userguide/)

**Articles**
- [Multi-Modal Content Processing with FAISS Memory](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-faiss-memory-39hg)

## Best Practices

**Development Workflow**
1. Start with Chapter 1 for fundamentals
2. Add capabilities progressively
3. Test locally with FAISS (Chapter 3)
4. Deploy to production with S3 Vectors (Chapter 4)

**Memory Management**
- Use `user_id` for multi-user isolation
- Set similarity thresholds (0.7-0.8 recommended)
- Implement data retention policies

**Cost Control**
- Monitor Bedrock API usage
- Optimize prompt lengths
- Use appropriate model sizes

## Troubleshooting

**Common Issues**

| Issue | Solution |
|-------|----------|
| AWS credentials not found | Run `aws configure` |
| Bedrock access denied | Enable models in Bedrock console |
| Video generation fails | Verify S3 bucket exists and has permissions |
| Memory not persisting | Check file permissions for FAISS index |

**Need help?** Check the [Strands Agents documentation](https://strandsagents.com/) or open an issue.

---

**Ready to build?** Start with [Chapter 1: Basic Multimodal Processing](01-multimodal-basic.ipynb)

---

🇻🇪🇨🇱 **Created by** [Eli](https://www.linkedin.com/in/lizfue/) | [Dev.to](https://dev.to/elizabethfuentes12) | [GitHub](https://github.com/elizabethfuentes12/)
