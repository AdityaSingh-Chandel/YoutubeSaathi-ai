// The ONLY place the frontend talks to the backend. No AI logic here.
async function post(path, body) {
  let res;
  try {
    res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch {
    throw new Error('Could not reach the server. Please try again.');
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(data?.error?.message || 'Something went wrong. Please try again.');
  return data;
}

export const analyzeVideo = (youtube_url) => post('/api/analyze', { youtube_url });
export const askQuestion = (session_id, question) => post('/api/question', { session_id, question });
