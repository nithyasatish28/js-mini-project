import { useCallback, useEffect, useMemo, useState } from 'react'

const API_URL = '/items'

const NAV_ITEMS = [
  { id: 'browse', label: 'Browse items', icon: '⌕' },
  { id: 'report', label: 'Report an item', icon: '＋' },
]

const EMPTY_ITEM = {
  name: '',
  description: '',
  contact: '',
  location: '',
}

function formatDate(value) {
  if (!value) return '—'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '—'
  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(date)
}

function StatusBadge({ status }) {
  const normalized = String(status || 'active').trim().toLowerCase()
  const safeStatus = ['active', 'resolved'].includes(normalized) ? normalized : 'active'

  return (
    <span className="status-badge" data-status={safeStatus}>
      {safeStatus === 'active' ? 'Open' : 'Resolved'}
    </span>
  )
}

function EmptyState({ icon, children }) {
  return (
    <div className="empty-state">
      {icon && <span className="empty-icon" aria-hidden="true">{icon}</span>}
      {children}
    </div>
  )
}

async function requestJson(url, options) {
  let response
  try {
    response = await fetch(url, options)
  } catch {
    throw new Error('Could not reach the API. Start the backend and try again.')
  }

  const result = await response.json().catch(() => null)
  if (!response.ok) {
    const detail = result?.detail
    const message = Array.isArray(detail)
      ? detail.map((issue) => typeof issue === 'string' ? issue : issue?.msg || '').filter(Boolean).join(' ')
      : detail
    throw new Error(message || `Request failed (${response.status}).`)
  }
  return result
}

async function fetchItems() {
  const data = await requestJson(API_URL, {
    headers: { Accept: 'application/json' },
  })
  if (!Array.isArray(data)) throw new Error('The API returned an unexpected response.')
  return data
}

