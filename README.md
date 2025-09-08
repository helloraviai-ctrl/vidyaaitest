---
title: Vidya AI Frontend
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: static
pinned: false
license: mit
---

# Vidya AI Educational Content Generator - Frontend

Beautiful, responsive frontend for the Vidya AI educational content generator.

## Features

- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- 📱 **Mobile-First**: Optimized for all device sizes
- 🎬 **Video Player**: Built-in video player with controls
- 📚 **Educational Content**: Structured learning material display
- 🔄 **Real-time Updates**: Live progress tracking
- 🎯 **User-Friendly**: Simple topic input with instant results

## Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **Static Export**: Optimized for deployment

## Backend Integration

This frontend connects to the Vidya AI backend API for:
- Content generation
- Progress tracking
- File downloads
- Status monitoring

## Environment Variables

Set these in your Hugging Face Space settings:

```
NEXT_PUBLIC_API_URL=https://your-backend-space.hf.space
```

## Usage

1. Enter any educational topic
2. Click "Create & Play Educational Video"
3. Watch as AI generates content, audio, and visuals
4. Enjoy your personalized educational video!

## Deployment

This is configured for static export and can be deployed to:
- Hugging Face Spaces (recommended)
- Netlify
- Vercel
- Any static hosting service