"""
S3 Video Memory Tool - Similar to mem0_memory but using S3 Vectors with JSON classification

This tool provides memory management capabilities using Amazon S3 Vectors
for storing and retrieving conversation history with automatic JSON classification
and user-specific filtering.
"""

import boto3
import json
import uuid
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from strands import tool

# Initialize Rich console
console = Console()

@tool
def s3_video_memory(
    action: str,
    content: str = None,
    query: str = None,
    user_id: str = None,
    agent_id: str = None,
    metadata: Dict[str, Any] = None,
    vector_bucket_name: str = None,
    index_name: str = None,
    top_k: int = 5,
    region_name: str = None,
    embedding_model: str = "amazon.titan-embed-text-v2:0",
    model_id: str = None,
    min_score: float = 0.7
) -> Dict[str, Any]:
    """
    Memory management tool using S3 Vectors with automatic JSON classification.
    
    Similar to mem0_memory but uses S3 Vectors as backend instead of OpenSearch/FAISS/Mem0.
    
    Args:
        action: Action to perform (store, retrieve, list, delete)
        content: Content to store (required for store action)
        query: Search query (required for retrieve action)
        user_id: User ID for filtering (required for store, retrieve, list)
        agent_id: Agent ID for filtering (alternative to user_id)
        metadata: Additional metadata to store
        vector_bucket_name: S3 Vector bucket name (uses VECTOR_BUCKET_NAME env if not specified)
        index_name: Vector index name (default: "default-index")
        top_k: Number of results to return (default: 5)
        region_name: AWS region (default: "us-west-2")
        embedding_model: Bedrock embedding model (default: "amazon.titan-embed-text-v2:0")
        model_id: Bedrock model for classification 
        min_score: Minimum similarity score for search results (default: 0.7)
        
    Returns:
        Dict with status and operation results
    """
    
    try:
        # Validate required parameters
        if not action:
            raise ValueError("action parameter is required")
        
        # Initialize clients
        bedrock_client = boto3.client("bedrock-runtime", region_name=region_name)
        s3vectors_client = boto3.client("s3vectors", region_name=region_name)
        
        # Get vector bucket name
        if not vector_bucket_name:
            vector_bucket_name = os.environ.get("VECTOR_BUCKET_NAME")
            if not vector_bucket_name:
                raise ValueError("Vector bucket name not provided. Set VECTOR_BUCKET_NAME environment variable or provide vector_bucket_name parameter.")
        
        # Get index name from environment variable
        
        if not index_name:
            index_name = os.environ.get("VECTOR_INDEX")
            if not index_name:
                raise ValueError("Index name not provided. Set VECTOR_INDEX environment variable or provide index_name parameter.")
        
        # Handle different actions
        if action == "store":
            if not content:
                raise ValueError("content is required for store action")
            if not user_id and not agent_id:
                raise ValueError("Either user_id or agent_id must be provided for store action")
            
            # Show confirmation dialog unless in bypass mode
   
            _store_memory(bedrock_client, s3vectors_client, vector_bucket_name, index_name, content, user_id, agent_id, metadata, embedding_model, model_id)
            content_preview = content[:500] + "..." if len(content) > 500 else content
            identifier = f"user {user_id}" if user_id else f"agent {agent_id}"
            console.print(Panel(content_preview, title=f"[bold green]Memory to store for {identifier}", border_style="green"))
            
        elif action == "retrieve":
            if not query:
                raise ValueError("query is required for retrieve action")
            if not user_id and not agent_id:
                raise ValueError("Either user_id or agent_id must be provided for retrieve action")
            
            result = _retrieve_memories(bedrock_client, s3vectors_client, vector_bucket_name, index_name, query, user_id, agent_id, top_k, embedding_model, min_score)
            
            # Display results
            if result["status"] == "success" and result.get("memories"):
                panel = format_retrieve_response(result["memories"])
                console.print(panel)
            
            return result
            
        elif action == "list":
            if not user_id and not agent_id:
                raise ValueError("Either user_id or agent_id must be provided for list action")
            
            result = _list_memories(s3vectors_client, vector_bucket_name, index_name, user_id, agent_id, top_k)
            
            # Display results
            if result["status"] == "success" and result.get("memories"):
                panel = format_list_response(result["memories"])
                console.print(panel)
            
            return result
            
        elif action == "delete":
            if not metadata or "vector_key" not in metadata:
                raise ValueError("vector_key in metadata is required for delete action")
            
            console.print(Panel(f"Vector Key: {metadata['vector_key']}", title="[bold red]⚠️ Memory to be permanently deleted", border_style="red"))
            
            result = _delete_memory(s3vectors_client, vector_bucket_name, index_name, metadata["vector_key"])
            
            # Display result
            if result["status"] == "success":
                panel = format_delete_response(metadata["vector_key"])
                console.print(panel)
            
            return result
            
        else:
            raise ValueError(f"Invalid action: {action}. Available actions: store, retrieve, list, delete")
            
    except Exception as e:
        error_panel = Panel(
            Text(str(e), style="red"),
            title="❌ S3 Video Memory Error",
            border_style="red"
        )
        console.print(error_panel)
        return {
            "status": "error",
            "content": [{"text": f"❌ Error: {str(e)}"}]
        }


