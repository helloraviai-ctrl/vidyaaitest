# Hugging Face Spaces Deployment Guide for Vidya AI

This guide will help you deploy both the frontend and backend of Vidya AI to Hugging Face Spaces.

## Prerequisites

- ✅ Hugging Face account: [https://huggingface.co/helloraviai](https://huggingface.co/helloraviai)
- ✅ API keys for AI services (Groq, Azure Speech, etc.)
- ✅ Git repository with your code

## Deployment Overview

You'll create **two separate Hugging Face Spaces**:
1. **Backend Space**: Docker-based FastAPI service
2. **Frontend Space**: Static Next.js application

## Step 1: Deploy Backend to Hugging Face Spaces

### 1.1 Create Backend Space

1. **Go to [Hugging Face Spaces](https://huggingface.co/spaces)**
2. **Click "Create new Space"**
3. **Configure the Space:**
   - **Space name**: `vidyaai-backend` (or your preferred name)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU Basic (free) or upgrade if needed
   - **Visibility**: Public

### 1.2 Upload Backend Code

**Option A: Git Integration (Recommended)**
1. **Connect your GitHub repository**
2. **Set the path to**: `backend/`
3. **Enable auto-deploy from main branch**

**Option B: Manual Upload**
1. **Upload these files to your Space:**
   - `backend/main.py`
   - `backend/app.py`
   - `backend/requirements.txt`
   - `backend/Dockerfile`
   - `backend/README.md`
   - `backend/models/` (entire folder)
   - `backend/services/` (entire folder)

### 1.3 Set Environment Variables

In your backend Space settings, add these environment variables:

```
GROQ_API_KEY=your_groq_api_key_here
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
AZURE_VOICE_NAME=en-US-AriaNeural
OPENAI_API_KEY=your_openai_api_key_here (optional)
STABILITY_API_KEY=your_stability_api_key_here (optional)
```

### 1.4 Deploy Backend

1. **Click "Deploy"** in your Space
2. **Wait for deployment to complete** (5-10 minutes)
3. **Note your backend URL**: `https://helloraviai-vidyaai-backend.hf.space`

## Step 2: Deploy Frontend to Hugging Face Spaces

### 2.1 Create Frontend Space

1. **Go to [Hugging Face Spaces](https://huggingface.co/spaces)**
2. **Click "Create new Space"**
3. **Configure the Space:**
   - **Space name**: `vidyaai-frontend` (or your preferred name)
   - **License**: MIT
   - **SDK**: Static
   - **Visibility**: Public

### 2.2 Upload Frontend Code

**Option A: Git Integration (Recommended)**
1. **Connect your GitHub repository**
2. **Set the path to**: `/` (root)
3. **Enable auto-deploy from main branch**

**Option B: Manual Upload**
1. **Build the frontend locally:**
   ```bash
   npm install
   npm run build
   ```
2. **Upload the `out/` folder contents** to your Space

### 2.3 Set Environment Variables

In your frontend Space settings, add:

```
NEXT_PUBLIC_API_URL=https://helloraviai-vidyaai-backend.hf.space
```

### 2.4 Deploy Frontend

1. **Click "Deploy"** in your Space
2. **Wait for deployment to complete** (2-5 minutes)
3. **Note your frontend URL**: `https://helloraviai-vidyaai-frontend.hf.space`

## Step 3: Update Backend CORS (if needed)

If you encounter CORS issues, update the backend CORS configuration:

1. **Go to your backend Space**
2. **Edit `main.py`**
3. **Update the CORS origins** to include your frontend URL:
   ```python
   allow_origins=[
       "*",  # Allow all origins for Hugging Face Spaces
       "https://*.hf.space",
       "https://*.huggingface.co",
       "https://helloraviai-vidyaai-frontend.hf.space"
   ],
   ```
4. **Redeploy the backend**

## Step 4: Test Your Deployment

### 4.1 Test Backend
1. **Visit your backend URL**: `https://helloraviai-vidyaai-backend.hf.space`
2. **You should see**: `{"message":"Vidya AI Educational Content Generator API","status":"healthy"}`

### 4.2 Test Frontend
1. **Visit your frontend URL**: `https://helloraviai-vidyaai-frontend.hf.space`
2. **Enter a topic** (e.g., "Photosynthesis")
3. **Click "Create & Play Educational Video"**
4. **Check if the API call works**

### 4.3 Debug Issues
1. **Open browser developer tools (F12)**
2. **Check Console tab** for errors
3. **Check Network tab** for API calls
4. **Use the test page**: `/test` for detailed debugging

## Step 5: Customize Your Spaces

### 5.1 Update Space Descriptions
- **Backend**: "AI-powered backend for educational content generation"
- **Frontend**: "Beautiful frontend for Vidya AI educational videos"

### 5.2 Add Tags
- `education`
- `ai`
- `video-generation`
- `fastapi`
- `nextjs`

### 5.3 Update README Files
- Customize the README files in both Spaces
- Add usage examples
- Include API documentation

## Step 6: Monitor and Maintain

### 6.1 Monitor Performance
- Check Space logs for errors
- Monitor API response times
- Track usage statistics

### 6.2 Update Dependencies
- Regularly update Python packages
- Update Node.js dependencies
- Monitor for security updates

### 6.3 Scale if Needed
- Upgrade to higher hardware tiers if needed
- Consider caching strategies
- Optimize for performance

## Troubleshooting

### Common Issues

**Issue**: Backend not starting
**Solution**: Check Docker logs, verify environment variables

**Issue**: CORS errors
**Solution**: Update CORS configuration in backend

**Issue**: Frontend not loading
**Solution**: Check static file paths, verify build output

**Issue**: API calls failing
**Solution**: Verify backend URL, check network connectivity

### Getting Help

1. **Check Hugging Face Spaces documentation**
2. **Review Space logs for errors**
3. **Test API endpoints directly**
4. **Use browser developer tools for debugging**

## URLs After Deployment

- **Backend**: `https://helloraviai-vidyaai-backend.hf.space`
- **Frontend**: `https://helloraviai-vidyaai-frontend.hf.space`
- **Your Profile**: [https://huggingface.co/helloraviai](https://huggingface.co/helloraviai)

## Next Steps

After successful deployment:
1. **Share your Spaces** with the community
2. **Add to your Hugging Face profile**
3. **Create documentation** and examples
4. **Monitor usage** and gather feedback
5. **Iterate and improve** based on user feedback

Your Vidya AI app will now be live on Hugging Face Spaces! 🚀
