"""
Enhanced Visual Content Generator
Creates professional, well-formatted visual slides with improved text layout
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from typing import List, Dict, Any, Tuple
import textwrap

class EnhancedVisualService:
    """
    Enhanced visual service for creating professional educational slides
    """
    
    def __init__(self):
        """Initialize the enhanced visual service"""
        self.fonts = self._load_fonts()
        self.color_schemes = self._get_color_schemes()
    
    def _load_fonts(self) -> Dict[str, ImageFont.FreeTypeFont]:
        """Load high-quality fonts with fallbacks"""
        fonts = {}
        font_configs = [
            ("title", 64, ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 
                          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]),
            ("subtitle", 48, ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]),
            ("content", 32, ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]),
            ("bullet", 28, ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                           "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]),
            ("small", 24, ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                          "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"])
        ]
        
        for name, size, paths in font_configs:
            font = None
            for path in paths:
                if os.path.exists(path):
                    try:
                        font = ImageFont.truetype(path, size)
                        break
                    except:
                        continue
            
            if not font:
                font = ImageFont.load_default()
            
            fonts[name] = font
        
        return fonts
    
    def _get_color_schemes(self) -> Dict[str, Dict[str, str]]:
        """Get professional color schemes"""
        return {
            "professional": {
                "bg_primary": "#1e293b",
                "bg_secondary": "#334155",
                "accent": "#3b82f6",
                "accent_light": "#60a5fa",
                "text_primary": "#ffffff",
                "text_secondary": "#e2e8f0",
                "text_muted": "#94a3b8",
                "highlight": "#fbbf24",
                "success": "#10b981",
                "warning": "#f59e0b"
            },
            "modern": {
                "bg_primary": "#0f172a",
                "bg_secondary": "#1e293b",
                "accent": "#8b5cf6",
                "accent_light": "#a78bfa",
                "text_primary": "#ffffff",
                "text_secondary": "#e2e8f0",
                "text_muted": "#94a3b8",
                "highlight": "#f59e0b",
                "success": "#10b981",
                "warning": "#ef4444"
            }
        }
    
    def create_enhanced_slide(
        self, 
        section: Dict[str, Any], 
        section_index: int, 
        total_sections: int,
        topic: str,
        output_path: str,
        color_scheme: str = "professional"
    ) -> str:
        """Create an enhanced professional slide"""
        colors = self.color_schemes[color_scheme]
        
        # Create high-resolution canvas
        img = Image.new('RGB', (1920, 1080), color=colors["bg_primary"])
        draw = ImageDraw.Draw(img)
        
        # Create sophisticated background
        self._create_background(img, draw, colors)
        
        # Add header section
        self._add_header(draw, topic, section_index, total_sections, colors)
        
        # Add main content with improved formatting
        self._add_main_content(draw, section, colors)
        
        # Add footer with progress
        self._add_footer(draw, section_index, total_sections, colors)
        
        # Save with high quality
        img.save(output_path, "PNG", quality=95, optimize=True)
        
        return output_path
    
    def _create_background(self, img: Image.Image, draw: ImageDraw.Draw, colors: Dict[str, str]):
        """Create sophisticated background with gradients and effects"""
        width, height = img.size
        
        # Create gradient background
        for y in range(height):
            ratio = y / height
            r = int(int(colors["bg_primary"][1:3], 16) * (1 - ratio * 0.3))
            g = int(int(colors["bg_primary"][3:5], 16) * (1 - ratio * 0.3))
            b = int(int(colors["bg_primary"][5:7], 16) * (1 - ratio * 0.3))
            color = (min(255, r), min(255, g), min(255, b))
            draw.line([(0, y), (width, y)], fill=color)
        
        # Add subtle geometric patterns
        center_x, center_y = width // 2, height // 2
        
        # Create subtle geometric elements
        for i in range(3):
            radius = 150 + i * 100
            for angle in range(0, 360, 45):
                x = center_x + radius * math.cos(math.radians(angle))
                y = center_y + radius * math.sin(math.radians(angle))
                # Draw subtle circles
                draw.ellipse([x-15, y-15, x+15, y+15], 
                           fill=(*self._hex_to_rgb(colors["accent"]), 20),
                           outline=(*self._hex_to_rgb(colors["accent"]), 40))
        
        # Add floating particles
        for i in range(20):
            x = (i * 96 + random.randint(0, 50)) % width
            y = (i * 54 + random.randint(0, 30)) % height
            size = random.randint(2, 6)
            draw.ellipse([x-size, y-size, x+size, y+size], 
                        fill=(*self._hex_to_rgb(colors["accent_light"]), 60))
    
    def _add_header(self, draw: ImageDraw.Draw, topic: str, section_index: int, total_sections: int, colors: Dict[str, str]):
        """Add professional header section"""
        # Topic title
        topic_text = f"📚 {topic.title()}"
        self._draw_text_with_effects(draw, (80, 60), topic_text, self.fonts["title"], 
                                   colors["text_primary"], colors["accent"], 3)
        
        # Section indicator
        section_text = f"Section {section_index + 1} of {total_sections}"
        self._draw_text_with_effects(draw, (1600, 60), section_text, self.fonts["small"], 
                                   colors["success"], colors["bg_secondary"], 2)
        
        # Decorative line
        draw.line([(80, 140), (1840, 140)], fill=colors["accent"], width=3)
    
    def _add_main_content(self, draw: ImageDraw.Draw, section: Dict[str, Any], colors: Dict[str, str]):
        """Add main content with improved formatting"""
        # Section title
        title = section.get("title", "Untitled Section")
        self._draw_text_with_effects(draw, (100, 180), title, self.fonts["subtitle"], 
                                   colors["text_primary"], colors["accent"], 4)
        
        # Decorative line under title
        draw.line([(100, 250), (900, 250)], fill=colors["accent"], width=4)
        
        # Main content area
        content = section.get("content", "")
        formatted_content = self._format_content_for_display(content)
        
        # Create content box
        content_box = (80, 300, 1200, 700)
        self._draw_content_box(draw, content_box, colors)
        
        # Draw formatted content
        self._draw_formatted_content(draw, (100, 320), formatted_content, colors)
        
        # Key points section
        if "key_points" in section and section["key_points"]:
            self._add_key_points_section(draw, section["key_points"], colors)
        
        # Visual description
        if "visual_description" in section and section["visual_description"]:
            self._add_visual_description(draw, section["visual_description"], colors)
    
    def _add_key_points_section(self, draw: ImageDraw.Draw, key_points: List[str], colors: Dict[str, str]):
        """Add enhanced key points section"""
        # Key points box
        box_x, box_y = 1300, 300
        box_width, box_height = 500, 400
        
        # Draw key points background
        draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], 
                      fill=(*self._hex_to_rgb(colors["highlight"]), 30),
                      outline=(*self._hex_to_rgb(colors["highlight"]), 80))
        
        # Key points title
        self._draw_text_with_effects(draw, (box_x + 20, box_y + 20), "Key Points:", 
                                   self.fonts["bullet"], colors["highlight"], colors["bg_secondary"], 2)
        
        # Draw key points
        for i, point in enumerate(key_points[:5]):  # Max 5 points
            point_y = box_y + 70 + (i * 60)
            if point_y < box_y + box_height - 20:
                formatted_point = self._format_key_point(point)
                bullet_text = f"• {formatted_point}"
                self._draw_text_with_effects(draw, (box_x + 30, point_y), bullet_text, 
                                           self.fonts["bullet"], colors["text_secondary"], 
                                           colors["bg_secondary"], 1)
    
    def _add_visual_description(self, draw: ImageDraw.Draw, visual_desc: str, colors: Dict[str, str]):
        """Add visual description section"""
        desc_y = 750
        desc_text = f"Visual: {visual_desc[:100]}..."
        self._draw_text_with_effects(draw, (100, desc_y), desc_text, self.fonts["small"], 
                                   colors["accent_light"], colors["bg_secondary"], 1)
    
    def _add_footer(self, draw: ImageDraw.Draw, section_index: int, total_sections: int, colors: Dict[str, str]):
        """Add professional footer with progress"""
        # Progress bar
        progress_width = 600
        progress_height = 12
        progress_x = 100
        progress_y = 950
        
        # Progress background
        draw.rectangle([progress_x, progress_y, progress_x + progress_width, progress_y + progress_height], 
                      fill=colors["bg_secondary"], outline=colors["accent"])
        
        # Progress fill
        progress_fill = (section_index + 1) / total_sections
        fill_width = int(progress_width * progress_fill)
        draw.rectangle([progress_x, progress_y, progress_x + fill_width, progress_y + progress_height], 
                      fill=colors["accent"])
        
        # Progress text
        progress_text = f"{int(progress_fill * 100)}%"
        self._draw_text_with_effects(draw, (progress_x + progress_width + 20, progress_y - 5), 
                                   progress_text, self.fonts["small"], colors["text_muted"], 
                                   colors["bg_secondary"], 1)
    
    def _draw_content_box(self, draw: ImageDraw.Draw, box: Tuple[int, int, int, int], colors: Dict[str, str]):
        """Draw content box with glass effect"""
        x1, y1, x2, y2 = box
        
        # Glass effect background
        for alpha in range(20, 0, -2):
            color = (*self._hex_to_rgb(colors["text_primary"]), alpha)
            draw.rectangle([x1-alpha, y1-alpha, x2+alpha, y2+alpha], 
                          outline=color, width=1)
        
        # Main content background
        draw.rectangle(box, fill=(*self._hex_to_rgb(colors["text_primary"]), 15), 
                      outline=(*self._hex_to_rgb(colors["text_primary"]), 40))
    
    def _draw_formatted_content(self, draw: ImageDraw.Draw, position: Tuple[int, int], content: str, colors: Dict[str, str]):
        """Draw content with proper formatting and spacing"""
        x, y = position
        max_width = 1000
        
        # Split into paragraphs
        paragraphs = content.split('\n\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                y += 30
                continue
            
            # Handle line breaks within paragraphs
            lines = paragraph.split('\n')
            
            for line in lines:
                if not line.strip():
                    y += 25
                    continue
                
                # Word wrap
                wrapped_lines = self._wrap_text(line, self.fonts["content"], max_width)
                
                for wrapped_line in wrapped_lines:
                    self._draw_text_with_effects(draw, (x, y), wrapped_line, self.fonts["content"], 
                                               colors["text_secondary"], colors["bg_secondary"], 1)
                    y += 35
                
                y += 10  # Extra space between lines
            
            y += 20  # Space between paragraphs
    
    def _draw_text_with_effects(self, draw: ImageDraw.Draw, position: Tuple[int, int], text: str, 
                               font: ImageFont.FreeTypeFont, text_color: str, outline_color: str, outline_width: int):
        """Draw text with professional effects"""
        x, y = position
        
        # Draw outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)
    
    def _format_content_for_display(self, content: str) -> str:
        """Format content for better display"""
        # Clean up the text
        content = content.strip()
        
        # Add proper paragraph breaks
        content = content.replace('. ', '.\n\n')
        content = content.replace('! ', '!\n\n')
        content = content.replace('? ', '?\n\n')
        
        # Clean up multiple line breaks
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        
        # Ensure proper capitalization
        sentences = content.split('.')
        formatted_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if sentence and not sentence[0].isupper():
                    sentence = sentence[0].upper() + sentence[1:]
                formatted_sentences.append(sentence)
        
        content = '. '.join(formatted_sentences)
        if content and not content.endswith('.'):
            content += '.'
        
        # Limit length for display
        if len(content) > 800:
            truncated = content[:800]
            last_period = truncated.rfind('.')
            if last_period > 600:
                content = truncated[:last_period + 1] + "..."
            else:
                content = truncated + "..."
        
        return content
    
    def _format_key_point(self, point: str) -> str:
        """Format individual key points"""
        point = point.strip()
        if point and not point[0].isupper():
            point = point[0].upper() + point[1:]
        if point and not point.endswith('.'):
            point += '.'
        return point
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
