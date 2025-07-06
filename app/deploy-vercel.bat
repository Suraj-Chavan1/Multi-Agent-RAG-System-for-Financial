@echo off
echo 🚀 Vercel Deployment for Financial RAG System
echo.

REM Check if we're in the app directory
if not exist "main.py" (
    echo ❌ Error: Please run this script from the app directory
    echo 📁 Navigate to the app folder first
    pause
    exit /b 1
)

echo ✅ Found main.py - proceeding with deployment
echo.

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
) else (
    echo ✅ Vercel CLI found
)
echo.

echo 🔐 Logging into Vercel...
vercel login
echo.

echo 🌐 Deploying to Vercel...
vercel --prod
echo.

echo ✅ Deployment complete!
echo 🔗 Your API will be available at the URL provided by Vercel
echo.
echo 📊 Remember to set your environment variables in Vercel dashboard:
echo   - PINECONE_API_KEY
echo   - PINECONE_INDEX_NAME
echo   - PINECONE_ENVIRONMENT  
echo   - GEMINI_API_KEY
echo   - GEMINI_MODEL_NAME
echo   - GEMINI_EMBEDDING_MODEL
echo.
echo 🌐 Test your deployment:
echo   - GET https://your-app.vercel.app/health
echo   - GET https://your-app.vercel.app/
echo.
pause
