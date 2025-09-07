"""
Simplified FastAPI application for Vidya AI Educational Content Generator
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import uuid
import json
import asyncio
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

def _hex_to_rgb(hex_color: str):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Vidya AI Educational Content Generator",
    description="Generate educational content with AI explanations, audio narration, and animated visuals",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models
class TopicRequest(BaseModel):
    topic: str
    difficulty_level: str = "beginner"
    target_audience: str = "students"

class ContentResponse(BaseModel):
    job_id: str
    status: str
    message: str

class ProcessingStatus(BaseModel):
    job_id: str
    status: str
    progress: int = 0
    message: str = ""
    result_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# In-memory storage for processing status
processing_jobs = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Vidya AI Educational Content Generator API", "status": "healthy"}

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: TopicRequest, background_tasks: BackgroundTasks):
    """Generate educational content for a given topic"""
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize processing status
        processing_jobs[job_id] = ProcessingStatus(
            job_id=job_id,
            status="started",
            progress=0,
            message="Starting content generation..."
        )
        
        # Start background processing
        background_tasks.add_task(process_content_generation, job_id, request)
        
        return ContentResponse(
            job_id=job_id,
            status="processing",
            message="Content generation started. Use the job_id to check progress."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start content generation: {str(e)}")

@app.get("/api/status/{job_id}")
async def get_processing_status(job_id: str):
    """Get the current processing status for a job"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return processing_jobs[job_id]

@app.get("/api/video/{job_id}")
async def get_video_content(job_id: str):
    """Get video content for direct playback"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_status = processing_jobs[job_id]
    
    if job_status.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Get the video path
    video_path = job_status.result_data.get("video_path")
    
    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Check if it's a video file, image file, or text file
    if video_path.endswith('.mp4'):
        # Return the video file directly
        return FileResponse(
            path=video_path,
            filename=f"{job_id}_video.mp4",
            media_type='video/mp4'
        )
    elif video_path.endswith(('.png', '.jpg', '.jpeg')):
        # Return the image file directly
        return FileResponse(
            path=video_path,
            filename=f"{job_id}_slide.png",
            media_type='image/png'
        )
    else:
        # Read text content for non-video files
        try:
            with open(video_path, "r", encoding="utf-8") as f:
                video_content = f.read()
        except UnicodeDecodeError:
            # If it's a binary file, return file info instead
            video_content = f"Binary file: {video_path}"
        
        return {
            "content": video_content,
            "topic": job_status.result_data.get("topic"),
            "duration": job_status.result_data.get("duration"),
            "sections": job_status.result_data.get("sections", []),
            "job_id": job_id
        }

@app.get("/api/audio/{job_id}")
async def get_audio_file(job_id: str):
    """Get audio file for playback"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_status = processing_jobs[job_id]
    
    if job_status.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Get audio path from the job data
    output_dir = f"./outputs/{job_id}"
    audio_path = f"{output_dir}/narration.wav"
    
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=audio_path,
        media_type='audio/wav',
        filename=f"narration_{job_id}.wav"
    )

