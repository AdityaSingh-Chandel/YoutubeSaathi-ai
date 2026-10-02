import { useState } from 'react';

// Copies entirely in the browser. No API call.
export default function CopyButton({ text, label }) {
  const [done, setDone] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement('textarea');
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }
    setDone(true);
    setTimeout(() => setDone(false), 1500);
  }

  return (
    <button className="secondary" onClick={copy}>
      {done ? 'Copied' : label}
    </button>
  );
}
