#!/usr/bin/env python3
"""Quick start script for the backend server"""

import os
import sys
import subprocess

def check_requirements():
    """Check if requirements are installed"""
    try:
        import fastapi
        import groq
        import azure.cognitiveservices.speech
        print("✅ All requirements installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_env():
    """Check if environment variables are set"""
    required_vars = ["GROQ_API_KEY", "AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]
    missing = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("Copy env.example to .env and fill in your API keys")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main function to start the server"""
    print("🚀 Starting Vidya AI Backend Server...")
    
    if not check_requirements():
        sys.exit(1)
    
    if not check_env():
        sys.exit(1)
    
    # Create directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    
    print("🌐 Server starting at http://localhost:8000")
    print("📚 API docs available at http://localhost:8000/docs")
    
    # Start the server
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
