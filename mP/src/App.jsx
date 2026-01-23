import { useEffect, useState } from 'react'
import './App.css'

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000'

function App() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')
  const [genre, setGenre] = useState('')

  const fetchBooks = async (n = 5) => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API}/fake-users?n=${n}`)
      if (!res.ok) throw new Error(res.statusText)
      const data = await res.json()
      setBooks(data.data || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadAll = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API}/data`)
      if (!res.ok) throw new Error(res.statusText)
      const data = await res.json()
      setBooks(data.data || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const addBook = async () => {
    if (!title || !author || !genre) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API}/book`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, author, genre })
      })
      if (!res.ok) throw new Error(res.statusText)
      const book = await res.json()
      setBooks(prev => [...prev, book])
      setTitle('')
      setAuthor('')
      setGenre('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const deleteBook = async (id) => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API}/book/${id}`, { method: 'DELETE' })
      if (!res.ok) throw new Error(res.statusText)
      setBooks(prev => prev.filter(b => b.id !== id))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const clearAll = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API}/data`, { method: 'DELETE' })
      if (!res.ok) throw new Error(res.statusText)
      setBooks([])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBooks()
  }, [])

  const filtered = books.filter(b => 
    (b.author || '').toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="App">
      <header className="app-header">
        <h1>Gestione Libreria</h1>
        <div className="controls">
          <button onClick={() => fetchBooks(5)}>Genera</button>
          <button onClick={loadAll}>Mostra tutti</button>
          <button onClick={clearAll}>Cancella tutto</button>
          <input
            type="search"
            placeholder="Cerca..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </header>

      {loading && <p>Caricamento...</p>}
      {error && <p className="error">Errore: {error}</p>}

      <section className="books-section">
        <h2>Libri: {filtered.length}</h2>
        <div className="users-grid">
          {filtered.map((b, i) => (
            <div key={b.id || i} className="user-row">
              <div className="book-header">
                <strong>{b.author}</strong>
                <button onClick={() => deleteBook(b.id)}>×</button>
              </div>
              <div className="book-title">{b.title}</div>
              <div className="book-genre">{b.genre}</div>
              <div className="small">{b.year_published} · {b.isbn}</div>
            </div>
          ))}
        </div>
      </section>

      <footer className="add-book-form">
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Titolo" />
        <input value={author} onChange={(e) => setAuthor(e.target.value)} placeholder="Autore" />
        <input value={genre} onChange={(e) => setGenre(e.target.value)} placeholder="Genere" />
        <button onClick={addBook}>Aggiungi</button>
      </footer>
    </div>
  )
}

export default App
