# Auto-Deploy Setup for Hugging Face Spaces

This guide will help you set up automatic deployment from your GitHub repository to Hugging Face Spaces.

## Prerequisites

- ✅ GitHub repository with your code
- ✅ Hugging Face account: [https://huggingface.co/helloraviai](https://huggingface.co/helloraviai)
- ✅ Hugging Face Spaces created (backend and frontend)

## Step 1: Create Hugging Face Spaces

### 1.1 Create Backend Space
1. **Go to [Hugging Face Spaces](https://huggingface.co/spaces)**
2. **Click "Create new Space"**
3. **Configure:**
   - **Space name**: `vidyaai-backend`
   - **Owner**: `helloraviai`
   - **SDK**: Docker
   - **Hardware**: CPU Basic (free)
   - **Visibility**: Public
4. **Click "Create Space"**

### 1.2 Create Frontend Space
1. **Create another Space**
2. **Configure:**
   - **Space name**: `vidyaai-frontend`
   - **Owner**: `helloraviai`
   - **SDK**: Static
   - **Visibility**: Public
3. **Click "Create Space"**

## Step 2: Get Hugging Face Token

### 2.1 Generate Access Token
1. **Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)**
2. **Click "New token"**
3. **Configure:**
   - **Name**: `github-actions-deploy`
   - **Type**: Write
   - **Expiration**: No expiration (or set as needed)
4. **Click "Generate token"**
5. **Copy the token** (you'll need it for GitHub)

## Step 3: Configure GitHub Secrets

### 3.1 Add Hugging Face Token to GitHub
1. **Go to your GitHub repository**
2. **Click "Settings" tab**
3. **Click "Secrets and variables" → "Actions"**
4. **Click "New repository secret"**
5. **Configure:**
   - **Name**: `HF_TOKEN`
   - **Secret**: Paste your Hugging Face token
6. **Click "Add secret"**

## Step 4: Set Up Environment Variables in Spaces

### 4.1 Backend Space Environment Variables
1. **Go to your backend Space**: `https://huggingface.co/spaces/helloraviai/vidyaai-backend`
2. **Click "Settings" tab**
3. **Scroll to "Environment variables"**
4. **Add these variables:**
   ```
   GROQ_API_KEY=your_groq_api_key
   AZURE_SPEECH_KEY=your_azure_speech_key
   AZURE_SPEECH_REGION=your_azure_region
   AZURE_VOICE_NAME=en-US-AriaNeural
   OPENAI_API_KEY=your_openai_api_key (optional)
   STABILITY_API_KEY=your_stability_api_key (optional)
   ```

### 4.2 Frontend Space Environment Variables
1. **Go to your frontend Space**: `https://huggingface.co/spaces/helloraviai/vidyaai-frontend`
2. **Click "Settings" tab**
3. **Scroll to "Environment variables"**
4. **Add this variable:**
   ```
   NEXT_PUBLIC_API_URL=https://helloraviai-vidyaai-backend.hf.space
   ```

## Step 5: Enable Auto-Deploy

### 5.1 Push Code to GitHub
The GitHub Actions workflows are already configured in your repository:
- `.github/workflows/deploy-backend.yml` - Deploys backend on changes to `backend/` folder
- `.github/workflows/deploy-frontend.yml` - Deploys frontend on changes to frontend files

### 5.2 Test Auto-Deploy
1. **Make a small change** to any file in the `backend/` folder
2. **Commit and push** to the main branch
3. **Check GitHub Actions** tab in your repository
4. **Watch the deployment** happen automatically

## Step 6: Monitor Deployments

### 6.1 GitHub Actions
- **Go to your GitHub repository**
- **Click "Actions" tab**
- **Monitor deployment status**
- **Check logs if deployment fails**

### 6.2 Hugging Face Spaces
- **Check your Spaces** for updates
- **Monitor build logs** in Space settings
- **Test the deployed applications**

## How Auto-Deploy Works

### Backend Auto-Deploy
- **Triggers**: Changes to files in `backend/` folder
- **Process**: 
  1. Installs Python dependencies
  2. Uploads backend code to HF Space
  3. Builds Docker container
  4. Deploys to Space

### Frontend Auto-Deploy
- **Triggers**: Changes to frontend files (`app/`, `package.json`, etc.)
- **Process**:
  1. Installs Node.js dependencies
  2. Builds Next.js application
  3. Uploads static files to HF Space
  4. Deploys to Space

## Troubleshooting

### Common Issues

**Issue**: GitHub Actions failing
**Solution**: 
- Check HF_TOKEN secret is set correctly
- Verify Space names match in workflow files
- Check GitHub Actions logs for specific errors

**Issue**: Deployment not triggering
**Solution**:
- Ensure files are in correct paths
- Check workflow file syntax
- Verify push is to main branch

**Issue**: Environment variables not working
**Solution**:
- Set variables in HF Space settings
- Check variable names match exactly
- Redeploy after setting variables

### Getting Help

1. **Check GitHub Actions logs** for detailed error messages
2. **Check HF Space build logs** for deployment issues
3. **Verify all secrets and environment variables** are set correctly
4. **Test manual deployment** first before auto-deploy

## URLs After Setup

- **Backend**: `https://helloraviai-vidyaai-backend.hf.space`
- **Frontend**: `https://helloraviai-vidyaai-frontend.hf.space`
- **Your Profile**: [https://huggingface.co/helloraviai](https://huggingface.co/helloraviai)

## Benefits of Auto-Deploy

- ✅ **Automatic updates** when you push code
- ✅ **No manual deployment** required
- ✅ **Consistent deployments** every time
- ✅ **Version control** integration
- ✅ **Easy rollback** if needed
- ✅ **Team collaboration** friendly

Your Vidya AI app will now automatically deploy to Hugging Face Spaces whenever you push changes to GitHub! 🚀
