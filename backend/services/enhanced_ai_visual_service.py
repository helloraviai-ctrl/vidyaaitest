"""
Enhanced AI Visual Service that combines AI-generated visuals with professional slide design
"""

import os
import asyncio
from typing import Optional, Dict, Any, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap

from .ai_visual_service import AIVisualService
from .enhanced_visual_service import EnhancedVisualService

class EnhancedAIVisualService:
    """
    Enhanced AI visual service that combines AI-generated images with professional slide design
    """
    
    def __init__(self):
        """Initialize the enhanced AI visual service"""
        self.ai_visual_service = AIVisualService()
        self.enhanced_visual_service = EnhancedVisualService()
        self.use_ai_generation = self.ai_visual_service.use_ai_generation
        
        print(f"Enhanced AI Visual Service initialized. AI Generation: {self.use_ai_generation}")
    
    async def create_enhanced_slide_with_ai_visual(
        self, 
        section: Dict[str, Any], 
        section_index: int, 
        total_sections: int,
        topic: str,
        output_path: str,
        color_scheme: str = "professional"
    ) -> str:
        """Create an enhanced slide with AI-generated visual elements"""
        
        # Try to generate AI visual first
        ai_visual_path = None
        if self.use_ai_generation:
            try:
                ai_visual_path = await self._generate_ai_visual_for_section(
                    topic, section, section_index
                )
            except Exception as e:
                print(f"AI visual generation failed: {e}")
                ai_visual_path = None
        
        # Create the enhanced slide with or without AI visual
        if ai_visual_path:
            return await self._create_slide_with_ai_visual(
                section, section_index, total_sections, topic, 
                output_path, color_scheme, ai_visual_path
            )
        else:
            # Fallback to enhanced visual service
            return self.enhanced_visual_service.create_enhanced_slide(
                section, section_index, total_sections, topic, output_path, color_scheme
            )
    
    async def _generate_ai_visual_for_section(
        self, 
        topic: str, 
        section: Dict[str, Any], 
        section_index: int
    ) -> Optional[str]:
        """Generate AI visual for a specific section"""
        
        section_title = section.get("title", f"Section {section_index + 1}")
        content = section.get("content", "")
        visual_description = section.get("visual_description", "")
        
        # Determine visual type based on content
        visual_type = self._determine_visual_type(topic, content, visual_description)
        
        # Generate AI visual
        ai_visual_path = await self.ai_visual_service.generate_educational_visual(
            topic=topic,
            section_title=section_title,
            content=content,
            visual_type=visual_type
        )
        
        return ai_visual_path
    
    def _determine_visual_type(self, topic: str, content: str, visual_description: str) -> str:
        """Determine the best visual type based on content"""
        
        # Check visual description for hints
        if "diagram" in visual_description.lower():
            return "diagram"
        elif "chart" in visual_description.lower() or "graph" in visual_description.lower():
            return "chart"
        elif "illustration" in visual_description.lower() or "drawing" in visual_description.lower():
            return "illustration"
        elif "animation" in visual_description.lower() or "animated" in visual_description.lower():
            return "illustration"  # DALL-E doesn't do animations, use illustration
        
        # Check content for hints
        if "process" in content.lower() or "step" in content.lower():
            return "diagram"
        elif "data" in content.lower() or "statistics" in content.lower():
            return "chart"
        elif "structure" in content.lower() or "model" in content.lower():
            return "diagram"
        
        # Check topic for hints
        if any(word in topic.lower() for word in ["physics", "chemistry", "biology", "science"]):
            return "diagram"
        elif any(word in topic.lower() for word in ["math", "mathematics", "statistics"]):
            return "chart"
        elif any(word in topic.lower() for word in ["art", "design", "creative"]):
            return "illustration"
        
        # Default to diagram
        return "diagram"
    
    async def _create_slide_with_ai_visual(
        self, 
        section: Dict[str, Any], 
        section_index: int, 
        total_sections: int,
        topic: str,
        output_path: str,
        color_scheme: str,
        ai_visual_path: str
    ) -> str:
        """Create slide incorporating AI-generated visual"""
        
        # Load the AI-generated visual
        try:
            ai_visual = Image.open(ai_visual_path)
            ai_visual = ai_visual.convert('RGB')
            
            # Resize AI visual to fit slide
            ai_visual = self._resize_ai_visual(ai_visual)
            
            # Create the enhanced slide
            slide_path = self.enhanced_visual_service.create_enhanced_slide(
                section, section_index, total_sections, topic, output_path, color_scheme
            )
            
            # Load the slide and composite with AI visual
            slide = Image.open(slide_path)
            slide = self._composite_ai_visual_with_slide(slide, ai_visual, section)
            
            # Save the final slide
            slide.save(output_path, "PNG", quality=95, optimize=True)
            
            # Clean up temporary AI visual
            if os.path.exists(ai_visual_path):
                os.remove(ai_visual_path)
            
            return output_path
            
        except Exception as e:
            print(f"Error creating slide with AI visual: {e}")
            # Fallback to regular enhanced slide
            return self.enhanced_visual_service.create_enhanced_slide(
                section, section_index, total_sections, topic, output_path, color_scheme
            )
    
    def _resize_ai_visual(self, ai_visual: Image.Image) -> Image.Image:
        """Resize AI visual to appropriate size for slide"""
        
        # Target size for AI visual on slide
        target_width = 600
        target_height = 400
        
        # Maintain aspect ratio
        ai_visual.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Create new image with exact target size and paste centered
        resized_visual = Image.new('RGB', (target_width, target_height), (255, 255, 255))
        
        # Calculate position to center the visual
        x = (target_width - ai_visual.width) // 2
        y = (target_height - ai_visual.height) // 2
        
        resized_visual.paste(ai_visual, (x, y))
        
        return resized_visual
    
    def _composite_ai_visual_with_slide(
        self, 
        slide: Image.Image, 
        ai_visual: Image.Image, 
        section: Dict[str, Any]
    ) -> Image.Image:
        """Composite AI visual with the slide"""
        
        # Create a copy of the slide
        final_slide = slide.copy()
        
        # Position for AI visual (right side of slide)
        visual_x = 1300
        visual_y = 300
        
        # Create a semi-transparent overlay for the AI visual
        overlay = Image.new('RGBA', ai_visual.size, (255, 255, 255, 240))
        ai_visual_with_overlay = Image.alpha_composite(
            ai_visual.convert('RGBA'), overlay
        ).convert('RGB')
        
        # Add a subtle border to the AI visual
        border_size = 4
        bordered_visual = Image.new('RGB', 
            (ai_visual.width + border_size * 2, ai_visual.height + border_size * 2), 
            (59, 130, 246)  # Blue border
        )
        bordered_visual.paste(ai_visual_with_overlay, (border_size, border_size))
        
        # Paste the AI visual onto the slide
        final_slide.paste(bordered_visual, (visual_x, visual_y))
        
        # Add a label for the AI visual
        self._add_ai_visual_label(final_slide, visual_x, visual_y + ai_visual.height + 20)
        
        return final_slide
    
    def _add_ai_visual_label(self, slide: Image.Image, x: int, y: int):
        """Add a label for the AI visual"""
        
        draw = ImageDraw.Draw(slide)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Draw label
        label_text = "AI-Generated Visual"
        draw.text((x, y), label_text, fill=(59, 130, 246), font=font)
    
    async def create_multiple_enhanced_slides(
        self, 
        sections: List[Dict[str, Any]], 
        topic: str,
        output_dir: str,
        color_scheme: str = "professional"
    ) -> List[str]:
        """Create multiple enhanced slides with AI visuals"""
        
        slide_paths = []
        total_sections = len(sections)
        
        # Create slides with some parallel processing for AI visuals
        tasks = []
        for i, section in enumerate(sections):
            slide_path = f"{output_dir}/slide_{i+1}.png"
            task = self.create_enhanced_slide_with_ai_visual(
                section, i, total_sections, topic, slide_path, color_scheme
            )
            tasks.append(task)
        
        # Execute tasks with limited concurrency to avoid API rate limits
        semaphore = asyncio.Semaphore(2)  # Limit to 2 concurrent AI visual generations
        
        async def limited_task(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[limited_task(task) for task in tasks])
        slide_paths.extend(results)
        
        return slide_paths
