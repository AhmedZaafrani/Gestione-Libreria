import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

function App() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')

  const fetchUsers = async ({ n = 5, reset = false } = {}) => {
    setLoading(true)
    setError(null)
    try {
      const url = new URL('/fake-users', API_BASE)
      url.searchParams.set('n', String(n))
      if (reset) url.searchParams.set('reset', '0')

      const res = await fetch(url.toString())
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
      const json = await res.json()
      // backend returns { generated, total_stored, data }
      setUsers(json.data || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchAll = async () => {
    setLoading(true)
    setError(null)
    try {
      const url = new URL('/data', API_BASE)
      const res = await fetch(url.toString())
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
      const json = await res.json()
      setUsers(json.data || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers({ n: 5 })
  }, [])

  return (
    <div className="App">
      <div className="controls">
        <button onClick={fetchAll}>Show All Stored</button>
        <button onClick={() => setUsers([])}>Clear</button>
        
        <div style={{ display: 'inline-block', marginLeft: 12 }}>
          <input
            type="search"
            placeholder="Cerca per nome..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ padding: '6px', minWidth: 200 }}
          />
        </div>
        </div>

  {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      <div>
        <h2>Stored users: {users.length}</h2>
        <ul>
          {users
            .filter((u) =>
              u.name.toLowerCase().includes(searchTerm.trim().toLowerCase())
            )
            .map((u, i) => (
              <li key={i} className="user-row">
                <strong>{u.author}</strong> — {u.title} — {u.genre}
                <div className="small">{u.year_published} — {u.isbn}</div>
              </li>
            ))}
        </ul>
      </div>
    </div>
  )
}

export default App
