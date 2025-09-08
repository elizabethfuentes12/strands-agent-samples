# S3 Vector Memory Tool for Strands Agents

A memory management tool for [Strands Agents](https://strandsagents.com/) that uses Amazon S3 Vectors as the backend. This tool provides functionality similar to `mem0_memory` with AWS-native vector storage.

## Features

- **mem0_memory Compatible**: Drop-in replacement with the same API and functionality
- **Amazon S3 Vectors Backend**: AWS-native vector storage with automatic scaling
- **User Isolation**: Secure memory separation by user_id
- **Automatic Context**: Context retrieval for conversation continuity
- **Multi-Modal Support**: Works with text, images, documents, and video content
- **Environment Configuration**: Setup with environment variables

## Installation

```bash
# Install required dependencies
pip install strands-agents boto3

# Configure AWS credentials
aws configure
```

## Configuration

Set up your environment variables:

```bash
export VECTOR_BUCKET_NAME="your-s3-vector-bucket"
export VECTOR_INDEX_NAME="your-vector-index"
export AWS_REGION="us-east-1"
export EMBEDDING_MODEL="amazon.titan-embed-text-v2:0"
```

Configure directly in code:

```python
from s3_memory import s3_vector_memory

# Configuration via parameters
result = s3_vector_memory(
    action="store",
    content="Your content here",
    user_id="user123",
    vector_bucket_name="your-bucket",
    index_name="your-index",
    region_name="us-east-1"
)
```

## Usage

### Basic Operations

```python
from strands import Agent
from s3_memory import s3_vector_memory

# Create agent with S3 memory
agent = Agent(tools=[s3_vector_memory])

# The agent automatically uses memory for context
response = agent("What did we discuss about AWS architecture?")
```

### Direct Tool Usage

```python
# Store a memory
result = s3_vector_memory(
    action="store",
    content="You prefer serverless architecture and want cost optimization",
    user_id="user123"
)

# Retrieve relevant memories
result = s3_vector_memory(
    action="retrieve",
    query="serverless preferences",
    user_id="user123"
)

# List all memories
result = s3_vector_memory(
    action="list",
    user_id="user123"
)

# Auto store and retrieve (main action)
result = s3_vector_memory(
    action="auto_store_and_retrieve",
    content="Current conversation content",
    query="relevant context search",
    user_id="user123"
)
```

## Actions

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `store` | Store new memory | `content`, `user_id` |
| `retrieve` | Search memories | `query`, `user_id` |
| `list` | List all memories | `user_id` |
| `auto_store_and_retrieve` | Store and retrieve context | `user_id`, optional `content`/`query` |
| `auto_context` | Get conversation context | `user_id` |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | str | Required | Operation to perform |
| `content` | str | None | Content to store |
| `query` | str | None | Search query |
| `user_id` | str | Required | User identifier for isolation |
| `vector_bucket_name` | str | env var | S3 Vector bucket name |
| `index_name` | str | env var | Vector index name |
| `top_k` | int | 20 | Maximum results |
| `min_score` | float | 0.1 | Similarity threshold |
| `region_name` | str | us-east-1 | AWS region |
| `embedding_model` | str | titan-embed-text-v2:0 | Bedrock model |

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Strands       │    │   S3 Memory      │    │   Amazon S3     │
│   Agent         │───▶│   Tool           │───▶│   Vectors       │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Amazon         │
                       │   Bedrock        │
                       │   (Embeddings)   │
                       └──────────────────┘
```

## Security Features

- **User Isolation**: All operations are filtered by `user_id`
- **Validation**: Security checks at multiple levels
- **Access Control**: Memories are isolated between users
- **AWS IAM Integration**: Uses your AWS credentials and permissions

## Response Format

### Store Response
```json
{
  "status": "success",
  "message": "Memory stored successfully",
  "memory_key": "user123_20250108_143022_abc123"
}
```

### Retrieve Response
```json
{
  "status": "success",
  "memories": [
    {
      "id": "memory_key",
      "memory": "content text",
      "similarity": 0.85,
      "created_at": "2025-01-08T14:30:22"
    }
  ],
  "total_found": 1
}
```

## Comparison with mem0_memory

| Feature | mem0_memory | s3_memory |
|---------|-------------|-----------------|
| Backend | OpenSearch/FAISS/Mem0 | Amazon S3 Vectors |
| Scaling | Manual | Automatic |
| Cost | Infrastructure costs | Pay-per-use |
| Setup | Complex | AWS native |
| API | Same | Same |
| Performance | High | High |
| Multi-region | Manual | Built-in |

## Customization

### Custom Embedding Models

```python
# Use different Bedrock embedding models
result = s3_vector_memory(
    action="store",
    content="Your content",
    user_id="user123",
    embedding_model="cohere.embed-english-v3"  # Alternative model
)

# Or set globally
os.environ['EMBEDDING_MODEL'] = 'cohere.embed-multilingual-v3'
```

### Custom Similarity Thresholds

```python
# Adjust similarity thresholds for different use cases
result = s3_vector_memory(
    action="retrieve",
    query="search query",
    user_id="user123",
    min_score=0.05  # More permissive (finds more results)
)

# Strict matching
result = s3_vector_memory(
    action="retrieve", 
    query="search query",
    user_id="user123",
    min_score=0.8   # Stricter (fewer, more relevant results)
)
```

### Custom Memory Categories

```python
# Add metadata for categorization
def store_categorized_memory(content, category, user_id):
    """Store memory with custom category metadata"""
    enhanced_content = f"[{category.upper()}] {content}"
    return s3_vector_memory(
        action="store",
        content=enhanced_content,
        user_id=user_id
    )

# Usage
store_categorized_memory("AWS Lambda pricing discussion", "PRICING", "user123")
store_categorized_memory("Serverless architecture preferences", "PREFERENCES", "user123")
```

### Custom Memory Filters

```python
# Create domain-specific memory functions
def store_technical_insight(insight, technology, user_id):
    """Store technical insights with technology tags"""
    tagged_content = f"TECH-{technology}: {insight}"
    return s3_vector_memory(
        action="store",
        content=tagged_content,
        user_id=user_id
    )

def retrieve_by_technology(technology, user_id):
    """Retrieve memories for specific technology"""
    return s3_vector_memory(
        action="retrieve",
        query=f"TECH-{technology}",
        user_id=user_id,
        min_score=0.3
    )

# Usage
store_technical_insight("Lambda cold starts can be reduced with provisioned concurrency", "AWS-LAMBDA", "user123")
lambda_memories = retrieve_by_technology("AWS-LAMBDA", "user123")
```

### Custom Agent Integration

```python
from strands import Agent, tool

@tool
def enhanced_s3_memory(
    action: str,
    content: str = None,
    query: str = None,
    user_id: str = None,
    category: str = "general",
    priority: str = "normal"
):
    """Enhanced S3 memory with custom categorization"""
    
    if action == "store" and content:
        # Add priority and category to content
        enhanced_content = f"[{priority.upper()}][{category.upper()}] {content}"
        return s3_vector_memory(
            action="store",
            content=enhanced_content,
            user_id=user_id
        )
    
    # Pass through other actions
    return s3_vector_memory(
        action=action,
        content=content,
        query=query,
        user_id=user_id
    )

# Create agent with enhanced memory
agent = Agent(tools=[enhanced_s3_memory])
```

### Environment-Specific Configuration

```python
# Development environment
def setup_dev_memory():
    os.environ['VECTOR_BUCKET_NAME'] = 'dev-vector-store'
    os.environ['VECTOR_INDEX_NAME'] = 'dev-index'
    os.environ['MIN_SIMILARITY_SCORE'] = '0.05'  # More permissive for testing

# Production environment  
def setup_prod_memory():
    os.environ['VECTOR_BUCKET_NAME'] = 'prod-vector-store'
    os.environ['VECTOR_INDEX_NAME'] = 'prod-index'
    os.environ['MIN_SIMILARITY_SCORE'] = '0.3'   # Stricter for production

# Usage
if os.environ.get('ENVIRONMENT') == 'production':
    setup_prod_memory()
else:
    setup_dev_memory()
```

### Custom Memory Lifecycle

```python
def memory_with_ttl(content, user_id, ttl_days=30):
    """Store memory with time-to-live metadata"""
    from datetime import datetime, timedelta
    
    expiry_date = datetime.now() + timedelta(days=ttl_days)
    ttl_content = f"[EXPIRES:{expiry_date.isoformat()}] {content}"
    
    return s3_vector_memory(
        action="store",
        content=ttl_content,
        user_id=user_id
    )

def cleanup_expired_memories(user_id):
    """Retrieve and identify expired memories"""
    all_memories = s3_vector_memory(action="list", user_id=user_id)
    
    expired = []
    for memory in all_memories.get('memories', []):
        if '[EXPIRES:' in memory['memory']:
            # Extract expiry date and check if expired
            # Implementation depends on your cleanup strategy
            pass
    
    return expired

# Usage
memory_with_ttl("Temporary project notes", "user123", ttl_days=7)
```

## Advanced Usage

### Multi-Modal Content

```python
# Store image analysis results
s3_vector_memory(
    action="store",
    content="You uploaded architectural diagram showing microservices with API Gateway, Lambda functions, and DynamoDB",
    user_id="user123"
)

# Store document processing results
s3_vector_memory(
    action="store", 
    content="Document contains AWS best practices for serverless architecture with cost optimization strategies",
    user_id="user123"
)
```

### Conversation Context Management

```python
# At conversation start
context = s3_vector_memory(
    action="auto_context",
    user_id="user123"
)

# During conversation (automatic)
result = s3_vector_memory(
    action="auto_store_and_retrieve",
    content="You are asking about Lambda pricing models",
    query="AWS Lambda costs pricing",
    user_id="user123"
)
```

## Troubleshooting

### Common Issues

1. **No memories found**: Check `min_score` threshold (try 0.05)
2. **AWS permissions**: Verify S3 Vectors and Bedrock access
3. **Region mismatch**: Verify all services are in the same region
4. **Bucket not found**: Check `VECTOR_BUCKET_NAME` configuration

### Debug Mode

```python
# Turn on verbose logging
import logging
logging.getLogger("strands").setLevel(logging.DEBUG)
```

## Examples

See the complete notebook example: `multi-understanding-with-s3-memory.ipynb`

## Contributing

This tool is part of the Strands Agents ecosystem. For issues and contributions, refer to the main Strands Agents documentation.

## License

This project follows the same license as Strands Agents.

---

**Blog Series**: This is part of a multi-modal AI processing series. Previous episode: [Multi-Modal Content Processing with Strands Agent and FAISS Memory](https://dev.to/aws/multi-modal-content-processing-with-strands-agent-and-faiss-memory-39hg)
