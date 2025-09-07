"""
Pydantic models for content generation requests and responses
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class DifficultyLevel(str, Enum):
    """Enumeration for difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class TargetAudience(str, Enum):
    """Enumeration for target audiences"""
    CHILDREN = "children"
    STUDENTS = "students"
    ADULTS = "adults"
    PROFESSIONALS = "professionals"

class TopicRequest(BaseModel):
    """
    Request model for topic-based content generation
    
    Attributes:
        topic: The main topic to explain
        difficulty_level: Target difficulty level for the explanation
        target_audience: Intended audience for the content
        voice_name: Azure voice to use for narration (optional)
        animation_style: Style of animations to generate (optional)
        duration_preference: Preferred video duration in minutes (optional)
    """
    topic: str = Field(..., min_length=1, max_length=200, description="The topic to explain")
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER, description="Difficulty level")
    target_audience: TargetAudience = Field(default=TargetAudience.STUDENTS, description="Target audience")
    voice_name: Optional[str] = Field(default=None, description="Azure voice name for narration")
    animation_style: Optional[str] = Field(default="hand_drawn", description="Animation style preference")
    duration_preference: Optional[int] = Field(default=5, ge=1, le=30, description="Preferred duration in minutes")

class ContentSection(BaseModel):
    """
    Model for individual content sections following structured educational slide format
    
    Attributes:
        title: Section title with emoji (e.g., "🌍 Explain Gravity")
        subheading: Bold, underlined question or definition
        content: Main content text (3-5 sentences, boxed format)
        key_points: List of key points to highlight (3-4 points, max 10 words each)
        visual_description: Description of what should be visualized
        duration_estimate: Estimated duration for this section in seconds
    """
    title: str
    subheading: Optional[str] = None
    content: str
    key_points: List[str]
    visual_description: str
    duration_estimate: int

class ContentResponse(BaseModel):
    """
    Response model for content generation requests
    
    Attributes:
        job_id: Unique identifier for tracking the generation process
        status: Current status of the generation process
        message: Human-readable status message
    """
    job_id: str
    status: str
    message: str

class ProcessingStatus(BaseModel):
    """
    Model for tracking processing status
    
    Attributes:
        job_id: Unique identifier for the job
        status: Current processing status
        progress: Progress percentage (0-100)
        message: Current status message
        result_data: Optional result data when completed
        error: Optional error message if failed
    """
    job_id: str
    status: str
    progress: int = 0
    message: str = ""
    result_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def update_status(self, status: str, progress: int, message: str, result_data: Optional[Dict[str, Any]] = None):
        """Update the processing status"""
        self.status = status
        self.progress = progress
        self.message = message
        if result_data:
            self.result_data = result_data

class ExplanationData(BaseModel):
    """
    Model for structured explanation data from Groq AI
    
    Attributes:
        full_explanation: Complete explanation text
        sections: List of structured sections
        key_concepts: List of key concepts to highlight
        summary: Brief summary of the topic
        estimated_duration: Estimated total duration in seconds
    """
    full_explanation: str
    sections: List[ContentSection]
    key_concepts: List[str]
    summary: str
    estimated_duration: int

class AudioGenerationRequest(BaseModel):
    """
    Request model for audio generation
    
    Attributes:
        text: Text to convert to speech
        voice_name: Azure voice name
        output_format: Audio output format
        speaking_rate: Speech rate (optional)
    """
    text: str
    voice_name: Optional[str] = "en-US-AriaNeural"
    output_format: str = "wav"
    speaking_rate: Optional[float] = 1.0

class AnimationRequest(BaseModel):
    """
    Request model for animation generation
    
    Attributes:
        section: Content section to animate
        style: Animation style
        duration: Animation duration in seconds
        output_format: Video output format
    """
    section: ContentSection
    style: str = "hand_drawn"
    duration: int
    output_format: str = "mp4"

class VideoCombinationRequest(BaseModel):
    """
    Request model for video combination
    
    Attributes:
        audio_path: Path to audio file
        animation_paths: List of animation file paths
        output_path: Output video path
        transition_duration: Duration of transitions between sections
    """
    audio_path: str
    animation_paths: List[str]
    output_path: str
    transition_duration: float = 0.5
