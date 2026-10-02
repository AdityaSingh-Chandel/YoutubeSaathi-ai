import { ApiError } from '../middleware/errorHandler.js';

const BASE = () => process.env.AI_SERVICE_URL || 'http://localhost:8000';

async function call(method, path, body) {
  let res;
  try {
    res = await fetch(`${BASE()}${path}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(180_000), // analysis of long videos can take a while
    });
  } catch {
    throw new ApiError(503, 'AI_SERVICE_UNAVAILABLE', 'The analysis service is unavailable. Please try again later.');
  }
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const e = data?.error;
    throw new ApiError(
      res.status >= 400 ? res.status : 502,
      e?.code || 'AI_FAILED',
      e?.message || 'AI processing temporarily failed. Please try again.'
    );
  }
  return data;
}

export const analyze = (youtube_url) => call('POST', '/analyze', { youtube_url });
export const question = (session_id, q) => call('POST', '/question', { session_id, question: q });
export const deleteSession = (id) => call('DELETE', `/session/${encodeURIComponent(id)}`);
