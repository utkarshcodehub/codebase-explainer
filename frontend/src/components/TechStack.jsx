const CATEGORY_COLORS = {
  language: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
  framework: { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
  database: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
  devops: { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200' },
  styling: { bg: 'bg-pink-50', text: 'text-pink-700', border: 'border-pink-200' },
  testing: { bg: 'bg-amber-50', text: 'text-amber-700', border: 'border-amber-200' },
  other: { bg: 'bg-gray-50', text: 'text-gray-600', border: 'border-gray-200' },
}

export default function TechStack({ stack }) {
  return (
    <div className="flex flex-wrap gap-2.5">
      {stack.map((item, i) => {
        const colors = CATEGORY_COLORS[item.category] || CATEGORY_COLORS.other
        return (
          <div
            key={i}
            className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-lg border ${colors.bg} ${colors.border}`}
          >
            <span className={`font-body text-sm font-medium ${colors.text}`}>{item.name}</span>
            <span className="font-mono text-[10px] text-muted/40 uppercase">{item.category}</span>
            {item.confidence === 'likely' && (
              <span className="text-[10px] text-muted/30 italic">?</span>
            )}
          </div>
        )
      })}
    </div>
  )
}
