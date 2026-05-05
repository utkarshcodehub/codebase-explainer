const IMPORTANCE_STYLES = {
  critical: { dot: 'bg-red-400', label: 'text-red-600' },
  important: { dot: 'bg-amber-400', label: 'text-amber-600' },
  supporting: { dot: 'bg-green-400', label: 'text-green-600' },
}

export default function FileMap({ modules, entryPoints }) {
  return (
    <div className="space-y-6">
      {/* Entry Points */}
      {entryPoints && entryPoints.length > 0 && (
        <div>
          <h4 className="font-body text-xs font-semibold text-muted/60 uppercase tracking-wider mb-3">Entry Points</h4>
          <div className="space-y-2">
            {entryPoints.map((ep, i) => (
              <div key={i} className="flex items-start gap-3 p-3 bg-accent/5 border border-accent/10 rounded-lg">
                <span className="font-mono text-sm text-accent shrink-0 mt-0.5">→</span>
                <div>
                  <span className="font-mono text-sm text-ink">{ep.file}</span>
                  <p className="font-body text-xs text-muted mt-0.5">{ep.purpose}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Modules */}
      <div className="grid gap-2">
        {modules.map((mod, i) => {
          const style = IMPORTANCE_STYLES[mod.importance] || IMPORTANCE_STYLES.supporting
          return (
            <div key={i} className="flex items-start gap-3 p-3 bg-white border border-border rounded-lg">
              <div className={`w-2 h-2 rounded-full ${style.dot} shrink-0 mt-1.5`} />
              <div className="flex-1 min-w-0">
                <div className="flex items-baseline gap-2">
                  <span className="font-mono text-sm text-ink truncate">{mod.path}</span>
                  <span className={`font-mono text-[10px] uppercase ${style.label}`}>{mod.importance}</span>
                </div>
                <p className="font-body text-xs text-muted mt-0.5">{mod.role}</p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
