import { SearchBar } from '../components/SearchBar'
import { BriefingCard } from '../components/BriefingCard'
import { LoadingSpinner } from '../components/LoadingSpinner'
import { useBriefing } from '../hooks/useBriefing'

export function HomePage() {
  const { status, data, errorMessage, fetchBriefing, reset } = useBriefing()

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.logo}>
          <span style={styles.logoIcon}>📰</span>
          <span style={styles.logoText}>News Research Agent</span>
        </div>
        <p style={styles.tagline}>
          Agentic editorial briefings powered by LangGraph + RAG
        </p>
      </header>

      <main style={styles.main}>
        <div style={styles.searchWrapper}>
          <SearchBar onSubmit={fetchBriefing} loading={status === 'loading'} />
          {status !== 'idle' && (
            <button onClick={reset} style={styles.resetBtn}>
              ← New search
            </button>
          )}
        </div>

        {status === 'loading' && <LoadingSpinner />}

        {status === 'error' && (
          <div style={styles.errorCard}>
            <strong>Something went wrong</strong>
            <p style={styles.errorMsg}>{errorMessage}</p>
          </div>
        )}

        {status === 'success' && data && (
          <BriefingCard data={data} />
        )}

        {status === 'idle' && (
          <div style={styles.emptyState}>
            <p style={styles.emptyTitle}>Enter a news topic to get started</p>
            <div style={styles.examples}>
              {[
                'Federal Reserve interest rates',
                'AI regulation legislation',
                'US jobs report',
                'Electric vehicle sales',
              ].map(topic => (
                <button
                  key={topic}
                  style={styles.exampleChip}
                  onClick={() => fetchBriefing(topic)}
                >
                  {topic}
                </button>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer style={styles.footer}>
        Built with LangGraph · ChromaDB · FastAPI · React
      </footer>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  header: {
    background: '#1B3A6B',
    color: '#fff',
    padding: '1.5rem 2rem',
    textAlign: 'center',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    marginBottom: '0.4rem',
  },
  logoIcon: {
    fontSize: '1.6rem',
  },
  logoText: {
    fontSize: '1.4rem',
    fontWeight: 700,
    letterSpacing: '-0.02em',
  },
  tagline: {
    margin: 0,
    fontSize: '0.88rem',
    color: '#93c5fd',
  },
  main: {
    flex: 1,
    maxWidth: '820px',
    width: '100%',
    margin: '0 auto',
    padding: '2rem 1.5rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  },
  searchWrapper: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.6rem',
  },
  resetBtn: {
    alignSelf: 'flex-start',
    background: 'none',
    border: 'none',
    color: '#6b7280',
    fontSize: '0.85rem',
    cursor: 'pointer',
    padding: 0,
    fontFamily: 'inherit',
  },
  errorCard: {
    background: '#fef2f2',
    border: '1.5px solid #fecaca',
    borderRadius: '10px',
    padding: '1.25rem 1.5rem',
    color: '#991b1b',
  },
  errorMsg: {
    margin: '0.4rem 0 0',
    fontSize: '0.9rem',
    fontWeight: 400,
  },
  emptyState: {
    textAlign: 'center',
    padding: '2rem 0',
  },
  emptyTitle: {
    color: '#9ca3af',
    fontSize: '1rem',
    marginBottom: '1.25rem',
  },
  examples: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.6rem',
    justifyContent: 'center',
  },
  exampleChip: {
    background: '#fff',
    border: '1.5px solid #e5e7eb',
    borderRadius: '999px',
    padding: '0.45rem 1rem',
    fontSize: '0.85rem',
    color: '#374151',
    cursor: 'pointer',
    fontFamily: 'inherit',
  },
  footer: {
    textAlign: 'center',
    padding: '1.25rem',
    fontSize: '0.78rem',
    color: '#9ca3af',
    borderTop: '1px solid #e5e7eb',
  },
}