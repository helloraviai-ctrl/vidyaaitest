import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    groq_key: process.env.GROQ_API_KEY ? 'SET' : 'NOT SET',
    openai_key: process.env.OPENAI_API_KEY ? 'SET' : 'NOT SET',
    stability_key: process.env.STABILITY_API_KEY ? 'SET' : 'NOT SET',
    azure_key: process.env.AZURE_SPEECH_KEY ? 'SET' : 'NOT SET',
    azure_region: process.env.AZURE_SPEECH_REGION ? 'SET' : 'NOT SET',
    node_env: process.env.NODE_ENV
  });
}
