"""
S3 Vector Memory Tool for Strands Agents

Memory management tool using Amazon S3 Vectors with automatic context and user isolation.
Similar to mem0_memory functionality for Strands Agents.
"""

import boto3
import json
import uuid
import os
from typing import Dict, List
from datetime import datetime
from strands import tool

@tool
def s3_vector_memory(
    action: str,
    content: str = None,
    query: str = None,
    user_id: str = None,
    vector_bucket_name: str = None,
    index_name: str = None,
    top_k: int = 20,
    region_name: str = None,
    embedding_model: str = None,
    min_score: float = 0.1,
    max_context_memories: int = 10,
    auto_inject_context: bool = True
) -> Dict:
    """
    Memory management for S3 Vectors with automatic context like mem0_memory.
    
    Actions:
    - auto_store_and_retrieve: Store current interaction and retrieve relevant context (main action)
    - store: Store new memory
    - retrieve: Search memories  
    - list: List user memories
    - auto_context: Get context for conversation start
    
    Args:
        action: Operation to perform
        content: Content to store (for store/auto_store_and_retrieve)
        query: Search query (for retrieve/auto_store_and_retrieve)
        user_id: User identifier (required for security)
        vector_bucket_name: S3 Vector bucket (env: VECTOR_BUCKET_NAME)
        index_name: Vector index (env: VECTOR_INDEX_NAME)
        top_k: Maximum results to return
        region_name: AWS region (env: AWS_REGION, default: us-east-1)
        embedding_model: Bedrock model (env: EMBEDDING_MODEL, default: amazon.titan-embed-text-v2:0)
        min_score: Minimum similarity threshold
        max_context_memories: Max memories for auto-context
        auto_inject_context: Enable automatic context injection
        
    Returns:
        Dict with operation results and status
    """
    
    # Validate required parameters for security
    if not user_id:
        return {"status": "error", "message": "user_id is required"}
    
    try:
        # Load configuration from environment variables or use provided parameters
        config = {
            "bucket_name": vector_bucket_name or os.environ.get('VECTOR_BUCKET_NAME', 'multimodal-vector-store'),
            "index_name": index_name or os.environ.get('VECTOR_INDEX_NAME', 'strands-multimodal'),
            "region": region_name or os.environ.get('AWS_REGION', 'us-east-1'),
            "model_id": embedding_model or os.environ.get('EMBEDDING_MODEL', 'amazon.titan-embed-text-v2:0')
        }
        
        # Initialize AWS clients for Bedrock and S3 Vectors
        bedrock = boto3.client("bedrock-runtime", region_name=config["region"])
        s3vectors = boto3.client("s3vectors", region_name=config["region"])
        
        # Route to appropriate function based on action
        if action == "auto_store_and_retrieve":
            return _auto_store_and_retrieve(s3vectors, bedrock, config, content, query, user_id, 
                                          top_k, min_score, max_context_memories)
        elif action == "store":
            return _store_memory(s3vectors, bedrock, config, content, user_id)
        elif action == "retrieve":
            result = _retrieve_memories(s3vectors, bedrock, config, query, user_id, top_k, min_score)
            # Optionally inject automatic context for enhanced responses
            if auto_inject_context:
                context = _get_auto_context(s3vectors, bedrock, config, user_id, query, max_context_memories, min_score)
                result["context_summary"] = context.get("summary", "")
            return result
        elif action == "list":
            return _list_memories(s3vectors, bedrock, config, user_id, top_k)
        elif action == "auto_context":
            return _get_auto_context(s3vectors, bedrock, config, user_id, query or "", max_context_memories, min_score)
        else:
            return {"status": "error", "message": f"Invalid action: {action}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def _generate_embedding(bedrock, model_id: str, text: str) -> List[float]:
    """Generate text embedding using Amazon Bedrock"""
    # Truncate text if exceeds model limit (8000 chars for Titan)
    if len(text) > 8000:
        text = text[:8000]
    
    # Call Bedrock to generate embedding
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text})
    )
    
    # Extract and return embedding vector
    return json.loads(response["body"].read())["embedding"]

def _auto_store_and_retrieve(s3vectors, bedrock, config, content, query, user_id, top_k, min_score, max_context_memories):
    """Main action: Store current interaction and retrieve relevant context (like mem0_memory)"""
    
    # First retrieve relevant context if query is provided
    if query:
        retrieve_result = _retrieve_memories(s3vectors, bedrock, config, query, user_id, top_k, min_score)
    else:
        retrieve_result = {"memories": [], "status": "success"}
    
    # Then store the current interaction if content is provided
    if content:
        store_result = _store_memory(s3vectors, bedrock, config, content, user_id)
        
        # Return combined results for agent to process
        return {
            "status": "success",
            "action": "auto_store_and_retrieve",
            "stored": store_result,
            "retrieved": retrieve_result,
            "context_memories": retrieve_result.get("memories", [])
        }
    else:
        return retrieve_result

