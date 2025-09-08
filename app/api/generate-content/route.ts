import { NextRequest, NextResponse } from 'next/server';

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
    const groqApiKey = process.env.GROQ_API_KEY;
    if (!groqApiKey) {
      throw new Error('GROQ_API_KEY not found in environment variables');
    }

    const explanationData = await generateExplanationWithGroq(
      request.topic,
      request.difficulty_level,
      request.target_audience,
      groqApiKey
    );

    updateJobStatus(jobId, 'generating_audio', 30, 'Converting text to speech...');

    // Step 2: Generate audio narration
    const azureSpeechKey = process.env.AZURE_SPEECH_KEY;
    const azureSpeechRegion = process.env.AZURE_SPEECH_REGION;
    
    if (!azureSpeechKey || !azureSpeechRegion) {
      throw new Error('Azure Speech credentials not found in environment variables');
    }

    const audioPath = await generateAudioWithAzure(
      explanationData.full_explanation,
      azureSpeechKey,
      azureSpeechRegion
    );

    updateJobStatus(jobId, 'generating_animations', 50, 'Creating animated visuals...');

    // Step 3: Generate animations for each section
    const animationPaths = [];
    for (let i = 0; i < explanationData.sections.length; i++) {
      const section = explanationData.sections[i];
      const animationPath = await createSectionAnimation(section, i);
      animationPaths.push(animationPath);
    }

    updateJobStatus(jobId, 'combining_video', 80, 'Combining audio and visuals...');

    // Step 4: Combine audio and animations into final video
    const finalVideoPath = await createFinalVideo(audioPath, animationPaths);

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

async function generateExplanationWithGroq(topic: string, difficulty: string, audience: string, apiKey: string) {
  // Simplified Groq API call
  const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'llama3-8b-8192',
      messages: [
        {
          role: 'system',
          content: `You are an educational content generator. Create structured explanations for ${audience} at ${difficulty} level.`
        },
        {
          role: 'user',
          content: `Generate educational content about: ${topic}`
        }
      ],
      temperature: 0.7,
      max_tokens: 2000
    })
  });

  if (!response.ok) {
    throw new Error(`Groq API error: ${response.status}`);
  }

  const data = await response.json();
  const content = data.choices[0].message.content;

  // Parse and structure the content
  const sections = content.split('\n\n').map((section: string, index: number) => ({
    title: `Section ${index + 1}`,
    content: section.trim(),
    duration: 10
  }));

  return {
    full_explanation: content,
    sections: sections
  };
}

async function generateAudioWithAzure(text: string, apiKey: string, region: string) {
  // Simplified Azure Speech API call
  const response = await fetch(`https://${region}.tts.speech.microsoft.com/cognitiveservices/v1`, {
    method: 'POST',
    headers: {
      'Ocp-Apim-Subscription-Key': apiKey,
      'Content-Type': 'application/ssml+xml',
      'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm'
    },
    body: `<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' name='en-US-AriaNeural'>${text}</voice></speak>`
  });

  if (!response.ok) {
    throw new Error(`Azure Speech API error: ${response.status}`);
  }

  // Return a mock audio path for now
  return `/tmp/audio_${Date.now()}.wav`;
}

async function createSectionAnimation(section: any, index: number) {
  // Simplified animation creation
  return `/tmp/animation_${index}_${Date.now()}.mp4`;
}

async function createFinalVideo(audioPath: string, animationPaths: string[]) {
  // Simplified video creation
  return `/tmp/video_${Date.now()}.mp4`;
}

// Export the processing jobs for other API routes
export { processingJobs };
