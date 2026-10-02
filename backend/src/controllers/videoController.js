import { ApiError } from '../middleware/errorHandler.js';
import { parseYouTubeId } from '../services/youtubeUrl.js';
import * as ai from '../services/aiService.js';

export async function analyze(req, res) {
  const url = req.body?.youtube_url;
  if (typeof url !== 'string' || !parseYouTubeId(url)) {
    throw new ApiError(400, 'INVALID_URL', 'Please enter a valid YouTube URL.');
  }
  res.json(await ai.analyze(url.trim()));
}

export async function question(req, res) {
  const { session_id, question: q } = req.body || {};
  if (typeof q !== 'string' || !q.trim()) {
    throw new ApiError(400, 'EMPTY_QUESTION', 'Please enter a question.');
  }
  if (q.length > 1000) {
    throw new ApiError(400, 'QUESTION_TOO_LONG', 'Please keep your question under 1000 characters.');
  }
  if (typeof session_id !== 'string' || !session_id) {
    throw new ApiError(404, 'SESSION_EXPIRED', 'This analysis session has expired. Please analyze the video again.');
  }
  res.json(await ai.question(session_id, q.trim()));
}

export async function removeSession(req, res) {
  await ai.deleteSession(req.params.id);
  res.json({ deleted: true });
}
