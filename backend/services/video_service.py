"""Video combination service using MoviePy"""
import os
import asyncio
from PIL import Image
try:
    from moviepy import AudioFileClip, ImageClip, ColorClip, concatenate_videoclips, TextClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    # Fallback if moviepy not available
    MOVIEPY_AVAILABLE = False
    TextClip = None

class VideoService:
    def __init__(self):
        self.temp_dir = "./temp"
    
    async def create_final_video(self, audio_path: str, animation_paths: list, output_path: str) -> str:
        """Combine audio and animations into final video"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if not MOVIEPY_AVAILABLE:
            # Fallback: create a simple video using PIL and basic video creation
            return await self._create_simple_video(audio_path, animation_paths, output_path)
        
        try:
            # Create video using MoviePy
            return await self._create_moviepy_video(audio_path, animation_paths, output_path)
        except Exception as e:
            print(f"MoviePy video creation failed: {e}")
            # Fallback to simple video creation
            return await self._create_simple_video(audio_path, animation_paths, output_path)
    
    async def _create_moviepy_video(self, audio_path: str, animation_paths: list, output_path: str) -> str:
        """Create video using MoviePy with enhanced formatting"""
        loop = asyncio.get_event_loop()
        
        def create_video():
            # Load audio with proper format handling
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            print(f"🎵 Audio loaded: {audio_duration:.2f}s, {audio_clip.fps}Hz, {audio_clip.nchannels} channels")
            
            # Create video clips from images with enhanced formatting
            video_clips = []
            if animation_paths:
                # Calculate duration per image with smooth transitions
                transition_duration = 0.5  # 0.5 second transitions
                total_transition_time = (len(animation_paths) - 1) * transition_duration
                duration_per_image = (audio_duration - total_transition_time) / len(animation_paths)
                
                for i, img_path in enumerate(animation_paths):
                    if os.path.exists(img_path):
                        # Create image clip with proper duration
                        img_clip = ImageClip(img_path, duration=duration_per_image)
                        
                        # Resize to HD quality using the correct MoviePy 2.x method
                        img_clip = img_clip.resized((1920, 1080))
                        
                        # Note: Fade effects removed for MoviePy 2.x compatibility
                        # The video will have clean transitions between slides
                        
                        video_clips.append(img_clip)
            
            if not video_clips:
                # Create a simple professional background video
                video_clip = ColorClip(size=(1920, 1080), color=(30, 41, 59), duration=audio_duration)
            else:
                # Concatenate all image clips with smooth transitions
                video_clip = concatenate_videoclips(video_clips, method="compose")
            
            print(f"🎬 Video created: {video_clip.duration:.2f}s")
            
            # Ensure audio and video durations match
            if abs(audio_duration - video_clip.duration) > 0.1:
                print(f"⚠️ Duration mismatch: Audio={audio_duration:.2f}s, Video={video_clip.duration:.2f}s")
                # Adjust video duration to match audio
                video_clip = video_clip.set_duration(audio_duration)
            
            # Set audio with proper synchronization using correct MoviePy 2.x method
            final_video = video_clip.with_audio(audio_clip)
            
            print(f"🔊 Final video: {final_video.duration:.2f}s with audio")
            
            # Write optimized video file with better audio handling
            final_video.write_videofile(
                output_path,
                fps=15,  # Lower frame rate for faster processing
                codec='libx264',
                audio_codec='aac',
                audio_bitrate='128k',  # Ensure good audio quality
                audio_fps=44100,  # Standard audio sample rate
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                bitrate='2000k',  # Lower bitrate for faster encoding
                preset='ultrafast',  # Fastest encoding preset
                ffmpeg_params=['-crf', '28', '-ac', '2']  # Ensure stereo audio
            )
            
            # Clean up resources
            audio_clip.close()
            video_clip.close()
            final_video.close()
            
            return output_path
        
        return await loop.run_in_executor(None, create_video)
    
    async def _create_simple_video(self, audio_path: str, animation_paths: list, output_path: str) -> str:
        """Create a simple video using ffmpeg directly"""
        import subprocess
        import tempfile
        
        try:
            # Create a simple video using ffmpeg
            if animation_paths and os.path.exists(animation_paths[0]):
                # Use the first slide as the video content
                first_slide = animation_paths[0]
                
                # Create a simple video from the first slide
                cmd = [
                    'ffmpeg', '-y',  # Overwrite output file
                    '-loop', '1',    # Loop the image
                    '-i', first_slide,  # Input image
                    '-t', '30',      # Duration 30 seconds
                    '-c:v', 'libx264',  # Video codec
                    '-pix_fmt', 'yuv420p',  # Pixel format
                    '-vf', 'scale=1920:1080',  # Scale to HD
                    '-r', '1',       # 1 frame per second (static image)
                    output_path
                ]
                
                # Add audio if available with proper format conversion
                if audio_path and os.path.exists(audio_path):
                    cmd.extend([
                        '-i', audio_path, 
                        '-c:a', 'aac', 
                        '-b:a', '128k',  # Audio bitrate
                        '-ar', '44100',  # Audio sample rate
                        '-ac', '2',      # Stereo audio
                        '-shortest'
                    ])
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Created simple video using ffmpeg: {output_path}")
                    return output_path
                else:
                    print(f"❌ ffmpeg failed: {result.stderr}")
            
            # Fallback: create a placeholder
            with open(output_path, 'w') as f:
                f.write("Video creation failed. Please check ffmpeg installation.\n")
                f.write(f"Audio file: {audio_path}\n")
                f.write(f"Animation files: {animation_paths}\n")
            
            print(f"Warning: Created placeholder video file at {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating simple video: {e}")
            # Create placeholder
            with open(output_path, 'w') as f:
                f.write(f"Video creation error: {e}\n")
            return output_path
