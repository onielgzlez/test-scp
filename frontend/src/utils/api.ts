interface QueryResponse {
  response: string;
  data?: any;
  error?: string;
}

function generateSessionId(): string {
  return 'session_' + Math.random().toString(36).substring(2, 15)
}

export default async function sendQuery(query: string): Promise<QueryResponse> {
  try {
    const request = await fetch('/api/ask.json', {
      method: "POST",
      body: JSON.stringify({
        chatInput: query,
        sessionId: generateSessionId(),
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const response = await request.json()

    return {
      ...response,
    }
  } catch (error) {
    console.error('Error sending query to n8n:', error);
    
    return {
      response: 'Sorry, I encountered an error processing your request.',
      error: error instanceof Error ? error.message : String(error),
    }
  }
}