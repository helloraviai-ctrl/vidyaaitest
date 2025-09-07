# 🎓 Vidya AI - Educational Content Generator

An AI-powered educational platform that generates engaging videos with voice narration, animated visuals, and structured learning content.

## ✨ Features

- 🤖 **AI-Powered Content Generation**: Uses Groq AI and OpenAI to create educational content
- 🎬 **Video Generation**: Creates educational videos with clean white theme
- 🎵 **Voice Narration**: Text-to-speech with multiple fallback options
- 📱 **Mobile Responsive**: Fully optimized for mobile devices
- 🎨 **Professional Design**: Clean, modern UI inspired by Coursera/Khan Academy
- ⚡ **Fast Performance**: Optimized for speed and mobile networks

## 🚀 Live Demo

- **Frontend**: [Deployed on Netlify](https://your-app-name.netlify.app)
- **Backend**: [Deployed on Heroku/Railway](https://your-backend-url.herokuapp.com)

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type-safe JavaScript
- **Lucide React** - Beautiful icons

### Backend
- **FastAPI** - Modern Python web framework
- **Groq AI** - Fast AI inference
- **Azure Speech Services** - Text-to-speech
- **MoviePy** - Video processing
- **PIL/Pillow** - Image generation

## 📱 Mobile Responsive Features

- ✅ Responsive breakpoints (xs, sm, md, lg, xl)
- ✅ Touch-friendly interface (44px minimum touch targets)
- ✅ Mobile-optimized typography
- ✅ Adaptive video player
- ✅ Fast loading on mobile networks
- ✅ Battery-efficient design

## 🎯 Content Format

Each educational video follows a structured format:

1. **Title Section**: Big title with emoji and centered text
2. **Subtitle/Question**: Bold italic question format
3. **Main Explanation**: 3-5 short sentences in a clean box
4. **Key Points**: 3-4 bullet points (max 10 words each)
5. **Visual Instruction**: Simple animation/graphic suggestion

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/helloraviai-ctrl/vidyaaitest.git
   cd vidyaaitest
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Set up backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Environment variables**
   ```bash
   # Copy and configure environment variables
   cp backend/env.example backend/.env
   # Edit backend/.env with your API keys
   ```

5. **Run the application**
   ```bash
   # Terminal 1: Start backend
   cd backend
   source venv/bin/activate
   python main.py

   # Terminal 2: Start frontend
   npm run dev
   ```

6. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🌐 Deployment

### Netlify (Frontend)

1. **Connect to GitHub**
   - Go to [Netlify](https://netlify.com)
   - Connect your GitHub repository
   - Select `helloraviai-ctrl/vidyaaitest`

2. **Build Settings**
   - Build command: `npm run build`
   - Publish directory: `out`
   - Node version: `18`

3. **Environment Variables**
   - Add any required environment variables in Netlify dashboard

### Backend Deployment

Deploy the backend to your preferred platform:

- **Heroku**: Use the included `Procfile`
- **Railway**: Connect GitHub repository
- **Render**: Use the build configuration
- **DigitalOcean**: Use App Platform

## 📁 Project Structure

```
vidyaaitest/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Main page
├── backend/               # FastAPI backend
│   ├── main.py           # Main application
│   ├── services/         # AI and video services
│   ├── models/           # Data models
│   └── requirements.txt  # Python dependencies
├── public/               # Static assets
├── netlify.toml         # Netlify configuration
├── next.config.js       # Next.js configuration
├── tailwind.config.js   # Tailwind configuration
└── package.json         # Node.js dependencies
```

## 🔧 Configuration

### Environment Variables

Create `backend/.env` with:

```env
# AI Services
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key

# Azure Speech (optional)
AZURE_SPEECH_KEY=your_azure_speech_key
AZURE_SPEECH_REGION=your_azure_region

# Other settings
DEBUG=True
```

### Customization

- **Colors**: Edit `tailwind.config.js` for theme colors
- **Content Format**: Modify `services/ai_service_manager.py`
- **Video Theme**: Update `services/animation_service.py`
- **Mobile Breakpoints**: Adjust in `app/page.tsx`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq AI](https://groq.com) for fast AI inference
- [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/) for TTS
- [Next.js](https://nextjs.org) for the amazing React framework
- [Tailwind CSS](https://tailwindcss.com) for utility-first styling

## 📞 Support

If you have any questions or need help:

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/helloraviai-ctrl/vidyaaitest/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/helloraviai-ctrl/vidyaaitest/discussions)

---

**Made with ❤️ for education and learning**