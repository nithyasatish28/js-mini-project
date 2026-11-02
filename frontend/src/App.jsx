import { useCallback, useEffect, useMemo, useState } from 'react'

const API_URL = '/complaints'

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: '▦' },
  { id: 'warden', label: 'Warden workspace', icon: '≡' },
  { id: 'mine', label: 'My complaints', icon: '⌕' },
  { id: 'raise', label: 'Raise a complaint', icon: '＋' },
]

const CATEGORIES = [
  'Plumbing',
  'Electrical',
  'Cleanliness',
  'Furniture',
  'Internet / Wi-Fi',
  'Other',
]

const EMPTY_COMPLAINT = {
  roll_no: '',
  room_no: '',
  catagory: '',
  description: '',
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
  const safeStatus = ['active', 'pending', 'resolved', 'closed'].includes(normalized)
    ? normalized
    : 'active'

  return (
    <span className="status-badge" data-status={safeStatus}>
      {safeStatus.charAt(0).toUpperCase() + safeStatus.slice(1)}
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
    throw new Error('Could not reach the complaint API. Start the backend and try again.')
  }

  const result = await response.json().catch(() => null)
  if (response.status === 502) {
    throw new Error('The complaint API is not running. Start it with npm start in the backend folder, then try again.')
  }
  if (!response.ok) {
    const detail = result?.detail
    const message = Array.isArray(detail)
      ? detail.map((issue) => typeof issue === 'string' ? issue : issue?.msg || '').filter(Boolean).join(' ')
      : detail
    throw new Error(message || `Request failed (${response.status}).`)
  }
  return result
}

async function fetchComplaints(complaintStatus = '') {
  const url = complaintStatus
    ? `${API_URL}/status/${encodeURIComponent(complaintStatus)}`
    : API_URL
  const data = await requestJson(url, {
    headers: { Accept: 'application/json' },
  })
  if (!Array.isArray(data)) throw new Error('The API returned an unexpected response.')
  return data
}

