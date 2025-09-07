# Netlify Deployment Guide for Vidya AI Frontend

This guide will help you deploy your Vidya AI frontend to Netlify and connect it to your Render backend.

## Prerequisites

- ✅ Your backend is deployed on Render at: `https://vidyaaibot.onrender.com`
- ✅ Your frontend code is ready with static export configuration
- ✅ Netlify account (free tier is sufficient)

## Step 1: Prepare Your Repository

### 1.1 Environment Variables
Your frontend is already configured to use environment variables. The key variable is:
```bash
NEXT_PUBLIC_API_URL=https://vidyaaibot.onrender.com
```

### 1.2 Build Configuration
Your `next.config.js` is already configured for static export:
```javascript
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  images: {
    unoptimized: true, // Required for static export
  },
}
```

### 1.3 Netlify Configuration
Your `netlify.toml` is already configured with:
- Build settings
- Redirect rules for SPA
- Security headers
- API proxy to your Render backend

## Step 2: Deploy to Netlify

### Option A: Deploy via Netlify Dashboard (Recommended)

1. **Go to Netlify Dashboard**
   - Visit [netlify.com](https://netlify.com)
   - Sign in to your account

2. **Create New Site**
   - Click "Add new site" → "Import an existing project"
   - Connect your Git provider (GitHub, GitLab, or Bitbucket)
   - Select your repository

3. **Configure Build Settings**
   - **Base directory**: Leave empty (root directory)
   - **Build command**: `npm run build`
   - **Publish directory**: `out`

4. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add the following variable:
     ```
     NEXT_PUBLIC_API_URL = https://vidyaaibot.onrender.com
     ```

5. **Deploy**
   - Click "Deploy site"
   - Wait for the build to complete

### Option B: Deploy via Netlify CLI

1. **Install Netlify CLI**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**
   ```bash
   netlify login
   ```

3. **Build and Deploy**
   ```bash
   # Build the project
   npm run build
   
   # Deploy to Netlify
   netlify deploy --prod --dir=out
   ```

## Step 3: Configure Environment Variables in Netlify

### Required Environment Variables:
```
NEXT_PUBLIC_API_URL=https://vidyaaibot.onrender.com
```

### Optional Environment Variables:
```
NEXT_PUBLIC_GA_ID=your-google-analytics-id
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_ERROR_REPORTING=true
```

### How to Set Environment Variables:
1. Go to your Netlify site dashboard
2. Navigate to **Site settings** → **Environment variables**
3. Click **Add variable**
4. Add each variable with its value
5. Click **Save**

## Step 4: Test Your Deployment

### 4.1 Test Frontend
1. Visit your Netlify site URL
2. Try entering a topic (e.g., "Photosynthesis")
3. Check if the request reaches your backend

### 4.2 Test Backend Connection
1. Open browser developer tools
2. Go to Network tab
3. Submit a topic
4. Verify API calls are going to `https://vidyaaibot.onrender.com`

### 4.3 Common Issues and Solutions

**Issue**: CORS errors
**Solution**: Your backend should have CORS configured for your Netlify domain

**Issue**: 404 errors on API calls
**Solution**: Check that your Render backend is running and accessible

**Issue**: Build failures
**Solution**: Check Netlify build logs for specific errors

## Step 5: Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to Site settings → Domain management
   - Click "Add custom domain"
   - Enter your domain name

2. **Configure DNS**
   - Add a CNAME record pointing to your Netlify site
   - Or use Netlify's nameservers

## Step 6: Performance Optimization

### 6.1 Enable Netlify Features
- **Netlify Analytics**: Monitor site performance
- **Netlify Forms**: If you add contact forms
- **Netlify Functions**: For serverless functions (if needed)

### 6.2 Optimize Images
Your Next.js config already includes image optimization:
```javascript
images: {
  unoptimized: true,
  formats: ['image/webp', 'image/avif'],
}
```

### 6.3 Enable Compression
Your `netlify.toml` includes compression settings in headers.

## Step 7: Monitoring and Maintenance

### 7.1 Monitor Performance
- Use Netlify Analytics
- Monitor Core Web Vitals
- Check build times

### 7.2 Set up Notifications
- Enable build notifications
- Set up uptime monitoring
- Configure error tracking

## Troubleshooting

### Build Issues
```bash
# Check build logs in Netlify dashboard
# Common fixes:
npm install
npm run build
```

### API Connection Issues
```bash
# Test backend directly
curl https://vidyaaibot.onrender.com/

# Check CORS settings in backend
# Verify environment variables are set
```

### Performance Issues
- Enable Netlify's CDN
- Optimize images
- Use lazy loading
- Minimize bundle size

## Security Considerations

Your `netlify.toml` already includes security headers:
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

## Support

If you encounter issues:
1. Check Netlify build logs
2. Verify environment variables
3. Test backend connectivity
4. Check browser console for errors
5. Review this guide for common solutions

## Next Steps

After successful deployment:
1. Set up monitoring and analytics
2. Configure custom domain (if desired)
3. Set up automated deployments from your Git repository
4. Consider adding error tracking (Sentry)
5. Implement performance monitoring

Your Vidya AI app should now be live on Netlify and connected to your Render backend! 🚀
