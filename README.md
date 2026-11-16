# Strands Agent Samples

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/AWS-Bedrock-orange.svg" alt="AWS Bedrock">
  <img src="https://img.shields.io/badge/License-MIT--0-green.svg" alt="License MIT-0">
</p>

Production-ready examples for building **multimodal AI agents** with the [Strands Agent framework](https://strandsagents.com/). Process images, documents, and videos with persistent memory using **10-30 lines of code**.

---

## 🎯 What You'll Build

Build intelligent agents that process multiple content types with the SDK's **vended tools** plus a few small custom tools from this repo:

| Content Type | Formats | Tool |
|--------------|---------|------|
| **Images** | PNG, JPEG, GIF, WebP | `read` (SDK vended), `generate_image` (custom, Stability AI on Bedrock) |
| **Documents** | PDF, CSV, DOCX, XLS, XLSX | `read` (SDK vended) |
| **Videos** | MP4, MOV, AVI, MKV, WebM | `video_reader` (custom, Amazon Nova 2 Lite), `generate_video` (custom, Luma AI Ray 2) |
| **Memory** | local files, Amazon S3 Vectors | `MemoryManager` + `FileMemoryStore` (SDK), `s3_vector_memory` (custom) |

**Why Strands Agents?**

```python
# Traditional approach: 100+ lines of custom code
# Strands approach: a few lines with vended tools

from strands import Agent
from strands.models import BedrockModel
from strands.vended_tools import read, http_request

agent = Agent(
    model=BedrockModel(model_id="global.anthropic.claude-haiku-5-5"),
    tools=[read, http_request]  # SDK vended tools ready to use!
)

response = agent("Read /path/to/diagram.jpg and explain the architecture")
```

✅ **10-30 lines of code** for complete agents  
✅ **Vended tools** - `read`, `write`, `http_request`, `subagent`, A2A client... ship with the SDK  
✅ **AWS-native** - Seamless Bedrock integration  
✅ **Production-ready** - Memory, observability included

> **Updated for `strands-agents` 1.65 / `strands-agents-tools` 0.9 / `mcp` 2.x.** The community tools package removed `image_reader`, `file_read`, `file_write`, `http_request`, `use_llm`, `use_aws`, `calculator`, `mem0_memory`, `generate_image` and `nova_reels` in 0.9.0; see the [migration guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/). Model IDs were updated to models that are **ACTIVE** on Amazon Bedrock (Claude 3.x / Sonnet 4 reached end of life, Nova Reel/Canvas were removed): check the [model lifecycle page](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html).

---

## 🚀 Quick Start

### Prerequisites

- AWS account with [Amazon Bedrock](https://aws.amazon.com/bedrock/) access
- Python 3.10 or later (tested with 3.11)
- AWS CLI configured

### Installation

```bash
# Clone repository
git clone https://github.com/elizabethfuentes12/strands-agent-samples
cd strands-agent-samples/notebook

# Set up environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure AWS
aws configure

# Open notebooks in your preferred IDE
# VS Code, JupyterLab, or any notebook editor
```

---

## 📚 Complete Learning Path

| # | Notebook | Built-in Tools | Code | What You Build |
|---|----------|----------------|------|----------------|
| **Beginner** | | | | |
| 1 | [Hello World](notebook/01-hello-world-strands-agents.ipynb) | Basic tools | ~10 lines | Basic agent setup |
| 2 | [Custom Tools](notebook/02-custom-tools.ipynb) | Custom tools | ~15 lines | Tool integration |
| 3 | [MCP Integration](notebook/03-mcp-integration.ipynb) | MCP | ~20 lines | External services |
| **Multimodal AI** | **[📁 multimodal_understanding/](notebook/multimodal_understanding/)** | | | |
| 01 | [Image & Document Analysis](notebook/multimodal_understanding/01-multimodal-basic.ipynb) | `read` | ~15 lines | Multimodal content processing |
| 02 | [Video Analysis & MCP](notebook/multimodal_understanding/02-multimodal-with-mcp.ipynb) | `video_reader`, MCP | ~20 lines | Video processing + external tools |
| 03 | [Local Long-Term Memory](notebook/multimodal_understanding/03-multimodal-with-faiss.ipynb) | `MemoryManager`, `FileMemoryStore` | ~25 lines | Cross-session memory |
| 04 | [Production Memory with S3](notebook/multimodal_understanding/04-multimodal-with-s3-vectors.ipynb) | `s3_vector_memory` | ~25 lines | AWS-native vector storage |
| 05 | [AI Content Generation](notebook/multimodal_understanding/05-travel-content-generator.ipynb) | `generate_image`, `generate_video`, `write` | ~30 lines | Generate images & videos |
| 06 | [Intelligent Travel Assistant](notebook/multimodal_understanding/06-travel-assistant-demo.ipynb) | All tools combined | ~35 lines | Complete AI assistant |
| **Advanced** | | | | |
| 4 | [MCP Tools](notebook/04-Strands_MCP_AND_Tools.ipynb) | MCP servers | ~25 lines | Custom MCP servers |
| 5 | [Agent-to-Agent](notebook/05-Strands_A2A_Tools.ipynb) | A2A protocol | ~30 lines | Multi-agent systems |
| 6 | [Observability](notebook/06-Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb) | LangFuse, RAGAS | ~35 lines | Production monitoring |

**[📖 Detailed guides](notebook/README.md)** | **[📝 Article](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-faiss-memory-39hg)**

---

## 🏗️ Repository Structure

```
strands-agent-samples/
├── notebook/                              # Learning materials
│   ├── 01-hello-world-strands-agents.ipynb
│   ├── 02-custom-tools.ipynb
│   ├── 03-mcp-integration.ipynb
│   ├── 04-Strands_MCP_AND_Tools.ipynb
│   ├── 05-Strands_A2A_Tools.ipynb
│   ├── 06-Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb
│   ├── multimodal_understanding/         # 6-chapter journey
│   │   ├── 01-multimodal-basic.ipynb
│   │   ├── 02-multimodal-with-mcp.ipynb
│   │   ├── 03-multimodal-with-faiss.ipynb
│   │   ├── 04-multimodal-with-s3-vectors.ipynb
│   │   ├── 05-travel-content-generator.ipynb
│   │   ├── 06-travel-assistant-demo.ipynb
│   │   ├── video_reader.py
│   │   ├── video_reader_local.py
│   │   ├── s3_memory.py
│   │   ├── content_tools.py                   # image/video generation tools (Bedrock)
│   │   └── travel_content_generator.py
│   ├── mcp_calulator.py
│   ├── run_a2a_system.py
│   ├── strands-a2a-inter-agent/           # A2A sample (MCP server + 2 agents)
│   ├── data-sample/                      # Test files
│   └── requirements.txt
└── my_agent_cdk/                         # AWS CDK deployment
    ├── lambdas/code/lambda-s-agent       # Weather agent
    └── lambdas/code/lambda-s-multimodal  # Multimodal agent
```

---

## 🎯 Key Features

### Multimodal Processing

Process diverse content types through unified interfaces:

- **Image Analysis** - Visual understanding with Claude Haiku 5.5
- **Document Processing** - Text extraction from PDFs, Office files
- **Video Analysis** - Frame extraction and temporal understanding
- **Content Generation** - Create images (Stability AI) and videos (Luma AI Ray 2) on Amazon Bedrock

### Memory Systems

Build agents that remember and learn:

- **FileMemoryStore** - Local, zero-infrastructure memory for development (Strands `MemoryManager`)
- **S3 Vectors** - AWS-native production memory
- **User Isolation** - Multi-tenant memory management
- **Semantic Search** - Context-aware information retrieval

### Production Patterns

Enterprise-ready implementations:

- **Observability** - LangFuse tracing and monitoring
- **Evaluation** - RAGAS metrics for quality assessment
- **Multi-Agent** - A2A protocol for agent collaboration
- **Serverless** - AWS Lambda deployment with CDK

---

## 🛠️ Technologies

### AI Models

| Model | Purpose | Use Case |
|-------|---------|----------|
| [Claude Haiku 5.5](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) (`global.anthropic.claude-haiku-5-5`) | Text, images, documents | Agent reasoning, multimodal understanding |
| [Amazon Nova 2 Lite](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) (`us.amazon.nova-2-lite-v1:0`) | Video analysis | Video content processing |
| [Stability AI Stable Image Core](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-stable-image-core-text-image-request-response.html) | Image generation | Create visual content |
| [Luma AI Ray 2](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-luma.html) | Video generation | Generate video content (async) |
| [Amazon Nova Multimodal Embeddings](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) | Vector generation | Semantic search (S3 Vectors) |

### AWS Services

| Service | Purpose |
|---------|---------|
| [Amazon Bedrock](https://aws.amazon.com/bedrock/) | Model inference |
| [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) | Vector storage |
| [Amazon S3](https://aws.amazon.com/s3/) | Media storage |
| [AWS Lambda](https://aws.amazon.com/lambda/) | Serverless compute |

### Frameworks

| Framework | Purpose |
|-----------|---------|
| [Strands Agents SDK](https://github.com/strands-agents/sdk-python) | Agent framework |
| [Model Context Protocol Python SDK](https://py.sdk.modelcontextprotocol.io/v2/) | MCP servers and clients (v2) |
| [LangFuse](https://langfuse.com/) | Observability |
| [RAGAS](https://docs.ragas.io/) | Evaluation |

---

## 💡 Use Cases

### Content Intelligence
- Automated content moderation for images and videos
- Document analysis for compliance and insights
- Multi-format data extraction and processing

### Intelligent Assistants
- Customer support with conversation memory
- Research assistants with cross-modal correlation
- Educational tutors with adaptive learning

### Enterprise Solutions
- Business intelligence with automated insights
- Knowledge management with semantic search
- Automated content generation pipelines

---

## ☁️ AWS CDK Deployment

Deploy serverless agents to AWS Lambda:

```bash
cd my_agent_cdk

# Install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Package Lambda layers
pip install -r layers/lambda_requirements.txt \
  --python-version 3.12 \
  --platform manylinux2014_aarch64 \
  --target layers/strands/_dependencies \
  --only-binary=:all:

python layers/package_for_lambda.py

# Deploy
cdk bootstrap  # First time only
cdk deploy
```

**Available Functions:**
- **Weather Agent** - Forecasting with Strands Agent
- **Multimodal Agent** - Process images, documents, videos

**[📖 View CDK documentation →](my_agent_cdk/README.md)**

---

## 📖 Documentation

### Strands Agents
- [Official Documentation](https://strandsagents.com/)
- [SDK Repository](https://github.com/strands-agents/sdk-python)
- [Tools Package](https://github.com/strands-agents/tools) and [community tools migration guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/)
- [Amazon Bedrock model lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html)

### AWS Services
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Amazon S3 Vectors Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
- [Amazon Nova Models](https://docs.aws.amazon.com/nova/latest/userguide/)

### Frameworks
- [LangFuse Documentation](https://langfuse.com/docs)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent-to-Agent Protocol](https://a2a.ai/)

### Articles
- [Multi-Modal Content Processing with FAISS Memory](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-faiss-memory-39hg)

---

## 🎓 Best Practices

### Development Workflow
1. Start with beginner notebooks
2. Progress through multimodal journey
3. Test locally with `FileMemoryStore`
4. Deploy to production with S3 Vectors

### Cost Optimization
- Use `FileMemoryStore` for development (free, local)
- Monitor Bedrock API usage
- Optimize prompt lengths
- Use appropriate model sizes

### Production Deployment
- Implement observability with LangFuse
- Set up evaluation with RAGAS
- Use S3 Vectors for scalable memory
- Follow AWS security best practices

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| AWS credentials not found | Run `aws configure` with valid credentials |
| Bedrock access denied | Enable models in [Bedrock console](https://console.aws.amazon.com/bedrock/) |
| Import errors | Verify `pip install -r requirements.txt` completed |
| Video generation fails | Check the S3 bucket exists in us-west-2 (same region as the Luma model) and has permissions |
| `ImportError ... was removed in v0.9.0` | You are importing from `strands_tools`; use `strands.vended_tools` (see the migration guide above) |
| `No module named 'mcp.server.fastmcp'` | MCP SDK 2.x: use `from mcp.server.mcpserver import MCPServer` |
| `temperature is deprecated for this model` | Claude 4.7+ models reject `temperature`/`top_p`/`top_k`; remove them |

**Need help?** Check [Strands documentation](https://strandsagents.com/) or [open an issue](https://github.com/elizabethfuentes12/strands-agent-samples/issues).

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔒 Security

Report security issues per [CONTRIBUTING.md](CONTRIBUTING.md#security-issue-notifications).

## 📄 License

This library is licensed under the MIT-0 License. See [LICENSE](LICENSE).

---

<p align="center">
  <strong>Ready to build intelligent multimodal AI agents?</strong><br>
  Start with the <a href="notebook/">notebooks</a> and explore the possibilities.
</p>

---

<p align="center">
  🇻🇪🇨🇱 <strong>Created by</strong> <a href="https://www.linkedin.com/in/lizfue/">Eli</a> | 
  <a href="https://dev.to/elizabethfuentes12">Dev.to</a> | 
  <a href="https://github.com/elizabethfuentes12/">GitHub</a> | 
  <a href="https://twitter.com/elizabethfue12">Twitter</a> | 
  <a href="https://www.youtube.com/channel/UCr0Gnc-t30m4xyrvsQpNp2Q">YouTube</a>
</p>
