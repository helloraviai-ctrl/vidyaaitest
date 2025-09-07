"""
Advanced AI Service Manager for Educational Content Generation
Uses multiple AI models and auto-selects the best one based on requirements
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import available AI services
from groq import Groq
from openai import AsyncOpenAI

class ModelType(Enum):
    GROQ_LLAMA = "groq_llama"
    GROQ_MIXTRAL = "groq_mixtral"
    GROQ_GEMMA = "groq_gemma"
    OPENAI_GPT4 = "openai_gpt4"
    OPENAI_GPT35 = "openai_gpt35"
    OPENAI_GPT4_TURBO = "openai_gpt4_turbo"

class ContentType(Enum):
    EDUCATIONAL = "educational"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"

class AIServiceManager:
    """
    Advanced AI service manager that auto-selects the best model based on requirements
    """
    
    def __init__(self):
        """Initialize all available AI services"""
        self.groq_client = None
        self.openai_client = None
        self.available_models = []
        
        # Initialize Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            try:
                self.groq_client = Groq(api_key=groq_key)
                self.available_models.extend([
                    ModelType.GROQ_LLAMA,
                    ModelType.GROQ_MIXTRAL,
                    ModelType.GROQ_GEMMA
                ])
                print(f"✅ Groq client initialized successfully")
            except Exception as e:
                print(f"❌ Groq client initialization failed: {e}")
        
        # Initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                self.openai_client = AsyncOpenAI(api_key=openai_key)
                self.available_models.extend([
                    ModelType.OPENAI_GPT4,
                    ModelType.OPENAI_GPT35,
                    ModelType.OPENAI_GPT4_TURBO
                ])
                print(f"✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"❌ OpenAI client initialization failed: {e}")
        
        print(f"Available AI models: {[model.value for model in self.available_models]}")
    
    def select_best_model(self, content_type: ContentType, complexity: str, speed_priority: bool = True) -> ModelType:
        """
        Auto-select the best model based on requirements with enhanced logic
        """
        if not self.available_models:
            raise ValueError("No AI models available")
        
        # Enhanced model selection logic
        if speed_priority:
            # Prioritize speed (Groq models are faster)
            if ModelType.GROQ_LLAMA in self.available_models:
                return ModelType.GROQ_LLAMA
            elif ModelType.GROQ_GEMMA in self.available_models:
                return ModelType.GROQ_GEMMA
            elif ModelType.GROQ_MIXTRAL in self.available_models:
                return ModelType.GROQ_MIXTRAL
            elif ModelType.OPENAI_GPT35 in self.available_models:
                return ModelType.OPENAI_GPT35
            else:
                return ModelType.OPENAI_GPT4
        else:
            # Prioritize quality based on content type and complexity
            if content_type == ContentType.TECHNICAL:
                if complexity == "advanced" and ModelType.OPENAI_GPT4_TURBO in self.available_models:
                    return ModelType.OPENAI_GPT4_TURBO
                elif ModelType.OPENAI_GPT4 in self.available_models:
                    return ModelType.OPENAI_GPT4
                elif ModelType.GROQ_MIXTRAL in self.available_models:
                    return ModelType.GROQ_MIXTRAL
            elif content_type == ContentType.CREATIVE:
                if ModelType.OPENAI_GPT4_TURBO in self.available_models:
                    return ModelType.OPENAI_GPT4_TURBO
                elif ModelType.OPENAI_GPT4 in self.available_models:
                    return ModelType.OPENAI_GPT4
                elif ModelType.GROQ_MIXTRAL in self.available_models:
                    return ModelType.GROQ_MIXTRAL
            elif content_type == ContentType.EDUCATIONAL:
                if ModelType.GROQ_MIXTRAL in self.available_models:
                    return ModelType.GROQ_MIXTRAL
                elif ModelType.OPENAI_GPT4 in self.available_models:
                    return ModelType.OPENAI_GPT4
                elif ModelType.GROQ_GEMMA in self.available_models:
                    return ModelType.GROQ_GEMMA
            
            # Fallback to best available
            if ModelType.OPENAI_GPT4_TURBO in self.available_models:
                return ModelType.OPENAI_GPT4_TURBO
            elif ModelType.OPENAI_GPT4 in self.available_models:
                return ModelType.OPENAI_GPT4
            elif ModelType.GROQ_MIXTRAL in self.available_models:
                return ModelType.GROQ_MIXTRAL
            else:
                return ModelType.GROQ_LLAMA
    
    async def generate_enhanced_content(
        self, 
        topic: str, 
        difficulty: str, 
        audience: str,
        content_type: ContentType = ContentType.EDUCATIONAL,
        speed_priority: bool = True
    ) -> Dict[str, Any]:
        """
        Generate enhanced educational content using the best available model
        """
        model = self.select_best_model(content_type, difficulty, speed_priority)
        
        if model in [ModelType.GROQ_LLAMA, ModelType.GROQ_MIXTRAL]:
            return await self._generate_with_groq(topic, difficulty, audience, model)
        elif model in [ModelType.OPENAI_GPT4, ModelType.OPENAI_GPT35]:
            return await self._generate_with_openai(topic, difficulty, audience, model)
        else:
            raise ValueError(f"Unsupported model: {model}")
    
    async def _generate_with_groq(self, topic: str, difficulty: str, audience: str, model: ModelType) -> Dict[str, Any]:
        """Generate content using Groq models"""
        if not self.groq_client:
            raise ValueError("Groq client not initialized")
        
        # Select specific Groq model
        if model == ModelType.GROQ_LLAMA:
            model_name = "llama-3.1-8b-instant"
        elif model == ModelType.GROQ_MIXTRAL:
            model_name = "mixtral-8x7b-32768"
        elif model == ModelType.GROQ_GEMMA:
            model_name = "gemma-7b-it"
        else:
            model_name = "llama-3.1-8b-instant"
        
        prompt = self._create_enhanced_prompt(topic, difficulty, audience)
        
        try:
            response = self.groq_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator specializing in creating engaging, well-structured educational materials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                top_p=0.9
            )
            
            content = response.choices[0].message.content
            return self._parse_enhanced_response(content, topic)
            
        except Exception as e:
            print(f"Groq generation failed: {e}")
            # Fallback to basic generation
            return self._create_fallback_content(topic, difficulty, audience)
    
    async def _generate_with_openai(self, topic: str, difficulty: str, audience: str, model: ModelType) -> Dict[str, Any]:
        """Generate content using OpenAI models"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Select specific OpenAI model
        if model == ModelType.OPENAI_GPT4:
            model_name = "gpt-4"
        elif model == ModelType.OPENAI_GPT4_TURBO:
            model_name = "gpt-4-turbo-preview"
        elif model == ModelType.OPENAI_GPT35:
            model_name = "gpt-3.5-turbo"
        else:
            model_name = "gpt-3.5-turbo"
        
        prompt = self._create_enhanced_prompt(topic, difficulty, audience)
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator specializing in creating engaging, well-structured educational materials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                top_p=0.9
            )
            
            content = response.choices[0].message.content
            return self._parse_enhanced_response(content, topic)
            
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            # Fallback to basic generation
            return self._create_fallback_content(topic, difficulty, audience)
    
    def _create_enhanced_prompt(self, topic: str, difficulty: str, audience: str) -> str:
        """Create an enhanced prompt for structured educational slide format"""
        return f"""
You are an expert educational content generator. Your job is to create clean, engaging, and well-structured educational slides or video script segments.

Create educational content for: "{topic}"
Target Audience: {audience}
Difficulty Level: {difficulty}

ALWAYS follow these STRICT FORMATTING RULES:

1. **Title Section**  
   - Use a big, clear headline for the topic.  
   - Example: "🌍 Explain Gravity"  

2. **Subheading / Question**  
   - Present the key question or definition in bold, underlined text.  
   - Example: "What is Artificial Intelligence?"  

3. **Main Explanation (Boxed)**  
   - Use 3–5 sentences only.  
   - Short, simple, clear.  
   - No long paragraphs.  
   - Put inside a clean text box.  

4. **Key Points (Bulleted List)**  
   - Always 3 to 4 points.  
   - Each bullet max 10 words.  
   - Example:  
     • Mimics human intelligence  
     • Learns from data  
     • Widely used in tech  

5. **Visual Suggestion (Mandatory)**  
   - Always suggest one simple visual or animation.  
   - Example: "Visual: Animated brain connecting to computer with data flow."  

6. **Tone & Style**  
   - Keep language easy to understand (age 12+ friendly).  
   - No jargon unless explained.  
   - Each section should look like a slide in a professional course.  

7. **Consistency**  
   - Always include: Title, Subheading, Explanation, Key Points, Visual.  
   - Do NOT skip any.  
   - Never mix random formatting.  

Create 3-4 slides following this exact format. Each slide should be self-contained and educational.

CRITICAL: Follow the format EXACTLY. Each section must have:
- Title with emoji (e.g., "🌍 Explain Gravity")
- Subheading in bold with question format (e.g., "**What is Gravity?**")
- Content in 3-5 short sentences only
- 4 key points (max 10 words each, bullet format)
- Visual description starting with "Visual:"

EXAMPLE FORMAT:
Title: "🌍 Explain Gravity"
Subheading: "**What is Gravity?**"
Content: "Gravity is a force that pulls objects toward each other. It keeps us on Earth and holds planets in orbit. Without gravity, everything would float away into space. This invisible force affects everything around us."
Key Points: ["• Pulls objects toward each other", "• Keeps us on Earth", "• Holds planets in orbit", "• Affects everything around us"]
Visual: "Visual: Animated Earth with objects falling toward it, showing gravitational pull."

Return ONLY valid JSON with this structure:
{{
    "summary": "Brief engaging summary of the topic",
    "key_concepts": ["concept1", "concept2", "concept3", "concept4"],
    "sections": [
        {{
            "title": "🌍 [Topic with Emoji]",
            "subheading": "**[Key Question or Definition]**",
            "content": "Short, simple explanation in 3-5 sentences. Clear and engaging. Easy to understand. Perfect for educational slides.",
            "key_points": ["• Point 1 (max 10 words)", "• Point 2 (max 10 words)", "• Point 3 (max 10 words)", "• Point 4 (max 10 words)"],
            "visual_description": "Visual: [Simple visual suggestion with animation elements]",
            "duration_estimate": 45
        }}
    ],
    "full_explanation": "Complete flowing explanation for narration that ties all slides together...",
    "estimated_duration": 180
}}

Final Output = Clean, structured educational slide text ready to be used in video or presentation.
"""
    
    def _parse_enhanced_response(self, content: str, topic: str) -> Dict[str, Any]:
        """Parse the AI response with enhanced error handling"""
        try:
            # Try to extract JSON from the response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            else:
                json_content = content.strip()
            
            # Clean the JSON content to remove control characters
            import re
            # Remove control characters except newlines, tabs, and carriage returns
            json_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', json_content)
            # Also remove any trailing commas before closing braces/brackets
            json_content = re.sub(r',(\s*[}\]])', r'\1', json_content)
            # Remove any leading/trailing whitespace
            json_content = json_content.strip()
            
            # Parse JSON
            data = json.loads(json_content)
            
            # Enhance the content with better formatting
            return self._enhance_content_formatting(data, topic)
            
        except Exception as e:
            print(f"Failed to parse AI response: {e}")
            print(f"Content preview: {content[:500]}...")
            print(f"Cleaned JSON preview: {json_content[:500] if 'json_content' in locals() else 'N/A'}...")
            return self._create_fallback_content(topic, "beginner", "students")
    
    def _enhance_content_formatting(self, data: Dict[str, Any], topic: str) -> Dict[str, Any]:
        """Enhance content formatting for better visual presentation"""
        # Enhance sections
        if "sections" in data:
            for section in data["sections"]:
                # Improve content formatting
                if "content" in section:
                    section["content"] = self._format_section_content(section["content"])
                
                # Enhance key points
                if "key_points" in section:
                    section["key_points"] = [self._format_key_point(point) for point in section["key_points"]]
        
        # Enhance full explanation
        if "full_explanation" in data:
            data["full_explanation"] = self._format_full_explanation(data["full_explanation"])
        
        return data
    
    def _format_section_content(self, content: str) -> str:
        """Format section content for better readability"""
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
        
        return content
    
    def _format_key_point(self, point: str) -> str:
        """Format individual key points"""
        point = point.strip()
        if point and not point[0].isupper():
            point = point[0].upper() + point[1:]
        if point and not point.endswith('.'):
            point += '.'
        return point
    
    def _format_full_explanation(self, explanation: str) -> str:
        """Format the full explanation for audio narration"""
        # Add natural pauses
        explanation = explanation.replace('. ', '. ')
        explanation = explanation.replace(', ', ', ')
        
        # Ensure proper flow
        explanation = explanation.replace('  ', ' ')
        explanation = explanation.strip()
        
        return explanation
    
    def _create_fallback_content(self, topic: str, difficulty: str, audience: str) -> Dict[str, Any]:
        """Create fallback content when AI generation fails"""
        # Create more specific content based on the topic
        if "ai" in topic.lower() or "artificial intelligence" in topic.lower():
            return self._create_ai_fallback_content(topic, difficulty, audience)
        elif "science" in topic.lower() or "physics" in topic.lower() or "chemistry" in topic.lower():
            return self._create_science_fallback_content(topic, difficulty, audience)
        elif "history" in topic.lower() or "war" in topic.lower():
            return self._create_history_fallback_content(topic, difficulty, audience)
        else:
            return self._create_general_fallback_content(topic, difficulty, audience)
    
    def _create_ai_fallback_content(self, topic: str, difficulty: str, audience: str) -> Dict[str, Any]:
        """Create AI-specific fallback content following proper format"""
        return {
            "summary": f"Artificial Intelligence (AI) is revolutionizing how we interact with technology and solve complex problems. This {difficulty} level explanation is designed for {audience}.",
            "key_concepts": [
                "What is Artificial Intelligence",
                "Machine Learning and Deep Learning", 
                "AI Applications in Daily Life",
                "The Future of AI"
            ],
            "sections": [
                {
                    "title": "🤖 What is Artificial Intelligence?",
                    "subheading": "**What is Artificial Intelligence?**",
                    "content": "Artificial Intelligence refers to computer systems that can perform tasks requiring human intelligence. These systems can learn, reason, and solve problems. AI analyzes data to recognize patterns and make decisions. It powers many technologies we use daily.",
                    "key_points": [
                        "• Mimics human intelligence in machines",
                        "• Learns from data and experience", 
                        "• Widely used in technology today",
                        "• Powers voice assistants and apps"
                    ],
                    "visual_description": "Visual: Animated brain connecting to computer with data flow",
                    "duration_estimate": 60
                },
                {
                    "title": "🧠 Machine Learning and Deep Learning",
                    "subheading": "**How do machines learn?**",
                    "content": "Machine Learning helps computers improve through experience without explicit programming. Deep Learning uses neural networks inspired by the human brain. These systems process vast amounts of data automatically. They enable modern AI applications we use today.",
                    "key_points": [
                        "• Computers learn from data automatically",
                        "• Neural networks mimic brain structure",
                        "• Powers image and speech recognition",
                        "• Enables modern AI applications"
                    ],
                    "visual_description": "Visual: Animated neural network with nodes and connections showing data processing",
                    "duration_estimate": 70
                },
                {
                    "title": "📱 AI Applications in Daily Life",
                    "subheading": "**Where do we see AI today?**",
                    "content": "AI works behind the scenes in many daily technologies. Smartphones use AI for facial recognition and voice commands. Streaming services recommend content using AI. Navigation apps find routes and predict traffic with AI.",
                    "key_points": [
                        "• Powers smartphone features and apps",
                        "• Recommendation systems use AI",
                        "• Transforms healthcare and transportation",
                        "• Works behind the scenes daily"
                    ],
                    "visual_description": "Visual: Collage of AI applications showing smartphone, medical equipment, self-driving car, and streaming interface",
                    "duration_estimate": 65
                }
            ],
            "full_explanation": f"Welcome to our exploration of Artificial Intelligence! AI is one of the most exciting and rapidly evolving fields in technology today. We'll discover how AI works, where it's already being used, and what the future might hold. Whether you're a {audience} interested in technology or just curious about how your smartphone seems to 'know' what you want, this {difficulty} level explanation will give you a solid understanding of AI and its impact on our world.",
            "estimated_duration": 195,
            "topic": topic
        }
    
    def _create_science_fallback_content(self, topic: str, difficulty: str, audience: str) -> Dict[str, Any]:
        """Create science-specific fallback content"""
        return {
            "summary": f"Science helps us understand the natural world through observation, experimentation, and logical reasoning. This {difficulty} level explanation of {topic} is designed for {audience}.",
            "key_concepts": [
                f"Understanding {topic}",
                f"Scientific principles behind {topic}",
                f"Real-world applications of {topic}",
                f"Future developments in {topic}"
            ],
            "sections": [
                {
                    "title": f"Introduction to {topic}",
                    "content": f"Science is our way of understanding the natural world through careful observation and experimentation. {topic} is a fascinating area of scientific study that helps us understand how things work.\n\nThrough scientific methods, we can discover the underlying principles that govern {topic} and use this knowledge to solve problems and improve our lives.",
                    "key_points": [
                        f"{topic} is based on scientific principles",
                        "Observation and experimentation are key",
                        "Scientific knowledge helps solve real problems"
                    ],
                    "visual_description": f"Scientific laboratory setting with equipment and diagrams related to {topic}",
                    "duration_estimate": 50
                },
                {
                    "title": f"Key Scientific Principles",
                    "content": f"The study of {topic} is built on fundamental scientific principles that have been tested and verified through experiments. These principles help us predict how {topic} will behave under different conditions.\n\nUnderstanding these principles allows scientists and engineers to develop new technologies and applications that benefit society.",
                    "key_points": [
                        f"Scientific principles govern {topic}",
                        "Experiments verify these principles",
                        "Principles enable technological development"
                    ],
                    "visual_description": f"Animated diagrams showing the scientific principles behind {topic}",
                    "duration_estimate": 55
                },
                {
                    "title": f"Applications and Impact",
                    "content": f"The knowledge gained from studying {topic} has led to many practical applications that affect our daily lives. From medical treatments to environmental solutions, the applications of {topic} are vast and growing.\n\nAs our understanding deepens, we continue to find new ways to apply this knowledge for the benefit of humanity and the planet.",
                    "key_points": [
                        f"{topic} has many practical applications",
                        "Applications improve our daily lives",
                        "New applications are constantly being developed"
                    ],
                    "visual_description": f"Real-world examples showing applications of {topic} in various fields",
                    "duration_estimate": 50
                }
            ],
            "full_explanation": f"Science is our greatest tool for understanding the world around us. Through the study of {topic}, we gain insights into how the natural world works and how we can use this knowledge to improve our lives. This {difficulty} level explanation is designed for {audience} who want to understand the scientific principles behind {topic} and see how this knowledge is applied in the real world.",
            "estimated_duration": 155,
            "topic": topic
        }
    
    def _create_history_fallback_content(self, topic: str, difficulty: str, audience: str) -> Dict[str, Any]:
        """Create history-specific fallback content"""
        return {
            "summary": f"History helps us understand how past events have shaped our world today. This {difficulty} level exploration of {topic} is designed for {audience}.",
            "key_concepts": [
                f"Historical context of {topic}",
                f"Key events and figures",
                f"Impact on the modern world",
                f"Lessons from history"
            ],
            "sections": [
                {
                    "title": f"Historical Background of {topic}",
                    "content": f"Understanding {topic} requires us to look at the historical context in which it occurred. History is not just about dates and facts, but about understanding the causes and effects of events.\n\nBy studying the past, we can better understand the present and make more informed decisions about the future.",
                    "key_points": [
                        f"{topic} occurred in a specific historical context",
                        "Understanding causes and effects is important",
                        "History helps us understand the present"
                    ],
                    "visual_description": f"Historical timeline and maps showing the context of {topic}",
                    "duration_estimate": 55
                },
                {
                    "title": f"Key Events and Figures",
                    "content": f"The story of {topic} involves many important events and influential people who shaped its course. These individuals and events had lasting impacts that we still feel today.\n\nBy studying these key figures and events, we can understand how decisions made in the past continue to influence our world.",
                    "key_points": [
                        f"Important figures played key roles in {topic}",
                        "Major events shaped the course of history",
                        "Past decisions still influence us today"
                    ],
                    "visual_description": f"Portraits of key figures and scenes from important events in {topic}",
                    "duration_estimate": 60
                },
                {
                    "title": f"Impact on the Modern World",
                    "content": f"The events and developments related to {topic} have had lasting effects that continue to shape our world today. Understanding these connections helps us see how the past influences the present.\n\nBy learning from history, we can better understand current events and make more informed decisions about the future.",
                    "key_points": [
                        f"{topic} continues to influence the modern world",
                        "Understanding history helps with current events",
                        "We can learn valuable lessons from the past"
                    ],
                    "visual_description": f"Modern world connections showing how {topic} influences today's society",
                    "duration_estimate": 55
                }
            ],
            "full_explanation": f"History is more than just a record of past events - it's a guide to understanding our world today. Through exploring {topic}, we'll discover how past events, decisions, and people have shaped the world we live in. This {difficulty} level explanation is designed for {audience} who want to understand not just what happened, but why it matters today.",
            "estimated_duration": 170,
            "topic": topic
        }
    
    def _create_general_fallback_content(self, topic: str, difficulty: str, audience: str) -> Dict[str, Any]:
        """Create general fallback content for any topic"""
        return {
            "summary": f"Welcome to our comprehensive explanation of {topic}. This {difficulty} level content is designed for {audience}.",
            "key_concepts": [
                f"Understanding {topic}",
                f"Key principles of {topic}",
                f"Applications of {topic}",
                f"Real-world examples"
            ],
            "sections": [
                {
                    "title": f"🌍 Explain {topic}",
                    "subheading": f"**What is {topic}?**",
                    "content": f"{topic} is a fundamental concept that affects our daily lives. It helps us understand how things work in the world around us. Learning about {topic} opens new perspectives and connections. This knowledge is essential for understanding many other subjects.",
                    "key_points": [
                        f"• {topic} affects daily life",
                        "• Helps understand how things work",
                        "• Opens new perspectives",
                        "• Essential for other subjects"
                    ],
                    "visual_description": f"Visual: Animated diagram showing {topic} in action with clear, engaging graphics",
                    "duration_estimate": 45
                },
                {
                    "title": f"🔬 How {topic} Works",
                    "subheading": f"**What are the key principles?**",
                    "content": f"The key principles of {topic} form the foundation of our understanding. These principles work together to create the effects we observe. Understanding these principles helps us predict and explain behavior. They connect to many other areas of knowledge.",
                    "key_points": [
                        f"• Key principles of {topic}",
                        "• How principles work together",
                        "• Helps predict behavior",
                        "• Connects to other knowledge"
                    ],
                    "visual_description": f"Visual: Animated diagrams showing the key principles of {topic} with clear visual representations",
                    "duration_estimate": 50
                },
                {
                    "title": f"🌐 Real-World Applications",
                    "subheading": f"**Where do we see {topic}?**",
                    "content": f"{topic} appears in many real-world situations and applications. It's used in technology, medicine, and everyday life. Understanding these applications shows why {topic} matters. This knowledge helps us solve problems and make decisions.",
                    "key_points": [
                        f"• {topic} in technology",
                        "• Used in medicine",
                        "• Appears in daily life",
                        "• Helps solve problems"
                    ],
                    "visual_description": f"Visual: Real-world examples and scenarios showing {topic} in action",
                    "duration_estimate": 45
                }
            ],
            "full_explanation": f"Welcome to our comprehensive exploration of {topic}. Today, we'll take a journey through this fascinating subject, designed specifically for {audience} at a {difficulty} level. {topic} is more than just a concept - it's a way of understanding the world around us. We'll start with the basics, build up to more complex ideas, and see how this knowledge applies in real life. By the end of our time together, you'll have a solid foundation in {topic} and understand why it matters.",
            "estimated_duration": 140,
            "topic": topic
        }
