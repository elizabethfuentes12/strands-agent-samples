# Strands Agent Samples

A comprehensive repository for implementing and demonstrating multi-modal understanding capabilities using the [Strands Agent framework](https://strandsagents.com/). This project enables processing and analysis of various types of content including documents, images, and videos with advanced features like persistent memory, observability, and inter-agent communication.

## Overview

This repository contains tools and examples for building AI agents capable of understanding and processing multiple types of media:
- **Images** (PNG, JPEG/JPG, GIF, WebP)
- **Documents** (PDF, CSV, DOCX, XLS, XLSX)
- **Videos** (MP4, MOV, AVI, MKV, WebM)

## 📚 Notebooks and Examples

| Use Case | Overview | Features | Language |
|----------|----------|----------|----------|
| [🎯 Multi-Agent Multimodal Analysis](notebook/multi-understanding.ipynb) | Basic demonstration notebook that shows how to process and analyze different types of media (images, documents, videos) and analyzing content and generating human-readable responses using Strands Agent | Multi-modal processing, AWS Bedrock integration, Custom tools | Python |
| [🎯 Multi-Agent Multimodal Analysis with FAISS Memory](notebook/multi-understanding-with-memory.ipynb) | Advanced notebook showcasing multi-modal (images, documents, videos) analysis with FAISS memory capabilities for storing and retrieving information across sessions | FAISS memory, Persistent storage, Cross-session continuity, User-specific memory | Python |
| [🔍 Observability with LangFuse and Evaluation with RAGAS](notebook/Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb) | Comprehensive notebook demonstrating how to implement observability and evaluation for Strands agents using LangFuse for tracing and RAGAS for evaluation metrics with a restaurant recommendation use case | LangFuse tracing, RAGAS evaluation, Performance monitoring, Quality assessment | Python |
| [🔧 Model Context Protocol (MCP) Tools](notebook/Strands_MCP_AND_Tools.ipynb) | Tutorial notebook showing how to create and integrate MCP servers with Strands agents, including custom calculator tools and weather services | MCP server creation, Custom tools, Protocol integration, Calculator and weather examples | Python |
| [🤝 Agent-to-Agent (A2A) Protocol](notebook/Strands_A2A_Tools.ipynb) | Advanced notebook demonstrating inter-agent communication using the A2A protocol, showcasing how multiple agents can collaborate and share information | Inter-agent communication, A2A protocol, Collaborative workflows, Multi-agent systems | Python |
| [📹 S3 Video Memory Demo](notebook/s3_video_memory_demo.ipynb) | Specialized notebook for processing videos stored in S3 with memory capabilities, combining cloud storage with intelligent video analysis | S3 integration, Cloud video processing, Memory storage, Scalable pipelines | Python |

## 🛠️ Supporting Tools and Files

| File | Description | Purpose |
|------|-------------|---------|
| [Video Reader Custom Tool](notebook/video_reader.py) | A custom tool for processing video content. It extracts frames from videos at specified intervals, converts them to base64-encoded images, and provides them to the agent for analysis | Video frame extraction and analysis |
| [MCP Calculator](notebook/mcp_calulator.py) | Example MCP server implementation for calculator functionality | MCP server example |
| [Requirements](notebook/requirements.txt) | Required Python packages for running all notebooks | Dependency management |

## 🚀 Key Features

### 🎯 Multi-Modal Processing
- **Image Analysis**: Process and understand visual content
- **Document Processing**: Extract and summarize text from various formats
- **Video Analysis**: Frame extraction and temporal understanding
- **Cross-Modal Correlation**: Connect insights across different media types

### 🧠 Memory & Persistence
- **FAISS-Powered Search**: Efficient similarity search for relevant information
- **Cross-Session Memory**: Information persists between application restarts
- **User-Specific Storage**: Personalized memory with unique user IDs
- **Contextual Retrieval**: Smart retrieval based on query context

### 🔍 Observability & Evaluation
- **LangFuse Integration**: Comprehensive tracing and monitoring
- **RAGAS Metrics**: Automated evaluation of agent performance
- **Performance Monitoring**: Real-time insights into agent behavior
- **Quality Assessment**: Continuous improvement through evaluation

### 🔧 Protocol Integration
- **Model Context Protocol (MCP)**: Standardized tool integration
- **Agent-to-Agent (A2A)**: Inter-agent communication and collaboration
- **Custom Tool Development**: Build specialized tools for specific needs
- **Serverless Deployment**: Cloud-native implementations

### ☁️ Cloud Integration
- **AWS Bedrock**: Access to state-of-the-art foundation models
- **S3 Storage**: Scalable storage for media files
- **Lambda Functions**: Serverless agent deployment
- **CDK Infrastructure**: Infrastructure as code

## 📁 Repository Structure

```
strands-agent-multi-understanding/
├── notebook/                           # Jupyter notebooks and examples
│   ├── multi-understanding.ipynb      # Basic multi-modal processing
│   ├── multi-understanding-with-memory.ipynb  # Advanced with FAISS memory
│   ├── Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb
│   ├── Strands_MCP_AND_Tools.ipynb    # MCP integration examples
│   ├── Strands_A2A_Tools.ipynb        # Agent-to-Agent communication
│   ├── s3_video_memory_demo.ipynb     # S3 video processing
│   ├── video_reader.py                # Custom video processing tool
│   ├── s3_video_memory.py             # S3 video memory tool
│   ├── mcp_calulator.py               # MCP calculator server
│   ├── requirements.txt               # Python dependencies
│   └── data-sample/                   # Sample files for testing
└── my_agent_cdk/                      # AWS CDK application
    ├── lambdas/code/lambda-s-agent    # Weather forecasting Lambda
    └── lambdas/code/lambda-s-multimodal # Multi-modal processing Lambda
```

## 🏁 Getting Started

### Prerequisites
- Python 3.8+
- AWS account with Bedrock access
- AWS CLI configured
- Node.js (for CDK deployment)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone [strands-agent-samples](https://github.com/elizabethfuentes12/strands-agent-samples)
   ```

2. **Set up the notebook environment**:
   ```bash
   cd notebook
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials** for Bedrock access:
   ```bash
   aws configure
   ```

4. **Start exploring**:
   ```bash
   jupyter notebook
   ```

### Recommended Learning Path

1. **Start with basics**: `multi-understanding.ipynb`
2. **Add memory**: `multi-understanding-with-memory.ipynb`
3. **Learn observability**: `Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb`
4. **Explore protocols**: `Strands_MCP_AND_Tools.ipynb`
5. **Advanced collaboration**: `Strands_A2A_Tools.ipynb`

## 🏗️ CDK Application

The `/my_agent_cdk/` directory contains an AWS CDK application for deploying serverless Lambda functions:

### Available Lambda Functions

| Function | Description | Use Case |
|----------|-------------|----------|
| **Weather Forecasting Agent** | Lambda function using Strands Agent for weather forecasting | API-based weather services |
| **Multi-modal Processing Agent** | Lambda function for processing images, documents, and videos | Serverless content analysis |

### Deployment Instructions

1. **Navigate to CDK directory**:
   ```bash
   cd my_agent_cdk
   ```

2. **Install dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Package Lambda layers**:
   ```bash
   pip install -r layers/lambda_requirements.txt --python-version 3.12 --platform manylinux2014_aarch64 --target layers/strands/_dependencies --only-binary=:all:
   python layers/package_for_lambda.py
   ```

4. **Deploy**:
   ```bash
   cdk bootstrap  # First time only
   cdk deploy
   ```

For detailed instructions, see the [CDK application README](my_agent_cdk/README.md).

## 💡 Use Cases

- **Content Analysis**: Automated processing of mixed media content
- **Knowledge Management**: Building searchable knowledge bases from various media types
- **Educational Tools**: Multi-modal learning assistants with memory
- **Business Intelligence**: Extracting insights from documents, images, and videos
- **Quality Assurance**: Automated evaluation and monitoring of AI agents
- **Collaborative AI**: Multi-agent systems for complex workflows
- **Customer Support**: Intelligent assistants with observability and evaluation
- **Research & Development**: Advanced AI experimentation with proper tooling

## 📖 Resources

- [Strands Agent Documentation](https://strandsagents.com/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [LangFuse Documentation](https://langfuse.com/docs)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Agent-to-Agent Protocol](https://a2a.ai/)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔒 Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for security issue notifications.

## 📄 License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.

---

**🇻🇪🇨🇱 ¡Gracias!**

[Eli](https://www.linkedin.com/in/lizfue/) | [Dev.to](https://dev.to/elizabethfuentes12) | [GitHub](https://github.com/elizabethfuentes12/) | [Twitter](https://twitter.com/elizabethfue12) | [YouTube](https://www.youtube.com/channel/UCr0Gnc-t30m4xyrvsQpNp2Q)

---

*Ready to build intelligent multi-modal AI agents? Start with the notebooks and explore the endless possibilities!*