def _store_memory(s3vectors, bedrock, config, content, user_id):
    """Store memory with user isolation (like mem0_memory store action)"""
    if not content:
        return {"status": "error", "message": "content is required"}
    
    # Generate embedding for the content
    embedding = _generate_embedding(bedrock, config["model_id"], content)
    
    # Create unique memory key with user_id prefix for security
    memory_key = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    # Prepare vector data with metadata
    vector_data = {
        "key": memory_key,
        "data": {"float32": [float(x) for x in embedding]},  # Convert to float32 for S3 Vectors
        "metadata": {
            "user_id": user_id,
            "content": content,  # Store original content as-is (like mem0_memory)
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # Store vector in S3 Vectors index
    s3vectors.put_vectors(
        vectorBucketName=config["bucket_name"],
        indexName=config["index_name"],
        vectors=[vector_data]
    )
    
    return {
        "status": "success", 
        "message": "Memory stored successfully", 
        "memory_key": memory_key
    }

def _retrieve_memories(s3vectors, bedrock, config, query, user_id, top_k, min_score):
    """Retrieve memories for the agent to use (returns data, no internal RAG)"""
    if not query:
        return {"status": "error", "message": "query is required"}
    
    # Generate embedding for the search query
    query_embedding = _generate_embedding(bedrock, config["model_id"], query)
    
    # Search vectors with user-specific filter for security
    response = s3vectors.query_vectors(
        vectorBucketName=config["bucket_name"],
        indexName=config["index_name"],
        queryVector={"float32": query_embedding},
        topK=top_k,
        filter={"user_id": user_id},  # Ensure user isolation
        returnDistance=True,
        returnMetadata=True
    )
    
    # Process and filter results by similarity threshold
    memories = []
    for vector in response.get("vectors", []):
        # Double-check user_id for security
        if vector["metadata"].get("user_id") != user_id:
            continue
            
        # Calculate similarity score (1 - distance)
        similarity = 1.0 - vector.get("distance", 1.0)
        
        # Only include memories above minimum similarity threshold
        if similarity >= min_score:
            memories.append({
                "id": vector["key"],
                "memory": vector["metadata"].get("content", ""),
                "similarity": round(similarity, 3),
                "created_at": vector["metadata"].get("timestamp", "")
            })
    
    # Sort by similarity score (highest first)
    memories.sort(key=lambda x: x["similarity"], reverse=True)
    
    # Return data in mem0_memory format for agent to process
    return {
        "status": "success",
        "memories": memories[:top_k],
        "total_found": len(memories),
        "query": query
    }

def _list_memories(s3vectors, bedrock, config, user_id, top_k):
    """List all user memories with formatted output like mem0_memory"""
    # Use generic query to retrieve all user memories (not similarity-based)
    generic_embedding = _generate_embedding(bedrock, config["model_id"], "user memories")
    
    # Query all vectors for this user
    response = s3vectors.query_vectors(
        vectorBucketName=config["bucket_name"],
        indexName=config["index_name"],
        queryVector={"float32": generic_embedding},
        topK=top_k,
        filter={"user_id": user_id},  # User isolation
        returnMetadata=True
    )
    
    # Process all results without similarity filtering
    memories = []
    for i, vector in enumerate(response.get("vectors", []), 1):
        # Security check for user isolation
        if vector["metadata"].get("user_id") != user_id:
            continue
            
        # Format memory in mem0_memory style
        memories.append({
            "id": vector["key"],
            "memory": vector["metadata"].get("content", ""),
            "created_at": vector["metadata"].get("timestamp", ""),
            "updated_at": vector["metadata"].get("timestamp", "")
        })
    
    # Sort by creation timestamp (newest first)
    memories.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    # Display formatted output like mem0_memory
    if memories:
        print(f"\n📚 Found {len(memories)} memories for user {user_id}:")
        print("=" * 60)
        
        for i, memory in enumerate(memories, 1):
            print(f"\n{i}. Memory ID: {memory['id']}")
            print(f"   Content: {memory['memory'][:100]}{'...' if len(memory['memory']) > 100 else ''}")
            print(f"   Created: {memory['created_at'][:19] if memory['created_at'] else 'Unknown'}")
            
        print("\n" + "=" * 60)
    else:
        print(f"\n📭 No memories found for user {user_id}")
    
    return {
        "status": "success", 
        "memories": memories, 
        "total_found": len(memories)
    }

def _get_auto_context(s3vectors, bedrock, config, user_id, current_input, max_memories, min_score):
    """Get automatic context for conversation personalization (like mem0_memory auto-context)"""
    
    # Use current input or fallback to generic context query
    context_query = current_input or "user preferences, conversation history, important information"
    
    # Use lower threshold for context retrieval (more permissive)
    context_threshold = max(0.1, min_score - 0.2)
    
    # Generate embedding for context search
    query_embedding = _generate_embedding(bedrock, config["model_id"], context_query)
    
    # Search for relevant context memories
    response = s3vectors.query_vectors(
        vectorBucketName=config["bucket_name"],
        indexName=config["index_name"],
        queryVector={"float32": query_embedding},
        topK=max_memories,
        filter={"user_id": user_id},  # User isolation for context
        returnMetadata=True,
        returnDistance=True
    )
    
    # Process and filter context memories
    context_memories = []
    for vector in response.get("vectors", []):
        # Ensure user isolation
        if vector["metadata"].get("user_id") != user_id:
            continue
            
        # Calculate similarity for context relevance
        similarity = 1.0 - vector.get("distance", 1.0)
        
        # Include memories above context threshold
        if similarity >= context_threshold:
            context_memories.append({
                "content": vector["metadata"].get("content", ""),
                "similarity": round(similarity, 3),
                "timestamp": vector["metadata"].get("timestamp", "")
            })
    
    # Create context summary for agent use
    if context_memories:
        context_summary = "\n".join([f"- {mem['content']}" for mem in context_memories[:5]])
    else:
        context_summary = f"New user interaction for {user_id}"
    
    return {
        "status": "success",
        "context_memories": context_memories,
        "summary": context_summary,
        "total_context": len(context_memories)
    }
