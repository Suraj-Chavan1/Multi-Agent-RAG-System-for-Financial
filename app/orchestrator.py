"""
LangGraph Orchestrator - Central router for Financial RAG System
Routes queries between FinancialAgent (yfinance) and DocumentAgent (RAG) 
based on presence of document_ids
"""

import asyncio
import logging
import os
import uuid
from typing import Dict, Any, List, Optional, Literal, TypedDict, Annotated, Sequence
from dataclasses import dataclass
from datetime import datetime
import operator
import functools

# LangChain and LangGraph imports
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

# Try to import MemorySaver, fallback to simple dict-based memory
try:
    from langgraph.checkpoint.memory import MemorySaver
    MEMORY_AVAILABLE = True
except ImportError:
    try:
        from langgraph.checkpoint import MemorySaver
        MEMORY_AVAILABLE = True
    except ImportError:
        # Simple fallback memory implementation
        class MemorySaver:
            def __init__(self):
                self.memory = {}
            
            def get_state(self, config):
                return None
                
            def put_state(self, config, state):
                pass
        
        MEMORY_AVAILABLE = False

# Import agents from agents folder
from agents.financial_agent import FinancialAgent
from agents.document_agent import DocumentAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# INITIALIZE LLM
# =============================================================================

# Load environment variables for LLM configuration
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in environment variables")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0,
    max_tokens=4000,
    verbose=False,
    google_api_key=GEMINI_API_KEY
)

