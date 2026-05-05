import { useEffect, useRef, useState } from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  theme: 'neutral',
  fontFamily: 'IBM Plex Sans',
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true,
    curve: 'basis',
  },
  securityLevel: 'loose',
})

function sanitizeChart(raw) {
  let chart = raw.trim()

  // Strip markdown code fences
  chart = chart.replace(/^```mermaid\s*/i, '').replace(/^```\s*/m, '').replace(/```$/m, '').trim()

  // Ensure it starts with a graph/flowchart declaration
  if (!/^(graph|flowchart)\s/i.test(chart)) {
    chart = 'graph TD\n' + chart
  }

  // Process line by line to fix labels
  const lines = chart.split('\n')
  const cleaned = lines.map((line, i) => {
    if (i === 0) return line // keep graph declaration

    // Fix labels inside brackets: replace problematic chars
    // Match node definitions like A[Label] or A[Label with (parens)]
    return line.replace(/\[([^\]]*)\]/g, (match, label) => {
      let clean = label
        .replace(/[()]/g, ' ')
        .replace(/["/\\:;!@#$%^&*{}|<>~`]/g, ' ')
        .replace(/'/g, '')
        .replace(/\s+/g, ' ')
        .trim()
      return `[${clean}]`
    })
  })

  return cleaned.join('\n')
}

export default function MermaidDiagram({ chart }) {
  const containerRef = useRef(null)
  const [error, setError] = useState(false)
  const [rawChart, setRawChart] = useState('')

  useEffect(() => {
    if (!chart || !containerRef.current) return

    const sanitized = sanitizeChart(chart)
    setRawChart(sanitized)

    const render = async () => {
      try {
        const id = `mermaid-${Date.now()}`
        const { svg } = await mermaid.render(id, sanitized)
        if (containerRef.current) {
          containerRef.current.innerHTML = svg
        }
      } catch (e) {
        console.error('Mermaid render error:', e)
        setError(true)
      }
    }
    render()
  }, [chart])

  if (error) {
    return (
      <div className="p-5 bg-surface border border-border rounded-xl">
        <p className="font-body text-xs text-muted mb-3">Diagram could not be rendered. Raw structure:</p>
        <pre className="font-mono text-xs text-ink/60 whitespace-pre-wrap overflow-x-auto leading-5">{rawChart}</pre>
      </div>
    )
  }

  return (
    <div className="p-6 bg-white border border-border rounded-xl mermaid-container overflow-x-auto" ref={containerRef}>
      <p className="font-body text-xs text-muted">Rendering diagram...</p>
    </div>
  )
}