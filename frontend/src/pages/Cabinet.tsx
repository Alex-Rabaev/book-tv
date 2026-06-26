import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'

import { getHealth } from '../api/client'

export function Cabinet() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
  })

  return (
    <section>
      <h1>Personal Cabinet</h1>
      <p>
        Backend status:{' '}
        {isLoading ? 'checking…' : isError ? 'unreachable' : (data?.status ?? 'unknown')}
      </p>
      <nav>
        <Link to="/">Back to sign in</Link>
      </nav>
    </section>
  )
}
