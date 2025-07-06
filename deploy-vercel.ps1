# Vercel Deployment Script for Windows PowerShell
# Run this script from the project root directory

Write-Host "🚀 Starting Vercel Deployment Process..." -ForegroundColor Green

# Check if Vercel CLI is installed
try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
}

# Login to Vercel (if not already logged in)
Write-Host "🔐 Checking Vercel authentication..." -ForegroundColor Yellow
try {
    vercel whoami
} catch {
    vercel login
}

# Get environment variables from user
Write-Host "🔧 Setting up environment variables..." -ForegroundColor Yellow
Write-Host "You'll be prompted to enter your API keys:" -ForegroundColor Cyan

$PINECONE_API_KEY = Read-Host "Enter PINECONE_API_KEY"
$PINECONE_INDEX_NAME = Read-Host "Enter PINECONE_INDEX_NAME (default: financial-rag-768)"
if ([string]::IsNullOrWhiteSpace($PINECONE_INDEX_NAME)) { $PINECONE_INDEX_NAME = "financial-rag-768" }

$PINECONE_ENVIRONMENT = Read-Host "Enter PINECONE_ENVIRONMENT (default: us-east-1)"
if ([string]::IsNullOrWhiteSpace($PINECONE_ENVIRONMENT)) { $PINECONE_ENVIRONMENT = "us-east-1" }

$GEMINI_API_KEY = Read-Host "Enter GEMINI_API_KEY"

$GEMINI_MODEL_NAME = Read-Host "Enter GEMINI_MODEL_NAME (default: gemini-2.5-flash)"
if ([string]::IsNullOrWhiteSpace($GEMINI_MODEL_NAME)) { $GEMINI_MODEL_NAME = "gemini-2.5-flash" }

$GEMINI_EMBEDDING_MODEL = Read-Host "Enter GEMINI_EMBEDDING_MODEL (default: models/embedding-001)"
if ([string]::IsNullOrWhiteSpace($GEMINI_EMBEDDING_MODEL)) { $GEMINI_EMBEDDING_MODEL = "models/embedding-001" }

# Set environment variables in Vercel
Write-Host "📝 Adding environment variables to Vercel..." -ForegroundColor Yellow
echo $PINECONE_API_KEY | vercel env add PINECONE_API_KEY production
echo $PINECONE_INDEX_NAME | vercel env add PINECONE_INDEX_NAME production
echo $PINECONE_ENVIRONMENT | vercel env add PINECONE_ENVIRONMENT production
echo $GEMINI_API_KEY | vercel env add GEMINI_API_KEY production
echo $GEMINI_MODEL_NAME | vercel env add GEMINI_MODEL_NAME production
echo $GEMINI_EMBEDDING_MODEL | vercel env add GEMINI_EMBEDDING_MODEL production

# Deploy to Vercel
Write-Host "🌐 Deploying to Vercel..." -ForegroundColor Green
vercel --prod

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🔗 Your API will be available at the URL provided by Vercel" -ForegroundColor Cyan
Write-Host "📊 Test your deployment with:" -ForegroundColor Cyan
Write-Host "   - GET https://your-app.vercel.app/health" -ForegroundColor White
Write-Host "   - GET https://your-app.vercel.app/" -ForegroundColor White
