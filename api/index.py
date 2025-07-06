import sys
import os
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(app_dir))

# Import the FastAPI app
from main import app

# Vercel expects this function signature
def handler(event, context):
    return app

# Export app for Vercel
application = app
