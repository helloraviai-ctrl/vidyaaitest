#!/usr/bin/env python3
"""
Test script to verify the optimized fast system
"""

import requests
import time
import json

def test_fast_system():
    """Test the optimized fast system"""
    
    print("🚀 Testing Optimized Fast System")
    print("=" * 50)
    
    # Test topic
    topic = "Photosynthesis"
    
    print(f"📝 Testing with topic: {topic}")
    print("⏱️  Starting timer...")
    
    start_time = time.time()
    
    # Make request
    url = "http://localhost:8000/api/generate-content"
    payload = {
        "topic": topic,
        "difficulty_level": "beginner",
        "target_audience": "students"
    }
    
    try:
        print("📤 Sending request...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Request failed: {response.status_code}")
            return
        
        data = response.json()
        job_id = data["job_id"]
        print(f"✅ Request successful. Job ID: {job_id}")
        
        # Poll for completion
        print("⏳ Waiting for completion...")
        max_wait = 60  # 1 minute max
        wait_time = 0
        
        while wait_time < max_wait:
            status_response = requests.get(f"http://localhost:8000/api/status/{job_id}")
            
            if status_response.status_code != 200:
                print(f"❌ Status check failed: {status_response.status_code}")
                return
            
            status_data = status_response.json()
            status = status_data.get('status', 'unknown')
            progress = status_data.get('progress', 0)
            message = status_data.get('message', '')
            
            print(f"📊 {status} - {message} ({progress}%)")
            
            if status == 'completed':
                end_time = time.time()
                total_time = end_time - start_time
                
                print(f"✅ COMPLETED in {total_time:.1f} seconds!")
                print(f"🎉 That's {total_time/60:.1f} minutes - Much faster!")
                
                # Show results
                result_data = status_data.get('result_data', {})
                sections = result_data.get('sections', [])
                generation_type = result_data.get('generation_type', 'unknown')
                
                print(f"📊 Generation Type: {generation_type}")
                print(f"📝 Sections Generated: {len(sections)}")
                
                if sections:
                    first_section = sections[0]
                    print(f"📌 First Section Title: {first_section.get('title', 'N/A')}")
                    print(f"📦 Has Subheading: {'✅' if first_section.get('subheading') else '❌'}")
                    print(f"🎨 Has Visual Description: {'✅' if first_section.get('visual_description') else '❌'}")
                
                return True
                
            elif status == 'failed':
                error = status_data.get('error', 'Unknown error')
                print(f"❌ Generation failed: {error}")
                return False
            
            time.sleep(2)
            wait_time += 2
        
        print("⏰ Timeout - Still too slow")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_fast_system()
    
    if success:
        print("\n🎉 SUCCESS: Fast system is working!")
        print("📈 Performance improvements:")
        print("   • Reduced video quality settings")
        print("   • Faster AI visual generation")
        print("   • Optimized content structure")
        print("   • Skip heavy video processing in fast mode")
    else:
        print("\n❌ FAILED: System still needs optimization")
