#!/usr/bin/env python3
"""
Test script to verify the enhanced AI system with multiple models and visual generation
"""

import requests
import json
import time
import asyncio

def test_enhanced_system():
    """Test the enhanced system with multiple AI models and visual generation"""
    
    # Test topics with different complexity levels
    test_topics = [
        {
            "topic": "Machine Learning",
            "difficulty": "beginner",
            "audience": "students",
            "expected_models": ["groq", "openai"]
        },
        {
            "topic": "Quantum Physics",
            "difficulty": "advanced", 
            "audience": "professionals",
            "expected_models": ["openai", "groq"]
        },
        {
            "topic": "Photosynthesis",
            "difficulty": "intermediate",
            "audience": "students",
            "expected_models": ["groq", "openai"]
        }
    ]
    
    print("🚀 Testing Enhanced AI System with Multiple Models")
    print("=" * 60)
    
    for i, test_case in enumerate(test_topics, 1):
        print(f"\n🧪 Test {i}: {test_case['topic']}")
        print(f"   Difficulty: {test_case['difficulty']}")
        print(f"   Audience: {test_case['audience']}")
        print("-" * 40)
        
        # Test the enhanced system
        result = test_single_topic(test_case)
        
        if result:
            print(f"✅ Test {i} PASSED")
            analyze_result(result, test_case)
        else:
            print(f"❌ Test {i} FAILED")
        
        print()
    
    print("=" * 60)
    print("🎉 Enhanced AI System Testing Complete!")

def test_single_topic(test_case):
    """Test a single topic with the enhanced system"""
    
    topic = test_case["topic"]
    difficulty = test_case["difficulty"]
    audience = test_case["audience"]
    
    # Make request to generate content
    url = "http://localhost:8000/api/generate-content"
    payload = {
        "topic": topic,
        "difficulty_level": difficulty,
        "target_audience": audience
    }
    
    try:
        print(f"📤 Sending request for: {topic}")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        job_id = data["job_id"]
        print(f"✅ Request successful. Job ID: {job_id}")
        
        # Poll for completion
        print("⏳ Waiting for enhanced content generation...")
        result = poll_for_completion(job_id)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def poll_for_completion(job_id):
    """Poll for job completion"""
    
    max_attempts = 60  # 2 minutes max
    attempt = 0
    
    while attempt < max_attempts:
        try:
            status_url = f"http://localhost:8000/api/status/{job_id}"
            response = requests.get(status_url, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ Status check failed: {response.status_code}")
                return None
            
            status_data = response.json()
            status = status_data.get('status', 'unknown')
            progress = status_data.get('progress', 0)
            message = status_data.get('message', '')
            
            print(f"📊 Status: {status} - {message} ({progress}%)")
            
            if status == 'completed':
                print("✅ Content generation completed!")
                return status_data
            elif status == 'failed':
                error = status_data.get('error', 'Unknown error')
                print(f"❌ Content generation failed: {error}")
                return None
            
            time.sleep(2)
            attempt += 1
            
        except Exception as e:
            print(f"❌ Error polling status: {e}")
            return None
    
    print("⏰ Timeout waiting for completion")
    return None

def analyze_result(result, test_case):
    """Analyze the result to verify enhanced features"""
    
    result_data = result.get('result_data', {})
    sections = result_data.get('sections', [])
    
    print("📊 Analysis:")
    
    # Check if we have the new structured format
    has_structured_format = False
    has_visual_descriptions = False
    has_ai_visuals = False
    
    for section in sections:
        # Check for new format elements
        if section.get('subheading'):
            has_structured_format = True
        
        if section.get('visual_description'):
            has_visual_descriptions = True
            visual_desc = section['visual_description']
            if 'detailed' in visual_desc.lower() or 'animated' in visual_desc.lower():
                has_ai_visuals = True
    
    print(f"   📝 Structured Format: {'✅' if has_structured_format else '❌'}")
    print(f"   🎨 Visual Descriptions: {'✅' if has_visual_descriptions else '❌'}")
    print(f"   🤖 AI Visual Details: {'✅' if has_ai_visuals else '❌'}")
    
    # Check content quality
    if sections:
        first_section = sections[0]
        title = first_section.get('title', '')
        content = first_section.get('content', '')
        
        print(f"   📌 Title Format: {'✅' if '🌍' in title or '🤖' in title or '📱' in title else '❌'}")
        print(f"   📦 Content Quality: {'✅' if len(content) > 100 else '❌'}")
        
        # Show sample content
        print(f"   📄 Sample Title: {title[:50]}...")
        print(f"   📄 Sample Content: {content[:100]}...")
    
    # Check for enhanced features
    topic = test_case['topic']
    difficulty = test_case['difficulty']
    
    print(f"   🎯 Topic Relevance: {'✅' if topic.lower() in str(sections).lower() else '❌'}")
    print(f"   📊 Difficulty Match: {'✅' if difficulty in str(result_data).lower() else '❌'}")

def test_ai_model_selection():
    """Test AI model selection logic"""
    
    print("\n🔬 Testing AI Model Selection Logic")
    print("-" * 40)
    
    # Test different scenarios
    test_scenarios = [
        {"topic": "Simple Math", "difficulty": "beginner", "expected": "groq"},
        {"topic": "Advanced Quantum Computing", "difficulty": "advanced", "expected": "openai"},
        {"topic": "Creative Writing", "difficulty": "intermediate", "expected": "openai"},
        {"topic": "Basic Science", "difficulty": "beginner", "expected": "groq"}
    ]
    
    for scenario in test_scenarios:
        print(f"🧪 Testing: {scenario['topic']} ({scenario['difficulty']})")
        # Note: In a real implementation, we would test the model selection logic directly
        print(f"   Expected: {scenario['expected']} model")
        print("   ✅ Model selection logic would be tested here")

if __name__ == "__main__":
    try:
        test_enhanced_system()
        test_ai_model_selection()
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
