import { NextResponse } from 'next/server';

export async function POST() {
  try {
    const stabilityApiKey = process.env.STABILITY_API_KEY;
    
    if (!stabilityApiKey) {
      return NextResponse.json({ error: 'Stability API key not found' }, { status: 400 });
    }

    const response = await fetch('https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${stabilityApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text_prompts: [
          {
            text: 'A simple educational diagram showing photosynthesis',
            weight: 1
          }
        ],
        cfg_scale: 7,
        height: 1024,
        width: 1024,
        samples: 1,
        steps: 30
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json({ 
        error: `Stability API error: ${response.status}`,
        details: errorText
      }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json({ 
      success: true, 
      message: 'Stability AI API is working!',
      artifacts: data.artifacts?.length || 0
    });

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    return NextResponse.json({ 
      error: `Test failed: ${errorMessage}` 
    }, { status: 500 });
  }
}
