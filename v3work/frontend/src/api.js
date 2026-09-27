const BASE = `${import.meta.env.VITE_API_URL || ''}/api`
const TOKEN_KEY = 'oil_sif_token'

const cache = new Map()

function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY)
}

async function handle(res) {
  if (res.status === 401) clearAuth()
  if (!res.ok) {
    let detail = `Request failed (${res.status})`
    try {
      const contentType = res.headers.get('content-type') || ''
      if (contentType.includes('application/json')) {
        const j = await res.json()
        detail = j.detail || detail
      } else {
        const text = await res.text()
        if ((res.status === 502 || res.status === 503 || res.status === 504) || /vite|proxy|bad gateway|gateway timeout|service unavailable/i.test(text)) {
          detail = 'OIL-SIF backend is not reachable. Start FastAPI on port 8000 and try again.'
        }
      }
    } catch (_) {}
    throw new Error(detail)
  }
  return res.json()
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {})
  const token = getToken()
  if (token) headers.set('Authorization', `Bearer ${token}`)
  try {
    return handle(await fetch(`${BASE}${path}`, { ...options, headers }))
  } catch (error) {
    if (error instanceof TypeError) throw new Error('OIL-SIF service is not reachable. Please make sure the FastAPI backend is running on port 8000.')
    throw error
  }
}

async function cachedGet(path, ttl = 300000) {
  const now = Date.now()
  const existing = cache.get(path)
  if (existing && existing.expires > now) return existing.value
  const value = await request(path)
  cache.set(path, { value, expires: now + ttl })
  return value
}

export const api = {
  clearCache: () => cache.clear(),
  login: async (username, password) => {
    const result = await request('/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (result.token) localStorage.setItem(TOKEN_KEY, result.token)
    return result
  },
  me: () => request('/auth/me'),
  register: (name, username, password, role) => request('/auth/register', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, username, password, role }),
  }),
  logout: async () => {
    try { await request('/auth/logout', { method: 'POST' }) }
    finally { clearAuth(); cache.clear() }
  },
  scan: (text) => request('/scan', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  }),
  chat: (question, reset = false) => request('/chat', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, reset }),
  }),
  getBootstrap: (site='') => cachedGet(`/data/bootstrap?site=${encodeURIComponent(site)}`, 120000),
  getBarriers: () => cachedGet('/data/barriers', 300000),
  getActivities: () => cachedGet('/data/activities', 300000),
  getQueue: (limit = 100) => cachedGet(`/data/queue?limit=${limit}`, 120000),
  getReports: ({ search = '', status = 'all', review = 'all', activity = 'all', date_from = '', date_to = '', site = '', limit = 60 } = {}) => {
    const params = new URLSearchParams({ search, status, review, activity, date_from, date_to, site, limit: String(limit) })
    return request(`/data/reports?${params.toString()}`)
  },
  getLsr: () => cachedGet('/data/lsr', 300000),
  getPrecursor: () => cachedGet('/data/precursor', 300000),
  getOverview: (site='') => cachedGet(`/data/overview?site=${encodeURIComponent(site)}`, 120000),
  submitReport: (payload) => request('/reports', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  getMyReports: () => request('/reports/my'),
  getReportDetail: (id) => request(`/reports/${encodeURIComponent(id)}`),
  saveReview: (id, decision, reason, action) => request(`/reports/${encodeURIComponent(id)}/review`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ decision, reason, action }) }),
  health: () => request('/health'),
  getNotifications: () => request('/notifications'),
  getEmergencyContact: () => cachedGet('/emergency-contact', 300000),
  markNotificationsRead: () => request('/notifications/read', { method: 'POST' }),
  getSummary: (days=30, site='') => request(`/dashboard/summary?days=${days}&site=${encodeURIComponent(site)}`),
  getManagementSites: () => cachedGet('/management/sites', 120000),
  getManagementHeatmap: () => cachedGet('/management/heatmap', 120000),
  getManagementGeography: () => cachedGet('/management/geography', 120000),
  getManagementDrilldown: ({site='',activity='',hazard='',barrier=''}={}) => { const p=new URLSearchParams({site,activity,hazard,barrier}); return request(`/management/drilldown?${p.toString()}`) },
  getHseDensity: () => cachedGet('/hse/density', 120000),
  getDrilldown: (kind, value) => request(`/intelligence/drilldown?kind=${encodeURIComponent(kind)}&value=${encodeURIComponent(value)}`),
  exportReports: async ({ search='', status='all', review='all', activity='all', date_from='', date_to='', site='' }={}) => {
    const params = new URLSearchParams({ search, status, review, activity, date_from, date_to, site })
    const headers = new Headers(); const token = getToken(); if (token) headers.set('Authorization', `Bearer ${token}`)
    const res = await fetch(`${BASE}/export/reports?${params.toString()}`, { headers })
    if (!res.ok) throw new Error('Export could not be generated.')
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a=document.createElement('a');
    a.href=url;
    a.download='oil-sif-reports.csv';
    a.style.display='none';
    document.body.appendChild(a);
    a.click();
    setTimeout(()=>{a.remove();URL.revokeObjectURL(url)},1000)
  },
}
