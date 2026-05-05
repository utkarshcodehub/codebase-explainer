export default function OnboardingGuide({ guide }) {
  return (
    <div className="space-y-8">
      {/* Start Here */}
      {guide.start_here && (
        <div className="p-5 bg-accent/5 border border-accent/15 rounded-xl">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-accent text-lg">📖</span>
            <h4 className="font-display text-lg text-ink">Start Here</h4>
          </div>
          <p className="font-body text-sm text-ink/80 leading-relaxed">{guide.start_here}</p>
        </div>
      )}

      {/* Reading Order */}
      {guide.reading_order && guide.reading_order.length > 0 && (
        <div>
          <h4 className="font-body text-xs font-semibold text-muted/60 uppercase tracking-wider mb-3">
            Suggested Reading Order
          </h4>
          <div className="relative pl-8">
            <div className="absolute left-3 top-2 bottom-2 w-px bg-border" />
            {guide.reading_order.map((file, i) => (
              <div key={i} className="relative flex items-center gap-3 py-2">
                <div className="absolute left-[-20px] w-6 h-6 rounded-full bg-surface border border-border flex items-center justify-center">
                  <span className="font-mono text-[10px] text-muted">{i + 1}</span>
                </div>
                <span className="font-mono text-sm text-ink">{file}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Concepts */}
      {guide.key_concepts && guide.key_concepts.length > 0 && (
        <div>
          <h4 className="font-body text-xs font-semibold text-muted/60 uppercase tracking-wider mb-3">
            Key Concepts to Understand
          </h4>
          <div className="flex flex-wrap gap-2">
            {guide.key_concepts.map((concept, i) => (
              <span
                key={i}
                className="px-3 py-1.5 bg-surface border border-border rounded-md font-body text-sm text-ink/70"
              >
                {concept}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Common Tasks */}
      {guide.common_tasks && guide.common_tasks.length > 0 && (
        <div>
          <h4 className="font-body text-xs font-semibold text-muted/60 uppercase tracking-wider mb-3">
            Common Tasks
          </h4>
          <div className="grid gap-3">
            {guide.common_tasks.map((task, i) => (
              <div key={i} className="p-4 bg-white border border-border rounded-lg">
                <p className="font-body text-sm font-medium text-ink">{task.task}</p>
                {task.files && (
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {task.files.map((f, j) => (
                      <span key={j} className="font-mono text-[11px] text-accent/70 bg-accent/5 px-2 py-0.5 rounded">
                        {f}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
