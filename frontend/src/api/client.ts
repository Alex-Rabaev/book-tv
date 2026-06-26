// Typed API client. The frontend talks ONLY to the book-tv backend (AD-2);
// no third-party API is ever called from the browser.

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export class ApiError extends Error {
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { Accept: 'application/json' },
  })
  if (!res.ok) {
    throw new ApiError(res.status, `Request failed: ${res.status}`)
  }
  return (await res.json()) as T
}

export interface HealthResponse {
  status: string
}

export function getHealth(): Promise<HealthResponse> {
  return apiGet<HealthResponse>('/health')
}
