import { Navigate, Route, Routes } from 'react-router-dom'

import { Cabinet } from './pages/Cabinet'
import { Login } from './pages/Login'

export function App() {
  return (
    <main>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/cabinet" element={<Cabinet />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </main>
  )
}

export default App
