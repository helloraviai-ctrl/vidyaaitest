"""High-quality animation service for creating educational visuals"""
import os
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from models.content_models import ContentSection

class AnimationService:
    def __init__(self):
        self.output_dir = "./outputs"
        # Try to load high-quality fonts
        self.title_font = self._load_font(48)
        self.subtitle_font = self._load_font(24)
        self.body_font = self._load_font(20)
        self.bullet_font = self._load_font(18)
    
    def _load_font(self, size):
        """Load a high-quality font with fallbacks"""
        try:
            # Try to use system fonts first
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/System/Library/Fonts/Arial.ttf",  # macOS
                "/Windows/Fonts/arial.ttf",  # Windows
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            
            # Fallback to default font but with larger size
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    async def create_section_animation(self, section: ContentSection, section_index: int, output_dir: str) -> str:
        """Create professional e-learning quality slide for a content section"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Create high-resolution image (1920x1080 for better quality)
        img = Image.new('RGB', (1920, 1080), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add professional gradient background
        self._add_professional_gradient_background(img, draw)
        
        # 1. BIG TITLE - Emoji + bold + centered
        title = section.title
        self._draw_professional_title(draw, title, (960, 100))
        
        # 2. SUBTITLE/QUESTION - Bold italic
        subtitle = section.subheading.replace('**', '').replace('*', '')  # Clean markdown
        self._draw_professional_subtitle(draw, subtitle, (960, 180))
        
        # 3. MAIN EXPLANATION BOX - Professional content box
        content = section.content
        self._draw_professional_content_box(draw, content, (150, 250), (1770, 450))
        
        # 4. KEY POINTS LIST - Professional bulleted list
        key_points = section.key_points
        self._draw_professional_key_points(draw, key_points, (150, 500))
        
        # 5. VISUAL INSTRUCTION - Professional visual suggestion
        visual_desc = section.visual_description
        self._draw_professional_visual_instruction(draw, visual_desc, (150, 750))
        
        # Add slide number at bottom right
        section_text = f"Slide {section_index + 1}"
        self._draw_professional_slide_number(draw, section_text, (1700, 1000))
        
        # Save the image with high quality
        output_path = os.path.join(output_dir, f"section_{section_index}.png")
        img.save(output_path, "PNG", quality=100, optimize=True)
        
        return output_path
    
    def _add_gradient_background(self, img, draw):
        """Add a professional gradient background"""
        width, height = img.size
        for y in range(height):
            # Create a professional gradient from dark blue to light blue
            progress = y / height
            r = int(30 + (200 - 30) * progress)  # 30 to 200
            g = int(41 + (220 - 41) * progress)  # 41 to 220
            b = int(59 + (255 - 59) * progress)  # 59 to 255
            color = (r, g, b)
            draw.line([(0, y), (width, y)], fill=color)
    
    def _draw_text_with_shadow(self, draw, text, position, font, text_color, shadow_color):
        """Draw text with a shadow effect for better readability"""
        x, y = position
        
        # Center the text horizontally
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        centered_x = x - text_width // 2
        
        # Draw shadow (offset by 2 pixels)
        draw.text((centered_x + 2, y + 2), text, font=font, fill=shadow_color)
        
        # Draw main text
        draw.text((centered_x, y), text, font=font, fill=text_color)
    
    def _draw_multiline_text(self, draw, text, position, font, color, max_width):
        """Draw multiline text with proper wrapping"""
        x, y = position
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
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
        
        # Draw each line
        for line in lines:
            self._draw_text_with_shadow(draw, line, (x, y), font, color, 'lightgray')
            y += 35  # Line spacing
    
    def _format_content(self, content):
        """Format content for better readability"""
        # Truncate if too long
        if len(content) > 500:
            content = content[:500] + "..."
        
        # Add some basic formatting
        content = content.replace('. ', '.\n')
        content = content.replace('! ', '!\n')
        content = content.replace('? ', '?\n')
        
        return content
    
    def _draw_title_section(self, draw, title, position):
        """Draw the title section - big, clear headline with emoji"""
        x, y = position
        # Ensure title has emoji if not present
        if not any(ord(char) > 127 for char in title):  # Check if emoji present
            # Add default emoji based on topic
            if 'gravity' in title.lower():
                title = f"🌍 {title}"
            elif 'electricity' in title.lower():
                title = f"⚡ {title}"
            elif 'photosynthesis' in title.lower():
                title = f"🌱 {title}"
            elif 'machine learning' in title.lower() or 'ai' in title.lower():
                title = f"🤖 {title}"
            else:
                title = f"📚 {title}"
        
        # Draw title with large font and shadow, centered
        self._draw_text_with_shadow(draw, title, (x, y), self.title_font, 'white', 'black')
    
    def _draw_subheading_section(self, draw, subtitle, position):
        """Draw the subheading/question - bold, underlined text"""
        x, y = position
        # Draw subtitle with underline effect
        self._draw_text_with_shadow(draw, subtitle, (x, y), self.subtitle_font, 'yellow', 'black')
        # Add underline
        bbox = draw.textbbox((x, y), subtitle, font=self.subtitle_font)
        text_width = bbox[2] - bbox[0]
        draw.line([(x - text_width//2, y + 35), (x + text_width//2, y + 35)], fill='yellow', width=3)
    
    def _draw_explanation_box(self, draw, content, start_pos, end_pos):
        """Draw the main explanation in a clean text box"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Draw box background
        draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255, 200), outline='white', width=3)
        
        # Draw content inside box
        self._draw_multiline_text(draw, content, (x1 + 20, y1 + 20), self.body_font, 'black', x2 - x1 - 40)
    
    def _draw_key_points_section(self, draw, key_points, position):
        """Draw key points as a bulleted list with consistent formatting"""
        x, y = position
        y_pos = y
        
        for i, point in enumerate(key_points[:4]):  # Show up to 4 points
            # Clean up the point text - remove any existing bullets
            clean_point = point.replace('•', '').replace('*', '').strip()
            # Ensure single bullet point
            bullet_text = f"• {clean_point}"
            self._draw_text_with_shadow(draw, bullet_text, (x, y_pos), self.bullet_font, 'yellow', 'black')
            y_pos += 50
    
    def _draw_visual_suggestion(self, draw, visual_desc, position):
        """Draw the visual suggestion"""
        x, y = position
        if visual_desc:
            # Clean up the visual description
            visual_text = visual_desc.replace('Visual: ', '').replace('Visual:', '')
            visual_text = f"Visual: {visual_text[:80]}..." if len(visual_text) > 80 else f"Visual: {visual_text}"
            self._draw_text_with_shadow(draw, visual_text, (x, y), self.subtitle_font, 'lightblue', 'black')
    
    def _add_clean_gradient_background(self, img, draw):
        """Add a clean, simple gradient background"""
        width, height = img.size
        for y in range(height):
            # Create a clean gradient from dark blue to light blue
            progress = y / height
            r = int(25 + (100 - 25) * progress)  # 25 to 100
            g = int(50 + (150 - 50) * progress)  # 50 to 150
            b = int(100 + (200 - 100) * progress)  # 100 to 200
            color = (r, g, b)
            draw.line([(0, y), (width, y)], fill=color)
    
    def _draw_clean_title(self, draw, title, position):
        """Draw a clean, simple title with emoji"""
        x, y = position
        
        # Ensure title has emoji
        if not any(ord(char) > 127 for char in title):
            if 'gravity' in title.lower():
                title = f"🌍 {title}"
            elif 'electricity' in title.lower():
                title = f"⚡ {title}"
            elif 'photosynthesis' in title.lower():
                title = f"🌱 {title}"
            elif 'machine learning' in title.lower() or 'ai' in title.lower():
                title = f"🤖 {title}"
            else:
                title = f"📚 {title}"
        
        # Draw title centered with shadow
        self._draw_centered_text_with_shadow(draw, title, (x, y), self.title_font, 'white', 'black')
    
    def _draw_clean_subheading(self, draw, subtitle, position):
        """Draw a clean subheading"""
        x, y = position
        # Draw subtitle centered with shadow
        self._draw_centered_text_with_shadow(draw, subtitle, (x, y), self.subtitle_font, 'yellow', 'black')
    
    def _draw_clean_content_box(self, draw, content, start_pos, end_pos):
        """Draw a clean content box with proper text"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Draw clean white box with border
        draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255, 230), outline='white', width=2)
        
        # Draw content inside box with proper margins
        self._draw_wrapped_text(draw, content, (x1 + 30, y1 + 30), self.body_font, 'black', x2 - x1 - 60)
    
    def _draw_clean_key_points(self, draw, key_points, position):
        """Draw clean key points with consistent bullets"""
        x, y = position
        y_pos = y
        
        for i, point in enumerate(key_points[:4]):
            # Clean up the point text
            clean_point = point.replace('•', '').replace('*', '').strip()
            bullet_text = f"• {clean_point}"
            
            # Draw with proper spacing
            self._draw_simple_text(draw, bullet_text, (x, y_pos), self.bullet_font, 'yellow')
            y_pos += 45
    
    def _draw_clean_visual_suggestion(self, draw, visual_desc, position):
        """Draw clean visual suggestion"""
        x, y = position
        if visual_desc:
            # Clean up the visual description
            visual_text = visual_desc.replace('Visual: ', '').replace('Visual:', '')
            visual_text = f"Visual: {visual_text[:100]}..." if len(visual_text) > 100 else f"Visual: {visual_text}"
            self._draw_simple_text(draw, visual_text, (x, y), self.subtitle_font, 'lightblue')
    
    def _draw_centered_text_with_shadow(self, draw, text, position, font, text_color, shadow_color):
        """Draw centered text with shadow"""
        x, y = position
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        centered_x = x - text_width // 2
        
        # Draw shadow
        draw.text((centered_x + 2, y + 2), text, font=font, fill=shadow_color)
        # Draw main text
        draw.text((centered_x, y), text, font=font, fill=text_color)
    
    def _draw_simple_text(self, draw, text, position, font, color):
        """Draw simple text without shadow"""
        x, y = position
        draw.text((x, y), text, font=font, fill=color)
    
    def _draw_wrapped_text(self, draw, text, position, font, color, max_width):
        """Draw wrapped text with proper line breaks"""
        x, y = position
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
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
        
        # Draw each line
        for line in lines:
            draw.text((x, y), line, font=font, fill=color)
            y += 35  # Line spacing
    
    def _add_professional_gradient_background(self, img, draw):
        """Add a clean white background matching the app theme"""
        width, height = img.size
        # Fill with clean white background like the app
        draw.rectangle([0, 0, width, height], fill=(255, 255, 255))
        
        # Add a very subtle light gradient for depth (barely visible)
        for y in range(height):
            progress = y / height
            r = int(250 + (255 - 250) * progress)   # 250 to 255
            g = int(250 + (255 - 250) * progress)  # 250 to 255
            b = int(255 + (255 - 255) * progress)  # 255 to 255
            color = (r, g, b)
            draw.line([(0, y), (width, y)], fill=color)
    
    def _draw_professional_title(self, draw, title, position):
        """Draw professional title with emoji, bold, and centered"""
        x, y = position
        
        # Ensure title has emoji
        if not any(ord(char) > 127 for char in title):
            if 'gravity' in title.lower():
                title = f"🌍 {title}"
            elif 'electricity' in title.lower():
                title = f"⚡ {title}"
            elif 'photosynthesis' in title.lower():
                title = f"🌱 {title}"
            elif 'machine learning' in title.lower() or 'ai' in title.lower() or 'artificial intelligence' in title.lower():
                title = f"🤖 {title}"
            elif 'photosynthesis' in title.lower():
                title = f"🌱 {title}"
            else:
                title = f"📚 {title}"
        
        # Draw title with professional styling (dark text for white background)
        self._draw_centered_text_with_professional_shadow(draw, title, (x, y), self.title_font, 'black', 'lightgray')
    
    def _draw_professional_subtitle(self, draw, subtitle, position):
        """Draw professional subtitle in bold italic"""
        x, y = position
        # Draw subtitle with professional styling (purple for app theme consistency)
        self._draw_centered_text_with_professional_shadow(draw, subtitle, (x, y), self.subtitle_font, 'purple', 'lightgray')
    
    def _draw_professional_content_box(self, draw, content, start_pos, end_pos):
        """Draw professional content box with proper styling"""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Draw clean white box with subtle border (matching app theme)
        draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255), outline=(220, 220, 220), width=2)
        
        # Draw content with professional typography
        self._draw_professional_wrapped_text(draw, content, (x1 + 40, y1 + 40), self.body_font, 'black', x2 - x1 - 80)
    
    def _draw_professional_key_points(self, draw, key_points, position):
        """Draw professional key points with bright colors"""
        x, y = position
        y_pos = y
        
        for i, point in enumerate(key_points[:4]):
            # Clean up the point text
            clean_point = point.replace('•', '').replace('*', '').strip()
            bullet_text = f"• {clean_point}"
            
            # Use teal/green for key points (matching app theme)
            self._draw_professional_text(draw, bullet_text, (x, y_pos), self.bullet_font, 'teal')
            y_pos += 50
    
    def _draw_professional_visual_instruction(self, draw, visual_desc, position):
        """Draw professional visual instruction"""
        x, y = position
        if visual_desc:
            # Clean up the visual description
            visual_text = visual_desc.replace('Visual: ', '').replace('Visual:', '')
            visual_text = f"Visual: {visual_text[:120]}..." if len(visual_text) > 120 else f"Visual: {visual_text}"
            self._draw_professional_text(draw, visual_text, (x, y), self.subtitle_font, 'gray')
    
    def _draw_professional_slide_number(self, draw, text, position):
        """Draw professional slide number"""
        x, y = position
        self._draw_professional_text(draw, text, (x, y), self.body_font, 'gray')
    
    def _draw_centered_text_with_professional_shadow(self, draw, text, position, font, text_color, shadow_color):
        """Draw centered text with professional shadow effect"""
        x, y = position
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        centered_x = x - text_width // 2
        
        # Draw professional shadow (larger offset for better depth)
        draw.text((centered_x + 3, y + 3), text, font=font, fill=shadow_color)
        # Draw main text
        draw.text((centered_x, y), text, font=font, fill=text_color)
    
    def _draw_professional_text(self, draw, text, position, font, color):
        """Draw professional text with subtle shadow"""
        x, y = position
        # Add subtle shadow for depth
        draw.text((x + 1, y + 1), text, font=font, fill='black')
        draw.text((x, y), text, font=font, fill=color)
    
    def _draw_professional_wrapped_text(self, draw, text, position, font, color, max_width):
        """Draw professional wrapped text with proper spacing"""
        x, y = position
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
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
        
        # Draw each line with professional spacing
        for line in lines:
            self._draw_professional_text(draw, line, (x, y), font, color)
            y += 40  # Professional line spacing