def _classify_content(bedrock_client, content: str, model_id: str) -> Dict[str, Any]:
    """Classify content into JSON structure using Bedrock LLM"""
    
    prompt = f"""
    Clasifica el siguiente contenido en JSON con esta estructura exacta:
    {{
        "summary": "resumen conciso del contenido",
        "category": "conversacion|pregunta|informacion|respuesta|instruccion|otro",
        "keywords": ["palabra1", "palabra2", "palabra3"],
        "sentiment": "positivo|negativo|neutral",
        "topics": ["tema1", "tema2"],
        "importance": "alta|media|baja",
        "context": "contexto o situación del contenido",
        "intent": "intención del usuario"
    }}
    
    Contenido a clasificar:
    {content}
    
    Responde SOLO con el JSON válido, sin texto adicional.
    """
    
    try:
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        
        result = json.loads(response['body'].read())
        classification_text = result['content'][0]['text']
        
        # Parse JSON response
        return json.loads(classification_text)
        
    except Exception as e:
        # Fallback classification if LLM fails
        return {
            "summary": content[:200] + "..." if len(content) > 200 else content,
            "category": "otro",
            "keywords": [],
            "sentiment": "neutral",
            "topics": [],
            "importance": "media",
            "context": "contenido sin clasificar",
            "intent": "desconocido"
        }


def _generate_embedding(bedrock_client, text: str, model_id: str) -> List[float]:
    """Generate embedding using Bedrock"""
    
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps({"inputText": text})
    )
    print(response)
    response_body = json.loads(response["body"].read())
    print(response_body)
    return response_body["embedding"]


