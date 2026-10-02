import { useState } from 'react';
import { analyzeVideo, askQuestion } from './api';
import CopyButton from './components/CopyButton';

const pad = (n) => String(n).padStart(2, '0');
function formatDuration(s) {
  if (!s) return '—';
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  return h ? `${h}:${pad(m)}:${pad(sec)}` : `${m}:${pad(sec)}`;
}

export default function App() {
  const [url, setUrl] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState('');

  const [question, setQuestion] = useState('');
  const [asking, setAsking] = useState(false);
  const [qaError, setQaError] = useState('');
  const [answers, setAnswers] = useState([]); // in-page only, newest first

  async function onAnalyze() {
    setError(''); setQaError(''); setAnalysis(null); setAnswers([]);
    if (!url.trim()) return setError('Please enter a valid YouTube URL.');
    setAnalyzing(true);
    try {
      setAnalysis(await analyzeVideo(url.trim()));
    } catch (e) {
      setError(e.message);
    } finally {
      setAnalyzing(false);
    }
  }

  async function onAsk() {
    setQaError('');
    if (!question.trim()) return setQaError('Please enter a question.');
    setAsking(true);
    try {
      const r = await askQuestion(analysis.session_id, question.trim());
      setAnswers((prev) => [{ question: question.trim(), ...r }, ...prev]);
      setQuestion('');
    } catch (e) {
      setQaError(e.message);
    } finally {
      setAsking(false);
    }
  }

  return (
    <main>
      <h1>YouTube Video AI Analyzer</h1>

      <section>
        <label htmlFor="url">Paste YouTube URL</label>
        <div className="row">
          <input id="url" value={url} placeholder="https://www.youtube.com/watch?v=..."
                 onChange={(e) => setUrl(e.target.value)}
                 onKeyDown={(e) => e.key === 'Enter' && !analyzing && onAnalyze()} />
          <button onClick={onAnalyze} disabled={analyzing}>
            {analyzing ? 'Analyzing…' : 'Analyze Video'}
          </button>
        </div>
        {analyzing && <p className="muted">Fetching transcript and building the index. Long videos can take a minute.</p>}
        {error && <p className="error" role="alert">{error}</p>}
      </section>

      {analysis && (
        <>
          <section>
            <h2>Video information</h2>
            <dl>
              <dt>Title</dt><dd>{analysis.video.title}</dd>
              <dt>Channel</dt><dd>{analysis.video.channel}</dd>
              <dt>Duration</dt><dd>{formatDuration(analysis.video.duration_seconds)}</dd>
            </dl>
          </section>

          <section>
            <h2>Summary</h2>
            <p className="text">{analysis.summary}</p>
            <CopyButton text={analysis.summary} label="Copy Summary" />
          </section>

          <section>
            <h2>Ask a question</h2>
            <div className="row">
              <input value={question} placeholder="What did the speaker say about…?"
                     onChange={(e) => setQuestion(e.target.value)}
                     onKeyDown={(e) => e.key === 'Enter' && !asking && onAsk()} />
              <button onClick={onAsk} disabled={asking}>{asking ? 'Thinking…' : 'Ask'}</button>
            </div>
            {qaError && <p className="error" role="alert">{qaError}</p>}

            {answers.map((a, i) => (
              <article key={answers.length - i} className="answer">
                <p className="muted">Q: {a.question}</p>
                <p className="text">{a.answer}</p>
                {!a.grounded && <p className="muted">Not found in the video.</p>}
                <CopyButton text={a.answer} label="Copy Answer" />
              </article>
            ))}
          </section>

          <section>
            <h2>Transcript</h2>
            <div className="transcript">{analysis.transcript}</div>
          </section>
        </>
      )}
    </main>
  );
}
