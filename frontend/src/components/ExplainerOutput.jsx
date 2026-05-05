import TechStack from './TechStack'
import FileMap from './FileMap'
import MermaidDiagram from './MermaidDiagram'
import OnboardingGuide from './OnboardingGuide'

export default function ExplainerOutput({ data }) {
  const { repo_info, files_analyzed, analysis } = data

  return (
    <div className="mt-12 space-y-10">
      {/* Repo Header */}
      <div className="fade-up fade-up-1">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="font-display text-2xl text-ink">{repo_info.full_name}</h2>
            {repo_info.description && (
              <p className="font-body text-sm text-muted mt-1.5 max-w-xl">{repo_info.description}</p>
            )}
          </div>
          {analysis.complexity_rating && (
            <div className="text-right shrink-0 ml-6">
              <div className="font-mono text-3xl font-medium text-accent">
                {analysis.complexity_rating.score}<span className="text-muted/30 text-lg">/10</span>
              </div>
              <div className="font-body text-xs text-muted mt-0.5">complexity</div>
            </div>
          )}
        </div>
        <div className="flex gap-4 mt-4 text-xs font-mono text-muted/60">
          <span>⭐ {repo_info.stars?.toLocaleString()}</span>
          <span>🍴 {repo_info.forks?.toLocaleString()}</span>
          <span>📁 {files_analyzed.length} files analyzed</span>
          {repo_info.language && <span className="text-accent/70">{repo_info.language}</span>}
        </div>
      </div>

      {/* Divider */}
      <hr className="border-border" />

      {/* Tech Stack */}
      {analysis.tech_stack && (
        <section className="fade-up fade-up-2">
          <SectionHeader num="01" title="Tech Stack" />
          <TechStack stack={analysis.tech_stack} />
        </section>
      )}

      {/* Architecture Summary */}
      {analysis.architecture_summary && (
        <section className="fade-up fade-up-3">
          <SectionHeader num="02" title="Architecture" />
          <div className="font-body text-sm leading-7 text-ink/80 max-w-3xl whitespace-pre-line">
            {analysis.architecture_summary}
          </div>
        </section>
      )}

      {/* Architecture Diagram */}
      {analysis.mermaid_diagram && (
        <section className="fade-up fade-up-4">
          <SectionHeader num="03" title="Architecture Diagram" />
          <MermaidDiagram chart={analysis.mermaid_diagram} />
        </section>
      )}

      {/* Key Modules & Files */}
      {analysis.key_modules && (
        <section className="fade-up fade-up-4">
          <SectionHeader num="04" title="Key Modules" />
          <FileMap modules={analysis.key_modules} entryPoints={analysis.entry_points} />
        </section>
      )}

      {/* Onboarding Guide */}
      {analysis.onboarding_guide && (
        <section className="fade-up fade-up-5">
          <SectionHeader num="05" title="Onboarding Guide" />
          <OnboardingGuide guide={analysis.onboarding_guide} />
        </section>
      )}
    </div>
  )
}

function SectionHeader({ num, title }) {
  return (
    <div className="flex items-baseline gap-3 mb-5">
      <span className="font-mono text-xs text-accent/50">{num}</span>
      <h3 className="font-display text-xl text-ink">{title}</h3>
      <div className="flex-1 border-b border-border/60 ml-2 translate-y-[-3px]" />
    </div>
  )
}
