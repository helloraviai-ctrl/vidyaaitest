import { NextRequest, NextResponse } from 'next/server';
import { GroqService } from '../../../../backend/services/groq_service';
import { AzureSpeechService } from '../../../../backend/services/azure_speech_service';
import { AnimationService } from '../../../../backend/services/animation_service';
import { VideoService } from '../../../../backend/services/video_service';

// In-memory storage for processing status (in production, use Redis or database)
const processingJobs = new Map();

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { topic, difficulty_level = 'beginner', target_audience = 'students' } = body;

    if (!topic) {
      return NextResponse.json(
        { error: 'Topic is required' },
        { status: 400 }
      );
    }

    // Generate unique job ID
    const jobId = Math.random().toString(36).substring(2, 15);
    
    // Initialize processing status
    processingJobs.set(jobId, {
      job_id: jobId,
      status: 'started',
      progress: 0,
      message: 'Starting content generation...'
    });

    // Start background processing
    processContentGeneration(jobId, { topic, difficulty_level, target_audience });

    return NextResponse.json({
      job_id: jobId,
      status: 'processing',
      message: 'Content generation started. Use the job_id to check progress.'
    });

  } catch (error) {
    console.error('Error in generate-content:', error);
    return NextResponse.json(
      { error: 'Failed to start content generation' },
      { status: 500 }
    );
  }
}

async function processContentGeneration(jobId: string, request: any) {
  try {
    // Update status
    updateJobStatus(jobId, 'generating_text', 10, 'Generating explanation text...');

    // Step 1: Generate structured explanation using Groq AI
    const groqService = new GroqService();
    const explanationData = await groqService.generate_explanation(
      request.topic,
      request.difficulty_level,
      request.target_audience
    );

    updateJobStatus(jobId, 'generating_audio', 30, 'Converting text to speech...');

    // Step 2: Generate audio narration
    const azureSpeechService = new AzureSpeechService();
    const audioPath = await azureSpeechService.text_to_speech(
      explanationData.full_explanation,
      `/tmp/${jobId}_narration.wav`,
      'en-US-AriaNeural'
    );

    updateJobStatus(jobId, 'generating_animations', 50, 'Creating animated visuals...');

    // Step 3: Generate animations for each section
    const animationService = new AnimationService();
    const animationPaths = [];
    for (let i = 0; i < explanationData.sections.length; i++) {
      const section = explanationData.sections[i];
      const animationPath = await animationService.create_section_animation(
        section,
        i,
        `/tmp/${jobId}_section_${i}.mp4`
      );
      animationPaths.push(animationPath);
    }

    updateJobStatus(jobId, 'combining_video', 80, 'Combining audio and visuals...');

    // Step 4: Combine audio and animations into final video
    const videoService = new VideoService();
    const finalVideoPath = await videoService.create_final_video(
      audioPath,
      animationPaths,
      `/tmp/${jobId}_final_video.mp4`
    );

    // Update final status
    updateJobStatus(
      jobId,
      'completed',
      100,
      'Content generation completed successfully!',
      {
        audio_path: audioPath,
        video_path: finalVideoPath,
        text_path: `/tmp/${jobId}_explanation.txt`,
        sections: explanationData.sections,
        topic: request.topic
      }
    );

  } catch (error) {
    console.error('Error in processContentGeneration:', error);
    updateJobStatus(
      jobId,
      'failed',
      processingJobs.get(jobId)?.progress || 0,
      `Content generation failed: ${error.message}`
    );
  }
}

function updateJobStatus(jobId: string, status: string, progress: number, message: string, resultData?: any) {
  const job = processingJobs.get(jobId);
  if (job) {
    job.status = status;
    job.progress = progress;
    job.message = message;
    if (resultData) {
      job.result_data = resultData;
    }
    processingJobs.set(jobId, job);
  }
}

// Export the processing jobs for other API routes
export { processingJobs };
