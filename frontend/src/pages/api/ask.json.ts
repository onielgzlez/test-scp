import { API_URL } from 'astro:env/server'

export async function POST({ request }: { request: Request }) {
  try {
    const body = await request.json()
    // Extract values from the request body
    const { chatInput, sessionId } = body
    
    if (!chatInput) {
      return new Response(
        JSON.stringify({ 
          error: 'Missing required fields: chatInput is required.'
        }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        }
      )
    }

    const response = await fetch(API_URL + "webhook-test/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        chatInput: chatInput,
        sessionId: sessionId,
      }),
    })

    if (response.ok) {
      const responseData = await response.json()
      const data = responseData[0]?.output
        || responseData[0]?.response
        || ''

      return new Response(
        JSON.stringify({ response: data }),
        {
          headers: { "Content-Type": "application/json" },
        }
      )
    } else {
      console.error('Error sending message:', response.status);

      return new Response(
        JSON.stringify({ error: 'Sorry, I encountered an error processing your request.' }),
        {
          headers: { "Content-Type": "application/json" },
        }
      )
    }
  } catch (error) {
    console.error('Error sending message:', error);

    return new Response(
      JSON.stringify({ error: 'Sorry, I encountered an error processing your request.' }),
      {
        headers: { "Content-Type": "application/json" },
      }
    )
  }
}