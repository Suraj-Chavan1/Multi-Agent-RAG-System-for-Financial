"""
Simplified FastAPI application for Financial RAG System
Single endpoint with document upload functionality
"""

import logging
import shutil
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import and validate configuration
try:
    from config import Config
    Config.validate()
except EnvironmentError as e:
    logging.error(f"Configuration error: {e}")
    # Allow app to start but log the error

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

# Remove this heavy import from startup
# from orchestrator import process_financial_query

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# FastAPI app instance
app = FastAPI(
    title="Financial RAG System",
    description="Simple system that routes between Financial and Document agents",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QueryRequest(BaseModel):
    question: str
    symbol: str = "AAPL"
    document_ids: Optional[List[str]] = None

class QueryResponse(BaseModel):
    answer: str
    route_taken: str
    success: bool

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Financial RAG System",
        "endpoints": {
            "query": "POST /query",
            "upload": "POST /upload", 
            "documents": "GET /documents",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check with environment validation"""
    try:
        from config import Config
        Config.validate()
        return {
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "environment": "configured"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "environment": "misconfigured"
        }

@app.get("/config-check")
async def config_check():
    """Check configuration status (for debugging)"""
    import os
    return {
        "pinecone_api_key": "✓ Set" if os.getenv("PINECONE_API_KEY") else "✗ Missing",
        "gemini_api_key": "✓ Set" if os.getenv("GEMINI_API_KEY") else "✗ Missing",
        "pinecone_index": os.getenv("PINECONE_INDEX_NAME", "Not set"),
        "gemini_model": os.getenv("GEMINI_MODEL_NAME", "Not set"),
    }

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Main query endpoint - routes between Financial and Document agents
    """
    try:
        logger.info(f"Query: {request.question[:50]}... | Symbol: {request.symbol} | Documents: {request.document_ids}")
        
        # Lazy import - only import when needed
        from orchestrator import process_financial_query
        
        # Route through orchestrator
        result = await process_financial_query(
            question=request.question,
            symbol=request.symbol,
            document_ids=request.document_ids
        )
        
        return QueryResponse(
            answer=result["answer"],
            route_taken=result["route_taken"],
            success=result["success"]
        )
        
    except Exception as e:
        logger.error(f"Query error: {e}")
        return QueryResponse(
            answer=f"Error: {str(e)}",
            route_taken="error",
            success=False
        )

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    """Upload PDF document"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(400, "Only PDF files supported")
        
        # Save file temporarily
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = UPLOAD_DIR / f"{timestamp}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Lazy import - only import when needed
        from agents.document_agent import DocumentAgent
        agent = DocumentAgent()
        result = await agent.upload_document(
            file_path=str(file_path)
        )
        
        # Clean up
        file_path.unlink()
        
        return {
            "success": result["success"],
            "document_id": result["document_id"],
            "message": "Document uploaded successfully"
        }
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(500, f"Upload failed: {e}")

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        # Lazy import - only import when needed
        from agents.document_agent import DocumentAgent
        agent = DocumentAgent()
        result = await agent.list_documents()
        return result
    except Exception as e:
        logger.error(f"List documents error: {e}")
        return {"success": False, "error": str(e), "documents": []}


# Vercel serverless handler
def handler(event, context):
    return app

# For Vercel compatibility
app_instance = app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)