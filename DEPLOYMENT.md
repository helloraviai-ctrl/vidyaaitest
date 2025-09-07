# 🚀 Deployment Guide - Vidya AI

This guide will help you deploy your Vidya AI application to Netlify and set up the backend.

## 📋 Prerequisites

- GitHub account
- Netlify account
- Backend hosting service (Heroku, Railway, Render, etc.)
- API keys for AI services

## 🌐 Frontend Deployment (Netlify)

### Step 1: Connect to Netlify

1. Go to [Netlify](https://netlify.com) and sign in
2. Click "New site from Git"
3. Choose "GitHub" and authorize Netlify
4. Select your repository: `helloraviai-ctrl/vidyaaitest`

### Step 2: Configure Build Settings

Netlify will auto-detect the settings from `netlify.toml`, but verify:

- **Build command**: `npm run build`
- **Publish directory**: `out`
- **Node version**: `18`

### Step 3: Environment Variables (Optional)

If you need any frontend environment variables:

1. Go to Site settings → Environment variables
2. Add any required variables

### Step 4: Deploy

1. Click "Deploy site"
2. Wait for the build to complete
3. Your site will be available at `https://your-site-name.netlify.app`

## 🔧 Backend Deployment

### Option 1: Heroku

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   cd backend
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY=your_groq_api_key
   heroku config:set AZURE_SPEECH_KEY=your_azure_speech_key
   heroku config:set AZURE_SPEECH_REGION=your_azure_region
   ```

4. **Deploy**
   ```bash
   git subtree push --prefix backend heroku main
   ```

### Option 2: Railway

1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Select the `backend` folder
4. Add environment variables in Railway dashboard
5. Deploy automatically

### Option 3: Render

1. Go to [Render](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python main.py`
6. Add environment variables
7. Deploy

## 🔗 Connect Frontend to Backend

### Update API URLs

1. **For Netlify**: Update the API URL in your frontend code
2. **For local development**: Keep `http://localhost:8000`
3. **For production**: Use your deployed backend URL

### Example Configuration

```javascript
// In your frontend code
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-backend-url.herokuapp.com'
  : 'http://localhost:8000';
```

## 🔐 Environment Variables

### Backend (.env file)

```env
# AI Services
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Azure Speech Services
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here

# Server Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=https://your-site-name.netlify.app
```

### Frontend (Netlify Environment Variables)

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.herokuapp.com
```

## 📱 Mobile Optimization

Your app is already optimized for mobile with:

- ✅ Responsive design
- ✅ Touch-friendly interface
- ✅ Fast loading
- ✅ Mobile-optimized images
- ✅ Progressive Web App features

## 🔍 Testing Deployment

### Frontend Testing

1. Visit your Netlify URL
2. Test on mobile devices
3. Check responsive design
4. Verify all features work

### Backend Testing

1. Test API endpoints
2. Verify AI content generation
3. Check video generation
4. Test voice synthesis

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Node.js version (should be 18+)
   - Verify all dependencies are installed
   - Check for TypeScript errors

2. **API Connection Issues**
   - Verify backend URL is correct
   - Check CORS settings
   - Ensure backend is running

3. **Environment Variables**
   - Double-check all API keys
   - Verify variable names match
   - Check for typos

### Debug Commands

```bash
# Check build locally
npm run build

# Test backend locally
cd backend
python main.py

# Check logs
heroku logs --tail  # For Heroku
railway logs        # For Railway
```

## 📊 Performance Monitoring

### Netlify Analytics

1. Enable Netlify Analytics in your dashboard
2. Monitor page views and performance
3. Check Core Web Vitals

### Backend Monitoring

1. Use your hosting platform's monitoring
2. Set up error tracking (Sentry, etc.)
3. Monitor API response times

## 🔄 Continuous Deployment

Your setup supports automatic deployments:

- **Frontend**: Deploys automatically on Git push to main
- **Backend**: Deploys automatically on Git push to main (if configured)

## 📞 Support

If you encounter issues:

1. Check the logs in your hosting platform
2. Verify all environment variables
3. Test locally first
4. Check GitHub Issues for known problems

---

**🎉 Congratulations! Your Vidya AI app is now deployed and ready for users!**
