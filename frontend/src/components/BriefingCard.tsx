import type { BriefingResponse } from '../types'

interface Props {
  data: BriefingResponse
}

export function BriefingCard({ data }: Props) {
  return (
    <div style={styles.wrapper}>

      {/* Header */}
      <div style={styles.header}>
        <h2 style={styles.topic}>{data.topic}</h2>
        <span style={styles.latency}>{data.latency_ms}ms</span>
      </div>

      {/* Human review banner */}
      {data.needs_human_review && (
        <div style={styles.reviewBanner}>
          <span>⚠️</span>
          <span>
            <strong>Editorial Review Required</strong> — conflicting claims detected in sources.
          </span>
        </div>
      )}

      {/* Briefing body */}
      <div style={styles.section}>
        <h3 style={styles.sectionTitle}>Editorial Briefing</h3>
        {data.briefing.split('\n\n').map((para, i) => (
          <p key={i} style={styles.paragraph}>{para}</p>
        ))}
      </div>

      {/* Conflict flags */}
      {data.conflict_flags.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Conflicting Claims</h3>
          {data.conflict_flags.map((flag, i) => (
            <div key={i} style={styles.conflictCard}>
              <div style={styles.conflictRow}>
                <span style={styles.conflictLabel}>Source A</span>
                <span style={styles.conflictSource}>{flag.source_a}</span>
              </div>
              <p style={styles.conflictClaim}>{flag.claim_a}</p>
              <div style={styles.divider} />
              <div style={styles.conflictRow}>
                <span style={styles.conflictLabel}>Source B</span>
                <span style={styles.conflictSource}>{flag.source_b}</span>
              </div>
              <p style={styles.conflictClaim}>{flag.claim_b}</p>
            </div>
          ))}
        </div>
      )}

      {/* Sources */}
      {data.sources.length > 0 && (
        <div style={styles.section}>
          <h3 style={styles.sectionTitle}>Sources</h3>
          <ul style={styles.sourceList}>
            {data.sources.map((src, i) => (
              <li key={i} style={styles.sourceItem}>
                <a href={src} target="_blank" rel="noopener noreferrer" style={styles.sourceLink}>
                  {src}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Error notice */}
      {data.error && (
        <div style={styles.errorNotice}>
          Agent warning: {data.error}
        </div>
      )}
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    background: '#fff',
    border: '1.5px solid #e5e7eb',
    borderRadius: '12px',
    padding: '2rem',
    width: '100%',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '1.25rem',
  },
  topic: {
    margin: 0,
    fontSize: '1.3rem',
    fontWeight: 700,
    color: '#1B3A6B',
  },
  latency: {
    fontSize: '0.78rem',
    color: '#9ca3af',
    marginLeft: '1rem',
    marginTop: '4px',
  },
  reviewBanner: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    background: '#fffbeb',
    border: '1px solid #fcd34d',
    borderRadius: '8px',
    padding: '0.75rem 1rem',
    marginBottom: '1.25rem',
    fontSize: '0.9rem',
    color: '#92400e',
  },
  section: {
    marginBottom: '1.5rem',
  },
  sectionTitle: {
    fontSize: '0.78rem',
    fontWeight: 700,
    textTransform: 'uppercase' as const,
    letterSpacing: '0.07em',
    color: '#6b7280',
    marginBottom: '0.75rem',
  },
  paragraph: {
    margin: '0 0 0.75rem',
    lineHeight: 1.7,
    color: '#111827',
    fontSize: '0.97rem',
  },
  conflictCard: {
    background: '#fef2f2',
    border: '1px solid #fecaca',
    borderRadius: '8px',
    padding: '1rem',
    marginBottom: '0.75rem',
  },
  conflictRow: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    marginBottom: '0.3rem',
  },
  conflictLabel: {
    fontSize: '0.72rem',
    fontWeight: 700,
    textTransform: 'uppercase' as const,
    color: '#b91c1c',
    background: '#fee2e2',
    padding: '2px 6px',
    borderRadius: '4px',
  },
  conflictSource: {
    fontSize: '0.78rem',
    color: '#6b7280',
  },
  conflictClaim: {
    margin: '0 0 0.5rem',
    fontSize: '0.9rem',
    color: '#1f2937',
    lineHeight: 1.5,
  },
  divider: {
    borderTop: '1px solid #fecaca',
    margin: '0.6rem 0',
  },
  sourceList: {
    margin: 0,
    padding: '0 0 0 1.2rem',
  },
  sourceItem: {
    marginBottom: '0.4rem',
  },
  sourceLink: {
    color: '#1B3A6B',
    fontSize: '0.85rem',
    wordBreak: 'break-all' as const,
  },
  errorNotice: {
    background: '#fef2f2',
    border: '1px solid #fecaca',
    borderRadius: '6px',
    padding: '0.6rem 0.9rem',
    fontSize: '0.85rem',
    color: '#991b1b',
  },
}