function App() {
  const [items, setItems] = useState([])
  const [activeView, setActiveView] = useState('browse')
  const [searchQuery, setSearchQuery] = useState('')
  const [apiError, setApiError] = useState('')
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState(null)
  const [form, setForm] = useState(EMPTY_ITEM)
  const [submitting, setSubmitting] = useState(false)

  const loadItems = useCallback(async () => {
    try {
      const data = await fetchItems()
      setItems(data)
      setApiError('')
      return true
    } catch (error) {
      setApiError(error.message)
      return false
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let isCurrent = true
    fetchItems()
      .then((data) => {
        if (isCurrent) {
          setItems(data)
          setApiError('')
        }
      })
      .catch((error) => {
        if (isCurrent) setApiError(error.message)
      })
      .finally(() => {
        if (isCurrent) setLoading(false)
      })

    return () => {
      isCurrent = false
    }
  }, [])

  useEffect(() => {
    if (!toast) return undefined
    const timer = window.setTimeout(() => setToast(null), 4200)
    return () => window.clearTimeout(timer)
  }, [toast])

  const sortedItems = useMemo(
    () => [...items].sort((a, b) => new Date(b.posted_at || 0) - new Date(a.posted_at || 0)),
    [items],
  )

  const filteredItems = useMemo(() => {
    const query = searchQuery.trim().toLowerCase()
    if (!query) return sortedItems
    return sortedItems.filter((item) => [
      item.name,
      item.description,
      item.location,
    ].some((value) => String(value || '').toLowerCase().includes(query)))
  }, [sortedItems, searchQuery])

  const activeCount = items.filter(
    (item) => String(item.status || 'active').toLowerCase() === 'active',
  ).length
  const locationCount = new Set(items.map((item) => item.location).filter(Boolean)).size

  function navigate(view) {
    setActiveView(view)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  function updateForm(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    try {
      const created = await requestJson(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          name: form.name.trim(),
          description: form.description.trim(),
          contact: form.contact.trim(),
          location: form.location.trim() || null,
        }),
      })
      setItems((current) => [created, ...current.filter((item) => item.id !== created.id)])
      setForm(EMPTY_ITEM)
      setSearchQuery('')
      navigate('browse')
      setToast({ kind: 'success', message: `${created.name} was added to the item board.` })
    } catch (error) {
      setToast({ kind: 'error', message: error.message })
    } finally {
      setSubmitting(false)
    }
  }

  const pageTitle = activeView === 'browse' ? 'Browse items' : 'Report an item'

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Main navigation">
        <a
          className="brand"
          href="#browse"
          onClick={(event) => {
            event.preventDefault()
            navigate('browse')
          }}
        >
          <span className="brand-mark" aria-hidden="true">⌕</span>
          <span>Found &amp; Returned<small>Community item board</small></span>
        </a>

        <p className="nav-label">Workspace</p>
        <nav className="nav-list" aria-label="Workspace">
          {NAV_ITEMS.map((item) => (
            <button
              className="nav-link"
              type="button"
              key={item.id}
              onClick={() => navigate(item.id)}
              aria-current={activeView === item.id ? 'page' : undefined}
            >
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <strong>Help reunite an item</strong>
            <p>Add a clear description and a way to contact you so its owner can get in touch.</p>
          </div>
          <div className="sidebar-foot">
            <span className="avatar" aria-hidden="true">FR</span>
            <span><strong>Community member</strong><small>Lost &amp; found board</small></span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Lost &amp; Found <span aria-hidden="true">/</span> <strong>{pageTitle}</strong>
          </div>
          <div className="topbar-actions">
            <span className="topbar-date">
              {new Intl.DateTimeFormat(undefined, {
                weekday: 'short',
                month: 'short',
                day: 'numeric',
              }).format(new Date())}
            </span>
            <span className={`connection ${apiError ? 'connection-error' : loading ? 'connection-loading' : ''}`}>
              <span className="connection-dot" aria-hidden="true" />
              {apiError ? 'API unavailable' : loading ? 'Connecting' : 'API connected'}
            </span>
          </div>
        </header>

        {apiError && (
          <div className="api-alert" role="alert">
            <strong>Couldn’t load items.</strong>
            <span>{apiError}</span>
            <button className="text-button" type="button" onClick={loadItems}>Try again</button>
          </div>
        )}

        {activeView === 'browse' && (
          <section aria-labelledby="browse-title">
            <div className="hero">
              <div className="hero-overlay" aria-hidden="true" />
              <div className="hero-content">
                <span className="hero-kicker">A little help goes a long way</span>
                <h1 id="browse-title">Let’s get lost things found.</h1>
                <p>Browse recent reports or share an item you’ve lost. A few details can help it find its way home.</p>
                <button className="primary-button hero-button" type="button" onClick={() => navigate('report')}>
                  ＋ Report an item
                </button>
              </div>
            </div>

            <section className="stats" aria-label="Item board overview">
              <article className="stat-card">
                <div className="stat-top"><span>Total reports</span><span className="stat-icon" aria-hidden="true">▤</span></div>
                <strong>{loading && !items.length ? '—' : items.length}</strong>
              </article>
              <article className="stat-card">
                <div className="stat-top"><span>Open reports</span><span className="stat-icon" aria-hidden="true">◷</span></div>
                <strong>{loading && !items.length ? '—' : activeCount}</strong>
              </article>
              <article className="stat-card">
                <div className="stat-top"><span>Locations</span><span className="stat-icon" aria-hidden="true">⌕</span></div>
                <strong>{loading && !items.length ? '—' : locationCount}</strong>
              </article>
            </section>

            <section className="panel item-board" aria-label="Reported items">
              <div className="panel-header">
                <div><h2>Recent item reports</h2><p>Search by item, description, or location</p></div>
                <button className="text-button" type="button" onClick={() => navigate('report')}>
                  Add a report <span aria-hidden="true">→</span>
                </button>
              </div>
              <div className="toolbar">
                <input
                  className="search-input"
                  type="search"
                  value={searchQuery}
                  onChange={(event) => setSearchQuery(event.target.value)}
                  placeholder="Search items or locations…"
                  aria-label="Search item reports"
                />
                <span className="filter-count">
                  {filteredItems.length} {filteredItems.length === 1 ? 'report' : 'reports'}
                </span>
              </div>

              {loading ? (
                <EmptyState>Loading item reports…</EmptyState>
              ) : filteredItems.length ? (
                <div className="item-grid">
                  {filteredItems.map((item) => (
                    <article className="item-card" key={item.id}>
                      <div className="item-card-top">
                        <span className="item-category">Item #{item.id}</span>
                        <StatusBadge status={item.status} />
                      </div>
                      <h3>{item.name}</h3>
                      <p className="item-description">{item.description}</p>
                      <div className="item-meta">
                        <span><strong>Location</strong>{item.location || 'Not specified'}</span>
                        <span><strong>Posted</strong>{formatDate(item.posted_at)}</span>
                        <span><strong>Contact</strong>{item.contact}</span>
                      </div>
                    </article>
                  ))}
                </div>
              ) : (
                <EmptyState icon="⌕">
                  {searchQuery ? 'No reports match your search.' : 'No items have been reported yet. Be the first to add one.'}
                </EmptyState>
              )}
            </section>
          </section>
        )}

        {activeView === 'report' && (
          <section aria-labelledby="report-title">
            <div className="page-heading">
              <div><p className="eyebrow">Help an item find its way</p><h1 id="report-title">Report an item</h1><p>Share what it looks like and how its owner can reach you.</p></div>
              <button className="secondary-button" type="button" onClick={() => navigate('browse')}>Browse reports</button>
            </div>
            <section className="panel form-panel">
              <div className="form-intro">
                <span className="stat-icon" aria-hidden="true">✎</span>
                <div><h2>What did you lose?</h2><p>Include a useful description and contact details. Location is optional.</p></div>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-field">
                    <label htmlFor="item-name">Item name <span className="required">*</span></label>
                    <input
                      className="form-control"
                      id="item-name"
                      name="name"
                      type="text"
                      maxLength="120"
                      value={form.name}
                      onChange={updateForm}
                      placeholder="e.g. Blue water bottle"
                      required
                    />
                  </div>
                  <div className="form-field">
                    <label htmlFor="item-location">Last seen location</label>
                    <input
                      className="form-control"
                      id="item-location"
                      name="location"
                      type="text"
                      maxLength="200"
                      value={form.location}
                      onChange={updateForm}
                      placeholder="e.g. Library, second floor"
                    />
                  </div>
                  <div className="form-field form-field-full">
                    <label htmlFor="item-description">Description <span className="required">*</span></label>
                    <textarea
                      className="form-control"
                      id="item-description"
                      name="description"
                      rows="4"
                      maxLength="1000"
                      value={form.description}
                      onChange={updateForm}
                      placeholder="Describe the item and any details that could help identify it."
                      required
                    />
                  </div>
                  <div className="form-field form-field-full">
                    <label htmlFor="item-contact">Contact details <span className="required">*</span></label>
                    <input
                      className="form-control"
                      id="item-contact"
                      name="contact"
                      type="text"
                      maxLength="200"
                      value={form.contact}
                      onChange={updateForm}
                      placeholder="Email address or phone number"
                      required
                    />
                    <span className="form-hint">This will be visible on the report so someone can contact you.</span>
                  </div>
                </div>
                <div className="form-footer">
                  <span className="form-hint">Fields marked with * are required.</span>
                  <button className="primary-button" type="submit" disabled={submitting}>
                    {submitting ? 'Submitting…' : '＋ Submit report'}
                  </button>
                </div>
              </form>
            </section>
          </section>
        )}
      </main>

      {toast && (
        <div className={`toast toast-${toast.kind}`} role={toast.kind === 'error' ? 'alert' : 'status'}>
          <span>{toast.message}</span>
          <button type="button" onClick={() => setToast(null)} aria-label="Dismiss notification">×</button>
        </div>
      )}
    </div>
  )
}

export default App
