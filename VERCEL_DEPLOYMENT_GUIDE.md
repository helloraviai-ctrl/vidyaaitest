# Vercel Deployment Guide for Vidya AI (Full Stack)

This guide will help you deploy both frontend and backend to Vercel using serverless functions.

## Prerequisites

- ✅ Vercel account (free tier available)
- ✅ GitHub repository with your code
- ✅ API keys for AI services (Groq, Azure Speech)

## Architecture

- **Frontend**: Next.js app deployed on Vercel
- **Backend**: Vercel serverless functions (API routes)
- **AI Services**: Groq AI, Azure Speech Services
- **File Storage**: Temporary files in serverless functions

## Quick Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Import your repository**: `helloraviai-ctrl/vidyaaitest`
5. **Configure project:**
   - **Framework Preset**: Next.js
   - **Root Directory**: `./` (root)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next` (default)
6. **Add Environment Variables:**
   ```
   GROQ_API_KEY=your_groq_api_key
   AZURE_SPEECH_KEY=your_azure_speech_key
   AZURE_SPEECH_REGION=your_azure_region
   ```
7. **Click "Deploy"**

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (your account)
# - Link to existing project? N
# - Project name: vidya-ai-app
# - Directory: ./
# - Override settings? N
```

## Environment Variables

Set these in your Vercel project settings:

### Required
```
GROQ_API_KEY=your_groq_api_key
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region
```

### Optional
```
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_api_key
NEXT_PUBLIC_GA_ID=your-google-analytics-id
```

## API Routes

Your app includes these serverless functions:

- **`/api/health`** - Health check endpoint
- **`/api/generate-content`** - Generate educational content
- **`/api/status/[job_id]`** - Check processing status
- **`/api/download/[job_id]/[file_type]`** - Download generated files

## Configuration Files

- **`vercel.json`**: Vercel configuration with function timeouts
- **`requirements.txt`**: Python dependencies for serverless functions
- **`next.config.js`**: Next.js configuration for Vercel
- **`.vercelignore`**: Files to exclude from deployment

## How It Works

1. **User enters topic** in the frontend
2. **Frontend calls** `/api/generate-content`
3. **Serverless function** processes the request:
   - Generates content using Groq AI
   - Creates audio using Azure Speech
   - Generates animations
   - Combines into video
4. **Status updates** via `/api/status/[job_id]`
5. **File downloads** via `/api/download/[job_id]/[file_type]`

## Function Timeouts

- **Content Generation**: 5 minutes (300 seconds)
- **Status Check**: 30 seconds
- **File Download**: 1 minute (60 seconds)

## File Storage

- **Temporary files** stored in `/tmp/` directory
- **Files cleaned up** after processing
- **No persistent storage** (stateless functions)

## Testing Your Deployment

1. **Visit your Vercel URL**
2. **Test health endpoint**: `https://your-app.vercel.app/api/health`
3. **Enter a topic** (e.g., "Photosynthesis")
4. **Click "Create & Play Educational Video"**
5. **Monitor processing** via status endpoint
6. **Download generated files**

## Performance Considerations

- **Cold starts**: First request may be slower
- **Memory limits**: 1GB per function
- **Timeout limits**: 5 minutes max for content generation
- **File size limits**: 50MB per file

## Monitoring

- **Vercel Dashboard**: View function logs and metrics
- **Function Logs**: Monitor API calls and errors
- **Analytics**: Track usage and performance

## Troubleshooting

### Common Issues

**Issue**: Function timeout
**Solution**: Optimize processing or break into smaller steps

**Issue**: Memory limit exceeded
**Solution**: Reduce file sizes or optimize processing

**Issue**: API key errors
**Solution**: Verify environment variables are set correctly

**Issue**: File not found
**Solution**: Check file paths and temporary storage

### Getting Help

1. **Check Vercel function logs**
2. **Verify environment variables**
3. **Test API endpoints directly**
4. **Check browser console for errors**

## Benefits of Vercel Serverless

- 🚀 **Fast deployment** (2-3 minutes)
- 🌍 **Global edge functions** for performance
- 🔄 **Automatic scaling** based on demand
- 💰 **Pay per use** pricing model
- 🔒 **HTTPS by default**
- 📊 **Built-in monitoring**

## Limitations

- **Function timeout**: 5 minutes maximum
- **Memory limit**: 1GB per function
- **File storage**: Temporary only
- **Cold starts**: Initial request delay

## Custom Domain

1. **Go to Project Settings → Domains**
2. **Add your domain**
3. **Configure DNS** as instructed
4. **Enable HTTPS**

Your Vidya AI app will be fully deployed on Vercel with both frontend and backend! 🎯
