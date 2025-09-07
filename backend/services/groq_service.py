"""
Groq AI service for generating structured educational content
"""

import os
import json
from typing import Dict, List, Any
from groq import Groq
from models.content_models import ExplanationData, ContentSection, DifficultyLevel, TargetAudience

class GroqService:
    """
    Service class for interacting with Groq AI API to generate educational content
    
    This service uses Groq's fast inference capabilities to generate:
    - Structured explanations for any topic
    - Sectioned content for better video organization
    - Key concepts and visual descriptions
    """
    
    def __init__(self):
        """Initialize the Groq service with API key"""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"  # Using current Llama 3.1 model
    
    async def generate_explanation(self, topic: str, difficulty_level: DifficultyLevel, target_audience: TargetAudience) -> ExplanationData:
        """
        Generate a structured explanation for the given topic
        
        Args:
            topic: The topic to explain
            difficulty_level: Target difficulty level
            target_audience: Intended audience
            
        Returns:
            ExplanationData object with structured content
        """
        try:
            # Create the prompt for structured content generation
            prompt = self._create_structured_prompt(topic, difficulty_level, target_audience)
            
            # Generate content using Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content creator. Generate structured, engaging explanations that are perfect for creating educational videos with audio narration and visual animations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Parse the response
            content = response.choices[0].message.content
            
            # Extract structured data from the response
            explanation_data = self._parse_structured_response(content, topic)
            
            return explanation_data
            
        except Exception as e:
            raise Exception(f"Failed to generate explanation with Groq: {str(e)}")
    
    def _create_structured_prompt(self, topic: str, difficulty_level: DifficultyLevel, target_audience: TargetAudience) -> str:
        """
        Create a structured prompt for content generation
        
        Args:
            topic: The topic to explain
            difficulty_level: Target difficulty level
            target_audience: Intended audience
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
        Create a comprehensive educational explanation for the topic: "{topic}"
        
        Target Audience: {target_audience.value}
        Difficulty Level: {difficulty_level.value}
        
        Please structure your response as follows:
        
        1. **SUMMARY**: Provide a brief 2-3 sentence summary of the topic
        
        2. **KEY CONCEPTS**: List 3-5 key concepts that are essential to understand
        
        3. **STRUCTURED SECTIONS**: Break the explanation into 4-6 logical sections. For each section, provide:
           - Title (concise and engaging)
           - Content (2-3 well-structured paragraphs with clear explanations, examples, and transitions)
           - Key Points (3-4 bullet points highlighting important information)
           - Visual Description (detailed description of what should be visualized/animated)
           - Duration Estimate (estimated seconds for this section, total should be 3-5 minutes)
           
           IMPORTANT: Format the content with proper paragraph breaks, clear sentence structure, and engaging language.
        
        4. **FULL EXPLANATION**: Provide the complete explanation as a single flowing text suitable for audio narration
        
        Guidelines:
        - Use simple, clear language appropriate for {target_audience.value}
        - Make it engaging and conversational
        - Include analogies and examples where helpful
        - Ensure smooth transitions between sections
        - Visual descriptions should be specific and animation-friendly
        - Total duration should be approximately 3-5 minutes when spoken
        - Format content with proper paragraph breaks and structure
        - Use bullet points and clear organization
        - Make content visually appealing and easy to read
        - Include specific examples and real-world applications
        
        IMPORTANT: Format your response as valid JSON only. Do not include any markdown formatting, code blocks, or additional text. Return only the JSON object with the following structure:
        {{
            "summary": "Brief summary here",
            "key_concepts": ["concept1", "concept2", "concept3"],
            "sections": [
                {{
                    "title": "Section Title",
                    "content": "Section content here...",
                    "key_points": ["point1", "point2", "point3"],
                    "visual_description": "Detailed visual description...",
                    "duration_estimate": 30
                }}
            ],
            "full_explanation": "Complete flowing explanation for narration...",
            "estimated_duration": 180
        }}
        
        Ensure all text content is properly escaped for JSON and contains no control characters.
        """
        
        return prompt
    
    def _parse_structured_response(self, content: str, topic: str) -> ExplanationData:
        """
        Parse the structured response from Groq into ExplanationData object
        
        Args:
            content: Raw response content from Groq
            topic: Original topic for context
            
        Returns:
            ExplanationData object
        """
        try:
            # Try to extract JSON from the response
            # Look for JSON content between ```json and ``` or just parse the whole content
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            elif "```" in content:
                # Handle other code blocks
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_content = content[json_start:json_end].strip()
            elif content.strip().startswith("{") and content.strip().endswith("}"):
                # The entire content is JSON
                json_content = content.strip()
            elif "{" in content and "}" in content:
                # Find the first { and last } to extract JSON
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_content = content[json_start:json_end]
            else:
                # Fallback: create a basic structure from the content
                return self._create_fallback_structure(content, topic)
            
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
            
            # Validate that we have the expected structure
            if not isinstance(data, dict) or "sections" not in data:
                print("Invalid JSON structure, using fallback")
                return self._create_fallback_structure(content, topic)
            
            # Convert to ExplanationData
            sections = []
            for section_data in data.get("sections", []):
                if not isinstance(section_data, dict):
                    continue
                    
                section = ContentSection(
                    title=section_data.get("title", ""),
                    subheading=section_data.get("subheading", ""),
                    content=section_data.get("content", ""),
                    key_points=section_data.get("key_points", []),
                    visual_description=section_data.get("visual_description", ""),
                    duration_estimate=section_data.get("duration_estimate", 30)
                )
                sections.append(section)
            
            if not sections:
                print("No valid sections found, using fallback")
                return self._create_fallback_structure(content, topic)
            
            return ExplanationData(
                full_explanation=data.get("full_explanation", content),
                sections=sections,
                key_concepts=data.get("key_concepts", []),
                summary=data.get("summary", ""),
                estimated_duration=data.get("estimated_duration", 180)
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"JSON parsing failed: {e}")
            print(f"Content preview: {content[:500]}...")
            print(f"Cleaned JSON preview: {json_content[:500] if 'json_content' in locals() else 'N/A'}...")
            # Fallback to creating a basic structure
            return self._create_fallback_structure(content, topic)
    
    def _create_fallback_structure(self, content: str, topic: str) -> ExplanationData:
        """
        Create a fallback structure when JSON parsing fails
        
        Args:
            content: Raw content from Groq
            topic: Original topic
            
        Returns:
            Basic ExplanationData object
        """
        # Try to extract meaningful titles from the content
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Look for potential section titles (lines that might be titles)
        potential_titles = []
        for line in lines:
            # Look for lines that could be titles (short, capitalized, not too long)
            if (len(line) < 100 and 
                len(line) > 5 and 
                (line.isupper() or line.istitle()) and
                not line.startswith('{') and
                not line.startswith('"') and
                ':' not in line and
                '=' not in line):
                potential_titles.append(line)
        
        # Split content into paragraphs
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        
        # Create sections from paragraphs with better titles
        sections = []
        for i, paragraph in enumerate(paragraphs[:6]):  # Limit to 6 sections
            # Try to use a meaningful title if available
            if i < len(potential_titles):
                title = potential_titles[i]
            else:
                # Create a more meaningful title based on content
                first_sentence = paragraph.split('.')[0][:50]
                title = f"{first_sentence}..." if len(first_sentence) > 30 else first_sentence
            
            section = ContentSection(
                title=title,
                subheading="",
                content=paragraph,
                key_points=[f"Key point {j + 1}" for j in range(3)],
                visual_description=f"Visual representation of: {paragraph[:100]}...",
                duration_estimate=30
            )
            sections.append(section)
        
        return ExplanationData(
            full_explanation=content,
            sections=sections,
            key_concepts=[f"Concept {i + 1}" for i in range(3)],
            summary=f"An explanation of {topic}",
            estimated_duration=180
        )
    
    async def enhance_explanation(self, explanation_data: ExplanationData, enhancement_type: str) -> ExplanationData:
        """
        Enhance existing explanation with additional details
        
        Args:
            explanation_data: Existing explanation data
            enhancement_type: Type of enhancement (examples, analogies, exercises)
            
        Returns:
            Enhanced ExplanationData object
        """
        try:
            prompt = f"""
            Enhance the following educational content by adding {enhancement_type}:
            
            Topic: {explanation_data.summary}
            Current content: {explanation_data.full_explanation}
            
            Please provide enhanced content with better {enhancement_type} while maintaining the same structure.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert educator. Enhance the given content by adding more {enhancement_type}."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            enhanced_content = response.choices[0].message.content
            
            # Update the explanation data with enhanced content
            explanation_data.full_explanation = enhanced_content
            
            return explanation_data
            
        except Exception as e:
            raise Exception(f"Failed to enhance explanation: {str(e)}")
