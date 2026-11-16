import os
from urllib.parse import urlparse

from strands import Agent
from strands.models import BedrockModel
from strands.multiagent.a2a import A2AServer
from strands.tools.mcp.mcp_client import MCPClient

# Define URLs correctly - do not use os.environ.get() for literal values
EMPLOYEE_INFO_URL = "http://127.0.0.1:8002/mcp"
EMPLOYEE_AGENT_URL = "http://127.0.0.1:8001/"

# Create the MCP client. Passing `url=` makes MCPClient build the Streamable HTTP transport
# (the MCP Python SDK 2.x removed `streamablehttp_client`).
employee_mcp_client = MCPClient(url=EMPLOYEE_INFO_URL)

# Claude Haiku 5.5 on Amazon Bedrock through the `global.` cross-region inference profile.
# Model lifecycle: https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html
model = BedrockModel(
    model_id=os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def create_employee_agent(context_id: str) -> Agent:
    """Build one agent per A2A context (A2AServer calls this per conversation)."""
    return Agent(
        model=model,
        name="Employee Agent",
        description="Answers questions about employees",
        # Passing the MCPClient directly lets the agent manage the connection lifecycle.
        tools=[employee_mcp_client],
        system_prompt="you must abbreviate employee first names and list all their skills",
    )


# Create A2A server. `agent_factory` is the recommended (multi-tenant safe) way to wrap an agent:
# https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/
a2a_server = A2AServer(
    agent_factory=create_employee_agent,
    host=urlparse(EMPLOYEE_AGENT_URL).hostname,
    port=int(urlparse(EMPLOYEE_AGENT_URL).port),
)

# Start the server
if __name__ == "__main__":
    a2a_server.serve(host="0.0.0.0", port=8001)
