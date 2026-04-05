import { useState, type FormEvent } from 'react'

interface Props {
  onSubmit: (topic: string) => void
  loading: boolean
}

export function SearchBar({ onSubmit, loading }: Props) {
  const [value, setValue] = useState('')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (value.trim()) onSubmit(value.trim())
  }

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <input
        style={styles.input}
        type="text"
        placeholder="Enter a breaking news topic..."
        value={value}
        onChange={e => setValue(e.target.value)}
        disabled={loading}
        autoFocus
      />
      <button style={styles.button} type="submit" disabled={loading || !value.trim()}>
        {loading ? 'Researching…' : 'Research'}
      </button>
    </form>
  )
}

const styles: Record<string, React.CSSProperties> = {
  form: {
    display: 'flex',
    gap: '0.75rem',
    width: '100%',
  },
  input: {
    flex: 1,
    padding: '0.75rem 1rem',
    fontSize: '1rem',
    border: '1.5px solid #d1d5db',
    borderRadius: '8px',
    outline: 'none',
    fontFamily: 'inherit',
    background: '#fff',
  },
  button: {
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    fontWeight: 600,
    backgroundColor: '#1B3A6B',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    whiteSpace: 'nowrap' as const,
    fontFamily: 'inherit',
  },
}