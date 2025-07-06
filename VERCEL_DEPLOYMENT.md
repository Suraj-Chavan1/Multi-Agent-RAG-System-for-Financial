# 🚀 Vercel Deployment Guide for Multi-Agent RAG System

This guide will help you deploy your Multi-Agent RAG System backend on Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally
   ```powershell
   npm install -g vercel
   ```
3. **Environment Variables**: Have your API keys ready

## 🔧 Setup Steps

### 1. Install Vercel CLI and Login
```powershell
# Install Vercel CLI
npm install -g vercel

# Login to your Vercel account
vercel login
```

### 2. Configure Environment Variables
In your Vercel dashboard or via CLI, set these environment variables:

```bash
# Required Environment Variables
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=financial-rag-768
PINECONE_ENVIRONMENT=us-east-1
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_NAME=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=models/embedding-001
```

### 3. Deploy to Vercel

From your project root directory:

```powershell
# Navigate to project root
cd "d:\Backend\Test_Shit\Multi-Agent-RAG-System-for-Financial"

# Deploy to Vercel
vercel --prod
```

### 4. Set Environment Variables via CLI (Alternative)
```powershell
# Set environment variables via Vercel CLI
vercel env add PINECONE_API_KEY
vercel env add PINECONE_INDEX_NAME
vercel env add PINECONE_ENVIRONMENT
vercel env add GEMINI_API_KEY
vercel env add GEMINI_MODEL_NAME
vercel env add GEMINI_EMBEDDING_MODEL

# Redeploy after setting environment variables
vercel --prod
```

## 📁 File Structure for Vercel

```
Multi-Agent-RAG-System-for-Financial/
├── vercel.json                 # ✅ Vercel configuration
├── requirements.txt            # ✅ Python dependencies (root level)
├── api/
│   └── index.py               # ✅ Vercel entry point
├── app/
│   ├── main.py                # ✅ Modified FastAPI app
│   ├── orchestrator.py
│   ├── requirements.txt       # Original requirements
│   ├── .env                   # Local development only
│   └── agents/
│       ├── document_agent.py
│       └── financial_agent.py
└── Frontend/                  # Deploy separately
```

## 🌐 Vercel Configuration Details

### vercel.json
- Routes all requests to the FastAPI application
- Sets up serverless function with 30-second timeout
- Configures environment variables

### API Entry Point (api/index.py)
- Vercel-compatible handler for FastAPI
- Imports your main FastAPI application

## 🔍 Testing Your Deployment

Once deployed, test these endpoints:

```bash
# Health check
GET https://your-app.vercel.app/health

# Root endpoint
GET https://your-app.vercel.app/

# Upload document
POST https://your-app.vercel.app/upload

# Query endpoint
POST https://your-app.vercel.app/query
```

## 📊 Deployment Commands Summary

```powershell
# Step 1: Install and login to Vercel
npm install -g vercel
vercel login

# Step 2: Deploy from project root
cd "d:\Backend\Test_Shit\Multi-Agent-RAG-System-for-Financial"
vercel --prod

# Step 3: Set environment variables (if not set in dashboard)
vercel env add PINECONE_API_KEY
vercel env add GEMINI_API_KEY
# ... (add all required env vars)

# Step 4: Redeploy after env setup
vercel --prod
```

## ⚠️ Important Notes

1. **File Uploads**: Vercel has limitations on file uploads in serverless functions
2. **Function Timeout**: Maximum 30 seconds for hobby plan
3. **Cold Starts**: First request may be slower due to cold starts
4. **Memory Limits**: 1024MB for hobby plan
5. **Environment Variables**: Never commit .env files to version control

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure all dependencies are in root `requirements.txt`
2. **Timeout Issues**: Large file processing may timeout (consider background processing)
3. **Environment Variables**: Double-check all required env vars are set
4. **API Limits**: Monitor Gemini and Pinecone API usage

### Debug Commands:
```powershell
# Check deployment logs
vercel logs

# Check environment variables
vercel env ls

# Remove deployment
vercel remove
```

## 🎯 Next Steps

1. Deploy and test the backend
2. Update Frontend configuration to point to Vercel backend URL
3. Deploy Frontend separately (Vercel/Netlify)
4. Set up custom domain (optional)
5. Monitor performance and usage

## 📈 Production Considerations

1. **Upgrade Vercel Plan**: For higher limits and better performance
2. **Database**: Consider managed database for production
3. **Monitoring**: Set up error tracking and monitoring
4. **Caching**: Implement caching for better performance
5. **Rate Limiting**: Add rate limiting for API protection
