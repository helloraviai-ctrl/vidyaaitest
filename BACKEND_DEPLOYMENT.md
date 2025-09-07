# 🚀 Backend Deployment Guide

## Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

1. **Go to [Railway](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your repository**: `helloraviai-ctrl/vidyaaitest`
5. **Set Root Directory**: `backend`
6. **Add Environment Variables**:
   - `GROQ_API_KEY` = your_groq_api_key_here
   - `AZURE_SPEECH_KEY` = your_azure_speech_key_here
   - `AZURE_SPEECH_REGION` = your_azure_region_here
7. **Deploy** - Railway will automatically detect Python and deploy

### Option 2: Render (Free Tier Available)

1. **Go to [Render](https://render.com)**
2. **Sign up with GitHub**
3. **Click "New" → "Web Service"**
4. **Connect your repository**: `helloraviai-ctrl/vidyaaitest`
5. **Configure**:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. **Add Environment Variables** (same as above)
7. **Deploy**

### Option 3: Heroku

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Set environment variables**:
   ```bash
   heroku config:set GROQ_API_KEY=your_groq_api_key
   heroku config:set AZURE_SPEECH_KEY=your_azure_speech_key
   heroku config:set AZURE_SPEECH_REGION=your_azure_region
   ```
5. **Deploy**: `git subtree push --prefix backend heroku main`

## Environment Variables Needed

Copy these from your local `.env` file:

```env
GROQ_API_KEY=your_actual_groq_api_key
AZURE_SPEECH_KEY=your_actual_azure_speech_key
AZURE_SPEECH_REGION=your_actual_azure_region
AZURE_VOICE_NAME=en-US-AriaNeural
AZURE_VOICE_STYLE=chat
OPENAI_API_KEY=your_openai_api_key (if you have one)
```

## After Backend Deployment

1. **Get your backend URL** (e.g., `https://your-app.railway.app`)
2. **Go to Netlify** → Site settings → Environment variables
3. **Add**: `NEXT_PUBLIC_API_URL` = `https://your-backend-url`
4. **Redeploy your frontend**

## Testing

Once deployed, test your backend:
- Visit: `https://your-backend-url/docs`
- You should see the FastAPI documentation
- Test the `/api/generate-content` endpoint

## Troubleshooting

- **Build fails**: Check Python version (should be 3.12)
- **Environment variables**: Make sure all API keys are set
- **CORS errors**: Backend should allow your Netlify domain
- **Timeout**: Some platforms have request timeouts for long AI operations
