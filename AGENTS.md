# AGENTS.md

Guidance for AI coding agents (and humans) working on this repository.

## What this repo is

Sample notebooks and a CDK app showing how to build agents with the [Strands Agents SDK](https://strandsagents.com/) on Amazon Bedrock: basics, custom tools, MCP (Model Context Protocol), A2A (Agent-to-Agent), observability, and a 6-chapter multimodal series (images, documents, video, memory, content generation). Owner: Elizabeth Fuentes (AWS Developer Advocate). Public sample, MIT-0.

## Layout

```
notebook/                          # learning notebooks (run from this folder)
  01..06-*.ipynb                   # basics → custom tools → MCP → MCP+tools → A2A → LangFuse/RAGAS
  mcp_calulator.py                 # MCP server + Strands client demo (sic: filename typo is public, keep it)
  run_a2a_system.py                # starts the 3 A2A processes below
  strands-a2a-inter-agent/         # MCP server (8002) → Employee A2A agent (8001) → HR FastAPI agent (8000)
  multimodal_understanding/        # 6-chapter multimodal series + helper tools
    video_reader.py                # video → Bedrock Converse by S3 location (needs VIDEO_READER_S3_BUCKET)
    video_reader_local.py          # video → Bedrock Converse inline bytes (<20 MB)
    s3_memory.py                   # memory tool on Amazon S3 Vectors + Nova multimodal embeddings
    content_tools.py               # generate_image (Stability AI), generate_video/check_video_status (Luma Ray 2), download_from_s3
    travel_content_generator.py    # CLI version of notebook 05
  requirements.txt                 # pinned deps for every notebook
my_agent_cdk/                      # CDK (Python) stack: 2 Lambdas (weather agent, multimodal agent) + S3 sample bucket
  lambdas/code/lambda-s-agent/     # weather agent (vended http_request)
  lambdas/code/lambda-s-multimodal/# read (vended) + video_reader; MODEL_ID and REGION_NAME env vars
  layers/                          # Lambda layer build (pip --platform manylinux2014_aarch64, py3.12)
```

## Versions this repo targets (verified Nov 2026)

- `strands-agents==1.65.0`, `strands-agents-tools` is **not** needed anymore (0.9.0 removed most tools).
- `mcp==2.3.0` (MCP Python SDK **2.x**: `FastMCP` → `MCPServer`, `streamablehttp_client` removed; use `MCPClient(url=...)`).
- `boto3==1.44.3`, `aws-cdk-lib==2.277.0`, Python 3.10+ (tested 3.11), Lambda runtime python3.12 arm64.
- Models (all ACTIVE on Bedrock; always check https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html):
  - Agent reasoning: `global.anthropic.claude-haiku-5-5` (Claude API id `claude-haiku-5-5`). Claude 4.7+ models **reject `temperature`/`top_p`/`top_k`**.
  - Video understanding: `us.amazon.nova-2-lite-v1:0` (inference profile required).
  - Image generation: `stability.stable-image-core-v1:1` (us-west-2). Video generation: `luma.ray-v2:0` (us-west-2, async, S3 bucket in the same region).
  - Embeddings: `amazon.nova-2-multimodal-embeddings-v1:0` (S3 Vectors), `amazon.titan-embed-text-v1` (notebook 06).

## Commands

```bash
cd notebook && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
# run a notebook headless
jupyter nbconvert --to notebook --execute 02-custom-tools.ipynb --output /tmp/out.ipynb --ExecutePreprocessor.timeout=900
# MCP demo (notebook 03 needs the server running in another terminal: python mcp_custom_tools_server.py)
python mcp_calulator.py
# A2A demo
python run_a2a_system.py   # then: curl -X POST localhost:8000/inquire -H 'Content-Type: application/json' -d '{"question":"..."}'
# CDK
cd my_agent_cdk && pip install -r requirements.txt -r requirements-dev.txt
pip install -r layers/lambda_requirements.txt --python-version 3.12 --platform manylinux2014_aarch64 --target layers/strands/_dependencies --only-binary=:all:
python layers/package_for_lambda.py && npx aws-cdk@2 synth && pytest tests
```

Environment variables used by the samples: `AWS_REGION` (default us-east-1), `BEDROCK_MODEL_ID` (A2A/mcp_calulator), `VIDEO_READER_S3_BUCKET` (video_reader), `VECTOR_BUCKET_NAME` / `VECTOR_INDEX_NAME` / `EMBEDDING_MODEL` (s3_memory), `ANTHROPIC_API_KEY` (notebooks 01/04/06 Anthropic provider cells), `CONTENT_TOOLS_REGION` / `IMAGE_MODEL_ID` / `VIDEO_MODEL_ID` (content_tools).

## Conventions and gotchas

- Tools: use `strands.vended_tools` (`read`, `write`, `http_request`, `subagent`, `make_a2a_client`) instead of `strands_tools`. `read` returns images/PDFs as media blocks and **requires absolute paths**; notebooks compute `DATA = os.path.abspath("data-sample")`.
- Memory: notebook multimodal 03 uses `MemoryManager` + `FileMemoryStore` (local markdown under `.strands/memory/`). Mem0 is optional (`mem0-strands`), but mem0's Bedrock LLM always sends `temperature`, so it cannot use Claude 5.5 as extractor.
- Agent results: Claude 5.5 can return a `reasoningContent` block first; never index `message["content"][0]["text"]`, collect text blocks instead.
- MCP servers: `mcp.run(transport="streamable-http", host=..., port=...)`; transport options go to `run()`, not the constructor.
- Keep file names stable (public article links point to `03-multimodal-with-faiss.ipynb`).
- Generated artifacts are gitignored: `mcp_custom_tools_server*.py`, `output/`, `.strands/`, `restaurant-vectordb/`, `layers/strands/_dependencies`, `dependencies.zip`, `cdk.out/`.
- No Docker is required anywhere (layer is built with pip `--platform`).

## State / recent changes

- 2026-11: migrated to strands-agents 1.65 / strands-agents-tools 0.9 / mcp 2.x; replaced EOL models (Claude 3.x, Sonnet 4, Nova Pro video default, Nova Canvas/Reel) with ACTIVE ones; added `content_tools.py`; A2A sample moved to Bedrock + `make_a2a_client`; CDK bumped to aws-cdk-lib 2.277.0 and pytest 8+. All notebooks except 04 (Anthropic API) and 06 (LangFuse/RAGAS, needs third-party keys) were executed end to end against Bedrock.
