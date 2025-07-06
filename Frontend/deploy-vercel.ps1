# Frontend Vercel Deployment Script
# Run this script from the Frontend directory

Write-Host "🚀 Starting Frontend Deployment to Vercel..." -ForegroundColor Green

# Check if we're in the Frontend directory
if (!(Test-Path "package.json")) {
    Write-Host "❌ Error: Please run this script from the Frontend directory" -ForegroundColor Red
    Write-Host "📁 Navigate to: cd Frontend" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found package.json - proceeding with deployment" -ForegroundColor Green

# Check if Vercel CLI is installed
try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
}

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

# Login to Vercel (if not already logged in)
Write-Host "🔐 Checking Vercel authentication..." -ForegroundColor Yellow
try {
    vercel whoami
} catch {
    vercel login
}

# Get backend URL from user
Write-Host "🔧 Setting up environment variables..." -ForegroundColor Yellow
$BACKEND_URL = Read-Host "Enter your backend API URL (e.g., https://your-backend.vercel.app)"

if ($BACKEND_URL) {
    Write-Host "📝 Setting VITE_API_URL environment variable..." -ForegroundColor Yellow
    echo $BACKEND_URL | vercel env add VITE_API_URL production
}

# Deploy to Vercel
Write-Host "🌐 Deploying to Vercel..." -ForegroundColor Green
vercel --prod

Write-Host "✅ Frontend deployment complete!" -ForegroundColor Green
Write-Host "🔗 Your frontend will be available at the URL provided by Vercel" -ForegroundColor Cyan
Write-Host "📊 Make sure to update your backend CORS settings to include the frontend URL" -ForegroundColor Yellow
