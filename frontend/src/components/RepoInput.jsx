import { useState } from 'react'

export default function RepoInput({ onSubmit, loading }) {
  const [url, setUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (url.trim()) onSubmit(url.trim())
  }

  const examples = [
    'https://github.com/tiangolo/fastapi',
    'https://github.com/t3-oss/create-t3-app',
    'https://github.com/pocketbase/pocketbase',
  ]

  return (
    <div className="fade-up">
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-muted/40">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
              </svg>
            </span>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste a GitHub repository URL..."
              className="w-full pl-12 pr-4 py-4 bg-white border border-border rounded-xl font-mono text-sm text-ink placeholder:text-muted/40 focus:outline-none focus:border-accent/50 focus:ring-2 focus:ring-accent/10 transition-all"
              disabled={loading}
            />
          </div>
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="px-7 py-4 bg-ink text-parchment font-body text-sm font-medium rounded-xl hover:bg-ink/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
          >
            {loading ? 'Analyzing...' : 'Explain'}
          </button>
        </div>
      </form>

      <div className="mt-4 flex items-center gap-2 flex-wrap">
        <span className="font-body text-xs text-muted/50">Try:</span>
        {examples.map((ex) => (
          <button
            key={ex}
            onClick={() => { setUrl(ex); if (!loading) onSubmit(ex); }}
            disabled={loading}
            className="font-mono text-xs text-accent/70 hover:text-accent border border-transparent hover:border-accent/20 px-2.5 py-1 rounded-md transition-all disabled:opacity-40"
          >
            {ex.replace('https://github.com/', '')}
          </button>
        ))}
      </div>
    </div>
  )
}
