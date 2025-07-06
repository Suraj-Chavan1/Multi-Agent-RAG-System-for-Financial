import os
import logging
import asyncio
import time
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential
import google.generativeai as genai
from pinecone import Pinecone

# Document processing imports
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid
from datetime import datetime

from google.api_core.exceptions import ResourceExhausted

# ------------------------- Load Environment -------------------------
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash")  # Using flash model for better quota
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")  # Back to 768-dim embedding model

if not all([PINECONE_API_KEY, PINECONE_INDEX_NAME, GEMINI_API_KEY]):
    raise EnvironmentError("Missing required environment variables.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pinecone and Gemini lazily to avoid blocking server startup
pc = None
index = None
_index_verified = False

def get_pinecone_index():
    """Get Pinecone index with lazy initialization"""
    global pc, index, _index_verified
    
    if index is None:
        logger.info("Initializing Pinecone connection...")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
        
        # Verify index dimensions only once
        if not _index_verified:
            try:
                index_stats = index.describe_index_stats()
                if index_stats['dimension'] != 768:
                    logger.warning(f"Index dimension is {index_stats['dimension']} but expected 768. This might cause issues with embeddings.")
                else:
                    logger.info(f"Index dimension verified: {index_stats['dimension']}")
                _index_verified = True
            except Exception as e:
                logger.warning(f"Could not verify index dimensions: {e}")
    
    return index

genai.configure(api_key=GEMINI_API_KEY)

class DocumentAgent:
    def __init__(self):
        self.generation_model = genai.GenerativeModel(model_name=GEMINI_MODEL_NAME)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len
        )

    async def answer(
        self,
        question: str,
        document_ids: Optional[List[str]] = None,
        symbol: Optional[str] = None,
        top_k: int = 5,
    ) -> str:
        try:
            logger.info("Starting RAG answer generation.")
            query_embedding = await self._get_embedding(question)
            
            # Add small delay to avoid rate limiting
            await asyncio.sleep(1)
            
            filter_query = self._build_filter(document_ids, symbol)
            index = get_pinecone_index()
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_query or None,
            )
            if not results.matches:
                logger.warning("No matches found in Pinecone.")
                return "No relevant information found in the transcripts."
            context = self._construct_context(results.matches)
            
            # Try to generate answer with LLM, fallback to raw context if quota exceeded
            try:
                answer = await self._generate_answer(question, context)
                return answer
            except ResourceExhausted:
                logger.warning("LLM quota exceeded, returning raw context")
                return f"Based on the available transcripts:\n\n{context}\n\n(Note: AI processing unavailable due to quota limits)"
        except ResourceExhausted as e:
            logger.error(f"Gemini API quota exceeded: {e}")
            return (
                "You have exceeded your Gemini API quota. "
                "Please wait for your quota to refresh or upgrade your plan. "
                "See: https://ai.google.dev/gemini-api/docs/rate-limits"
            )
        except Exception as e:
            logger.exception(f"Error in DocumentAgent.answer: {e}")
            return f"An error occurred while processing your request: {str(e)}"

    def _build_filter(self, document_ids: Optional[List[str]], symbol: Optional[str]) -> dict:
        """Build filter for Pinecone query. Only uses document_ids, ignores symbol."""
        filters = {}
        if document_ids:
            filters["document_id"] = {"$in": document_ids}
        # Note: symbol is intentionally ignored - DocumentAgent only filters by document_id
        return filters

    def _construct_context(self, matches: List) -> str:
        return "\n\n".join(match.metadata.get("text", "") for match in matches)

    @retry(stop=stop_after_attempt(2), wait=wait_random_exponential(min=2, max=10))  # Reduced retries and longer waits
    async def _get_embedding(self, text: str) -> List[float]:
        logger.info("Generating embedding for the query.")
        response = await asyncio.to_thread(
            genai.embed_content,
            model=GEMINI_EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"  # Changed to retrieval_query for better performance
        )
        return response["embedding"]

    @retry(stop=stop_after_attempt(2), wait=wait_random_exponential(min=2, max=10))  # Reduced retries and longer waits
    async def _generate_answer(self, question: str, context: str) -> str:
        logger.info("Generating response from Gemini.")
        prompt = (
            "You are a financial assistant. Answer the question using ONLY the provided transcript context.\n\n"
            "Context:\n"
            f"{context}\n\n"
            f"Question: {question}\n\n"
            "If the answer is not in the context, say: "
            "'The answer is not available in the provided transcripts.'"
        )
        response = await asyncio.to_thread(self.generation_model.generate_content, prompt)
        return response.text.strip()

    async def upload_document(
        self,
        file_path: str,
        document_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Upload and process a document for RAG
        
        Args:
            file_path: Path to the document file (PDF)
            document_id: Optional custom document ID
            metadata: Optional additional metadata
            
        Returns:
            Dict with upload results and statistics
        """
        try:
            logger.info(f"Starting document upload for file: {file_path}")
            
            # Generate document ID if not provided
            if not document_id:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.basename(file_path).replace('.pdf', '')
                document_id = f"{filename}_{timestamp}_{str(uuid.uuid4())[:8]}"
            
            # Extract text from PDF
            text_content = await self._extract_text_from_pdf(file_path)
            if not text_content.strip():
                return {
                    "success": False,
                    "error": "No text could be extracted from the PDF",
                    "document_id": document_id
                }
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text_content)
            if not chunks:
                return {
                    "success": False,
                    "error": "No chunks created from document text",
                    "document_id": document_id
                }
            
            logger.info(f"Created {len(chunks)} chunks from document")
            
            # Generate embeddings and upload to Pinecone
            upload_results = await self._upload_chunks_to_pinecone(
                chunks=chunks,
                document_id=document_id,
                metadata=metadata or {}
            )
            
            return {
                "success": True,
                "document_id": document_id,
                "chunks_uploaded": len(chunks),
                "file_path": file_path,
                "upload_results": upload_results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            return {
                "success": False,
                "error": str(e),
                "document_id": document_id or "unknown"
            }

    async def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            logger.info(f"Extracting text from PDF: {file_path}")
            
            def extract_pdf_text():
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
            
            # Run PDF extraction in thread to avoid blocking
            text = await asyncio.to_thread(extract_pdf_text)
            logger.info(f"Extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    async def _upload_chunks_to_pinecone(
        self,
        chunks: List[str],
        document_id: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Upload text chunks to Pinecone with embeddings"""
        try:
            logger.info(f"Uploading {len(chunks)} chunks to Pinecone")
            
            vectors = []
            successful_chunks = 0
            failed_chunks = 0
            
            for i, chunk in enumerate(chunks):
                try:
                    # Generate embedding for chunk
                    embedding = await self._get_embedding_for_document(chunk)
                    
                    # Create vector with metadata (no symbol dependency)
                    vector_metadata = {
                        "text": chunk,
                        "document_id": document_id,
                        "chunk_index": i,
                        "chunk_count": len(chunks),
                        "upload_timestamp": datetime.now().isoformat(),
                        **metadata  # Include any additional metadata
                    }
                    
                    vectors.append({
                        "id": f"{document_id}_chunk_{i}",
                        "values": embedding,
                        "metadata": vector_metadata
                    })
                    
                    successful_chunks += 1
                    
                    # Add delay to avoid rate limiting
                    if i > 0 and i % 5 == 0:  # Every 5 chunks
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logger.warning(f"Failed to process chunk {i}: {e}")
                    failed_chunks += 1
                    continue
            
            # Upload vectors to Pinecone in batches
            if vectors:
                batch_size = 100
                upload_results = []
                index = get_pinecone_index()
                
                for i in range(0, len(vectors), batch_size):
                    batch = vectors[i:i + batch_size]
                    try:
                        result = await asyncio.to_thread(index.upsert, vectors=batch)
                        upload_results.append(result)
                        logger.info(f"Uploaded batch {i//batch_size + 1} ({len(batch)} vectors)")
                        
                        # Small delay between batches
                        if i + batch_size < len(vectors):
                            await asyncio.sleep(0.5)
                            
                    except Exception as e:
                        logger.error(f"Failed to upload batch {i//batch_size + 1}: {e}")
                        raise
            
            logger.info(f"Document upload completed. Successful: {successful_chunks}, Failed: {failed_chunks}")
            
            # Create a clean, serializable response
            return {
                "successful_chunks": successful_chunks,
                "failed_chunks": failed_chunks,
                "total_vectors_uploaded": len(vectors),
                "batches_processed": len(upload_results),
                "upload_summary": "Document successfully uploaded to Pinecone"
            }
            
        except Exception as e:
            logger.error(f"Error uploading chunks to Pinecone: {e}")
            raise

    @retry(stop=stop_after_attempt(2), wait=wait_random_exponential(min=2, max=10))
    async def _get_embedding_for_document(self, text: str) -> List[float]:
        """Generate embedding for document chunk"""
        response = await asyncio.to_thread(
            genai.embed_content,
            model=GEMINI_EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"  # Use document task type for indexing
        )
        return response["embedding"]

    async def list_documents(self) -> Dict[str, Any]:
        """List all uploaded documents"""
        try:
            index = get_pinecone_index()
            
            # Get a sample of vectors to find unique documents
            # Use a small non-zero vector instead of all zeros
            query_result = index.query(
                vector=[0.01] * 768,  # Small non-zero value
                top_k=10000,  # Large number to get many results
                include_metadata=True
            )
            
            # Extract unique documents
            documents = {}
            for match in query_result.matches:
                metadata = match.metadata
                doc_id = metadata.get("document_id")
                if doc_id and doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "upload_timestamp": metadata.get("upload_timestamp"),
                        "chunk_count": metadata.get("chunk_count", 0)
                    }
            
            return {
                "success": True,
                "documents": list(documents.values()),
                "total_documents": len(documents)
            }
            
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return {
                "success": False,
                "error": str(e),
                "documents": []
            }

    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a document and all its chunks from Pinecone"""
        try:
            logger.info(f"Deleting document: {document_id}")
            index = get_pinecone_index()
            
            # Find all vectors for this document
            query_result = index.query(
                vector=[0.01] * 768,  # Small non-zero value
                top_k=10000,
                include_metadata=True,
                filter={"document_id": document_id}
            )
            
            if not query_result.matches:
                return {
                    "success": False,
                    "error": f"No document found with ID: {document_id}"
                }
            
            # Extract vector IDs to delete
            vector_ids = [match.id for match in query_result.matches]
            
            # Delete vectors in batches
            batch_size = 1000
            deleted_count = 0
            
            for i in range(0, len(vector_ids), batch_size):
                batch_ids = vector_ids[i:i + batch_size]
                await asyncio.to_thread(index.delete, ids=batch_ids)
                deleted_count += len(batch_ids)
                logger.info(f"Deleted batch {i//batch_size + 1} ({len(batch_ids)} vectors)")
            
            return {
                "success": True,
                "document_id": document_id,
                "deleted_vectors": deleted_count,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return {
                "success": False,
                "error": str(e),
                "document_id": document_id
            }