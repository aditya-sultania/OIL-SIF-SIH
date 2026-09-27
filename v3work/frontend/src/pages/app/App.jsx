import React, { useEffect, useState, Suspense } from 'react'
import { TRANSLATIONS } from './translations.js'
import { api } from '../../api.js'
import LoginScreen from './LoginScreen.jsx'
import DashboardShell from './DashboardShell.jsx'
const EmployeeDashboard = React.lazy(() => import('./EmployeeDashboard.jsx'))
const HseDashboard = React.lazy(() => import('./HseDashboard.jsx'))
const ManagementDashboard = React.lazy(() => import('./ManagementDashboard.jsx'))
const Overview = React.lazy(() => import('./Overview.jsx'))
const IntelligenceDashboard = React.lazy(() => import('./IntelligenceDashboard.jsx'))
const ReportAnalysis = React.lazy(() => import('./ReportAnalysis.jsx'))
const Chatbot = React.lazy(() => import('./Chatbot.jsx'))
import { installLanguageObserver } from './translations_runtime.js'

const ROLE_HOME = { Employee: 'role', 'HSE Officer': 'role', Management: 'management' }
const ROLE_ALLOWED = {
  Employee: ['role'],
  'HSE Officer': ['overview', 'reports', 'intelligence', 'copilot', 'role'],
  Management: ['management'],
}
const emptyData = { overview: null, barriers: null, activities: null, lsr: null, precursor: null, queue: null }

export default function App() {
  const [language, setLanguageState] = useState(() => localStorage.getItem('oil_language') || 'English')
  const setLanguage = value => { window.__oilSifRestoreLanguage?.(); localStorage.setItem('oil_language', value); setLanguageState(value) }
  const [profile, setProfile] = useState(null)
  const [site, setSiteState] = useState(() => localStorage.getItem('oil_site') || 'Offshore Platform Alpha')
  const setSite = value => { localStorage.setItem('oil_site', value); api.clearCache?.(); setSiteState(value) }
  const [activePage, setActivePage] = useState('role')
  const [data, setData] = useState(emptyData)
  const [loading, setLoading] = useState(false)
  const [reportSeed, setReportSeed] = useState(null)
  const T = TRANSLATIONS[language] || TRANSLATIONS.English

  useEffect(() => { localStorage.setItem('oil_site', site) }, [site])
  useEffect(() => {
    const stop = installLanguageObserver(language)
    return stop
  }, [language])
  useEffect(() => {
    const code = language.includes('Urdu') || language.includes('Kashmiri') || language.includes('Sindhi') ? 'ur' : 'en'
    document.documentElement.dir = code === 'ur' ? 'rtl' : 'ltr'
    document.documentElement.lang = code
  }, [language])
  useEffect(() => {
    let cancelled = false
    if (!localStorage.getItem('oil_sif_token')) return undefined
    api.me().then(result => {
      if (!cancelled) { setProfile(result.user); setActivePage(ROLE_HOME[result.user.role] || 'role') }
    }).catch(() => localStorage.removeItem('oil_sif_token'))
    return () => { cancelled = true }
  }, [])

  useEffect(() => {
    if (!profile) return undefined
    // Management has its own compact endpoints (geography/sites) and does not
    // need the shared bootstrap payload. Avoid an unnecessary request during
    // the first post-login render.
    if (profile.role === 'Management') {
      setData(emptyData)
      setLoading(false)
      return undefined
    }
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const result = await api.getBootstrap(site)
        if (!cancelled) setData({
          overview: result.overview || null,
          barriers: result.barriers || null,
          activities: result.activities || null,
          lsr: result.lsr || null,
          precursor: result.precursor || null,
          queue: result.queue || null,
        })
      } catch (e) { console.error('OIL-SIF data load:', e) }
      finally { if (!cancelled) setLoading(false) }
    }
    load()
    return () => { cancelled = true }
  }, [profile, site])

  function navigate(page, seed = null) {
    const allowed = ROLE_ALLOWED[profile?.role] || []
    if (allowed.includes(page)) { setReportSeed(seed); setActivePage(page) }
  }
  async function handleLogin(result) {
    const user = result.user || result
    // Start fetching the management bundle immediately after authentication so
    // Vite can compile it while the shell is switching views.
    if (user.role === 'Management') import('./ManagementDashboard.jsx').catch(() => {})
    setProfile(user); setData(emptyData); setActivePage(ROLE_HOME[user.role] || 'role')
  }
  async function handleLogout() {
    await api.logout(); setData(emptyData); setProfile(null); setActivePage('role')
  }
  const allowed = profile ? ROLE_ALLOWED[profile.role] || [] : []
  const safePage = profile && allowed.includes(activePage) ? activePage : profile ? ROLE_HOME[profile.role] || 'role' : 'role'

  if (!profile) return <LoginScreen language={language} setLanguage={setLanguage} T={T} onLogin={handleLogin} />

  let page
  if (safePage === 'overview') page = <Overview T={T} data={data.overview} loading={loading && !data.overview} onNavigate={navigate} role={profile.role} />
  else if (safePage === 'reports') page = <ReportAnalysis T={T} data={data.queue} initialSeed={reportSeed} site={site} />
  else if (safePage === 'intelligence') page = <IntelligenceDashboard T={T} data={data} onNavigate={navigate} />
  else if (safePage === 'copilot') page = <Chatbot profile={profile} site={site} language={language} T={T} />
  else if (safePage === 'management' || (profile.role === 'Management' && safePage === 'overview')) page = <ManagementDashboard T={T} data={data.overview} site={site} onNavigate={navigate} />
  else if (profile.role === 'Employee') page = <EmployeeDashboard T={T} data={data} site={site} language={language} profile={profile} />
  else if (profile.role === 'HSE Officer') page = <HseDashboard T={T} data={data} site={site} onNavigate={navigate} />
  else page = <ManagementDashboard T={T} data={data.overview} site={site} onNavigate={navigate} />

  return <DashboardShell profile={profile} language={language} setLanguage={setLanguage} T={T}
    site={site} setSite={setSite} activePage={safePage} setActivePage={navigate} onLogout={handleLogout}>
    <Suspense fallback={<div className="dashboard-loading"><div className="loading-spinner" aria-hidden="true"/><strong>Preparing your safety dashboard…</strong><p>The workspace is loading the latest safety view.</p></div>}>
      {page}
    </Suspense>
  </DashboardShell>
}
