---
title: Vidya AI Backend
emoji: 🎓
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Vidya AI Educational Content Generator - Backend

AI-powered backend service for generating educational content with video, audio, and text explanations.

## Features

- 🤖 **AI Content Generation**: Uses Groq AI for fast, structured educational explanations
- 🎤 **Text-to-Speech**: Azure Speech Services for high-quality narration
- 🎬 **Animation Generation**: Manim-based animations for visual learning
- 🎥 **Video Creation**: Combines audio and visuals into educational videos
- 🚀 **Fast Processing**: Optimized for quick content generation

## API Endpoints

- `GET /` - Health check
- `POST /api/generate-content` - Generate educational content
- `GET /api/status/{job_id}` - Check processing status
- `GET /api/download/{job_id}/{file_type}` - Download generated files

## Environment Variables

Set these in your Hugging Face Space settings:

```
GROQ_API_KEY=your_groq_api_key
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region
OPENAI_API_KEY=your_openai_api_key (optional)
STABILITY_API_KEY=your_stability_api_key (optional)
```

## Usage

The backend automatically starts when the Space is deployed. It provides a REST API for the frontend to consume.

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Groq AI**: Fast AI inference
- **Azure Speech**: Text-to-speech services
- **Manim**: Mathematical animations
- **MoviePy**: Video processing