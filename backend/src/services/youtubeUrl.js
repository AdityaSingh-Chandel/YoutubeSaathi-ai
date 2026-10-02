const ID_RE = /^[\w-]{11}$/;
const HOSTS = new Set(['youtube.com', 'www.youtube.com', 'm.youtube.com']);

// Returns the video ID, or null if the URL is not a supported YouTube URL.
export function parseYouTubeId(input) {
  try {
    const u = new URL(String(input).trim());
    if (!['http:', 'https:'].includes(u.protocol)) return null;
    let id = null;
    if (u.hostname === 'youtu.be') id = u.pathname.slice(1).split('/')[0];
    else if (HOSTS.has(u.hostname)) {
      if (u.pathname === '/watch') id = u.searchParams.get('v');
      else id = (u.pathname.match(/^\/(?:shorts|embed)\/([\w-]{11})/) || [])[1] || null;
    }
    return id && ID_RE.test(id) ? id : null;
  } catch {
    return null;
  }
}
