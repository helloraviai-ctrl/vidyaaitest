# 🚀 Vidya AI Backend

This is the Python FastAPI backend for the Vidya AI educational content generator.

## 🎯 **For Render Deployment:**

### **Important Configuration:**
- **Root Directory**: `backend` (when deploying to Render)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Environment**: Python 3.12

### **Required Environment Variables:**
```
GROQ_API_KEY=your_groq_api_key_here
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here
AZURE_VOICE_NAME=en-US-AriaNeural
AZURE_VOICE_STYLE=chat
OPENAI_API_KEY=your_openai_api_key_here (optional)
CORS_ORIGINS=https://your-netlify-site.netlify.app
```

### **Deployment Steps:**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect repository: `helloraviai-ctrl/vidyaaitest`
4. **Set Root Directory to `backend`**
5. Add environment variables
6. Deploy!

## 🔧 **Local Development:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 📱 **API Endpoints:**
- `GET /` - Health check
- `POST /api/generate-content` - Generate educational content
- `GET /api/status/{job_id}` - Check processing status
- `GET /api/video/{job_id}` - Get generated video

## 🎉 **After Deployment:**
Your backend will be available at: `https://your-app.onrender.com`
Use this URL in your Netlify environment variable: `NEXT_PUBLIC_API_URL`
