'use client'

import { useState, useEffect } from 'react'
import { BookOpen, Mic, Video, Play, Pause, Volume2, VolumeX } from 'lucide-react'

export default function Home() {
  const [topic, setTopic] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [videoData, setVideoData] = useState<any>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isMuted, setIsMuted] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!topic.trim()) return

    setIsGenerating(true)
    setVideoData(null)
    setIsPlaying(false)
    
    // Use environment variable for API URL, fallback to localhost for development
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, difficulty_level: 'beginner', target_audience: 'students' })
      })
      
      const data = await response.json()
      
      // Poll for status
      const pollStatus = async () => {
        const statusResponse = await fetch(`${API_BASE_URL}/api/status/${data.job_id}`)
        const status = await statusResponse.json()
        
        if (status.status === 'completed') {
          // Check if we have a video path in the result data
          const videoPath = status.result_data?.video_path
          let videoUrl = null
          
          if (videoPath) {
            // If we have a video path, construct the URL
            if (videoPath.includes('.mp4')) {
              videoUrl = `${API_BASE_URL}/api/video/${data.job_id}`
            } else if (videoPath.includes('.png') || videoPath.includes('.jpg')) {
              videoUrl = `${API_BASE_URL}/api/video/${data.job_id}`
            } else {
              // For text files or other content, still try the video endpoint
              videoUrl = `${API_BASE_URL}/api/video/${data.job_id}`
            }
          } else {
            // Fallback: try the video endpoint anyway
            videoUrl = `${API_BASE_URL}/api/video/${data.job_id}`
          }
          
          // Create video data object with the video URL and status info
          const videoContent = {
            videoUrl: videoUrl,
            topic: status.result_data?.topic || topic,
            duration: status.result_data?.duration || "3-5 minutes",
            sections: status.result_data?.sections || [],
            job_id: data.job_id,
            videoPath: videoPath
          }
          
          setVideoData(videoContent)
          setIsGenerating(false)
        } else if (status.status === 'failed') {
          alert('Generation failed: ' + status.message)
          setIsGenerating(false)
        } else {
          setTimeout(pollStatus, 1000)
        }
      }
      
      pollStatus()
    } catch (error) {
      alert('Error: ' + error)
      setIsGenerating(false)
    }
  }

  const togglePlayPause = () => {
    const videoElement = document.querySelector('video')
    if (videoElement) {
      if (isPlaying) {
        videoElement.pause()
      } else {
        videoElement.play()
      }
    }
  }

  const toggleMute = () => {
    const videoElement = document.querySelector('video')
    if (videoElement) {
      videoElement.muted = !isMuted
      setIsMuted(!isMuted)
    }
  }

  const restartVideo = () => {
    const videoElement = document.querySelector('video')
    if (videoElement) {
      videoElement.currentTime = 0
      videoElement.play()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-4 sm:py-8">
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-800 mb-2 sm:mb-4">
            Vidya AI
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-gray-600 max-w-2xl mx-auto px-4">
            Enter any topic and watch your educational video play instantly!
          </p>
        </div>

        <div className="max-w-6xl mx-auto">
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-4 sm:p-6 md:p-8 mb-6 sm:mb-8">
            <div className="mb-4 sm:mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enter a topic to explain:
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Photosynthesis, Machine Learning, World War II..."
                className="w-full px-3 sm:px-4 py-2 sm:py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base sm:text-lg"
                disabled={isGenerating}
              />
            </div>
            
            <button
              type="submit"
              disabled={isGenerating || !topic.trim()}
              className="w-full bg-blue-600 text-white py-3 sm:py-4 px-4 sm:px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-base sm:text-lg font-semibold"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                  Creating Your Video...
                </>
              ) : (
                <>
                  <Play className="w-6 h-6" />
                  Create & Play Educational Video
                </>
              )}
            </button>
          </form>

          {isGenerating && (
            <div className="bg-white rounded-lg shadow-lg p-4 sm:p-6 md:p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-4 border-blue-600 mx-auto mb-4 sm:mb-6"></div>
              <h3 className="text-lg sm:text-xl font-semibold text-gray-800 mb-2">Creating Your Video</h3>
              <p className="text-sm sm:text-base text-gray-600">Generating AI explanation, visuals, and audio...</p>
              <p className="text-xs sm:text-sm text-gray-500 mt-2">Video will start playing automatically!</p>
            </div>
          )}

          {videoData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 lg:gap-8">
              {/* Video Player Section */}
              <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                {/* Video Player Header */}
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 sm:p-6">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-0">
                    <div className="flex-1">
                      <h2 className="text-lg sm:text-xl md:text-2xl font-bold mb-1 sm:mb-2">🎬 {videoData.topic}</h2>
                      <p className="text-blue-100 text-sm sm:text-base">Educational Video • {videoData.duration}</p>
                    </div>
                    <div className="flex items-center gap-2 sm:gap-4">
                      {videoData && videoData.videoUrl && videoData.videoUrl.includes('.mp4') ? (
                        <>
                          <button
                            onClick={toggleMute}
                            className="p-1.5 sm:p-2 rounded-full bg-white/20 hover:bg-white/30 transition-colors"
                            title={isMuted ? "Unmute" : "Mute"}
                          >
                            {isMuted ? <VolumeX className="w-4 h-4 sm:w-6 sm:h-6" /> : <Volume2 className="w-4 h-4 sm:w-6 sm:h-6" />}
                          </button>
                          <button
                            onClick={togglePlayPause}
                            className="p-2 sm:p-3 rounded-full bg-white/20 hover:bg-white/30 transition-colors"
                            title={isPlaying ? "Pause" : "Play"}
                          >
                            {isPlaying ? <Pause className="w-6 h-6 sm:w-8 sm:h-8" /> : <Play className="w-6 h-6 sm:w-8 sm:h-8" />}
                          </button>
                          <button
                            onClick={restartVideo}
                            className="p-1.5 sm:p-2 rounded-full bg-white/20 hover:bg-white/30 transition-colors"
                            title="Restart Video"
                          >
                            <svg className="w-4 h-4 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                            </svg>
                          </button>
                        </>
                      ) : (
                        <div className="text-white/80 text-sm">
                          📸 Educational Slide
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Video Content Area */}
                <div className="relative bg-black min-h-[250px] sm:min-h-[300px] md:min-h-[400px] flex items-center justify-center overflow-hidden">
                  {videoData.videoUrl ? (
                    <div className="w-full h-full relative">
                      {/* Check if it's a video or image */}
                      {videoData.videoPath && videoData.videoPath.includes('.mp4') ? (
                        /* Actual Video Player */
                        <video 
                          src={videoData.videoUrl}
                          controls
                          autoPlay
                          className="w-full h-full object-contain"
                          onPlay={() => setIsPlaying(true)}
                          onPause={() => setIsPlaying(false)}
                          onEnded={() => setIsPlaying(false)}
                          onError={(e) => {
                            console.error('Video error:', e);
                            console.log('Video URL:', videoData.videoUrl);
                            console.log('Video Path:', videoData.videoPath);
                          }}
                        >
                          Your browser does not support the video tag.
                        </video>
                      ) : (
                        /* Image Display for PNG/JPG content or fallback */
                        <div className="w-full h-full flex items-center justify-center p-2">
                          <img 
                            src={videoData.videoUrl}
                            alt={`Educational content for ${videoData.topic}`}
                            className="max-w-full max-h-full object-contain"
                            style={{ maxHeight: '250px' }}
                            onError={(e) => {
                              console.error('Image error:', e);
                              console.log('Video URL:', videoData.videoUrl);
                              console.log('Video Path:', videoData.videoPath);
                            }}
                          />
                        </div>
                      )}
                      
                    </div>
                  ) : (
                    <div className="text-center text-white p-4">
                      <div className="animate-spin rounded-full h-12 w-12 sm:h-16 sm:w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
                      <p className="text-base sm:text-xl">Loading content...</p>
                    </div>
                  )}
                </div>

                {/* Video Controls */}
                <div className="p-3 sm:p-4 bg-gray-50">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0">
                    <div className="flex items-center gap-2 sm:gap-4">
                      {videoData.videoUrl && videoData.videoUrl.includes('.mp4') ? (
                        <>
                          <span className="text-xs sm:text-sm text-gray-600">
                            {isPlaying ? '🔊 Playing' : '⏸️ Paused'}
                          </span>
                          <span className="text-xs sm:text-sm text-gray-600">
                            {isMuted ? '🔇 Muted' : '🔊 Audio On'}
                          </span>
                        </>
                      ) : (
                        <span className="text-xs sm:text-sm text-gray-600">
                          📸 Educational Slide Display
                        </span>
                      )}
                    </div>
                    <div className="text-xs sm:text-sm text-gray-600">
                      {videoData.videoUrl && videoData.videoUrl.includes('.mp4') ? (
                        `Duration: ${videoData.duration}`
                      ) : (
                        `Content: ${videoData.duration}`
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Educational Content Section */}
              <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="bg-gradient-to-r from-green-600 to-teal-600 text-white p-4 sm:p-6">
                  <h3 className="text-lg sm:text-xl md:text-2xl font-bold mb-2 flex items-center gap-2">
                    <BookOpen className="w-5 h-5 sm:w-6 sm:h-6" />
                    Educational Content
                  </h3>
                  <p className="text-green-100 text-sm sm:text-base">Structured learning material for {videoData.topic}</p>
                </div>

                <div className="p-4 sm:p-6 max-h-[400px] sm:max-h-[500px] md:max-h-[600px] overflow-y-auto">
                  {videoData.sections && videoData.sections.length > 0 ? (
                    <div className="space-y-4 sm:space-y-6 md:space-y-8">
                      {videoData.sections.map((section: any, index: number) => (
                        <div key={index} className="bg-white border-2 border-gray-200 rounded-xl p-3 sm:p-4 md:p-6 shadow-lg hover:shadow-xl transition-shadow">
                          {/* Slide Number */}
                          <div className="flex items-center justify-between mb-3 sm:mb-4">
                            <span className="bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xs sm:text-sm font-bold px-2 sm:px-3 py-1 rounded-full">
                              Slide {index + 1}
                            </span>
                            {section.duration_estimate && (
                              <span className="text-xs text-gray-500 bg-gray-100 px-2 sm:px-3 py-1 rounded-full">
                                ~{section.duration_estimate}s
                              </span>
                            )}
                          </div>

                          {/* Title Section with Emoji */}
                          <div className="mb-3 sm:mb-4">
                            <h4 className="text-lg sm:text-xl md:text-2xl font-bold text-gray-800 mb-2 text-center">
                              {section.title}
                            </h4>
                          </div>

                          {/* Subheading / Question */}
                          {section.subheading && (
                            <div className="mb-4 sm:mb-6 text-center">
                              <h5 className="text-sm sm:text-base md:text-lg font-bold text-gray-700 underline decoration-2 decoration-blue-500">
                                {section.subheading.replace(/\*\*/g, '')}
                              </h5>
                            </div>
                          )}

                          {/* Main Explanation (Boxed) */}
                          <div className="mb-4 sm:mb-6">
                            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-lg p-3 sm:p-4 shadow-inner">
                              <p className="text-gray-700 leading-relaxed text-sm sm:text-base font-medium text-center">
                                {section.content}
                              </p>
                            </div>
                          </div>

                          {/* Key Points (Bulleted List) */}
                          {section.key_points && section.key_points.length > 0 && (
                            <div className="mb-4 sm:mb-6">
                              <h6 className="text-xs sm:text-sm font-semibold text-gray-600 mb-2 sm:mb-3 text-center">Key Points</h6>
                              <ul className="space-y-1 sm:space-y-2">
                                {section.key_points.map((point: string, pointIndex: number) => (
                                  <li key={pointIndex} className="flex items-start gap-2 sm:gap-3 bg-green-50 p-2 sm:p-3 rounded-lg border border-green-200">
                                    <span className="text-green-600 font-bold mt-0.5 sm:mt-1 text-sm sm:text-lg flex-shrink-0">•</span>
                                    <span className="text-gray-700 text-xs sm:text-sm leading-relaxed font-medium">
                                      {point.replace(/^•\s*/, '')}
                                    </span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {/* Visual Suggestion */}
                          {section.visual_description && (
                            <div className="bg-gradient-to-r from-purple-50 to-pink-50 border-2 border-purple-200 rounded-lg p-3 sm:p-4">
                              <h6 className="text-xs sm:text-sm font-semibold text-purple-800 mb-2 flex items-center gap-2">
                                <Video className="w-3 h-3 sm:w-4 sm:h-4" />
                                Visual Suggestion
                              </h6>
                              <p className="text-purple-700 text-xs sm:text-sm leading-relaxed font-medium">
                                {section.visual_description}
                              </p>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-500">No structured content available for this topic.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
