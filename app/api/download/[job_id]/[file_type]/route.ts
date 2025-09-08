import { NextRequest, NextResponse } from 'next/server';
import { processingJobs } from '../../../generate-content/route';
import fs from 'fs';
import path from 'path';

export async function GET(
  request: NextRequest,
  { params }: { params: { job_id: string; file_type: string } }
) {
  try {
    const { job_id, file_type } = params;

    if (!job_id || !file_type) {
      return NextResponse.json(
        { error: 'Job ID and file type are required' },
        { status: 400 }
      );
    }

    const job = processingJobs.get(job_id);

    if (!job) {
      return NextResponse.json(
        { error: 'Job not found' },
        { status: 404 }
      );
    }

    if (job.status !== 'completed') {
      return NextResponse.json(
        { error: 'Job not completed yet' },
        { status: 400 }
      );
    }

    // Determine file path based on type
    let filePath: string;
    let contentType: string;
    let filename: string;

    switch (file_type) {
      case 'audio':
        filePath = job.result_data?.audio_path;
        contentType = 'audio/wav';
        filename = `${job_id}_audio.wav`;
        break;
      case 'video':
        filePath = job.result_data?.video_path;
        contentType = 'video/mp4';
        filename = `${job_id}_video.mp4`;
        break;
      case 'text':
        filePath = job.result_data?.text_path;
        contentType = 'text/plain';
        filename = `${job_id}_explanation.txt`;
        break;
      default:
        return NextResponse.json(
          { error: 'Invalid file type. Use: audio, video, or text' },
          { status: 400 }
        );
    }

    if (!filePath || !fs.existsSync(filePath)) {
      return NextResponse.json(
        { error: 'File not found' },
        { status: 404 }
      );
    }

    // Read file and return as response
    const fileBuffer = fs.readFileSync(filePath);

    return new NextResponse(fileBuffer, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Content-Length': fileBuffer.length.toString(),
      },
    });

  } catch (error) {
    console.error('Error in file download:', error);
    return NextResponse.json(
      { error: 'Failed to download file' },
      { status: 500 }
    );
  }
}
