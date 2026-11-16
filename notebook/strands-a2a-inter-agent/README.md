# Agent-to-Agent (A2A) Communication Example

This directory contains examples of Agent-to-Agent (A2A) communication using the MCP (Model Context Protocol) framework.

## Components

The system consists of three main components:

1. **MCP Server** (`server.py`): Provides employee data and skills information
2. **Employee Agent** (`employee-agent.py`): An agent that can answer questions about employees
3. **HR Agent** (`hr-agent.py`): An agent that can answer HR-related questions by communicating with the Employee Agent

## Setup and Running

### A2A System Runner: Runs the MCP Server, Employee Agent, and HR Agent in parallel

### 1. Configure AWS credentials

The agents call Claude Haiku 5.5 on Amazon Bedrock (`global.anthropic.claude-haiku-5-5`). Make sure your AWS credentials are configured and that you have [model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) in your account. Optional overrides:

```bash
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=global.anthropic.claude-haiku-5-5
```

### 2. Start the system:
  ```bash
   python run_a2a_system.py
```


### 4. Make Requests to the HR Agent

Once all three components are running, you can make requests to the HR Agent:

```bash
curl -X POST --location "http://0.0.0.0:8000/inquire" \
-H "Content-Type: application/json" \
-d '{"question": "list employees that have skills related to AI programming"}'
```

## Architecture

```
+-------------+         +----------------+         +------------+
|  HR Agent   |  <--->  | Employee Agent |  <--->  | MCP Server |
| (Port 8000) |         |  (Port 8001)   |         | (Port 8002)|
+-------------+         +----------------+         +------------+
       ^
       |
    User Requests
```

The HR Agent receives questions from users, communicates with the Employee Agent to get information, and the Employee Agent in turn communicates with the MCP Server to retrieve the actual data.

## Notes

- The MCP Server uses `MCPServer` from the MCP Python SDK 2.x (formerly `FastMCP`) to expose tools over Streamable HTTP at `http://127.0.0.1:8002/mcp`
- The Employee Agent uses `MCPClient(url=...)` and is exposed with `A2AServer(agent_factory=...)` on port 8001
- The HR Agent uses the SDK-vended `make_a2a_client` tool (replaces the removed `A2AClientToolProvider` from `strands-agents-tools`) and provides a REST API endpoint for users to ask questions
- Tested with `strands-agents` 1.65.0, `mcp` 2.3.0, `a2a-sdk` 0.3.26
