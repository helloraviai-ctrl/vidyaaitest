"""
Main FastAPI application for Vidya AI Educational Content Generator
Handles topic explanation generation, audio synthesis, and video creation
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import uuid
from typing import Optional, List
import asyncio
from dotenv import load_dotenv

# Import our custom modules
from services.ai_service_manager import AIServiceManager, ContentType
from services.azure_speech_service import AzureSpeechService
from services.animation_service import AnimationService
from services.video_service import VideoService
from models.content_models import TopicRequest, ContentResponse, ProcessingStatus

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
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service_manager = AIServiceManager()
azure_speech_service = AzureSpeechService()
animation_service = AnimationService()
video_service = VideoService()

# In-memory storage for processing status (in production, use Redis or database)
processing_jobs = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Vidya AI Educational Content Generator API", "status": "healthy"}

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: TopicRequest, background_tasks: BackgroundTasks):
    """
    Generate educational content for a given topic
    
    This endpoint:
    1. Generates a structured explanation using Groq AI
    2. Creates audio narration using Azure Speech
    3. Generates animated visuals using Manim
    4. Combines everything into a final video
    
    Args:
        request: TopicRequest containing the topic and optional parameters
        
    Returns:
        ContentResponse with job ID for tracking progress
    """
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
    """
    Get the current processing status for a job
    
    Args:
        job_id: Unique identifier for the processing job
        
    Returns:
        ProcessingStatus object with current progress
    """
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return processing_jobs[job_id]

@app.get("/api/download/{job_id}/{file_type}")
async def download_file(job_id: str, file_type: str):
    """
    Download generated files (audio, video, or text)
    
    Args:
        job_id: Unique identifier for the processing job
        file_type: Type of file to download (audio, video, text, or all)
        
    Returns:
        File download response
    """
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_status = processing_jobs[job_id]
    
    if job_status.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Determine file path based on type
    base_path = f"./outputs/{job_id}"
    
    if file_type == "audio":
        file_path = f"{base_path}/narration.wav"
    elif file_type == "video":
        file_path = f"{base_path}/final_video.mp4"
    elif file_type == "text":
        file_path = f"{base_path}/explanation.txt"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=f"{job_id}_{file_type}.{file_path.split('.')[-1]}",
        media_type='application/octet-stream'
    )

@app.get("/api/video/{job_id}")
async def get_video(job_id: str):
    """
    Get the generated video file for a job
    
    Args:
        job_id: Unique identifier for the processing job
        
    Returns:
        Video file response
    """
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_status = processing_jobs[job_id]
    
    if job_status.status != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    # Get video file path
    video_path = f"./outputs/{job_id}/final_video.mp4"
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        path=video_path,
        filename=f"{job_id}_video.mp4",
        media_type='video/mp4'
    )

async def process_content_generation(job_id: str, request: TopicRequest):
    """
    Background task to process content generation
    
    This function orchestrates the entire content generation pipeline:
    1. Generate explanation text using Groq AI
    2. Convert text to speech using Azure
    3. Generate animations for each section
    4. Combine audio and visuals into final video
    
    Args:
        job_id: Unique identifier for this processing job
        request: Original topic request
    """
    try:
        # Update status
        processing_jobs[job_id].update_status("generating_text", 10, "Generating explanation text...")
        
        # Step 1: Generate structured explanation using enhanced AI Service Manager
        explanation_data = await ai_service_manager.generate_enhanced_content(
            topic=request.topic,
            difficulty=request.difficulty_level.value,
            audience=request.target_audience.value,
            content_type=ContentType.EDUCATIONAL,
            speed_priority=True
        )
        
        # Save explanation text
        output_dir = f"./outputs/{job_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save structured explanation
        with open(f"{output_dir}/explanation.txt", "w", encoding="utf-8") as f:
            # Write structured content
            f.write("=== EDUCATIONAL CONTENT ===\n\n")
            f.write(f"Topic: {request.topic}\n")
            f.write(f"Summary: {explanation_data.get('summary', 'N/A')}\n\n")
            
            # Write each section
            sections = explanation_data.get("sections", [])
            for i, section in enumerate(sections):
                f.write(f"--- SLIDE {i+1} ---\n")
                f.write(f"Title: {section.get('title', 'N/A')}\n")
                f.write(f"Subheading: {section.get('subheading', 'N/A')}\n")
                f.write(f"Content: {section.get('content', 'N/A')}\n")
                f.write(f"Key Points:\n")
                for point in section.get('key_points', []):
                    f.write(f"  {point}\n")
                f.write(f"Visual: {section.get('visual_description', 'N/A')}\n\n")
            
            f.write("=== FULL NARRATION ===\n")
            f.write(explanation_data.get("full_explanation", "Content generation completed"))
        
        processing_jobs[job_id].update_status("generating_audio", 30, "Converting text to speech...")
        
        # Step 2: Generate audio narration
        audio_path = await azure_speech_service.text_to_speech(
            text=explanation_data.get("full_explanation", "Content generation completed"),
            output_path=f"{output_dir}/narration.wav",
            voice_name=request.voice_name
        )
        
        processing_jobs[job_id].update_status("generating_animations", 50, "Creating animated visuals...")
        
        # Step 3: Generate animations for each section
        animation_paths = []
        sections = explanation_data.get("sections", [])
        for i, section_data in enumerate(sections):
            # Convert dict to ContentSection object
            from models.content_models import ContentSection
            section = ContentSection(
                title=section_data.get("title", f"Section {i+1}"),
                subheading=section_data.get("subheading", ""),
                content=section_data.get("content", ""),
                key_points=section_data.get("key_points", []),
                visual_description=section_data.get("visual_description", ""),
                duration_estimate=section_data.get("duration_estimate", 30)
            )
            animation_path = await animation_service.create_section_animation(
                section=section,
                section_index=i,
                output_dir=output_dir
            )
            animation_paths.append(animation_path)
        
        processing_jobs[job_id].update_status("combining_video", 80, "Combining audio and visuals...")
        
        # Step 4: Combine audio and animations into final video
        final_video_path = await video_service.create_final_video(
            audio_path=audio_path,
            animation_paths=animation_paths,
            output_path=f"{output_dir}/final_video.mp4"
        )
        
        # Update final status
        processing_jobs[job_id].update_status(
            "completed", 
            100, 
            "Content generation completed successfully!",
            {
                "audio_path": audio_path,
                "video_path": final_video_path,
                "text_path": f"{output_dir}/explanation.txt",
                "sections": sections
            }
        )
        
    except Exception as e:
        # Update status with error
        processing_jobs[job_id].update_status(
            "failed", 
            processing_jobs[job_id].progress, 
            f"Content generation failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    # Create necessary directories
    os.makedirs("./uploads", exist_ok=True)
    os.makedirs("./outputs", exist_ok=True)
    os.makedirs("./temp", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=os.getenv("BACKEND_HOST", "0.0.0.0"),
        port=int(os.getenv("BACKEND_PORT", 8000)),
        reload=True
    )
