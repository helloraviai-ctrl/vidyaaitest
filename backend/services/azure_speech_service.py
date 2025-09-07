"""
Azure Speech Services integration for text-to-speech conversion
"""

import os
import asyncio
from typing import Optional
import azure.cognitiveservices.speech as speechsdk
from models.content_models import AudioGenerationRequest

class AzureSpeechService:
    """
    Service class for Azure Speech Services text-to-speech functionality
    
    This service provides:
    - High-quality text-to-speech conversion
    - Custom voice selection
    - Audio file output in various formats
    - Speech rate and style customization
    """
    
    def __init__(self):
        """Initialize Azure Speech service with credentials"""
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        self.fallback_mode = False
        
        if not self.speech_key or not self.speech_region:
            print("Warning: Azure Speech credentials not found. Using fallback mode.")
            print(f"Speech Key: {'Present' if self.speech_key else 'Missing'}")
            print(f"Speech Region: {'Present' if self.speech_region else 'Missing'}")
            self.fallback_mode = True
            return
        
        # Force fallback mode for now to ensure working voice
        print("🔧 Forcing fallback mode for reliable voice generation...")
        self.fallback_mode = True
        return
        
        try:
            # Configure speech service
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            
            # Set default voice and audio format
            self.speech_config.speech_synthesis_voice_name = os.getenv("AZURE_VOICE_NAME", "en-US-AriaNeural")
            self.speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
            
            print(f"✅ Azure Speech Service initialized successfully")
            print(f"Voice: {self.speech_config.speech_synthesis_voice_name}")
            print(f"Region: {self.speech_region}")
        except Exception as e:
            print(f"Warning: Failed to initialize Azure Speech Service: {e}. Using fallback mode.")
            self.fallback_mode = True
    
    async def text_to_speech(
        self, 
        text: str, 
        output_path: str, 
        voice_name: Optional[str] = None,
        speaking_rate: float = 1.0,
        speaking_style: Optional[str] = None
    ) -> str:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file should be saved
            voice_name: Azure voice name (optional, uses default if not provided)
            speaking_rate: Speech rate multiplier (0.5 to 2.0)
            speaking_style: Voice style (optional)
            
        Returns:
            Path to the generated audio file
        """
        # If in fallback mode, use simple text-to-speech
        if self.fallback_mode:
            return await self._fallback_text_to_speech(text, output_path)
        
        # Check if text is too long and split if necessary
        if len(text) > 2000:  # Azure has limits on text length
            print(f"⚠️ Text too long ({len(text)} chars), splitting into chunks...")
            return await self._text_to_speech_chunked(text, output_path, voice_name, speaking_rate, speaking_style)
        
        # Add timeout to prevent hanging
        import asyncio
        try:
            return await asyncio.wait_for(
                self._text_to_speech_direct(text, output_path, voice_name, speaking_rate, speaking_style),
                timeout=60.0  # 60 second timeout
            )
        except asyncio.TimeoutError:
            print("⏰ Azure Speech timeout, using fallback...")
            return await self._fallback_text_to_speech(text, output_path)
    
    async def _text_to_speech_chunked(
        self, 
        text: str, 
        output_path: str, 
        voice_name: Optional[str] = None,
        speaking_rate: float = 1.0,
        speaking_style: Optional[str] = None
    ) -> str:
        """
        Convert long text to speech by splitting into chunks
        
        Args:
            text: Long text to convert
            output_path: Path where audio file should be saved
            voice_name: Azure voice name
            speaking_rate: Speech rate
            speaking_style: Voice style
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Split text into sentences
            sentences = text.split('. ')
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) < 1500:  # Keep chunks under 1500 chars
                    current_chunk += sentence + ". "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + ". "
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            print(f"📝 Split text into {len(chunks)} chunks")
            
            # Generate audio for each chunk
            chunk_audio_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = output_path.replace('.wav', f'_chunk_{i}.wav')
                # Use the direct Azure method to avoid recursion
                chunk_audio = await self._text_to_speech_direct(
                    text=chunk,
                    output_path=chunk_path,
                    voice_name=voice_name,
                    speaking_rate=speaking_rate,
                    speaking_style=speaking_style
                )
                chunk_audio_paths.append(chunk_audio)
            
            # Combine all chunks into final audio
            return await self._combine_audio_files(chunk_audio_paths, output_path)
            
        except Exception as e:
            print(f"Chunked TTS failed: {e}. Using fallback.")
            return await self._fallback_text_to_speech(text, output_path)
    
    async def _combine_audio_files(self, audio_paths: list, output_path: str) -> str:
        """
        Combine multiple audio files into one
        
        Args:
            audio_paths: List of audio file paths
            output_path: Path for combined audio file
            
        Returns:
            Path to combined audio file
        """
        try:
            import subprocess
            
            # Use ffmpeg to combine audio files
            cmd = ['ffmpeg', '-y']  # Overwrite output
            
            # Add input files
            for audio_path in audio_paths:
                if os.path.exists(audio_path):
                    cmd.extend(['-i', audio_path])
            
            # Add filter to concatenate
            cmd.extend(['-filter_complex', f'concat=n={len(audio_paths)}:v=0:a=1[out]'])
            cmd.extend(['-map', '[out]', output_path])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Combined {len(audio_paths)} audio chunks into: {output_path}")
                
                # Clean up chunk files
                for audio_path in audio_paths:
                    if os.path.exists(audio_path):
                        os.remove(audio_path)
                
                return output_path
            else:
                print(f"❌ Failed to combine audio files: {result.stderr}")
                # Return the first chunk as fallback
                return audio_paths[0] if audio_paths else output_path
                
        except Exception as e:
            print(f"Audio combination failed: {e}")
            # Return the first chunk as fallback
            return audio_paths[0] if audio_paths else output_path
    
    async def _text_to_speech_direct(
        self, 
        text: str, 
        output_path: str, 
        voice_name: Optional[str] = None,
        speaking_rate: float = 1.0,
        speaking_style: Optional[str] = None
    ) -> str:
        """
        Direct text-to-speech without chunking (to avoid recursion)
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Configure voice if specified
            if voice_name:
                self.speech_config.speech_synthesis_voice_name = voice_name
            
            # Create audio output configuration
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
            
            # Create speech synthesizer
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Prepare SSML for enhanced speech control
            ssml_text = self._create_ssml(text, speaking_rate, speaking_style, voice_name)
            
            # Perform synthesis
            result = await self._synthesize_speech_async(speech_synthesizer, ssml_text)
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print(f"✅ Direct speech synthesis completed: {output_path}")
                return output_path
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"❌ Direct Azure Speech failed: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    print(f"Error details: {cancellation_details.error_details}")
                print("🔄 Using fallback TTS...")
                return await self._fallback_text_to_speech(text, output_path)
            else:
                print(f"❌ Direct Azure Speech failed with reason: {result.reason}. Using fallback.")
                return await self._fallback_text_to_speech(text, output_path)
                
        except Exception as e:
            print(f"Direct Azure Speech error: {str(e)}. Using fallback.")
            return await self._fallback_text_to_speech(text, output_path)
    
    def _create_ssml(
        self, 
        text: str, 
        speaking_rate: float, 
        speaking_style: Optional[str],
        voice_name: Optional[str]
    ) -> str:
        """
        Create SSML (Speech Synthesis Markup Language) for enhanced speech control
        
        Args:
            text: Text to convert
            speaking_rate: Speech rate
            speaking_style: Voice style
            voice_name: Voice name
            
        Returns:
            SSML formatted string
        """
        # Get voice name
        voice = voice_name or self.speech_config.speech_synthesis_voice_name
        
        # Create SSML with enhanced controls
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name="{voice}">
                <prosody rate="{speaking_rate}">
                    {self._add_speech_enhancements(text)}
                </prosody>
            </voice>
        </speak>
        """
        
        return ssml.strip()
    
    def _add_speech_enhancements(self, text: str) -> str:
        """
        Add speech enhancements to make the narration more engaging
        
        Args:
            text: Original text
            
        Returns:
            Enhanced text with SSML markup
        """
        # Add pauses for better pacing
        enhanced_text = text.replace(". ", ". <break time='0.5s'/> ")
        enhanced_text = enhanced_text.replace("! ", "! <break time='0.8s'/> ")
        enhanced_text = enhanced_text.replace("? ", "? <break time='0.8s'/> ")
        
        # Add emphasis to important words (basic implementation)
        # In a more sophisticated version, you could use NLP to identify important words
        important_words = ["important", "key", "main", "primary", "essential", "crucial"]
        for word in important_words:
            enhanced_text = enhanced_text.replace(f" {word} ", f" <emphasis level='moderate'>{word}</emphasis> ")
        
        return enhanced_text
    
    async def _synthesize_speech_async(self, synthesizer: speechsdk.SpeechSynthesizer, ssml: str) -> speechsdk.SpeechSynthesisResult:
        """
        Perform asynchronous speech synthesis
        
        Args:
            synthesizer: Speech synthesizer instance
            ssml: SSML text to synthesize
            
        Returns:
            Speech synthesis result
        """
        # Run synthesis in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, synthesizer.speak_ssml, ssml)
        return result
    
    async def get_available_voices(self) -> list:
        """
        Get list of available Azure voices
        
        Returns:
            List of available voice information
        """
        try:
            # This would typically require a separate API call to Azure
            # For now, return a curated list of popular voices
            voices = [
                {
                    "name": "en-US-AriaNeural",
                    "display_name": "Aria (Female, US English)",
                    "gender": "Female",
                    "locale": "en-US",
                    "style": "chat"
                },
                {
                    "name": "en-US-DavisNeural",
                    "display_name": "Davis (Male, US English)",
                    "gender": "Male",
                    "locale": "en-US",
                    "style": "chat"
                },
                {
                    "name": "en-US-JennyNeural",
                    "display_name": "Jenny (Female, US English)",
                    "gender": "Female",
                    "locale": "en-US",
                    "style": "assistant"
                },
                {
                    "name": "en-US-GuyNeural",
                    "display_name": "Guy (Male, US English)",
                    "gender": "Male",
                    "locale": "en-US",
                    "style": "newscast"
                },
                {
                    "name": "en-US-AmberNeural",
                    "display_name": "Amber (Female, US English)",
                    "gender": "Female",
                    "locale": "en-US",
                    "style": "chat"
                }
            ]
            
            return voices
            
        except Exception as e:
            raise Exception(f"Failed to get available voices: {str(e)}")
    
    async def create_audio_with_timing(self, text: str, output_path: str, voice_name: Optional[str] = None) -> dict:
        """
        Create audio file with timing information for video synchronization
        
        Args:
            text: Text to convert
            output_path: Output audio file path
            voice_name: Voice to use
            
        Returns:
            Dictionary with audio path and timing information
        """
        try:
            # Generate the audio file
            audio_path = await self.text_to_speech(text, output_path, voice_name)
            
            # Estimate timing based on text length and speaking rate
            # This is a rough estimation - in production, you might want to use
            # Azure's detailed timing information if available
            words_per_minute = 150  # Average speaking rate
            word_count = len(text.split())
            estimated_duration = (word_count / words_per_minute) * 60
            
            timing_info = {
                "audio_path": audio_path,
                "estimated_duration": estimated_duration,
                "word_count": word_count,
                "speaking_rate": 1.0
            }
            
            return timing_info
            
        except Exception as e:
            raise Exception(f"Failed to create audio with timing: {str(e)}")
    
    def validate_voice_name(self, voice_name: str) -> bool:
        """
        Validate if a voice name is supported
        
        Args:
            voice_name: Voice name to validate
            
        Returns:
            True if voice is valid, False otherwise
        """
        # List of commonly available Azure voices
        valid_voices = [
            "en-US-AriaNeural",
            "en-US-DavisNeural", 
            "en-US-JennyNeural",
            "en-US-GuyNeural",
            "en-US-AmberNeural",
            "en-US-AshleyNeural",
            "en-US-BrandonNeural",
            "en-US-ChristopherNeural",
            "en-US-CoraNeural",
            "en-US-ElizabethNeural"
        ]
        
        return voice_name in valid_voices
    
    async def _fallback_text_to_speech(self, text: str, output_path: str) -> str:
        """
        Enhanced fallback text-to-speech using multiple methods
        
        Args:
            text: Text to convert to speech
            output_path: Path where audio file should be saved
            
        Returns:
            Path to the generated audio file
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Method 1: Try using pyttsx3 (Python TTS library)
            try:
                import pyttsx3
                import threading
                
                def run_tts():
                    engine = pyttsx3.init()
                    
                    # Configure voice properties
                    voices = engine.getProperty('voices')
                    if voices:
                        # Try to find a female voice
                        for voice in voices:
                            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                                engine.setProperty('voice', voice.id)
                                break
                    
                    engine.setProperty('rate', 150)  # Speed
                    engine.setProperty('volume', 0.8)  # Volume
                    
                    # Save to file
                    engine.save_to_file(text, output_path)
                    engine.runAndWait()
                
                # Run TTS in a separate thread to avoid blocking
                tts_thread = threading.Thread(target=run_tts)
                tts_thread.start()
                tts_thread.join(timeout=30)  # Wait max 30 seconds
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                    print(f"✅ Fallback TTS completed using pyttsx3. Audio saved to: {output_path}")
                    return output_path
                    
            except ImportError:
                print("pyttsx3 not available, trying espeak...")
            except Exception as e:
                print(f"pyttsx3 failed: {e}, trying espeak...")
            
            # Method 2: Try espeak (system TTS)
            try:
                import subprocess
                import asyncio
                
                # Convert text to speech using espeak with better voice
                cmd = [
                    'espeak', 
                    '-s', '160',  # Speed (slightly faster)
                    '-v', 'en+f3',   # English female voice
                    '-g', '10',   # Gap between words
                    '-p', '50',   # Pitch
                    '-w', output_path,  # Output file
                    text
                ]
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0 and os.path.exists(output_path):
                    print(f"✅ Fallback TTS completed using espeak. Audio saved to: {output_path}")
                    return output_path
                else:
                    print(f"espeak failed: {stderr.decode()}")
                    
            except FileNotFoundError:
                print("espeak not found, trying gTTS...")
            except Exception as e:
                print(f"espeak failed: {e}, trying gTTS...")
            
            # Method 3: Try Google Text-to-Speech (gTTS)
            try:
                from gtts import gTTS
                import io
                
                # Create gTTS object
                tts = gTTS(text=text, lang='en', slow=False)
                
                # Save to file
                tts.save(output_path)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                    print(f"✅ Fallback TTS completed using gTTS. Audio saved to: {output_path}")
                    return output_path
                    
            except ImportError:
                print("gTTS not available, creating silent audio...")
            except Exception as e:
                print(f"gTTS failed: {e}, creating silent audio...")
            
            # Method 4: Create a simple silent audio file as last resort
            await self._create_silent_audio(text, output_path)
            print(f"⚠️ Created silent audio file as fallback: {output_path}")
            return output_path
            
        except Exception as e:
            # Last resort: create a minimal audio file
            await self._create_silent_audio(text, output_path)
            print(f"❌ All fallback TTS methods failed: {e}. Created silent audio: {output_path}")
            return output_path
    
    async def _create_silent_audio(self, text: str, output_path: str):
        """
        Create a silent audio file as last resort
        
        Args:
            text: Text content (for duration calculation)
            output_path: Path where audio file should be saved
        """
        try:
            # Calculate duration based on text length (rough estimate)
            words_per_minute = 150
            word_count = len(text.split())
            duration_seconds = max(5, (word_count / words_per_minute) * 60)  # At least 5 seconds
            
            # Create a simple WAV file with silence
            import wave
            import struct
            
            sample_rate = 22050
            num_samples = int(sample_rate * duration_seconds)
            
            # Create silent audio data
            silent_data = struct.pack('h' * num_samples, *([0] * num_samples))
            
            with wave.open(output_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(silent_data)
                
        except Exception as e:
            print(f"Failed to create silent audio: {e}")
            # Create an empty file as absolute fallback
            with open(output_path, 'w') as f:
                f.write("")
