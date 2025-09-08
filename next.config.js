/** @type {import('next').NextConfig} */
const nextConfig = {
  // Vercel deployment configuration
  output: 'standalone',
  
  // Image optimization for Vercel
  images: {
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  
  // Performance optimizations
  compress: true,
  poweredByHeader: false,
  
  // Experimental features for serverless functions
  experimental: {
    serverComponentsExternalPackages: ['groq', 'azure-cognitiveservices-speech'],
  },
}

module.exports = nextConfig
