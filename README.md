# Vidya AI - Educational Content Generator

🎓 AI-powered educational content generator with video, audio, and text explanations.

## Features

- 🤖 **AI Content Generation**: Uses Groq AI for fast, structured educational explanations
- 🎤 **Text-to-Speech**: Azure Speech Services for high-quality narration
- 🎬 **Animation Generation**: Manim-based animations for visual learning
- 🎥 **Video Creation**: Combines audio and visuals into educational videos
- 🚀 **Fast Processing**: Optimized for quick content generation

## Tech Stack

- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI Services**: Groq AI, Azure Speech Services
- **Deployment**: Vercel (Frontend), Render (Backend)

## Quick Start

1. **Clone the repository**
2. **Install dependencies**: `npm install`
3. **Run development server**: `npm run dev`
4. **Open**: [http://localhost:3000](http://localhost:3000)

## Deployment

### Frontend (Vercel)
- **Guide**: See `VERCEL_DEPLOYMENT_GUIDE.md`
- **URL**: Your Vercel deployment URL

### Backend (Render)
- **URL**: https://vidyaaibot.onrender.com
- **API Documentation**: Available at backend URL

## Environment Variables

### Frontend
```
NEXT_PUBLIC_API_URL=https://vidyaaibot.onrender.com
```

### Backend
```
GROQ_API_KEY=your_groq_api_key
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region
```

## Usage

1. **Enter any educational topic** (e.g., "Photosynthesis")
2. **Click "Create & Play Educational Video"**
3. **Watch AI generate content, audio, and visuals**
4. **Enjoy your personalized educational video!**

## API Endpoints

- `POST /api/generate-content` - Generate educational content
- `GET /api/status/{job_id}` - Check processing status
- `GET /api/download/{job_id}/{file_type}` - Download generated files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for education**
