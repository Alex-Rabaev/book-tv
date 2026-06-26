import { Link } from 'react-router-dom'

export function Login() {
  return (
    <section>
      <h1>book-tv — Sign in</h1>
      <p>Authentication is implemented in Epic 1 (Stories 1.2–1.4).</p>
      <nav>
        <Link to="/cabinet">Go to Personal Cabinet</Link>
      </nav>
    </section>
  )
}
