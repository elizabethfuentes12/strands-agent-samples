# Multi-Understanding Notebooks

This directory contains notebooks and supporting files for demonstrating multi-modal understanding capabilities using the [Strands Agent framework](https://strandsagents.com/).

## Contents

| Use Case | Overview | Language |
|----------|----------|----------|
| [🎯 Multi-Agent Multimodal Analysis](multi-understanding.ipynb) | Basic demonstration notebook that shows how to process and analyze different types of media (images, documents, videos) and analyzing content and generating human-readable responses using Strands Agent | Python |
| [🎯 Multi-Agent Multimodal Analysis with FAISS Memory](multi-understanding-with-memory.ipynb) | Advanced notebook showcasing multi-modal (images, documents, videos) analysis with FAISS memory capabilities for storing and retrieving information across sessions | Python |
| [🔍 Observability with LangFuse and Evaluation with RAGAS](Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb) | Comprehensive notebook demonstrating how to implement observability and evaluation for Strands agents using LangFuse for tracing and RAGAS for evaluation metrics with a restaurant recommendation use case | Python |
| [🔧 Model Context Protocol (MCP) Tools](Strands_MCP_AND_Tools.ipynb) | Tutorial notebook showing how to create and integrate MCP servers with Strands agents, including custom calculator tools and weather services | Python |
| [🤝 Agent-to-Agent (A2A) Protocol](Strands_A2A_Tools.ipynb) | Advanced notebook demonstrating inter-agent communication using the A2A protocol, showcasing how multiple agents can collaborate and share information | Python |


## Supporting Files

| File | Description |
|------|-------------|
| [Video Reader Custom Tool](video_reader.py) | A custom tool for processing video content. It extracts frames from videos at specified intervals, converts them to base64-encoded images, and provides them to the agent for analysis |
| [MCP Calculator](mcp_calulator.py) | Example MCP server implementation for calculator functionality |
| [Requirements](requirements.txt) | Required Python packages for running all notebooks |

## Getting Started

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure [AWS credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html) for Amazon Bedrock access.

4. Open the notebook that you want to explore
  

## Notebook Overview

### Basic Multi-Modal Processing
- **`multi-understanding.ipynb`**: Entry-level notebook demonstrating core multi-modal capabilities
- **`multi-understanding-with-memory.ipynb`**: Enhanced version with persistent memory using FAISS

### Advanced Features
- **`Strands_Observability_with_LangFuse_and_Evaluation_with_RAGAS.ipynb`**: Production-ready observability and evaluation
- **`Strands_MCP_AND_Tools.ipynb`**: Model Context Protocol integration
- **`Strands_A2A_Tools.ipynb`**: Agent-to-Agent communication patterns


## Sample Files

The `data-sample/` directory includes sample files for testing:
- `diagram.jpg` - Sample image file for image analysis
- `Welcome-Strands-Agents-SDK.pdf` - Sample PDF document for text extraction
- `Prompt-Engineering.pdf` - Sample PDF document for content analysis
- `moderation-video.mp4` - Sample video file for video frame extraction

## Key Features Demonstrated

### 🎯 Multi-Modal Processing
- Image analysis and understanding
- Document processing and summarization
- Video frame extraction and analysis
- Cross-modal content correlation

### 🧠 Memory & Persistence
- FAISS-powered similarity search
- Cross-session memory retention
- Contextual information retrieval
- User-specific memory storage

### 🔍 Observability & Evaluation
- LangFuse integration for tracing
- RAGAS metrics for evaluation
- Performance monitoring
- Quality assessment

### 🔧 Protocol Integration
- Model Context Protocol (MCP) servers
- Agent-to-Agent (A2A) communication
- Custom tool development
- Inter-agent collaboration

## Use Cases

- **Content Analysis**: Automated processing of mixed media content
- **Knowledge Management**: Building searchable knowledge bases from various media types
- **Educational Tools**: Multi-modal learning assistants
- **Business Intelligence**: Extracting insights from documents, images, and videos
- **Quality Assurance**: Automated evaluation and monitoring of AI agents
- **Collaborative AI**: Multi-agent systems for complex workflows


---

**Gracias**

🇻🇪🇨🇱 [Dev.to](https://dev.to/elizabethfuentes12) [Linkedin](https://www.linkedin.com/in/lizfue/) [GitHub](https://github.com/elizabethfuentes12/) [Twitter](https://twitter.com/elizabethfue12) [Instagram](https://www.instagram.com/elifue.tech) [Youtube](https://www.youtube.com/channel/UCr0Gnc-t30m4xyrvsQpNp2Q)
[Linktr](https://linktr.ee/elizabethfuentesleone)
