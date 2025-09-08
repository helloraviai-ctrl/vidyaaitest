"""
Hugging Face Spaces deployment entry point for Vidya AI Backend
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import and run the FastAPI app
from main import app

if __name__ == "__main__":
    import uvicorn
    
    # Create necessary directories
    os.makedirs("./uploads", exist_ok=True)
    os.makedirs("./outputs", exist_ok=True)
    os.makedirs("./temp", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=7860,  # Hugging Face Spaces default port
        reload=False
    )
