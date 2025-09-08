#!/bin/bash

# Vidya AI Auto-Deploy Script for Hugging Face Spaces
# This script helps with manual deployment to Hugging Face Spaces

set -e

echo "🚀 Vidya AI Deployment Script"
echo "=============================="

# Check if HF_TOKEN is set
if [ -z "$HF_TOKEN" ]; then
    echo "❌ Error: HF_TOKEN environment variable is not set"
    echo "Please set your Hugging Face token:"
    echo "export HF_TOKEN=your_huggingface_token_here"
    exit 1
fi

# Function to deploy backend
deploy_backend() {
    echo "📦 Deploying Backend to Hugging Face Spaces..."
    
    # Check if backend directory exists
    if [ ! -d "backend" ]; then
        echo "❌ Error: backend directory not found"
        exit 1
    fi
    
    # Install Python dependencies
    echo "📥 Installing Python dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..
    
    # Deploy to Hugging Face
    echo "🚀 Uploading backend to Hugging Face Spaces..."
    python -c "
from huggingface_hub import HfApi
import os
api = HfApi(token=os.getenv('HF_TOKEN'))
api.upload_folder(
    folder_path='./backend',
    repo_id='helloraviai/vidyaai-backend',
    repo_type='space',
    commit_message='Manual deployment from script'
)
print('✅ Backend deployed successfully!')
"
}

# Function to deploy frontend
deploy_frontend() {
    echo "📦 Deploying Frontend to Hugging Face Spaces..."
    
    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        echo "❌ Error: package.json not found"
        exit 1
    fi
    
    # Install Node.js dependencies
    echo "📥 Installing Node.js dependencies..."
    npm install
    
    # Build frontend
    echo "🔨 Building frontend..."
    NEXT_PUBLIC_API_URL=https://helloraviai-vidyaai-backend.hf.space npm run build
    
    # Check if build was successful
    if [ ! -d "out" ]; then
        echo "❌ Error: Build failed - out directory not found"
        exit 1
    fi
    
    # Deploy to Hugging Face
    echo "🚀 Uploading frontend to Hugging Face Spaces..."
    python -c "
from huggingface_hub import HfApi
import os
api = HfApi(token=os.getenv('HF_TOKEN'))
api.upload_folder(
    folder_path='./out',
    repo_id='helloraviai/vidyaai-frontend',
    repo_type='space',
    commit_message='Manual deployment from script'
)
print('✅ Frontend deployed successfully!')
"
}

# Function to deploy both
deploy_all() {
    echo "🚀 Deploying Both Backend and Frontend..."
    deploy_backend
    deploy_frontend
    echo "🎉 All deployments completed successfully!"
    echo ""
    echo "Your apps are now live at:"
    echo "Backend:  https://helloraviai-vidyaai-backend.hf.space"
    echo "Frontend: https://helloraviai-vidyaai-frontend.hf.space"
}

# Main script logic
case "${1:-all}" in
    "backend")
        deploy_backend
        ;;
    "frontend")
        deploy_frontend
        ;;
    "all")
        deploy_all
        ;;
    *)
        echo "Usage: $0 [backend|frontend|all]"
        echo ""
        echo "Options:"
        echo "  backend  - Deploy only the backend"
        echo "  frontend - Deploy only the frontend"
        echo "  all      - Deploy both (default)"
        echo ""
        echo "Make sure to set your HF_TOKEN environment variable:"
        echo "export HF_TOKEN=your_huggingface_token_here"
        exit 1
        ;;
esac