class LangGraphOrchestrator:
    """
    Central router that decides whether to query yfinance or use RAG based on presence of document_ids
    Uses LangGraph for sophisticated routing and memory management
    """
    
    def __init__(self, llm=None):
        """
        Initialize the orchestrator with LLM and agents
        
        Args:
            llm: Optional LLM instance. If not provided, uses default Gemini
        """
        self.llm = llm or globals()['llm']  # Use provided LLM or global default
        self.rag_agent = DocumentAgent()  # RAG agent for document queries
        self.financial_agent = FinancialAgent()  # Financial agent for yfinance queries
        
        logger.info("LangGraph Orchestrator initialized with agents")
    
    async def answer(
        self,
        question: str,
        symbol: Optional[str] = None,
        report_type: Optional[str] = None,
        document_ids: Optional[List[str]] = None,
        symbol_filter: Optional[str] = None,
        top_k: int = 5,
        thread_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Central routing method that decides which agent to use
        
        Args:
            question: The user's question
            symbol: Stock symbol for financial queries
            report_type: Type of financial report
            document_ids: List of document IDs (triggers RAG if provided)
            symbol_filter: Symbol filter for document search
            top_k: Number of top results for RAG
            thread_id: Thread ID for conversation memory
            user_id: User ID for user-specific memory
            
        Returns:
            tuple[str, str]: The response from the appropriate agent and the route taken
        """
        start_time = datetime.now()
        
        try:
            # Simple routing logic based on original requirement:
            # - If document_ids provided → Use DocumentAgent (RAG)
            # - If no document_ids → Use FinancialAgent (yfinance)
            
            # Check if document_ids are provided and valid
            has_valid_document_ids = document_ids and len(document_ids) > 0 and any(doc_id and doc_id.strip() and doc_id != "string" for doc_id in document_ids)
            
            if has_valid_document_ids:
                logger.info(f"Routing to DocumentAgent (RAG) - document_ids provided: {document_ids}")
                
                # Use DocumentAgent for RAG queries with explicit document IDs
                result = await self.rag_agent.answer(
                    question=question,
                    document_ids=document_ids,
                    top_k=top_k
                )
                
                route_taken = "document_agent_rag"
                
            else:
                logger.info(f"Routing to FinancialAgent (yfinance) - no valid document_ids provided")
                
                # Require symbol for financial queries
                if not symbol:
                    return "Error: 'symbol' is required for financial queries.", "error"
                
                # Use FinancialAgent for yfinance queries
                result = await self.financial_agent.answer(
                    question=question,
                    symbol=symbol,
                    report_type=report_type
                )
                
                route_taken = "financial_agent_yfinance"
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds() * 1000
            
            logger.info(f"Query completed via {route_taken} in {processing_time:.2f}ms")
            
            return result, route_taken
            
        except Exception as e:
            logger.error(f"Error in orchestrator routing: {e}")
            return f"Orchestrator error: {str(e)}", "error"
    
    async def process_query(
        self,
        question: str,
        symbol: str,
        document_ids: Optional[List[str]] = None,
        thread_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a query and return structured response with metadata
        
        Args:
            question: The user's question
            symbol: Stock symbol
            document_ids: Optional document IDs for RAG
            thread_id: Optional thread ID for memory
            user_id: Optional user ID
            
        Returns:
            Dict containing answer, metadata, and routing information
        """
        try:
            # Generate thread_id if not provided
            if thread_id is None:
                thread_id = str(uuid.uuid4())
            
            start_time = datetime.now()
            
            # Route the query and get the actual route taken
            answer, route_taken = await self.answer(
                question=question,
                symbol=symbol,
                document_ids=document_ids,
                thread_id=thread_id,
                user_id=user_id
            )
            
            # Determine agent used based on actual route taken
            if route_taken == "document_agent_rag":
                agent_used = "DocumentAgent"
            elif route_taken == "financial_agent_yfinance":
                agent_used = "FinancialAgent"
            else:
                agent_used = "none"
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds() * 1000
            
            # Return structured response
            return {
                "answer": answer,
                "symbol": symbol.upper(),
                "question": question,
                "route_taken": route_taken,
                "agent_used": agent_used,
                "document_ids_used": document_ids,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "processing_method": "langgraph_orchestrator",
                    "processing_time_ms": processing_time,
                    "thread_id": thread_id,
                    "llm_model": self.llm.model_name if hasattr(self.llm, 'model_name') else "gemini-1.5-flash"
                },
                "success": True,
                "processing_time_ms": processing_time,
                "thread_id": thread_id,
                "user_id": user_id,
                "conversation_history": []
            }
            
        except Exception as e:
            logger.error(f"Error in process_query: {e}")
            return {
                "answer": f"System error occurred: {str(e)}",
                "symbol": symbol,
                "question": question,
                "route_taken": "error",
                "agent_used": "none",
                "document_ids_used": document_ids,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "processing_time_ms": 1.0
                },
                "success": False,
                "processing_time_ms": 1.0,
                "thread_id": thread_id,
                "user_id": user_id,
                "conversation_history": []
            }

# =============================================================================
# GLOBAL ORCHESTRATOR INSTANCE
# =============================================================================

# Global orchestrator instance
orchestrator = None

async def get_orchestrator():
    """Get or create the global orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        orchestrator = LangGraphOrchestrator(llm=llm)
    return orchestrator

# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def process_financial_query(
    question: str,
    symbol: str,
    document_ids: Optional[List[str]] = None,
    thread_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to process queries through the orchestrator
    
    Args:
        question: The user's question
        symbol: Stock symbol
        document_ids: Optional document IDs (triggers RAG if provided)
        thread_id: Optional thread ID for memory
        user_id: Optional user ID
        
    Returns:
        Dict containing the response and metadata
    """
    orch = await get_orchestrator()
    return await orch.process_query(question, symbol, document_ids, thread_id, user_id)

async def get_conversation_history(thread_id: str) -> List[Dict[str, Any]]:
    """
    Convenience function to get conversation history
    """
    # Placeholder for conversation history retrieval
    return []

async def get_conversation_summary(thread_id: str) -> Dict[str, Any]:
    """
    Convenience function to get conversation summary
    """
    # Placeholder for conversation summary
    return {
        "summary": "Conversation summary not implemented in simple orchestrator.",
        "thread_id": thread_id,
        "generated_at": datetime.now().isoformat()
    }

logger.info("LangGraph Orchestrator module loaded successfully")