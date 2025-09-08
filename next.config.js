/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for Hugging Face Spaces
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  
  // Image optimization
  images: {
    unoptimized: true, // Required for static export
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  
  // Performance optimizations
  compress: true,
  poweredByHeader: false,
  
  // Base path for Hugging Face Spaces (if needed)
  // basePath: process.env.NODE_ENV === 'production' ? '/your-space-name' : '',
}

module.exports = nextConfig
