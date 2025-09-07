"""
AI-powered visual generation service for educational content
"""

import os
import requests
import base64
from typing import Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import io

class AIVisualService:
    """
    Service for generating AI-powered visuals for educational content
    
    This service can integrate with various AI image generation APIs:
    - OpenAI DALL-E
    - Stability AI
    - Midjourney API
    - Custom AI models
    """
    
    def __init__(self):
        """Initialize AI visual service"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.stability_api_key = os.getenv("STABILITY_API_KEY")
        self.use_ai_generation = bool(self.openai_api_key or self.stability_api_key)
        
        if not self.use_ai_generation:
            print("No AI API keys found. Using fallback visual generation.")
    
    async def generate_educational_visual(
        self, 
        topic: str, 
        section_title: str, 
        content: str,
        visual_type: str = "diagram"
    ) -> Optional[str]:
        """
        Generate an AI-powered visual for educational content
        
        Args:
            topic: Main topic of the content
            section_title: Title of the section
            content: Content description
            visual_type: Type of visual (diagram, illustration, chart, etc.)
            
        Returns:
            Path to generated image or None if generation fails
        """
        if not self.use_ai_generation:
            return None
        
        try:
            # Create a detailed prompt for AI generation
            prompt = self._create_visual_prompt(topic, section_title, content, visual_type)
            
            # Try different AI services
            if self.openai_api_key:
                return await self._generate_with_dalle(prompt)
            elif self.stability_api_key:
                return await self._generate_with_stability(prompt)
            
        except Exception as e:
            print(f"AI visual generation failed: {e}")
            return None
    
    def _create_visual_prompt(
        self, 
        topic: str, 
        section_title: str, 
        content: str,
        visual_type: str
    ) -> str:
        """Create a detailed prompt for AI image generation with enhanced specificity"""
        
        # Base prompt structure with enhanced detail
        base_prompt = f"Create a professional educational {visual_type} for: {section_title}. "
        
        # Add topic-specific details with more specificity
        if "physics" in topic.lower() or "newton" in topic.lower() or "force" in topic.lower():
            base_prompt += "Show physics concepts with clear diagrams, arrows, and scientific notation. Use blue and red colors for forces and motion. Include vector arrows, mathematical symbols, and clean geometric shapes."
        elif "biology" in topic.lower() or "photosynthesis" in topic.lower() or "cell" in topic.lower():
            base_prompt += "Show biological processes with green colors for plants, yellow for sunlight, and clear process arrows. Include cellular structures, molecular diagrams, and natural organic shapes."
        elif "chemistry" in topic.lower() or "atom" in topic.lower() or "molecule" in topic.lower():
            base_prompt += "Show molecular structures, chemical bonds, and atomic models with scientific accuracy. Use colorful spheres for atoms, lines for bonds, and include chemical formulas."
        elif "mathematics" in topic.lower() or "math" in topic.lower() or "equation" in topic.lower():
            base_prompt += "Show mathematical concepts with clear equations, graphs, and geometric shapes. Use clean lines, mathematical symbols, and coordinate systems."
        elif "ai" in topic.lower() or "artificial intelligence" in topic.lower() or "machine learning" in topic.lower():
            base_prompt += "Show AI concepts with neural networks, data flows, and computer elements. Use blue and purple colors, circuit patterns, and modern tech aesthetics."
        elif "history" in topic.lower() or "war" in topic.lower() or "ancient" in topic.lower():
            base_prompt += "Show historical elements with period-appropriate imagery, maps, and cultural symbols. Use warm earth tones and classical design elements."
        else:
            base_prompt += "Show the main concept with clear visual metaphors, diagrams, and educational elements. Use professional colors and clean design."
        
        # Add content-specific elements
        if "law" in content.lower() or "principle" in content.lower():
            base_prompt += " Include numbered steps, principles, or rules with clear hierarchy."
        if "process" in content.lower() or "step" in content.lower():
            base_prompt += " Show a step-by-step process with arrows, flow diagrams, and sequential elements."
        if "comparison" in content.lower() or "vs" in content.lower() or "difference" in content.lower():
            base_prompt += " Show side-by-side comparisons, before/after states, or contrasting elements."
        if "timeline" in content.lower() or "history" in content.lower():
            base_prompt += " Include chronological elements, timeline markers, and historical progression."
        
        # Enhanced style requirements
        base_prompt += " Style: Modern, clean, educational, professional, high contrast, suitable for students and presentations. Use flat design principles, avoid text overlays, focus on visual elements. Color palette should be vibrant but not overwhelming. Include subtle gradients and shadows for depth."
        
        return base_prompt
    
    async def _generate_with_dalle(self, prompt: str) -> Optional[str]:
        """Generate image using OpenAI DALL-E"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.openai_api_key)
            
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="512x512",  # Smaller size for faster generation
                quality="standard",
                n=1
            )
            
            # Download and save the image
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Save to temporary file
            temp_path = f"/tmp/ai_visual_{hash(prompt)}.png"
            with open(temp_path, 'wb') as f:
                f.write(image_response.content)
            
            return temp_path
            
        except Exception as e:
            print(f"DALL-E generation failed: {e}")
            return None
    
    async def _generate_with_stability(self, prompt: str) -> Optional[str]:
        """Generate image using Stability AI"""
        try:
            url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
            
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.stability_api_key}"
            }
            
            data = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1
                    }
                ],
                "cfg_scale": 7,
                "height": 512,  # Smaller size for faster generation
                "width": 512,
                "samples": 1,
                "steps": 20  # Fewer steps for faster generation
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            
            # Decode and save the image
            image_data = base64.b64decode(result["artifacts"][0]["base64"])
            temp_path = f"/tmp/ai_visual_{hash(prompt)}.png"
            
            with open(temp_path, 'wb') as f:
                f.write(image_data)
            
            return temp_path
            
        except Exception as e:
            print(f"Stability AI generation failed: {e}")
            return None
    
    def create_fallback_visual(self, topic: str, section_title: str, output_path: str) -> str:
        """
        Create a fallback visual when AI generation is not available
        
        Args:
            topic: Main topic
            section_title: Section title
            output_path: Where to save the visual
            
        Returns:
            Path to the created visual
        """
        # Create a simple but effective visual
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=(245, 248, 250))
        draw = ImageDraw.Draw(image)
        
        # Try to load a font
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Draw title
        draw.text((50, 50), section_title, fill='darkblue', font=title_font)
        
        # Draw topic-specific visual elements
        if "physics" in topic.lower() or "newton" in topic.lower():
            self._draw_physics_fallback(draw, width, height)
        elif "biology" in topic.lower():
            self._draw_biology_fallback(draw, width, height)
        elif "chemistry" in topic.lower():
            self._draw_chemistry_fallback(draw, width, height)
        else:
            self._draw_generic_fallback(draw, width, height, section_title)
        
        # Save the image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path, 'PNG')
        
        return output_path
    
    def _draw_physics_fallback(self, draw, width, height):
        """Draw physics-themed fallback visual"""
        # Draw force arrows
        for i in range(3):
            x = 200 + i * 150
            y = 300
            self._draw_arrow(draw, (x, y), (x + 80, y), 'red')
            draw.text((x, y + 20), f"Force {i+1}", fill='red', font=ImageFont.load_default())
        
        # Draw object
        draw.ellipse([400, 250, 500, 350], fill='blue', outline='darkblue', width=3)
        draw.text((420, 360), "Object", fill='blue', font=ImageFont.load_default())
    
    def _draw_biology_fallback(self, draw, width, height):
        """Draw biology-themed fallback visual"""
        # Draw plant/leaf
        draw.ellipse([300, 200, 500, 400], fill='green', outline='darkgreen', width=3)
        draw.text((350, 420), "Plant", fill='green', font=ImageFont.load_default())
        
        # Draw sun
        draw.ellipse([100, 100, 200, 200], fill='yellow', outline='orange', width=3)
        draw.text((120, 220), "Sun", fill='orange', font=ImageFont.load_default())
        
        # Draw arrows
        self._draw_arrow(draw, (200, 150), (300, 250), 'orange')
    
    def _draw_chemistry_fallback(self, draw, width, height):
        """Draw chemistry-themed fallback visual"""
        # Draw atoms
        for i in range(3):
            x = 200 + i * 150
            y = 300
            draw.ellipse([x-20, y-20, x+20, y+20], fill='lightblue', outline='blue', width=2)
            draw.text((x-10, y+30), f"Atom {i+1}", fill='blue', font=ImageFont.load_default())
        
        # Draw bonds
        for i in range(2):
            x1 = 220 + i * 150
            x2 = 280 + i * 150
            draw.line([x1, 300, x2, 300], fill='black', width=3)
    
    def _draw_generic_fallback(self, draw, width, height, title):
        """Draw generic fallback visual"""
        # Draw a simple diagram
        center_x, center_y = width // 2, height // 2
        
        # Main concept circle
        draw.ellipse([center_x-50, center_y-50, center_x+50, center_y+50], 
                    fill='lightblue', outline='blue', width=3)
        draw.text((center_x-30, center_y-10), "Main", fill='blue', font=ImageFont.load_default())
        
        # Related concepts
        for i in range(4):
            import math
            angle = i * 90
            x = center_x + 120 * math.cos(math.radians(angle))
            y = center_y + 120 * math.sin(math.radians(angle))
            
            draw.ellipse([x-30, y-30, x+30, y+30], 
                        fill='lightgreen', outline='green', width=2)
            draw.text((x-20, y-5), f"Item {i+1}", fill='green', font=ImageFont.load_default())
            
            # Connection line
            draw.line([center_x+50, center_y, x-30, y], fill='gray', width=2)
    
    def _draw_arrow(self, draw, start, end, color):
        """Draw an arrow from start to end"""
        # Draw main line
        draw.line([start, end], fill=color, width=3)
        
        # Calculate arrowhead
        import math
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        arrow_length = 15
        arrow_angle = math.pi / 6
        
        # Arrowhead points
        head1_x = end[0] - arrow_length * math.cos(angle - arrow_angle)
        head1_y = end[1] - arrow_length * math.sin(angle - arrow_angle)
        head2_x = end[0] - arrow_length * math.cos(angle + arrow_angle)
        head2_y = end[1] - arrow_length * math.sin(angle + arrow_angle)
        
        # Draw arrowhead
        draw.line([end, (head1_x, head1_y)], fill=color, width=3)
        draw.line([end, (head2_x, head2_y)], fill=color, width=3)

