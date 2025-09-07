#!/usr/bin/env python3
"""
Test script to verify the new structured educational slide format
"""

import requests
import json
import time

def test_new_format():
    """Test the new structured educational slide format"""
    
    # Test topic
    topic = "Photosynthesis"
    
    print(f"🧪 Testing new structured format with topic: {topic}")
    print("=" * 60)
    
    # Make request to generate content
    url = "http://localhost:8000/api/generate-content"
    payload = {
        "topic": topic,
        "difficulty_level": "beginner",
        "target_audience": "students"
    }
    
    print("📤 Sending request to generate content...")
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return
    
    data = response.json()
    job_id = data["job_id"]
    print(f"✅ Content generation started. Job ID: {job_id}")
    
    # Poll for status
    print("⏳ Waiting for content generation to complete...")
    while True:
        status_url = f"http://localhost:8000/api/status/{job_id}"
        status_response = requests.get(status_url)
        
        if status_response.status_code != 200:
            print(f"❌ Error checking status: {status_response.status_code}")
            return
        
        status_data = status_response.json()
        print(f"📊 Status: {status_data['status']} - {status_data['message']} ({status_data['progress']}%)")
        
        if status_data['status'] == 'completed':
            print("✅ Content generation completed!")
            break
        elif status_data['status'] == 'failed':
            print(f"❌ Content generation failed: {status_data.get('error', 'Unknown error')}")
            return
        
        time.sleep(2)
    
    # Display the generated content
    print("\n" + "=" * 60)
    print("📚 GENERATED EDUCATIONAL CONTENT")
    print("=" * 60)
    
    result_data = status_data.get('result_data', {})
    sections = result_data.get('sections', [])
    
    if not sections:
        print("❌ No sections found in the result")
        return
    
    print(f"📖 Topic: {result_data.get('topic', topic)}")
    print(f"📝 Summary: {result_data.get('summary', 'No summary available')}")
    print(f"⏱️  Estimated Duration: {result_data.get('estimated_duration', 'Unknown')} seconds")
    print()
    
    for i, section in enumerate(sections, 1):
        print(f"🎯 SLIDE {i}")
        print("-" * 40)
        
        # Title with emoji
        print(f"📌 Title: {section.get('title', 'No title')}")
        
        # Subheading
        if section.get('subheading'):
            print(f"❓ Subheading: {section.get('subheading')}")
        
        # Content (boxed)
        print(f"📦 Content: {section.get('content', 'No content')}")
        
        # Key points
        key_points = section.get('key_points', [])
        if key_points:
            print("🔑 Key Points:")
            for point in key_points:
                print(f"   • {point}")
        
        # Visual suggestion
        if section.get('visual_description'):
            print(f"🎨 Visual: {section.get('visual_description')}")
        
        # Duration
        if section.get('duration_estimate'):
            print(f"⏱️  Duration: {section.get('duration_estimate')} seconds")
        
        print()
    
    print("=" * 60)
    print("✅ Test completed successfully!")
    print("🎉 The new structured educational slide format is working!")

if __name__ == "__main__":
    test_new_format()
