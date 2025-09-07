"""
Fast Content Generation Service - Optimized for speed
Generates structured educational content with visuals without heavy video processing
"""

import os
import asyncio
from typing import Dict, List, Any, Optional
from .ai_service_manager import AIServiceManager, ContentType
from .enhanced_ai_visual_service import EnhancedAIVisualService

class FastContentService:
    """
    Fast content generation service that prioritizes speed over heavy video processing
    """
    
    def __init__(self):
        """Initialize the fast content service"""
        self.ai_manager = AIServiceManager()
        self.visual_service = EnhancedAIVisualService()
        
        print("Fast Content Service initialized - Optimized for speed")
    
    async def generate_fast_content(
        self, 
        topic: str, 
        difficulty: str, 
        audience: str
    ) -> Dict[str, Any]:
        """
        Generate educational content quickly without heavy video processing
        
        Args:
            topic: The topic to explain
            difficulty: Difficulty level
            audience: Target audience
            
        Returns:
            Dictionary with structured content and visual paths
        """
        
        print(f"🚀 Generating fast content for: {topic}")
        
        # Step 1: Generate structured content using AI
        print("📝 Generating AI content...")
        content_data = await self.ai_manager.generate_enhanced_content(
            topic=topic,
            difficulty=difficulty,
            audience=audience,
            content_type=ContentType.EDUCATIONAL,
            speed_priority=True  # Prioritize speed
        )
        
        # Step 2: Generate visual slides quickly
        print("🎨 Creating visual slides...")
        visual_paths = await self._generate_fast_visuals(content_data, topic)
        
        # Step 3: Create summary for frontend
        result = {
            "topic": topic,
            "summary": content_data.get("summary", f"Educational content about {topic}"),
            "sections": content_data.get("sections", []),
            "key_concepts": content_data.get("key_concepts", []),
            "visual_paths": visual_paths,
            "estimated_duration": content_data.get("estimated_duration", 120),
            "generation_type": "fast"
        }
        
        print(f"✅ Fast content generation completed for: {topic}")
        return result
    
    async def _generate_fast_visuals(self, content_data: Dict[str, Any], topic: str) -> List[str]:
        """Generate visual slides quickly"""
        
        sections = content_data.get("sections", [])
        if not sections:
            return []
        
        # Create output directory
        import uuid
        job_id = str(uuid.uuid4())
        output_dir = f"./outputs/{job_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate slides with limited AI visual generation for speed
        visual_paths = []
        
        for i, section in enumerate(sections):
            slide_path = f"{output_dir}/slide_{i+1}.png"
            
            try:
                # Create slide with basic visual (no AI generation for speed)
                await self._create_fast_slide(section, i, len(sections), topic, slide_path)
                visual_paths.append(slide_path)
                print(f"✅ Created fast slide {i+1}: {slide_path}")
                
            except Exception as e:
                print(f"❌ Failed to create slide {i+1}: {e}")
                # Create a simple fallback slide
                await self._create_fallback_slide(section, i, len(sections), topic, slide_path)
                visual_paths.append(slide_path)
        
        return visual_paths
    
    async def _create_fast_slide(
        self, 
        section: Dict[str, Any], 
        section_index: int, 
        total_sections: int,
        topic: str,
        output_path: str
    ) -> str:
        """Create a fast slide without AI visual generation"""
        
        # Use the enhanced visual service but skip AI generation
        from .enhanced_visual_service import EnhancedVisualService
        visual_service = EnhancedVisualService()
        
        return visual_service.create_enhanced_slide(
            section=section,
            section_index=section_index,
            total_sections=total_sections,
            topic=topic,
            output_path=output_path,
            color_scheme="professional"
        )
    
    async def _create_fallback_slide(
        self, 
        section: Dict[str, Any], 
        section_index: int, 
        total_sections: int,
        topic: str,
        output_path: str
    ) -> str:
        """Create a simple fallback slide"""
        
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple slide
        img = Image.new('RGB', (1920, 1080), color='#1e293b')
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            content_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
        
        # Draw title
        title = section.get("title", f"Section {section_index + 1}")
        draw.text((100, 100), title, fill='white', font=title_font)
        
        # Draw content
        content = section.get("content", "Content not available")
        # Wrap text
        lines = []
        words = content.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=content_font)
            text_width = bbox[2] - bbox[0]
            
            if text_width < 1600:  # Max width
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        y = 200
        for line in lines[:10]:  # Max 10 lines
            draw.text((100, y), line, fill='#e2e8f0', font=content_font)
            y += 40
        
        # Draw key points
        key_points = section.get("key_points", [])
        if key_points:
            y += 50
            draw.text((100, y), "Key Points:", fill='#3b82f6', font=content_font)
            y += 50
            
            for point in key_points[:4]:  # Max 4 points
                draw.text((120, y), f"• {point}", fill='#e2e8f0', font=content_font)
                y += 40
        
        # Save the image
        img.save(output_path, "PNG", quality=85, optimize=True)
        
        return output_path
