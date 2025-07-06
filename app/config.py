"""
Configuration module for the Financial RAG System
Handles environment variable loading and validation
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Configuration class with environment variable validation"""
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "financial-rag-768")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are present"""
        required_vars = {
            "PINECONE_API_KEY": cls.PINECONE_API_KEY,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise EnvironmentError(error_msg)
        
        logger.info("All required environment variables are present")
        return True
    
    @classmethod
    def log_config(cls):
        """Log configuration status (without exposing sensitive data)"""
        logger.info("Configuration loaded:")
        logger.info(f"  PINECONE_INDEX_NAME: {cls.PINECONE_INDEX_NAME}")
        logger.info(f"  PINECONE_ENVIRONMENT: {cls.PINECONE_ENVIRONMENT}")
        logger.info(f"  GEMINI_MODEL_NAME: {cls.GEMINI_MODEL_NAME}")
        logger.info(f"  GEMINI_EMBEDDING_MODEL: {cls.GEMINI_EMBEDDING_MODEL}")
        logger.info(f"  PINECONE_API_KEY: {'✓ Set' if cls.PINECONE_API_KEY else '✗ Missing'}")
        logger.info(f"  GEMINI_API_KEY: {'✓ Set' if cls.GEMINI_API_KEY else '✗ Missing'}")

# Validate configuration on import
try:
    Config.validate()
    Config.log_config()
except EnvironmentError as e:
    logger.error(f"Configuration validation failed: {e}")
    # Don't raise here to allow for graceful handling in production
