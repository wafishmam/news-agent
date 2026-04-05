import { useState, useCallback } from 'react'
import type { BriefingResponse, RequestStatus } from '../types'

export function useBriefing() {
  const [status, setStatus] = useState<RequestStatus>('idle')
  const [data, setData] = useState<BriefingResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const fetchBriefing = useCallback(async (topic: string) => {
    if (!topic.trim()) return

    setStatus('loading')
    setData(null)
    setErrorMessage(null)

    try {
      const res = await fetch('/api/briefing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      })

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail ?? `HTTP ${res.status}`)
      }

      const json: BriefingResponse = await res.json()
      setData(json)
      setStatus('success')
    } catch (e) {
      setErrorMessage(e instanceof Error ? e.message : 'Unknown error')
      setStatus('error')
    }
  }, [])

  const reset = useCallback(() => {
    setStatus('idle')
    setData(null)
    setErrorMessage(null)
  }, [])

  return { status, data, errorMessage, fetchBriefing, reset }
}