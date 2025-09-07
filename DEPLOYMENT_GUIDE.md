# 🚀 Complete Deployment Guide - Vidya AI

## 📋 **Deployment Strategy**
- **Frontend**: Deploy to Netlify (Static Site)
- **Backend**: Deploy to Render (Python API)

## 🌐 **Step 1: Deploy Frontend to Netlify**

### 1.1 Prepare for Netlify
Your app is already configured for Netlify with:
- ✅ `next.config.js` with `output: 'export'`
- ✅ `netlify.toml` configuration
- ✅ Static build in `out/` directory

### 1.2 Deploy to Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Click "New site from Git"
4. Select your repository: `helloraviai-ctrl/vidyaaitest`
5. Netlify will auto-detect settings from `netlify.toml`
6. Click "Deploy site"

### 1.3 Set Environment Variables in Netlify
1. Go to Site settings → Environment variables
2. Add: `NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com`
   (Update this after deploying backend)

## 🔧 **Step 2: Deploy Backend to Render**

### 2.1 Prepare Backend
Your backend is ready with:
- ✅ `requirements.txt` with all dependencies
- ✅ `main.py` with FastAPI app
- ✅ Proper CORS configuration

### 2.2 Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository: `helloraviai-ctrl/vidyaaitest`
5. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. Add Environment Variables:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   AZURE_SPEECH_KEY=your_azure_speech_key_here
   AZURE_SPEECH_REGION=your_azure_region_here
   AZURE_VOICE_NAME=en-US-AriaNeural
   AZURE_VOICE_STYLE=chat
   OPENAI_API_KEY=your_openai_api_key_here (optional)
   CORS_ORIGINS=https://your-netlify-site.netlify.app
   ```
7. Click "Create Web Service"

### 2.3 Get Backend URL
After deployment, you'll get a URL like: `https://your-app.onrender.com`

## 🔗 **Step 3: Connect Frontend to Backend**

### 3.1 Update Netlify Environment Variable
1. Go to your Netlify site settings
2. Update `NEXT_PUBLIC_API_URL` to your Render backend URL
3. Redeploy your site

### 3.2 Test the Connection
1. Visit your Netlify site
2. Try generating content
3. Check browser console for any errors

## 🎯 **Deployment Order**
1. **First**: Deploy backend to Render
2. **Second**: Deploy frontend to Netlify
3. **Third**: Update Netlify environment variable with backend URL
4. **Fourth**: Test the complete application

## 🔍 **Troubleshooting**

### Common Issues:
1. **CORS Errors**: Make sure `CORS_ORIGINS` includes your Netlify URL
2. **API Not Found**: Check that `NEXT_PUBLIC_API_URL` is correct
3. **Build Failures**: Check that all dependencies are in `requirements.txt`

### Testing Commands:
```bash
# Test backend locally
cd backend
python main.py

# Test frontend locally
npm run dev
```

## 📱 **Final Result**
- Frontend: `https://your-site.netlify.app`
- Backend: `https://your-app.onrender.com`
- Full working application with AI content generation!

## 🎉 **Success!**
Your Vidya AI app will be fully deployed and accessible worldwide!
