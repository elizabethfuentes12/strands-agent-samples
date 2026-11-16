# Strands Agents Learning Repository

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/AWS-Bedrock-orange.svg" alt="AWS Bedrock">
  <img src="https://img.shields.io/badge/Strands-Agents-purple.svg" alt="Strands Agents">
</p>

Learn to build production-ready AI agents with the [Strands Agent framework](https://strandsagents.com/). Hands-on examples from basic setup to advanced multimodal systems with **10-35 lines of code**.

---

## 🎯 What You'll Learn

Build intelligent agents using **built-in tools**—no custom code required:

| Skill Level | What You Build | Code Complexity |
|-------------|----------------|-----------------|
| **Beginner** | Basic agents with tools | 10-20 lines |
| **Intermediate** | Multimodal systems with memory | 20-30 lines |
| **Advanced** | Production systems with observability | 30-40 lines |

---

## 🚀 Quick Start

### Prerequisites

- AWS account with [Amazon Bedrock](https://aws.amazon.com/bedrock/) access
- Python 3.10 or later (tested with 3.11)
- AWS CLI configured (`aws configure`)

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Open notebooks in your preferred IDE
# Start with 01-hello-world-strands-agents.ipynb
```

---

## 📚 Learning Paths

### 📚 Complete Learning Path

| # | Notebook | Built-in Tools | Code | What You Build | Key Concept |
|---|----------|----------------|------|----------------|-------------|
| **1** | [👋 Hello World](01-hello-world-strands-agents.ipynb) | Basic tools | ~10 lines | Your first agent | Basic setup |
| **2** | [🔧 Custom Tools](02-custom-tools.ipynb) | Custom tools | ~15 lines | Tool integration | Create tools |
| **3** | [🔌 MCP Integration](03-mcp-integration.ipynb) | MCP | ~20 lines | External services | MCP protocol |
| **4** | [🔧 MCP Deep Dive](04-Strands_MCP_AND_Tools.ipynb) | MCP servers | ~25 lines | Custom MCP servers | Advanced MCP |
| **5** | [🤝 Agent-to-Agent](05-Strands_A2A_Tools.ipynb) | A2A protocol | ~30 lines | Multi-agent systems | Inter-agent comm |
| **6** | [🔍 Observability](06-Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb) | LangFuse, RAGAS | ~35 lines | Production monitoring | Observability |

### 🚀 Multimodal AI Tutorials

**[📁 multimodal_understanding/](multimodal_understanding/)** - 6 progressive tutorials from basic to production

| Tutorial | Notebook | Built-in Tools | Code | What You Build |
|----------|----------|----------------|------|----------------|
| **01** | [Image & Document Analysis](multimodal_understanding/01-multimodal-basic.ipynb) | `read` (SDK vended) | ~15 lines | Multimodal content processing |
| **02** | [Video Analysis & MCP](multimodal_understanding/02-multimodal-with-mcp.ipynb) | `video_reader`, MCP | ~20 lines | Video processing + external tools |
| **03** | [Local Long-Term Memory](multimodal_understanding/03-multimodal-with-faiss.ipynb) | `MemoryManager`, `FileMemoryStore` | ~25 lines | Cross-session memory |
| **04** | [Production Memory with S3](multimodal_understanding/04-multimodal-with-s3-vectors.ipynb) | `s3_vector_memory` | ~25 lines | AWS-native vector storage |
| **05** | [AI Content Generation](multimodal_understanding/05-travel-content-generator.ipynb) | `generate_image`, `generate_video`, `write` | ~30 lines | Generate images & videos |
| **06** | [Intelligent Travel Assistant](multimodal_understanding/06-travel-assistant-demo.ipynb) | All tools combined | ~35 lines | Complete AI assistant |

**[📖 View detailed multimodal guide →](multimodal_understanding/README.md)** | **[📝 Article](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-faiss-memory-39hg)**

---

## 🏗️ Repository Structure

```
notebook/
├── 01-hello-world-strands-agents.ipynb
├── 02-custom-tools.ipynb
├── 03-mcp-integration.ipynb
├── 04-Strands_MCP_AND_Tools.ipynb
├── 05-Strands_A2A_Tools.ipynb
├── 06-Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb
├── multimodal_understanding/              # 6-chapter journey
│   ├── 01-multimodal-basic.ipynb
│   ├── 02-multimodal-with-mcp.ipynb
│   ├── 03-multimodal-with-faiss.ipynb
│   ├── 04-multimodal-with-s3-vectors.ipynb
│   ├── 05-travel-content-generator.ipynb
│   ├── 06-travel-assistant-demo.ipynb
│   ├── video_reader.py
│   ├── video_reader_local.py
│   ├── s3_memory.py
│   └── travel_content_generator.py
├── mcp_calulator.py
├── mcp_custom_tools_server.py
├── run_a2a_system.py
├── data-sample/                           # Test files
└── requirements.txt
```

---

## 🎯 What You'll Build

### Foundations (Notebooks 01-03)

- Configure and run Strands agents
- Create custom tools for specific tasks
- Integrate external services via MCP

### Multimodal AI (multimodal_understanding/)

- Process images, documents, and videos
- Implement memory with `FileMemoryStore` (local) and S3 Vectors (production)
- Generate content with Stability AI and Luma AI models on Amazon Bedrock
- Build intelligent assistants

### Production Patterns (Advanced notebooks)

- Monitor agents with LangFuse
- Evaluate performance with RAGAS
- Build multi-agent systems
- Deploy serverless architectures

---

## 🛠️ Technologies

### AI Models

| Model | Purpose |
|-------|---------|
| [Claude Haiku 5.5](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) (`global.anthropic.claude-haiku-5-5`) | Text, images, documents |
| [Amazon Nova 2 Lite](https://docs.aws.amazon.com/nova/latest/userguide/what-is-nova.html) (`us.amazon.nova-2-lite-v1:0`) | Video analysis |
| [Stability AI Stable Image Core](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-diffusion-stable-image-core-text-image-request-response.html) | Image generation |
| [Luma AI Ray 2](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-luma.html) | Video generation |
| [Titan Embeddings](https://aws.amazon.com/bedrock/titan/) | Vector generation |

### AWS Services

| Service | Purpose |
|---------|---------|
| [Amazon Bedrock](https://aws.amazon.com/bedrock/) | Model inference |
| [Amazon S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) | Production memory |
| [Amazon S3](https://aws.amazon.com/s3/) | Media storage |
| [Amazon Transcribe](https://aws.amazon.com/transcribe/) | Audio processing |

### Frameworks

| Framework | Purpose |
|-----------|---------|
| [Strands Agents SDK](https://github.com/strands-agents/sdk-python) | Agent framework |
| [MCP Python SDK 2.x](https://py.sdk.modelcontextprotocol.io/v2/) | MCP servers and clients |
| [LangFuse](https://langfuse.com/) | Observability |
| [RAGAS](https://docs.ragas.io/) | Evaluation |

---

## 💡 Real-World Applications

### Content Intelligence
- Automated content moderation
- Document analysis for compliance
- Multi-format data extraction

### Intelligent Assistants
- Customer support with memory
- Research assistants with cross-modal correlation
- Educational tutors with adaptive learning

### Enterprise Solutions
- Business intelligence dashboards
- Knowledge management systems
- Automated content generation

---

## 📖 Documentation

### Strands Agents
- [Official Documentation](https://strandsagents.com/)
- [SDK Repository](https://github.com/strands-agents/sdk-python)
- [Tools Package](https://github.com/strands-agents/tools)

### AWS Services
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Amazon S3 Vectors Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
- [Amazon Nova Models](https://docs.aws.amazon.com/nova/latest/userguide/)

### Frameworks
- [LangFuse Documentation](https://langfuse.com/docs)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent-to-Agent Protocol](https://a2a.ai/)

---

## 🎓 Best Practices

### Learning Path
1. Start with hello-world notebook
2. Progress through custom tools and MCP
3. Complete multimodal journey sequentially
4. Explore advanced topics based on needs

### Development Workflow
- Test locally with `FileMemoryStore` before S3 Vectors
- Monitor costs with AWS Cost Explorer
- Use appropriate model sizes for tasks
- Implement error handling and retries

### Production Deployment
- Use S3 Vectors for scalable memory
- Implement observability with LangFuse
- Set up evaluation with RAGAS
- Follow AWS security best practices

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| AWS credentials error | Run `aws configure` with valid credentials |
| Bedrock access denied | Enable models in [Bedrock console](https://console.aws.amazon.com/bedrock/) |
| Import errors | Verify `pip install -r requirements.txt` completed |
| Memory not persisting | Check the `.strands/memory/` folder is writable (FileMemoryStore) or the S3 Vectors bucket/index names |
| `ImportError ... was removed in v0.9.0` | Import from `strands.vended_tools` instead of `strands_tools` ([migration guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/)) |
| `No module named 'mcp.server.fastmcp'` | MCP SDK 2.x renamed `FastMCP` to `MCPServer` (`from mcp.server.mcpserver import MCPServer`) |

**Need help?** Check [Strands documentation](https://strandsagents.com/) or open an issue.

---

<p align="center">
  <strong>Ready to start?</strong><br>
  Begin with <a href="01-hello-world-strands-agents.ipynb">01-hello-world-strands-agents.ipynb</a>
</p>

---

<p align="center">
  🇻🇪🇨🇱 <strong>Created by</strong> <a href="https://www.linkedin.com/in/lizfue/">Eli</a> | 
  <a href="https://dev.to/elizabethfuentes12">Dev.to</a> | 
  <a href="https://github.com/elizabethfuentes12/">GitHub</a> | 
  <a href="https://twitter.com/elizabethfue12">Twitter</a>
</p>
