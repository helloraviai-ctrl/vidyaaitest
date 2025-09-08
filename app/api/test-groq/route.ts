import { NextResponse } from 'next/server';

export async function POST() {
  try {
    const groqApiKey = process.env.GROQ_API_KEY;
    
    if (!groqApiKey) {
      return NextResponse.json({ error: 'Groq API key not found' }, { status: 400 });
    }

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${groqApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'llama-3.1-8b-instant',
        messages: [
          {
            role: 'user',
            content: 'Say "Hello, this is a test!"'
          }
        ],
        max_tokens: 50
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json({ 
        error: `Groq API error: ${response.status}`,
        details: errorText
      }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json({ 
      success: true, 
      message: data.choices[0].message.content 
    });

  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
    return NextResponse.json({ 
      error: `Test failed: ${errorMessage}` 
    }, { status: 500 });
  }
}
