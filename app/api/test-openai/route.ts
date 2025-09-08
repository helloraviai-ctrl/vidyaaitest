import { NextResponse } from 'next/server';

export async function POST() {
  try {
    const openaiApiKey = process.env.OPENAI_API_KEY;
    
    if (!openaiApiKey) {
      return NextResponse.json({ error: 'OpenAI API key not found' }, { status: 400 });
    }

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${openaiApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
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
        error: `OpenAI API error: ${response.status}`,
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