function ComplaintTable({
  complaints,
  showRollNumber = false,
  onView,
  onDelete,
  onUpdateStatus,
  emptyMessage = 'No complaints to show.',
}) {
  if (!complaints.length) {
    return (
      <div className="table-empty">
        <EmptyState icon="⌕">{emptyMessage}</EmptyState>
      </div>
    )
  }

  return (
    <div className="table-wrap">
      <table className="complaint-table">
        <thead>
          <tr>
            <th>Complaint</th>
            {showRollNumber && <th>Student / Room</th>}
            {!showRollNumber && <th>Room</th>}
            <th>Category</th>
            <th>Reported</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {complaints.map((complaint) => (
            <tr key={complaint.id}>
              <td>
                <span className="table-primary" title={complaint.description}>
                  {complaint.description || 'Hostel maintenance request'}
                </span>
                <span className="table-secondary">#{complaint.id}</span>
              </td>
              {showRollNumber ? (
                <td>
                  <span className="table-primary">{complaint.roll_no ?? '—'}</span>
                  <span className="table-secondary">Room {complaint.room_no || '—'}</span>
                </td>
              ) : (
                <td>{complaint.room_no || '—'}</td>
              )}
              <td>{complaint.catagory || 'Uncategorized'}</td>
              <td>{formatDate(complaint.created_on)}</td>
              <td><StatusBadge status={complaint.status} /></td>
              <td className="row-actions">
                <button className="text-button" type="button" onClick={() => onView(complaint)}>
                  View
                </button>
                {onUpdateStatus && (
                  <button className="text-button" type="button" onClick={() => onUpdateStatus(complaint)}>
                    {['resolved', 'closed'].includes(String(complaint.status || '').toLowerCase())
                      ? 'Reopen'
                      : 'Resolve'}
                  </button>
                )}
                {onDelete && (
                  <button
                    className="danger-button"
                    type="button"
                    onClick={() => onDelete(complaint)}
                    aria-label={`Delete complaint ${complaint.id}`}
                  >
                    Delete
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function App() {
  const [complaints, setComplaints] = useState([])
  const [activeView, setActiveView] = useState('dashboard')
  const [apiError, setApiError] = useState('')
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState(null)
  const [form, setForm] = useState(EMPTY_COMPLAINT)
  const [submitting, setSubmitting] = useState(false)
  const [wardenQuery, setWardenQuery] = useState('')
  const [wardenStatus, setWardenStatus] = useState('')
  const [rollQuery, setRollQuery] = useState('')
  const [searchedRoll, setSearchedRoll] = useState('')
  const [selectedComplaint, setSelectedComplaint] = useState(null)

  const loadComplaints = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchComplaints(wardenStatus)
      setComplaints(data)
      setApiError('')
      return true
    } catch (error) {
      setApiError(error.message)
      return false
    } finally {
      setLoading(false)
    }
  }, [wardenStatus])

  useEffect(() => {
    let isCurrent = true
    fetchComplaints(wardenStatus)
      .then((data) => {
        if (isCurrent) {
          setComplaints(data)
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
  }, [wardenStatus])

  useEffect(() => {
    if (!toast) return undefined
    const timer = window.setTimeout(() => setToast(null), 4200)
    return () => window.clearTimeout(timer)
  }, [toast])

  const sortedComplaints = useMemo(
    () => [...complaints].sort((a, b) => new Date(b.created_on || 0) - new Date(a.created_on || 0)),
    [complaints],
  )

  const filteredWardenComplaints = useMemo(() => {
    const query = wardenQuery.trim().toLowerCase()
    return sortedComplaints.filter((complaint) => !query || [
      complaint.description,
      complaint.catagory,
      complaint.room_no,
      complaint.roll_no,
      complaint.id,
    ].join(' ').toLowerCase().includes(query))
  }, [sortedComplaints, wardenQuery])

  const myComplaints = useMemo(
    () => sortedComplaints.filter((complaint) => String(complaint.roll_no) === searchedRoll),
    [sortedComplaints, searchedRoll],
  )
  const activeCount = complaints.filter(
    (complaint) => String(complaint.status || 'active').toLowerCase() === 'active',
  ).length
  const resolvedCount = complaints.filter(
    (complaint) => ['resolved', 'closed'].includes(String(complaint.status || '').toLowerCase()),
  ).length
  const categorySummary = useMemo(() => {
    const counts = new Map()
    complaints.forEach((complaint) => {
      const category = complaint.catagory || 'Uncategorized'
      counts.set(category, (counts.get(category) || 0) + 1)
    })
    return [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5)
  }, [complaints])

  function navigate(view) {
    if (view !== 'warden' && wardenStatus) {
      setLoading(true)
      setWardenStatus('')
    }
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
          roll_no: Number(form.roll_no),
          room_no: form.room_no.trim(),
          catagory: form.catagory || null,
          description: form.description.trim(),
          status: 'active',
        }),
      })
      setForm(EMPTY_COMPLAINT)
      setRollQuery(String(created.roll_no))
      setSearchedRoll(String(created.roll_no))
      setWardenStatus('')
      navigate('mine')
      let refreshed = true
      try {
        setComplaints(await fetchComplaints())
        setApiError('')
      } catch (error) {
        setApiError(error.message)
        refreshed = false
      }
      setToast({
        kind: refreshed ? 'success' : 'error',
        message: refreshed
          ? `Complaint #${created.id} submitted successfully.`
          : `Complaint #${created.id} was submitted, but the list could not be refreshed.`,
      })
    } catch (error) {
      setToast({ kind: 'error', message: error.message })
    } finally {
      setSubmitting(false)
    }
  }

  async function handleView(complaint) {
    try {
      const details = await requestJson(`${API_URL}/${encodeURIComponent(complaint.id)}`, {
        headers: { Accept: 'application/json' },
      })
      setSelectedComplaint(details)
    } catch (error) {
      setToast({ kind: 'error', message: error.message })
    }
  }

  async function handleDelete(complaint) {
    if (!window.confirm(`Delete complaint #${complaint.id}? This can’t be undone.`)) return
    try {
      await requestJson(`${API_URL}/${encodeURIComponent(complaint.id)}`, { method: 'DELETE' })
      setComplaints((current) => current.filter((item) => item.id !== complaint.id))
      setToast({ kind: 'success', message: `Complaint #${complaint.id} deleted.` })
    } catch (error) {
      setToast({ kind: 'error', message: error.message })
    }
  }

  async function handleUpdateStatus(complaint) {
    const isResolved = ['resolved', 'closed'].includes(String(complaint.status || '').toLowerCase())
    const status = isResolved ? 'active' : 'resolved'
    try {
      const updated = isResolved
        ? await requestJson(`${API_URL}/${encodeURIComponent(complaint.id)}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify({ status }),
        })
        : await requestJson(`${API_URL}/${encodeURIComponent(complaint.id)}/resolve`, {
          method: 'PATCH',
        })
      setComplaints((current) => wardenStatus && updated.status !== wardenStatus
        ? current.filter((item) => item.id !== updated.id)
        : current.map((item) => item.id === updated.id ? updated : item))
      setToast({ kind: 'success', message: `Complaint #${complaint.id} marked ${status}.` })
    } catch (error) {
      setToast({ kind: 'error', message: error.message })
    }
  }

  function handleMySearch(event) {
    event.preventDefault()
    setSearchedRoll(rollQuery.trim())
  }

  const pageTitle = {
    dashboard: 'Warden dashboard',
    warden: 'All complaints',
    mine: 'My complaints',
    raise: 'Raise a complaint',
  }[activeView]

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Main navigation">
        <a
          className="brand"
          href="#dashboard"
          onClick={(event) => {
            event.preventDefault()
            navigate('dashboard')
          }}
        >
          <span className="brand-mark" aria-hidden="true">⌂</span>
          <span>Hostel Care<small>Student services</small></span>
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
            <strong>Need urgent help?</strong>
            <p>For an immediate safety concern, please contact your hostel warden directly.</p>
          </div>
          <div className="sidebar-foot">
            <span className="avatar" aria-hidden="true">HC</span>
            <span><strong>Hostel resident</strong><small>Complaint portal</small></span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Hostel services <span aria-hidden="true">/</span> <strong>{pageTitle}</strong>
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
            <strong>Couldn’t load complaints.</strong>
            <span>{apiError}</span>
            <button className="text-button" type="button" onClick={loadComplaints}>Try again</button>
          </div>
        )}

        {activeView === 'dashboard' && (
          <section aria-labelledby="dashboard-title">
            <div className="hero">
              <div className="hero-overlay" aria-hidden="true" />
              <div className="hero-content">
                <span className="hero-kicker">A better stay starts here</span>
                <h1 id="dashboard-title">A home away from home, made better.</h1>
                <p>Something needs attention? Let us know. Every report helps make hostel life more comfortable.</p>
                <button className="primary-button hero-button" type="button" onClick={() => navigate('raise')}>
                  ＋ Raise a complaint
                </button>
              </div>
            </div>

            <section className="stats" aria-label="Complaint overview">
              <article className="stat-card">
                <div className="stat-top"><span>Total complaints</span><span className="stat-icon" aria-hidden="true">▤</span></div>
                <strong>{loading && !complaints.length ? '—' : complaints.length}</strong>
              </article>
              <article className="stat-card">
                <div className="stat-top"><span>Active</span><span className="stat-icon" aria-hidden="true">◷</span></div>
                <strong>{loading && !complaints.length ? '—' : activeCount}</strong>
              </article>
              <article className="stat-card">
                <div className="stat-top"><span>Resolved</span><span className="stat-icon" aria-hidden="true">✓</span></div>
                <strong>{loading && !complaints.length ? '—' : resolvedCount}</strong>
              </article>
            </section>

            <div className="content-grid">
              <section className="panel" aria-labelledby="recent-title">
                <div className="panel-header">
                  <div><h2 id="recent-title">Recent complaints</h2><p>Latest reports from your hostel</p></div>
                  <button className="text-button" type="button" onClick={() => navigate('warden')}>View all →</button>
                </div>
                {loading ? (
                  <EmptyState>Loading complaints…</EmptyState>
                ) : sortedComplaints.length ? (
                  <div className="complaint-list">
                    {sortedComplaints.slice(0, 5).map((complaint) => (
                      <article className="complaint-row" key={complaint.id}>
                        <div>
                          <p className="complaint-title">{complaint.description || 'Hostel maintenance request'}</p>
                          <div className="complaint-meta">
                            <span>{complaint.catagory || 'Uncategorized'}</span>
                            <span>Room {complaint.room_no || '—'}</span>
                            <span>{formatDate(complaint.created_on)}</span>
                          </div>
                        </div>
                        <StatusBadge status={complaint.status} />
                      </article>
                    ))}
                  </div>
                ) : (
                  <EmptyState icon="✓">No complaints yet. Raise one to get started.</EmptyState>
                )}
              </section>

              <section className="panel" aria-labelledby="category-title">
                <div className="panel-header">
                  <div><h2 id="category-title">By category</h2><p>What residents are reporting</p></div>
                </div>
                {categorySummary.length ? (
                  <div className="category-list">
                    {categorySummary.map(([category, count]) => (
                      <div className="category-item" key={category}>
                        <span>{category}</span><strong>{count}</strong>
                        <div className="category-track">
                          <div
                            className="category-fill"
                            style={{ width: `${Math.round((count / categorySummary[0][1]) * 100)}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <EmptyState>No category data to show yet.</EmptyState>
                )}
              </section>
            </div>
          </section>
        )}

        {activeView === 'warden' && (
          <section aria-labelledby="warden-title">
            <div className="page-heading">
              <div><p className="eyebrow">Warden workspace</p><h1 id="warden-title">All complaints</h1><p>Review and manage hostel maintenance reports.</p></div>
              <button className="secondary-button" type="button" onClick={loadComplaints}>↻ Refresh</button>
            </div>
            <section className="panel" aria-label="All hostel complaints">
              <div className="toolbar">
                <input
                  className="search-input"
                  type="search"
                  value={wardenQuery}
                  onChange={(event) => setWardenQuery(event.target.value)}
                  placeholder="Search reports, rooms, or students…"
                  aria-label="Search all complaints"
                />
                <select
                  className="control"
                  value={wardenStatus}
                  onChange={(event) => {
                    setLoading(true)
                    setWardenStatus(event.target.value)
                  }}
                  aria-label="Filter by status"
                >
                  <option value="">All statuses</option>
                  <option value="active">Active</option>
                  <option value="pending">Pending</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
                <span className="filter-count">{filteredWardenComplaints.length} complaints</span>
              </div>
              {loading ? (
                <EmptyState>Loading complaints…</EmptyState>
              ) : (
                <ComplaintTable
                  complaints={filteredWardenComplaints}
                  showRollNumber
                  onView={handleView}
                  onDelete={handleDelete}
                  onUpdateStatus={handleUpdateStatus}
                  emptyMessage={wardenQuery || wardenStatus
                    ? 'No complaints match your search.'
                    : 'There are no complaints to review yet.'}
                />
              )}
            </section>
          </section>
        )}

        {activeView === 'mine' && (
          <section aria-labelledby="mine-title">
            <div className="page-heading">
              <div><p className="eyebrow">Resident workspace</p><h1 id="mine-title">My complaints</h1><p>Look up reports submitted with your roll number.</p></div>
              <button className="secondary-button" type="button" onClick={() => navigate('raise')}>＋ New complaint</button>
            </div>
            <section className="panel" aria-label="Find your hostel complaints">
              <form className="toolbar" onSubmit={handleMySearch}>
                <input
                  className="search-input roll-input"
                  type="number"
                  min="1"
                  step="1"
                  value={rollQuery}
                  onChange={(event) => setRollQuery(event.target.value)}
                  placeholder="Enter your roll number"
                  aria-label="Your roll number"
                  required
                />
                <button className="secondary-button" type="submit">Find my complaints</button>
                <span className="filter-count">
                  {searchedRoll ? `${myComplaints.length} complaints found` : 'Enter your roll number to begin'}
                </span>
              </form>
              {!searchedRoll ? (
                <EmptyState icon="⌕">Enter your roll number to find your reports.</EmptyState>
              ) : loading ? (
                <EmptyState>Loading complaints…</EmptyState>
              ) : myComplaints.length ? (
                <ComplaintTable complaints={myComplaints} onView={handleView} />
              ) : (
                <EmptyState icon="⌕">No reports found for that roll number.</EmptyState>
              )}
            </section>
          </section>
        )}

        {activeView === 'raise' && (
          <section aria-labelledby="raise-title">
            <div className="page-heading">
              <div><p className="eyebrow">We’re here to help</p><h1 id="raise-title">Raise a complaint</h1><p>Tell us what needs attention in your hostel.</p></div>
            </div>
            <section className="panel form-panel">
              <div className="form-intro">
                <span className="stat-icon" aria-hidden="true">✎</span>
                <div><h2>Tell us what’s going on</h2><p>Share a few details so the warden can route your concern.</p></div>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="form-grid">
                  <div className="form-field">
                    <label htmlFor="roll-number">Student roll number <span className="required">*</span></label>
                    <input
                      className="form-control"
                      id="roll-number"
                      name="roll_no"
                      type="number"
                      min="1"
                      step="1"
                      value={form.roll_no}
                      onChange={updateForm}
                      placeholder="e.g. 21045"
                      required
                    />
                    <span className="form-hint">Use the roll number linked to your hostel record.</span>
                  </div>
                  <div className="form-field">
                    <label htmlFor="room-number">Room number <span className="required">*</span></label>
                    <input
                      className="form-control"
                      id="room-number"
                      name="room_no"
                      type="text"
                      maxLength="30"
                      value={form.room_no}
                      onChange={updateForm}
                      placeholder="e.g. B-204"
                      required
                    />
                  </div>
                  <div className="form-field">
                    <label htmlFor="category">Category</label>
                    <select
                      className="form-control"
                      id="category"
                      name="catagory"
                      value={form.catagory}
                      onChange={updateForm}
                    >
                      <option value="">Select a category</option>
                      {CATEGORIES.map((category) => <option key={category} value={category}>{category}</option>)}
                    </select>
                  </div>
                  <div className="form-field form-field-full">
                    <label htmlFor="description">Describe the issue</label>
                    <textarea
                      className="form-control"
                      id="description"
                      name="description"
                      rows="4"
                      maxLength="1000"
                      value={form.description}
                      onChange={updateForm}
                      placeholder="Add details that will help us resolve your complaint."
                    />
                  </div>
                </div>
                <div className="form-footer">
                  <span className="form-hint">Roll number and room are required.</span>
                  <button className="primary-button" type="submit" disabled={submitting}>
                    {submitting ? 'Submitting…' : '＋ Submit complaint'}
                  </button>
                </div>
              </form>
            </section>
          </section>
        )}
      </main>

      {selectedComplaint && (
        <div className="dialog-backdrop" onClick={() => setSelectedComplaint(null)}>
          <section
            className="complaint-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="complaint-dialog-title"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="panel-header">
              <div>
                <h2 id="complaint-dialog-title">Complaint #{selectedComplaint.id}</h2>
                <p>Submitted {formatDate(selectedComplaint.created_on)}</p>
              </div>
              <button className="text-button" type="button" onClick={() => setSelectedComplaint(null)}>Close</button>
            </div>
            <div className="complaint-dialog-content">
              <StatusBadge status={selectedComplaint.status} />
              <p>{selectedComplaint.description || 'No description provided.'}</p>
              <div className="complaint-details">
                <span><strong>Student</strong>{selectedComplaint.roll_no}</span>
                <span><strong>Room</strong>{selectedComplaint.room_no}</span>
                <span><strong>Category</strong>{selectedComplaint.catagory || 'Uncategorized'}</span>
                {selectedComplaint.resolved_on && (
                  <span><strong>Resolved</strong>{formatDate(selectedComplaint.resolved_on)}</span>
                )}
              </div>
            </div>
          </section>
        </div>
      )}

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
