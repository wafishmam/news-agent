export function LoadingSpinner() {
  return (
    <div style={styles.wrapper}>
      <div style={styles.spinner} />
      <div style={styles.steps}>
        <Step icon="🔍" label="Searching live sources…" />
        <Step icon="🗄️" label="Querying news archive…" />
        <Step icon="✍️" label="Drafting editorial briefing…" />
      </div>
    </div>
  )
}

function Step({ icon, label }: { icon: string; label: string }) {
  return (
    <div style={styles.step}>
      <span>{icon}</span>
      <span>{label}</span>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '2rem',
    padding: '3rem',
  },
  spinner: {
    width: '48px',
    height: '48px',
    border: '4px solid #e5e7eb',
    borderTop: '4px solid #1B3A6B',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  steps: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  step: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    color: '#6b7280',
    fontSize: '0.92rem',
  },
}