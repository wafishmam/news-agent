export interface ConflictFlag {
  claim_a: string
  claim_b: string
  source_a: string
  source_b: string
}

export interface BriefingResponse {
  topic: string
  briefing: string
  sources: string[]
  conflict_flags: ConflictFlag[]
  needs_human_review: boolean
  human_review_notes: string | null
  latency_ms: number
  error: string | null
}

export type RequestStatus = 'idle' | 'loading' | 'success' | 'error'