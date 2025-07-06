# 🚀 App-Only Vercel Deployment Guide

This guide focuses on deploying only the `app` folder as a standalone Vercel project.

## 📁 Project Structure for Deployment

```
app/
├── vercel.json              # ✅ Vercel configuration
├── .vercelignore           # ✅ Files to exclude
├── requirements.txt        # ✅ Python dependencies
├── main.py                 # ✅ FastAPI application (modified for Vercel)
├── orchestrator.py         # ✅ Core orchestrator
├── deploy-vercel.ps1       # ✅ Deployment script
├── agents/
│   ├── document_agent.py   # ✅ Document processing agent
│   └── financial_agent.py  # ✅ Financial data agent
└── .env                    # ❌ Local only (excluded from deployment)
```

## 🚀 Quick Deployment Steps

### Method 1: Using the Deployment Script

1. **Navigate to the app folder:**
   ```powershell
   cd "d:\Backend\Test_Shit\Multi-Agent-RAG-System-for-Financial\app"
   ```

2. **Run the deployment script:**
   ```powershell
   .\deploy-vercel.ps1
   ```

### Method 2: Manual Deployment

1. **Install Vercel CLI:**
   ```powershell
   npm install -g vercel
   ```

2. **Navigate to app folder:**
   ```powershell
   cd "d:\Backend\Test_Shit\Multi-Agent-RAG-System-for-Financial\app"
   ```

3. **Login to Vercel:**
   ```powershell
   vercel login
   ```

4. **Deploy:**
   ```powershell
   vercel --prod
   ```

5. **Set environment variables (one-time setup):**
   ```powershell
   vercel env add PINECONE_API_KEY production
   vercel env add PINECONE_INDEX_NAME production
   vercel env add PINECONE_ENVIRONMENT production
   vercel env add GEMINI_API_KEY production
   vercel env add GEMINI_MODEL_NAME production
   vercel env add GEMINI_EMBEDDING_MODEL production
   ```

## 🔧 Configuration Details

### vercel.json Features:
- **Direct main.py routing**: No API wrapper needed
- **CORS enabled**: Frontend can connect from any domain
- **30-second timeout**: Suitable for AI processing
- **1GB memory**: Handles document processing
- **Environment variables**: Secure API key storage

### Key Modifications Made:
1. **main.py**: Added Vercel handler function
2. **Simplified routing**: Direct FastAPI deployment
3. **Excluded files**: .env, uploads/, __pycache__/
4. **Production ready**: Optimized for serverless

## 📊 API Endpoints

After deployment, your API will have these endpoints:

- `GET /` - Root endpoint with API documentation
- `GET /health` - Health check
- `POST /query` - Main query processing
- `POST /upload` - Document upload
- `GET /documents` - List uploaded documents

## 🌐 Testing Your Deployment

```bash
# Health check
curl https://your-app.vercel.app/health

# Query example
curl -X POST https://your-app.vercel.app/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AAPL stock price?", "symbol": "AAPL"}'
```

## ⚙️ Environment Variables Required

Set these in Vercel dashboard or via CLI:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=financial-rag-768
PINECONE_ENVIRONMENT=us-east-1
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL_NAME=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=models/embedding-001
```

## 🔍 Troubleshooting

### Common Issues:
1. **Import errors**: All dependencies in requirements.txt
2. **Environment variables**: Check they're set in Vercel
3. **File uploads**: Limited to 4.5MB on hobby plan
4. **Cold starts**: First request may be slow

### Debug Commands:
```powershell
# View logs
vercel logs

# Check environment variables
vercel env ls

# Redeploy
vercel --prod
```

## 📈 Production Considerations

1. **File Storage**: Use cloud storage (AWS S3, Google Cloud) instead of local uploads
2. **Database**: Consider managed vector database
3. **Monitoring**: Set up error tracking
4. **Rate Limiting**: Add API rate limiting
5. **Caching**: Implement response caching

## 🎯 Next Steps

1. Deploy the app folder
2. Test all endpoints
3. Update frontend to use new API URL
4. Set up custom domain (optional)
5. Monitor performance and usage
