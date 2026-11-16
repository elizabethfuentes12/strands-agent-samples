import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from strands import Agent
from strands.models import BedrockModel
# `A2AClientToolProvider` from strands_tools was removed in strands-agents-tools 0.9.0.
# The SDK now vends an A2A client tool factory:
# https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/
from strands.vended_tools import make_a2a_client

EMPLOYEE_AGENT_URL = "http://127.0.0.1:8001/"

app = FastAPI(title="HR Agent API")

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Claude Haiku 5.5 on Amazon Bedrock through the `global.` cross-region inference profile.
model = BedrockModel(
    model_id=os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)

# The A2A client tool exposes `discover` and `send_message` operations to the model and only
# talks to the endpoints listed here.
a2a_client_tool = make_a2a_client(allowed_endpoints=[EMPLOYEE_AGENT_URL])

@app.post("/inquire")
async def ask_agent(request: QuestionRequest):
    async def generate():
        agent = Agent(
            model=model,
            tools=[a2a_client_tool],
            system_prompt=(
                "You are an HR assistant. Use the a2a_client tool to discover and ask the "
                f"Employee Agent at {EMPLOYEE_AGENT_URL} whenever you need employee information."
            ),
        )

        stream_response = agent.stream_async(request.question)

        async for event in stream_response:
            if "data" in event:
                yield event["data"]

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