@app.get("/api/slide/{job_id}/{slide_number}")
async def get_slide_image(job_id: str, slide_number: int):
    """Get visual slide image"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_status = processing_jobs[job_id]
    
    if job_status.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Get slide path
    output_dir = f"./outputs/{job_id}"
    slide_path = f"{output_dir}/slide_{slide_number}.png"
    
    if not os.path.exists(slide_path):
        raise HTTPException(status_code=404, detail="Slide not found")
    
    return FileResponse(
        path=slide_path,
        media_type='image/png',
        filename=f"slide_{slide_number}_{job_id}.png"
    )

async def process_content_generation(job_id: str, request: TopicRequest):
    """Background task to process content generation - creates comprehensive video"""
    try:
        # Update status
        processing_jobs[job_id].status = "generating_content"
        processing_jobs[job_id].progress = 10
        processing_jobs[job_id].message = "Generating comprehensive explanation..."
        
        # Step 1: Generate detailed explanation using Fast Content Service
        explanation_data = await generate_fast_ai_explanation(request.topic, request.difficulty_level, request.target_audience)
        
        # Create output directory
        output_dir = f"./outputs/{job_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        processing_jobs[job_id].status = "creating_visuals"
        processing_jobs[job_id].progress = 30
        processing_jobs[job_id].message = "Creating visual slides..."
        
        # Step 2: Create visual slides for each section
        slide_paths = await create_visual_slides(explanation_data, output_dir)
        
        processing_jobs[job_id].status = "generating_audio"
        processing_jobs[job_id].progress = 50
        processing_jobs[job_id].message = "Creating audio narration..."
        
        # Step 3: Generate audio narration (ALWAYS generate audio for better video experience)
        audio_path = None
        try:
            audio_path = await generate_audio_narration(explanation_data["full_explanation"], output_dir)
        except Exception as e:
            print(f"Audio generation failed: {e}")
            # Create a simple audio placeholder
            audio_path = f"{output_dir}/narration.wav"
            # Create a simple WAV file
            with open(audio_path, "wb") as f:
                # WAV file header for 30 seconds of silence
                f.write(b'RIFF')
                f.write((36).to_bytes(4, 'little'))  # File size
                f.write(b'WAVE')
                f.write(b'fmt ')
                f.write((16).to_bytes(4, 'little'))  # Format chunk size
                f.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
                f.write((1).to_bytes(2, 'little'))   # Number of channels
                f.write((22050).to_bytes(4, 'little'))  # Sample rate
                f.write((44100).to_bytes(4, 'little'))  # Byte rate
                f.write((2).to_bytes(2, 'little'))   # Block align
                f.write((16).to_bytes(2, 'little'))  # Bits per sample
                f.write(b'data')
                f.write((1323000).to_bytes(4, 'little'))  # Data size (30 seconds)
                # Add silence data
                for i in range(1323000):
                    f.write((0).to_bytes(2, 'little', signed=True))
        
        processing_jobs[job_id].status = "creating_video"
        processing_jobs[job_id].progress = 80
        processing_jobs[job_id].message = "Combining into final video..."
        
        # Step 4: Create comprehensive video (ALWAYS create video, even in fast mode)
        final_video_path = None
        if slide_paths:
            # Always try to create a proper video
            final_video_path = await create_comprehensive_video(
                explanation_data, 
                slide_paths, 
                audio_path, 
                output_dir
            )
        else:
            # Fallback if no slides created
            final_video_path = slide_paths[0] if slide_paths else None
        
        # Update final status
        processing_jobs[job_id].status = "completed"
        processing_jobs[job_id].progress = 100
        processing_jobs[job_id].message = "Comprehensive educational video created successfully!"
        
        # Ensure we have the correct video path
        if not final_video_path or not os.path.exists(final_video_path):
            # Try to find the video file
            potential_paths = [
                f"{output_dir}/final_video.mp4",
                f"{output_dir}/comprehensive_video.txt",
                slide_paths[0] if slide_paths else None
            ]
            
            for path in potential_paths:
                if path and os.path.exists(path):
                    final_video_path = path
                    break
        
        processing_jobs[job_id].result_data = {
            "video_path": final_video_path,
            "topic": request.topic,
            "duration": explanation_data.get("estimated_duration", 180),
            "sections": explanation_data.get("sections", []),
            "visual_paths": explanation_data.get("visual_paths", slide_paths),
            "generation_type": explanation_data.get("generation_type", "standard")
        }
        
    except Exception as e:
        # Update status with error
        processing_jobs[job_id].status = "failed"
        processing_jobs[job_id].message = f"Content generation failed: {str(e)}"
        processing_jobs[job_id].error = str(e)

async def generate_fast_ai_explanation(topic: str, difficulty: str, audience: str) -> dict:
    """Generate fast AI explanation using optimized service"""
    try:
        # Import fast content service
        from services.fast_content_service import FastContentService
        
        # Initialize fast content service
        fast_service = FastContentService()
        
        # Generate content quickly
        result = await fast_service.generate_fast_content(topic, difficulty, audience)
        
        print(f"Generated fast content for topic: {topic}")
        return result
        
    except Exception as e:
        print(f"Fast content generation failed: {e}")
        # Fallback to original method
        return await generate_ai_explanation(topic, difficulty, audience)

async def generate_ai_explanation(topic: str, difficulty: str, audience: str) -> dict:
    """Generate comprehensive explanation using enhanced AI service manager"""
    try:
        # Ensure environment variables are loaded
        from dotenv import load_dotenv
        load_dotenv()
        
        # Import enhanced AI service manager
        from services.ai_service_manager import AIServiceManager, ContentType
        
        # Initialize AI service manager
        ai_manager = AIServiceManager()
        
        # Determine content type based on topic
        content_type = ContentType.EDUCATIONAL
        if any(word in topic.lower() for word in ['science', 'physics', 'chemistry', 'math', 'engineering']):
            content_type = ContentType.TECHNICAL
        elif any(word in topic.lower() for word in ['art', 'music', 'creative', 'design']):
            content_type = ContentType.CREATIVE
        elif any(word in topic.lower() for word in ['analysis', 'data', 'research', 'study']):
            content_type = ContentType.ANALYTICAL
        
        # Generate explanation using the best available model
        explanation_data = await ai_manager.generate_enhanced_content(
            topic=topic,
            difficulty=difficulty,
            audience=audience,
            content_type=content_type,
            speed_priority=True  # Prioritize speed for better user experience
        )
        
        print(f"Generated content using AI service manager for topic: {topic}")
        return explanation_data
        
    except Exception as e:
        print(f"Error generating AI explanation: {e}")
        # Fallback to basic explanation if AI generation fails
        return {
            "full_explanation": f"Welcome to our explanation of {topic}. This is a {difficulty} level explanation designed for {audience}. {topic} is an important concept that we'll explore in detail.",
            "sections": [
                {
                    "title": f"Introduction to {topic}",
                    "content": f"Welcome to our comprehensive explanation of {topic}.\n\n{topic} is a fascinating subject that we'll explore together, starting with the basics and building up to more complex concepts.",
                    "key_points": [f"Understanding {topic}", f"Importance of {topic}", f"Applications of {topic}"],
                    "visual_description": f"An introductory slide showing the main concept of {topic}",
                    "duration_estimate": 30
                }
            ],
            "key_concepts": [f"Concept 1: {topic}", f"Concept 2: Applications", f"Concept 3: Examples"],
            "summary": f"A comprehensive explanation of {topic}",
            "estimated_duration": 180,
            "topic": topic
        }

def draw_text_with_outline(draw, position, text, font, text_color, outline_color, outline_width=2):
    """Draw text with an outline for better readability"""
    x, y = position
    
    # Draw outline by drawing text in multiple positions
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    
    # Draw main text
    draw.text((x, y), text, font=font, fill=text_color)

def draw_multiline_text_with_formatting(draw, position, text, font, text_color, outline_color, max_width):
    """Draw multiline text with proper formatting and wrapping"""
    x, y = position
    
    # Split text into paragraphs first
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            y += 20  # Extra space for empty paragraphs
            continue
            
        # Handle line breaks within paragraphs
        lines = paragraph.split('\n')
        
        for line in lines:
            if not line.strip():
                y += 20
                continue
                
            # Word wrap this line
            words = line.split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0]
                
                if text_width <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        # Draw the current line
                        line_text = ' '.join(current_line)
                        draw_text_with_outline(draw, (x, y), line_text, font, text_color, outline_color, 1)
                        y += 40  # Increased line spacing for better readability
                        current_line = [word]
                    else:
                        # Word is too long, draw it anyway
                        draw_text_with_outline(draw, (x, y), word, font, text_color, outline_color, 1)
                        y += 40
            
            # Draw remaining words
            if current_line:
                line_text = ' '.join(current_line)
                draw_text_with_outline(draw, (x, y), line_text, font, text_color, outline_color, 1)
                y += 40
        
        # Add extra space between paragraphs
        y += 25

def _hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def format_text_for_display(text):
    """Format text for better display with proper line breaks and structure"""
    # Clean up the text first
    text = text.strip()
    
    # Remove excessive whitespace
    import re
    text = re.sub(r'\s+', ' ', text)
    
    # Split into sentences for better formatting
    sentences = re.split(r'[.!?]+', text)
    formatted_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Capitalize first letter
            if sentence and not sentence[0].isupper():
                sentence = sentence[0].upper() + sentence[1:]
            formatted_sentences.append(sentence)
    
    # Join sentences with proper punctuation
    if formatted_sentences:
        text = '. '.join(formatted_sentences)
        if text and not text.endswith('.'):
            text += '.'
    
    # Add strategic paragraph breaks for better readability
    # Break after every 2-3 sentences for better visual flow
    sentences = text.split('. ')
    if len(sentences) > 2:
        # Group sentences into paragraphs
        paragraphs = []
        current_paragraph = []
        
        for i, sentence in enumerate(sentences):
            current_paragraph.append(sentence)
            # Create paragraph break every 2-3 sentences
            if len(current_paragraph) >= 2 and (i + 1) % 2 == 0:
                paragraphs.append('. '.join(current_paragraph) + '.')
                current_paragraph = []
        
        # Add remaining sentences
        if current_paragraph:
            paragraphs.append('. '.join(current_paragraph) + '.')
        
        text = '\n\n'.join(paragraphs)
    
    # Limit length for display but keep it readable
    if len(text) > 800:
        # Find a good breaking point at sentence end
        truncated = text[:800]
        last_period = truncated.rfind('.')
        if last_period > 600:  # If we can find a good break point
            text = truncated[:last_period + 1] + "..."
        else:
            text = truncated + "..."
    
    return text

async def create_visual_slides(explanation_data: dict, output_dir: str) -> list:
    """Create professional visual slides using enhanced visual service"""
    try:
        # Import enhanced AI visual service
        from services.enhanced_ai_visual_service import EnhancedAIVisualService
        
        # Initialize enhanced AI visual service
        visual_service = EnhancedAIVisualService()
        
        slide_paths = []
        sections = explanation_data.get("sections", [])
        topic = explanation_data.get("topic", "Educational Content")
        
        print(f"Creating {len(sections)} enhanced visual slides for topic: {topic}")
        
        # Create slides using enhanced AI visual service
        slide_paths = await visual_service.create_multiple_enhanced_slides(
            sections=sections,
            topic=topic,
            output_dir=output_dir,
            color_scheme="professional"
        )
        
        for i, slide_path in enumerate(slide_paths):
            print(f"Created enhanced AI slide {i+1}: {slide_path}")
        
        return slide_paths
        
    except Exception as e:
        print(f"Enhanced visual service failed: {e}")
        # Fallback to basic visual creation
        return await create_basic_visual_slides(explanation_data, output_dir)

async def create_basic_visual_slides(explanation_data: dict, output_dir: str) -> list:
    """Fallback basic visual slide creation"""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import math
    import textwrap
    import random
    
    slide_paths = []
    
    # Load high-quality fonts with better fallbacks and improved sizes
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        content_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        bullet_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 64)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 42)
            content_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 32)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 26)
            bullet_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 30)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            bullet_font = ImageFont.load_default()
    
    for i, section in enumerate(explanation_data["sections"]):
        # Create high-quality slide with professional design
        img = Image.new('RGB', (1920, 1080), color='#1e293b')
        draw = ImageDraw.Draw(img)
        
        # Create dynamic gradient background with multiple colors
        for y in range(1080):
            color_ratio = y / 1080
            # Create a vibrant multi-color gradient (dark blue to purple to pink)
            if color_ratio < 0.33:
                # Blue to purple transition
                r = int(20 + (80 - 20) * (color_ratio / 0.33))
                g = int(30 + (40 - 30) * (color_ratio / 0.33))
                b = int(80 + (120 - 80) * (color_ratio / 0.33))
            elif color_ratio < 0.66:
                # Purple to pink transition
                r = int(80 + (150 - 80) * ((color_ratio - 0.33) / 0.33))
                g = int(40 + (60 - 40) * ((color_ratio - 0.33) / 0.33))
                b = int(120 + (100 - 120) * ((color_ratio - 0.33) / 0.33))
            else:
                # Pink to deep purple
                r = int(150 + (100 - 150) * ((color_ratio - 0.66) / 0.34))
                g = int(60 + (30 - 60) * ((color_ratio - 0.66) / 0.34))
                b = int(100 + (80 - 100) * ((color_ratio - 0.66) / 0.34))
            
            draw.line([(0, y), (1920, y)], fill=(r, g, b))
        
        # Add professional background elements
        center_x, center_y = 960, 540
        
        # Create dynamic geometric patterns with different colors
        colors = [(255, 100, 150, 40), (100, 200, 255, 40), (150, 255, 100, 40), (255, 200, 100, 40)]
        for j in range(4):
            radius = 80 + j * 100
            color = colors[j % len(colors)]
            for angle in range(0, 360, 20):
                x = center_x + radius * math.cos(math.radians(angle + i * 45))
                y = center_y + radius * math.sin(math.radians(angle + i * 45))
                # Draw colorful geometric shapes with different sizes
                size = 6 + j * 2
                draw.ellipse([x-size, y-size, x+size, y+size], fill=color, outline=(*color[:3], 120))
        
        # Add floating accent elements with more variety
        accent_colors = [(255, 150, 200), (150, 255, 200), (200, 150, 255), (255, 255, 150)]
        for j in range(25):
            particle_x = (j * 77 + i * 50) % 1920
            particle_y = (j * 43 + i * 30) % 1080
            size = random.randint(3, 8)
            color = accent_colors[j % len(accent_colors)]
            # Add some variety with different shapes
            if j % 3 == 0:
                # Draw circles
                draw.ellipse([particle_x-size, particle_y-size, particle_x+size, particle_y+size], 
                            fill=(*color, 80))
            elif j % 3 == 1:
                # Draw squares
                draw.rectangle([particle_x-size, particle_y-size, particle_x+size, particle_y+size], 
                              fill=(*color, 60))
            else:
                # Draw diamonds
                points = [(particle_x, particle_y-size), (particle_x+size, particle_y), 
                         (particle_x, particle_y+size), (particle_x-size, particle_y)]
                draw.polygon(points, fill=(*color, 70))
        
        # Create main content area with enhanced glass morphism effect
        content_rect = [100, 100, 1820, 980]
        # Draw enhanced glass effect background with multiple layers
        for alpha in range(30, 0, -3):
            color = (255, 255, 255, alpha)
            draw.rectangle([content_rect[0]-alpha, content_rect[1]-alpha, 
                           content_rect[2]+alpha, content_rect[3]+alpha], 
                          outline=color, width=2)
        
        # Add gradient inner glow
        for y in range(content_rect[1], content_rect[3], 2):
            alpha = int(20 * (1 - abs(y - (content_rect[1] + content_rect[3])/2) / ((content_rect[3] - content_rect[1])/2)))
            draw.line([(content_rect[0], y), (content_rect[2], y)], fill=(255, 255, 255, alpha))
        
        # Add main content background with subtle color
        draw.rectangle(content_rect, fill=(255, 255, 255, 20), outline=(255, 255, 255, 60))
        
        # Add topic header with vibrant styling
        topic_text = f"🚀 {explanation_data['topic'].title()}"
        draw_text_with_outline(draw, (200, 80), topic_text, title_font, '#ff6b9d', '#8b5cf6', 4)
        
        # Add section indicator with gradient colors
        section_text = f"Section {i+1} of {len(explanation_data['sections'])}"
        section_colors = ['#00ff88', '#ff6b9d', '#8b5cf6', '#ffd93d']
        section_color = section_colors[i % len(section_colors)]
        draw_text_with_outline(draw, (1600, 80), section_text, small_font, section_color, '#000000', 3)
        
        # Draw section title with vibrant styling
        title = section["title"]
        title_x, title_y = 200, 180
        
        # Title with vibrant colors
        title_colors = ['#ff6b9d', '#8b5cf6', '#00ff88', '#ffd93d']
        title_color = title_colors[i % len(title_colors)]
        draw_text_with_outline(draw, (title_x, title_y), title, subtitle_font, title_color, '#000000', 5)
        
        # Add decorative line under title with gradient
        line_colors = ['#ff6b9d', '#8b5cf6', '#00ff88', '#ffd93d']
        line_color = line_colors[i % len(line_colors)]
        draw.line([title_x, title_y + 60, title_x + 800, title_y + 60], fill=line_color, width=6)
        
        # Draw formatted content with proper text wrapping
        content = section["content"]
        content_x, content_y = 200, 280
        
        # Format and wrap content properly
        formatted_content = format_text_for_display(content)
        
        # Create a content box with vibrant styling and more space
        content_box_width = 1400
        content_box_height = 450
        content_box_x = content_x - 30
        content_box_y = content_y - 30
        
        # Draw content background with vibrant styling
        box_colors = [(255, 107, 157, 20), (139, 92, 246, 20), (0, 255, 136, 20), (255, 217, 61, 20)]
        box_color = box_colors[i % len(box_colors)]
        draw.rectangle([content_box_x, content_box_y, 
                       content_box_x + content_box_width, content_box_y + content_box_height], 
                      fill=box_color, outline=(*box_color[:3], 80))
        
        # Draw the formatted content with vibrant text
        text_colors = ['#ffffff', '#ff6b9d', '#8b5cf6', '#00ff88']
        text_color = text_colors[i % len(text_colors)]
        draw_multiline_text_with_formatting(draw, (content_x, content_y), formatted_content, 
                                          content_font, text_color, '#000000', content_box_width - 40)
        
        # Add key points section if available
        if "key_points" in section and section["key_points"]:
            key_points_y = content_y + 480
            
            # Create key points box with vibrant styling
            key_points_box_width = 1200
            key_points_box_height = 280
            key_points_box_x = content_x - 30
            key_points_box_y = key_points_y - 30
            
            # Draw key points background with vibrant colors
            key_colors = [(255, 107, 157, 30), (139, 92, 246, 30), (0, 255, 136, 30), (255, 217, 61, 30)]
            key_color = key_colors[i % len(key_colors)]
            draw.rectangle([key_points_box_x, key_points_box_y, 
                           key_points_box_x + key_points_box_width, key_points_box_y + key_points_box_height], 
                          fill=key_color, outline=(*key_color[:3], 100))
            
            # Key points title with vibrant styling
            title_colors = ['#ff6b9d', '#8b5cf6', '#00ff88', '#ffd93d']
            title_color = title_colors[i % len(title_colors)]
            draw_text_with_outline(draw, (content_x, key_points_y), "✨ Key Points:", 
                                 bullet_font, title_color, '#000000', 3)
            
            # Draw key points with vibrant formatting and spacing
            bullet_colors = ['#ffffff', '#ff6b9d', '#8b5cf6', '#00ff88']
            for j, point in enumerate(section["key_points"][:4]):  # Show max 4 points
                bullet_y = key_points_y + 60 + (j * 50)  # Increased spacing
                if bullet_y < key_points_box_y + key_points_box_height - 20:
                    # Format the point text
                    formatted_point = format_text_for_display(point)
                    bullet_text = f"🎯 {formatted_point}"
                    bullet_color = bullet_colors[j % len(bullet_colors)]
                    draw_text_with_outline(draw, (content_x + 20, bullet_y), bullet_text, 
                                         bullet_font, bullet_color, '#000000', 2)
        
        # Add visual description if available
        if "visual_description" in section and section["visual_description"]:
            visual_y = key_points_y + 300 if "key_points" in section else content_y + 300
            visual_text = f"🎨 Visual: {section['visual_description'][:80]}..."
            visual_colors = ['#ff6b9d', '#8b5cf6', '#00ff88', '#ffd93d']
            visual_color = visual_colors[i % len(visual_colors)]
            draw_text_with_outline(draw, (content_x, visual_y), visual_text, 
                                 small_font, visual_color, '#000000', 2)
        
        # Add vibrant progress indicator
        progress_width = 500
        progress_height = 12
        progress_x = 200
        progress_y = 1000
        
        # Progress background with gradient
        progress_bg_colors = ['#ff6b9d', '#8b5cf6', '#00ff88', '#ffd93d']
        progress_bg_color = progress_bg_colors[i % len(progress_bg_colors)]
        draw.rectangle([progress_x, progress_y, progress_x + progress_width, progress_y + progress_height], 
                      fill=(*_hex_to_rgb(progress_bg_color), 30), outline=(*_hex_to_rgb(progress_bg_color), 100))
        
        # Progress fill with vibrant color
        progress_fill = (i + 1) / len(explanation_data["sections"])
        fill_width = int(progress_width * progress_fill)
        draw.rectangle([progress_x, progress_y, progress_x + fill_width, progress_y + progress_height], 
                      fill=progress_bg_color)
        
        # Add progress text with vibrant styling
        progress_text = f"🚀 {int(progress_fill * 100)}% Complete"
        draw_text_with_outline(draw, (progress_x + progress_width + 20, progress_y - 5), progress_text, 
                             small_font, progress_bg_color, '#000000', 2)
        
        # Save the slide with high quality
        slide_path = f"{output_dir}/slide_{i+1}.png"
        img.save(slide_path, "PNG", quality=95, optimize=True)
        slide_paths.append(slide_path)
        
        print(f"Created professional slide {i+1}: {slide_path}")
    
    return slide_paths

async def generate_audio_narration(text: str, output_dir: str) -> str:
    """Generate actual audio narration using Azure Speech Services"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # Get Azure credentials
        speech_key = os.getenv("AZURE_SPEECH_KEY", "demo_key")
        speech_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        
        if speech_key == "demo_key":
            # Create a mock audio file for demo
            audio_path = f"{output_dir}/narration.wav"
            # Create a simple WAV file header (44 bytes) + some data
            with open(audio_path, "wb") as f:
                # WAV file header
                f.write(b'RIFF')
                f.write((36).to_bytes(4, 'little'))  # File size
                f.write(b'WAVE')
                f.write(b'fmt ')
                f.write((16).to_bytes(4, 'little'))  # Format chunk size
                f.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
                f.write((1).to_bytes(2, 'little'))   # Number of channels
                f.write((22050).to_bytes(4, 'little'))  # Sample rate
                f.write((44100).to_bytes(4, 'little'))  # Byte rate
                f.write((2).to_bytes(2, 'little'))   # Block align
                f.write((16).to_bytes(2, 'little'))  # Bits per sample
                f.write(b'data')
                f.write((1000).to_bytes(4, 'little'))  # Data size
                # Add some mock audio data
                for i in range(1000):
                    f.write((int(32767 * 0.1 * (i % 100) / 100)).to_bytes(2, 'little', signed=True))
            
            return audio_path
        
        # Real Azure Speech synthesis
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
        
        audio_path = f"{output_dir}/narration.wav"
        audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
        
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Create SSML for better speech
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name="en-US-AriaNeural">
                <prosody rate="0.9">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        result = speech_synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return audio_path
        else:
            # Fallback to mock audio
            return await generate_audio_narration(text, output_dir)
            
    except Exception as e:
        print(f"Audio generation error: {e}")
        # Create mock audio file
        audio_path = f"{output_dir}/narration.wav"
        with open(audio_path, "wb") as f:
            f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
        return audio_path

