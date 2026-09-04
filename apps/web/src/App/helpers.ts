import type { Health, HealthResponse } from './types'

export function getApiBase(): string {
  return import.meta.env.VITE_API_URL ?? ''
}

export async function fetchHealth(): Promise<Health> {
  const response: Response = await fetch(`${getApiBase()}/api/health`)
  if (!response.ok) {
    throw new Error(response.statusText)
  }
  const data: HealthResponse = await response.json()
  if (data.status === 'ok') {
    return 'ok'
  }
  return 'error'
}
