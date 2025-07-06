#!/bin/bash

# Vercel Deployment Script for Multi-Agent RAG System
# Run this script from the project root directory

echo "🚀 Starting Vercel Deployment Process..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
else
    echo "✅ Vercel CLI found"
fi

# Login to Vercel (if not already logged in)
echo "🔐 Checking Vercel authentication..."
vercel whoami || vercel login

# Set environment variables (you'll be prompted for values)
echo "🔧 Setting up environment variables..."
echo "You'll be prompted to enter your API keys:"

read -p "Enter PINECONE_API_KEY: " PINECONE_API_KEY
read -p "Enter PINECONE_INDEX_NAME (default: financial-rag-768): " PINECONE_INDEX_NAME
PINECONE_INDEX_NAME=${PINECONE_INDEX_NAME:-financial-rag-768}
read -p "Enter PINECONE_ENVIRONMENT (default: us-east-1): " PINECONE_ENVIRONMENT
PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT:-us-east-1}
read -p "Enter GEMINI_API_KEY: " GEMINI_API_KEY
read -p "Enter GEMINI_MODEL_NAME (default: gemini-2.5-flash): " GEMINI_MODEL_NAME
GEMINI_MODEL_NAME=${GEMINI_MODEL_NAME:-gemini-2.5-flash}
read -p "Enter GEMINI_EMBEDDING_MODEL (default: models/embedding-001): " GEMINI_EMBEDDING_MODEL
GEMINI_EMBEDDING_MODEL=${GEMINI_EMBEDDING_MODEL:-models/embedding-001}

# Set environment variables in Vercel
echo "📝 Adding environment variables to Vercel..."
echo "$PINECONE_API_KEY" | vercel env add PINECONE_API_KEY production
echo "$PINECONE_INDEX_NAME" | vercel env add PINECONE_INDEX_NAME production
echo "$PINECONE_ENVIRONMENT" | vercel env add PINECONE_ENVIRONMENT production
echo "$GEMINI_API_KEY" | vercel env add GEMINI_API_KEY production
echo "$GEMINI_MODEL_NAME" | vercel env add GEMINI_MODEL_NAME production
echo "$GEMINI_EMBEDDING_MODEL" | vercel env add GEMINI_EMBEDDING_MODEL production

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Your API will be available at the URL provided by Vercel"
echo "📊 Test your deployment with:"
echo "   - GET https://your-app.vercel.app/health"
echo "   - GET https://your-app.vercel.app/"
