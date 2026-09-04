import { useEffect, useState } from 'react'
import { fetchHealth } from './helpers'
import type { Health } from './types'
import './styles.css'

function App() {
  const [health, setHealth] = useState<Health>('loading')

  useEffect(() => {
    fetchHealth()
      .then((status: Health) => {
        setHealth(status)
      })
      .catch(() => {
        setHealth('error')
      })
  }, [])

  return (
    <main>
      <h1>Kernal</h1>
      <p>
        API health: <strong data-status={health}>{health}</strong>
      </p>
    </main>
  )
}

export default App
