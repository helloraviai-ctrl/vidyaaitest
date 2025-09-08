import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    message: 'Vidya AI Educational Content Generator API',
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
}