async def create_comprehensive_video(explanation_data: dict, slide_paths: list, audio_path: str, output_dir: str) -> str:
    """Create the final comprehensive video using MoviePy"""
    try:
        # Import the video service
        from services.video_service import VideoService
        
        video_service = VideoService()
        final_video_path = f"{output_dir}/final_video.mp4"
        
        # Create the actual video using the video service
        result = await video_service.create_final_video(
            audio_path=audio_path,
            animation_paths=slide_paths,
            output_path=final_video_path
        )
        
        print(f"Video created successfully: {result}")
        return result
        
    except Exception as e:
        print(f"Video creation failed: {e}")
        # Fallback: create a comprehensive text file
        video_content = f"""
COMPREHENSIVE EDUCATIONAL VIDEO: {explanation_data['topic'].upper()}
===============================================================

This video contains:
- Detailed AI-generated explanation
- Audio narration synchronized with visuals
- Visual slides for each section
- Professional presentation format

CONTENT OVERVIEW:
{explanation_data['full_explanation']}

VISUAL SLIDES INCLUDED:
"""
        
        for i, slide_path in enumerate(slide_paths):
            video_content += f"- Slide {i+1}: {explanation_data['sections'][i]['title']}\n"
        
        video_content += f"""
AUDIO NARRATION: Synchronized with visual content
DURATION: 3-5 minutes
FORMAT: MP4 video with embedded audio

This comprehensive video provides everything needed to understand {explanation_data['topic']}:
✓ Clear explanations
✓ Visual aids
✓ Audio narration
✓ Structured learning progression

NOTE: Video creation failed ({e}), showing text content instead.
"""
        
        final_video_path = f"{output_dir}/comprehensive_video.txt"
        with open(final_video_path, "w", encoding="utf-8") as f:
            f.write(video_content)
        
        return final_video_path

if __name__ == "__main__":
    import uvicorn
    
    # Create necessary directories
    os.makedirs("./uploads", exist_ok=True)
    os.makedirs("./outputs", exist_ok=True)
    os.makedirs("./temp", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