def _store_memory(bedrock_client, s3vectors_client, bucket_name: str, index_name: str, content: str, user_id: str, agent_id: str, metadata: Dict[str, Any], embedding_model: str, model_id: str) -> Dict[str, Any]:
    """Store memory with JSON classification"""
    
    try:
        # Classify content
        classification = _classify_content(bedrock_client, content, model_id)
        print(classification)
        
        # Generate embedding from the summary (classified content)
        embedding = _generate_embedding(bedrock_client, classification, embedding_model)
        print(embedding)
        
        # Create vector key
        vector_key = str(uuid.uuid4())
        
        # Prepare metadata
        vector_metadata = {
            "vector_key": vector_key,
            "user_id": user_id,
            "agent_id": agent_id,
            "original_content": content,
            "classification": classification,
            "timestamp": datetime.now().isoformat(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add user-provided metadata
        if metadata:
            vector_metadata.update(metadata)

        print("vector_metadata ",vector_metadata)

        # Store vector in S3
        response = s3vectors_client.put_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            vectors=[{
                "key": vector_key,
                "data": {"float32": embedding},
                "metadata": vector_metadata
            }]
        )
        print("response ",response)
        
        # Format response like mem0_memory
        result = {
            "id": vector_key,
            "memory": classification,
            "event": "CREATED",
            "user_id": user_id,
            "agent_id": agent_id,
            "metadata": vector_metadata,
            "created_at": vector_metadata
        }
        
        # Display success message
        panel = format_store_response([result])
        console.print(panel)
        
        return {
            "status": "success",
            "content": [{"text": json.dumps([result], indent=2)}]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ Error storing memory: {str(e)}"}]
        }


def _retrieve_memories(bedrock_client, s3vectors_client, bucket_name: str, index_name: str, query: str, user_id: str, agent_id: str, top_k: int, embedding_model: str, min_score: float) -> Dict[str, Any]:
    """Retrieve memories using semantic search"""
    
    try:
        # Generate query embedding
        query_embedding = _generate_embedding(bedrock_client, query, embedding_model)
        
        # Prepare search parameters
        search_params = {
            "vectorBucketName": bucket_name,
            "indexName": index_name,
            "queryVector": {"float32": query_embedding},
            "topK": top_k,
            "returnDistance": True,
            "returnMetadata": True
        }
        
        # Add user/agent filter
        if user_id:
            search_params["filter"] = {"user_id": user_id}
        elif agent_id:
            search_params["filter"] = {"agent_id": agent_id}
        
        # Search vectors
        response = s3vectors_client.query_vectors(**search_params)
        print(response)

        print(json.dumps(response["vectors"], indent=2))
        
        # Format results like mem0_memory
        memories = []
        for vector in response.get("vectors", []):
            distance = vector.get("distance", 1.0)
            # Convert distance to similarity score (assuming cosine distance)
            similarity = 1.0 - distance
            
            # Filter by minimum score
            if similarity >= min_score:
                vector_metadata = vector.get("metadata", {})
                classification = vector_metadata.get("classification", {})
                
                memory = {
                    "id": vector.get("key"),
                    "memory": classification.get("summary", "No summary available"),
                    "score": similarity,
                    "user_id": vector_metadata.get("user_id"),
                    "agent_id": vector_metadata.get("agent_id"),
                    "created_at": vector_metadata.get("created_at"),
                    "metadata": {
                        "category": classification.get("category"),
                        "keywords": classification.get("keywords", []),
                        "sentiment": classification.get("sentiment"),
                        "topics": classification.get("topics", []),
                        "importance": classification.get("importance"),
                        "context": classification.get("context"),
                        "intent": classification.get("intent")
                    }
                }
                memories.append(memory)
        
        # Sort by score (highest first)
        memories.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "status": "success",
            "memories": memories,
            "content": [{"text": json.dumps(memories, indent=2)}]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ Error retrieving memories: {str(e)}"}]
        }


def _list_memories(s3vectors_client, bucket_name: str, index_name: str, user_id: str, agent_id: str, limit: int) -> Dict[str, Any]:
    """List memories for a user/agent"""
    
    try:
        # Since S3 Vectors doesn't have a direct "list" operation,
        # we'll do a broad search to get recent memories
        # This is a workaround - in production you might want to maintain a separate index
        
        # Use a broad query to get memories
        broad_query = "conversacion memoria contenido"
        
        # For now, we'll use a dummy embedding for broad search
        # In production, you might want to store an index of all vectors separately
        
        memories = []
        
        # This is a placeholder - S3 Vectors doesn't have a direct listing capability
        # You would need to implement a separate tracking mechanism
        
        return {
            "status": "success",
            "memories": memories,
            "content": [{"text": "📋 Note: Direct listing requires implementing a separate index. Use retrieve with a broad query to get recent memories."}]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ Error listing memories: {str(e)}"}]
        }


def _delete_memory(s3vectors_client, bucket_name: str, index_name: str, vector_key: str) -> Dict[str, Any]:
    """Delete a specific memory"""
    
    try:
        s3vectors_client.delete_vectors(
            vectorBucketName=bucket_name,
            indexName=index_name,
            keys=[vector_key]
        )
        
        return {
            "status": "success",
            "content": [{"text": f"✅ Memory {vector_key} deleted successfully"}]
        }
        
    except Exception as e:
        return {
            "status": "error",
            "content": [{"text": f"❌ Error deleting memory: {str(e)}"}]
        }


