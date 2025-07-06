"""
Test script for DocumentAgent RAG PDF upload and question answering.

Usage:
    1. Place a test PDF file in the same directory or supply the path.
    2. Set your .env variables for Pinecone and Gemini as required.
    3. Run: python test_document_agent.py
"""

import asyncio
import os
from document_agent import DocumentAgent  # Adjust import path as needed

TEST_PDF_PATH = "q4fy25-earnings-call-transcript.pdf"  # Path to your test PDF file
TEST_QUESTION = "What are the main financial highlights mentioned in this document?"

async def main():
    agent = DocumentAgent()

    # Upload PDF (no symbol required)
    print(f"Uploading PDF: {TEST_PDF_PATH}")
    upload_result = await agent.upload_document(
        file_path=TEST_PDF_PATH,
        metadata={
            "test_upload": True,
            "description": "Test PDF upload via DocumentAgent"
        }
    )
    print("Upload Result:", upload_result)

    if not upload_result.get("success"):
        print(f"Upload failed: {upload_result.get('error')}")
        return

    document_id = upload_result.get("document_id")
    print(f"Document ID: {document_id}")

    # Ask a question using RAG (only document_ids matter)
    print(f"\nAsking question: {TEST_QUESTION}")
    answer = await agent.answer(
        question=TEST_QUESTION,
        document_ids=[document_id],
        top_k=5
    )
    print(f"RAG Answer:\n{answer}")

if __name__ == "__main__":
    asyncio.run(main())