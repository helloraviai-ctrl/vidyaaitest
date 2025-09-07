# 🚨 RENDER DEPLOYMENT FIX

## ❌ **The Problem:**
You're trying to deploy the **entire repository** to Render, but your Next.js app is configured for static export (Netlify only).

## ✅ **The Solution:**
Deploy **ONLY the backend folder** to Render, and **ONLY the frontend** to Netlify.

## 🔧 **Step-by-Step Fix:**

### **1. Delete Current Render Service**
1. Go to your Render dashboard
2. Delete the current service that's failing
3. Start fresh

### **2. Create New Render Service (Backend Only)**
1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your repository: `helloraviai-ctrl/vidyaaitest`
4. **IMPORTANT**: Set **Root Directory** to `backend`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python main.py`
7. **Environment**: Python 3.12

### **3. Add Environment Variables**
```
GROQ_API_KEY=your_groq_api_key_here
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
AZURE_VOICE_NAME=en-US-AriaNeural
AZURE_VOICE_STYLE=chat
OPENAI_API_KEY=your_openai_api_key_here (optional)
CORS_ORIGINS=https://your-netlify-site.netlify.app
```

### **4. Deploy Backend**
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Get your backend URL (e.g., `https://your-app.onrender.com`)

### **5. Deploy Frontend to Netlify**
1. Go to [netlify.com](https://netlify.com)
2. Click "New site from Git"
3. Connect your repository: `helloraviai-ctrl/vidyaaitest`
4. **IMPORTANT**: Leave root directory as `.` (root)
5. Netlify will auto-detect settings from `netlify.toml`
6. Deploy!

### **6. Connect Frontend to Backend**
1. Go to Netlify dashboard
2. Site settings → Environment variables
3. Add: `NEXT_PUBLIC_API_URL=https://your-app.onrender.com`
4. Redeploy frontend

## 🎯 **Key Points:**
- **Render**: Deploy `backend` folder only
- **Netlify**: Deploy entire repository (root directory)
- **Backend URL**: Use for Netlify environment variable
- **Frontend URL**: Your final app URL

## ✅ **Result:**
- Backend: `https://your-app.onrender.com`
- Frontend: `https://your-site.netlify.app`
- Working AI app!