# Formatting functions similar to mem0_memory.py

def format_store_response(results: List[Dict]) -> Panel:
    """Format store memory response"""
    
    if not results:
        return Panel("No memories stored.", title="[bold yellow]No Memories Stored", border_style="yellow")
    
    table = Table(title="Memory Stored", show_header=True, header_style="bold magenta")
    table.add_column("Operation", style="green")
    table.add_column("Summary", style="yellow", width=50)
    table.add_column("Category", style="blue")
    table.add_column("Keywords", style="cyan")
    
    for memory in results:
        event = memory.get("event", "CREATED")
        summary = memory.get("memory", "No summary")
        classification = memory.get("metadata", {}).get("classification", {})
        category = classification.get("category", "N/A")
        keywords = ", ".join(classification.get("keywords", []))
        
        # Truncate summary if too long
        summary_preview = summary[:100] + "..." if len(summary) > 100 else summary
        
        table.add_row(event, summary_preview, category, keywords)
    
    return Panel(table, title="[bold green]Memory Stored", border_style="green")


def format_retrieve_response(memories: List[Dict]) -> Panel:
    """Format retrieve response"""
    
    if not memories:
        return Panel("No memories found matching the query.", title="[bold yellow]No Matches", border_style="yellow")
    
    table = Table(title="Search Results", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Memory", style="yellow", width=40)
    table.add_column("Score", style="green")
    table.add_column("Category", style="blue")
    table.add_column("Keywords", style="magenta")
    table.add_column("Created", style="white")
    
    for memory in memories:
        memory_id = memory.get("id", "unknown")[:8] + "..."
        content = memory.get("memory", "No content")
        score = memory.get("score", 0)
        created_at = memory.get("created_at", "Unknown")
        
        metadata = memory.get("metadata", {})
        category = metadata.get("category", "N/A")
        keywords = ", ".join(metadata.get("keywords", []))
        
        # Truncate content if too long
        content_preview = content[:80] + "..." if len(content) > 80 else content
        
        # Color code the score
        if score > 0.8:
            score_color = "green"
        elif score > 0.5:
            score_color = "yellow"
        else:
            score_color = "red"
        
        table.add_row(
            memory_id,
            content_preview,
            f"[{score_color}]{score:.3f}[/{score_color}]",
            category,
            keywords[:30] + "..." if len(keywords) > 30 else keywords,
            created_at
        )
    
    return Panel(table, title="[bold green]Search Results", border_style="green")


def format_list_response(memories: List[Dict]) -> Panel:
    """Format list memories response"""
    
    if not memories:
        return Panel("No memories found.", title="[bold yellow]No Memories", border_style="yellow")
    
    table = Table(title="Memories", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Memory", style="yellow", width=50)
    table.add_column("Category", style="blue")
    table.add_column("Created At", style="green")
    table.add_column("User ID", style="magenta")
    
    for memory in memories:
        memory_id = memory.get("id", "unknown")[:8] + "..."
        content = memory.get("memory", "No content")
        created_at = memory.get("created_at", "Unknown")
        user_id = memory.get("user_id", "Unknown")
        
        metadata = memory.get("metadata", {})
        category = metadata.get("category", "N/A")
        
        # Truncate content if too long
        content_preview = content[:100] + "..." if len(content) > 100 else content
        
        table.add_row(memory_id, content_preview, category, created_at, user_id)
    
    return Panel(table, title="[bold green]Memories List", border_style="green")


def format_delete_response(memory_id: str) -> Panel:
    """Format delete memory response"""
    
    content = [
        "✅ Memory deleted successfully:",
        f"🔑 Memory ID: {memory_id}",
    ]
    
    return Panel("\n".join(content), title="[bold green]Memory Deleted", border_style="green")