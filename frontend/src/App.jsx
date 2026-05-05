import { useState } from 'react'
import RepoInput from './components/RepoInput'
import ExplainerOutput from './components/ExplainerOutput'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [step, setStep] = useState('')

  const handleExplain = async (repoUrl) => {
    setLoading(true)
    setError(null)
    setResult(null)
    setStep('Fetching repository structure...')

    try {
      const timer1 = setTimeout(() => setStep('Analyzing file relationships...'), 4000)
      const timer2 = setTimeout(() => setStep('Generating architecture insights...'), 9000)
      const timer3 = setTimeout(() => setStep('Building onboarding guide...'), 15000)

      const resp = await fetch(`${API_URL}/api/explain`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl }),
      })

      clearTimeout(timer1)
      clearTimeout(timer2)
      clearTimeout(timer3)

      if (!resp.ok) {
        const data = await resp.json()
        throw new Error(data.detail || 'Failed to analyze repository')
      }

      const data = await resp.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
      setStep('')
    }
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b border-border">
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-baseline justify-between">
          <div>
            <h1 className="font-display text-3xl text-ink tracking-tight">
              Codebase Explainer
            </h1>
            <p className="font-body text-sm text-muted mt-1 font-light">
              Understand any GitHub repository in minutes
            </p>
          </div>
          <span className="font-mono text-xs text-muted/50 tracking-wider"> </span>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10">
        <RepoInput onSubmit={handleExplain} loading={loading} />

        {/* Loading State */}
        {loading && (
          <div className="mt-12 text-center">
            <div className="flex justify-center gap-2 mb-4">
              <div className="w-2.5 h-2.5 rounded-full bg-accent loading-dot" />
              <div className="w-2.5 h-2.5 rounded-full bg-accent loading-dot" />
              <div className="w-2.5 h-2.5 rounded-full bg-accent loading-dot" />
            </div>
            <p className="font-body text-sm text-muted">{step}</p>
            <div className="mt-4 max-w-xs mx-auto h-1 bg-border rounded-full overflow-hidden">
              <div className="h-full bg-accent/60 rounded-full progress-bar" />
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-8 p-5 bg-red-50 border border-red-200 rounded-lg">
            <p className="font-body text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && <ExplainerOutput data={result} />}
      </main>

      <footer className="border-t border-border mt-20">
        <div className="max-w-5xl mx-auto px-6 py-5 flex justify-between items-center">
          <span className="font-mono text-xs text-muted/40">codebase-explainer v1.0</span>
          <span className="font-body text-xs text-muted/40"> </span>
        </div>
      </footer>
    </div>
  )
}
