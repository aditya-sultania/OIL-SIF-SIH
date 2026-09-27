import React, { useEffect, useMemo, useState } from 'react'
import { LANGUAGES } from './translations.js'
import { api } from '../../api.js'

const SITES = ['Offshore Platform Alpha', 'Refinery Complex Beta', 'Pipeline Sector 4', 'Depot Terminal C']
const NAV_ITEMS = [
  { id:'overview', icon:'⌂', key:'overview', helpKey:'nav_overview_help', roles:['HSE Officer'] },
  { id:'reports', icon:'▤', key:'report_analysis', helpKey:'nav_reports_help', roles:['HSE Officer'] },
  { id:'intelligence', icon:'◈', key:'intelligence', helpKey:'nav_intelligence_help', roles:['HSE Officer'] },
  { id:'copilot', icon:'?', key:'ai_copilot', helpKey:'nav_copilot_help', roles:['HSE Officer'] },
  { id:'role', icon:'●', key:'my_dashboard', helpKey:'nav_role_help', roles:['Employee','HSE Officer'] },
  { id:'management', icon:'▥', key:'management_dashboard', helpKey:'nav_management_help', roles:['Management'] },
]
const tr=(T,k,f)=>T?.[k]||f
function roleLabel(role,T){return role==='Employee'?tr(T,'field_worker','Field Employee'):role==='HSE Officer'?tr(T,'hse_officer','HSE Officer'):tr(T,'management','Management')}

export default function DashboardShell({profile,language,setLanguage,T,onLogout,site,setSite,activePage,setActivePage,children}){
 const [navOpen,setNavOpen]=useState(false)
 const [sidebarCollapsed,setSidebarCollapsed]=useState(()=>localStorage.getItem('oil_sidebar_collapsed')==='1')
 const [theme,setTheme]=useState(()=>localStorage.getItem('oil_theme')||'light')
 const [accessibility,setAccessibility]=useState(()=>localStorage.getItem('oil_accessibility')==='1')
 const [helpOpen,setHelpOpen]=useState(false),[statusOpen,setStatusOpen]=useState(false),[noticeOpen,setNoticeOpen]=useState(false),[profileOpen,setProfileOpen]=useState(false),[settingsOpen,setSettingsOpen]=useState(false),[speaking,setSpeaking]=useState(false)
 const [notifications,setNotifications]=useState([]),[health,setHealth]=useState(null)
 useEffect(()=>{document.documentElement.dataset.theme=theme;localStorage.setItem('oil_theme',theme)},[theme])
 useEffect(()=>{document.documentElement.classList.toggle('accessibility-mode',accessibility);localStorage.setItem('oil_accessibility',accessibility?'1':'0')},[accessibility])
 useEffect(()=>{localStorage.setItem('oil_sidebar_collapsed',sidebarCollapsed?'1':'0')},[sidebarCollapsed])
 useEffect(()=>{
  const timer=setTimeout(()=>{
    api.getNotifications().then(r=>setNotifications(r.notifications||[])).catch(()=>{});
    api.health().then(setHealth).catch(()=>setHealth(null));
  },350)
  return ()=>clearTimeout(timer)
 },[])
 const role=profile.role, items=useMemo(()=>NAV_ITEMS.filter(x=>x.roles.includes(role)),[role]), active=items.find(x=>x.id===activePage)||items[0]
 const unread=notifications.filter(n=>!n.read).length
 const markRead=()=>{setNotifications(ns=>ns.map(n=>({...n,read:true})));api.markNotificationsRead().catch(()=>{})}
 const speak=()=>{
   window.speechSynthesis?.cancel();
   const text=[tr(T,'quick_help_title','Need help using OIL-SIF?'),tr(T,'help_report','Report'),tr(T,'help_report_text','Use voice or typing to describe an unsafe condition or near miss.'),tr(T,'help_review','Review'),tr(T,'help_review_text','Use the dashboard to see what needs attention.'),tr(T,'help_assistant','Ask the Assistant'),tr(T,'help_assistant_text','Ask safety questions in plain language.')].join('. ')
   const u=new SpeechSynthesisUtterance(text);u.onstart=()=>setSpeaking(true);u.onend=()=>setSpeaking(false);u.onerror=()=>setSpeaking(false);window.speechSynthesis?.speak(u)
 }
 const go=(page)=>{setProfileOpen(false);setSettingsOpen(false);setActivePage(page)}
 return <div className="app-shell">
  <header className="topbar">
   <button className="mobile-menu" onClick={()=>setNavOpen(v=>!v)} aria-label={tr(T,'open_menu','Open menu')}>☰</button>
   <div className="brand"><div className="brand-mark">O</div><div><strong>OIL-SIF</strong><span>{tr(T,'platform_name','Safety Intelligence Platform')}</span></div></div>
   <div className="topbar-right">
    <button className="status-link" onClick={()=>setStatusOpen(true)}><span className="status-dot"/> {tr(T,'system_operational','System operational')}</button>
    <button className="theme-toggle" onClick={()=>setTheme(v=>v==='dark'?'light':'dark')} aria-label={theme==='dark'?tr(T,'light_mode','Light mode'):tr(T,'dark_mode','Dark mode')} title={theme==='dark'?tr(T,'light_mode','Light mode'):tr(T,'dark_mode','Dark mode')}>{theme==='dark'?'☀':'☾'} <span>{theme==='dark'?tr(T,'light_mode','Light'):tr(T,'dark_mode','Dark')}</span></button>
    <button className="icon-btn" onClick={()=>{setNoticeOpen(v=>!v);markRead();setProfileOpen(false)}} aria-label={`${tr(T,'notifications','Notifications')} ${unread}`} title={tr(T,'notifications','Notifications')}>🔔{unread>0&&<b>{unread}</b>}</button>
    <button className="icon-btn help-top" onClick={()=>{setHelpOpen(true);setProfileOpen(false)}} aria-label={tr(T,'help','Help')}>?</button>
    <button className="user-menu" onClick={()=>{setProfileOpen(v=>!v);setNoticeOpen(false)}} aria-expanded={profileOpen}><span className="user-avatar">{(profile.name||'U')[0].toUpperCase()}</span><span className="user-copy"><b>{profile.name}</b><small>{roleLabel(role,T)}</small></span><span className="profile-chevron">⌄</span></button>
   </div>
  </header>
  {profileOpen&&<div className="popover profile-pop"><div className="profile-pop-head"><span className="user-avatar large">{(profile.name||'U')[0].toUpperCase()}</span><div><strong>{profile.name}</strong><span>{roleLabel(role,T)}</span></div></div><div className="profile-meta"><span>{tr(T,'username','Username')}</span><strong>{profile.username}</strong></div><button onClick={()=>setSettingsOpen(true)}>⚙ {tr(T,'settings','Settings')}</button><button onClick={()=>go(role==='Management'?'management':'role')}>◉ {tr(T,'my_dashboard','My Dashboard')}</button><button className="profile-signout" onClick={onLogout}>↪ {tr(T,'sign_out_safely','Sign out safely')}</button></div>}
  {noticeOpen&&<div className="popover notifications-pop"><div className="popover-head"><strong>{tr(T,'notifications','Notifications')}</strong><button onClick={()=>setNoticeOpen(false)}>×</button></div>{notifications.length?notifications.slice(-6).reverse().map((n,i)=><div className="notification-item" key={i}><span>{n.icon||'ℹ️'}</span><div><strong>{n.title}</strong><p>{n.text}</p><small>{n.time}</small></div></div>):<div className="empty-state">{tr(T,'no_notifications','No new notifications.')}</div>}</div>}
  {settingsOpen&&<div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&setSettingsOpen(false)}><div className="modal-card settings-card" role="dialog" aria-modal="true"><div className="modal-head"><div><span className="eyebrow">OIL-SIF</span><h2>{tr(T,'settings','Settings')}</h2></div><button className="close-btn" onClick={()=>setSettingsOpen(false)}>×</button></div><div className="settings-grid"><label>{tr(T,'select_lang','Language')}<select value={language} onChange={e=>setLanguage(e.target.value)}>{LANGUAGES.map(l=><option key={l}>{l}</option>)}</select></label><label>{tr(T,'appearance','Appearance')}<select value={theme} onChange={e=>setTheme(e.target.value)}><option value="light">{tr(T,'light_mode','Light mode')}</option><option value="dark">{tr(T,'dark_mode','Dark mode')}</option></select></label><label>{tr(T,'sidebar','Navigation')}<select value={sidebarCollapsed?'collapsed':'expanded'} onChange={e=>setSidebarCollapsed(e.target.value==='collapsed')}><option value="expanded">{tr(T,'expanded','Expanded')}</option><option value="collapsed">{tr(T,'collapsed','Collapsed')}</option></select></label><label>Accessibility<select value={accessibility?'enhanced':'standard'} onChange={e=>setAccessibility(e.target.value==='enhanced')}><option value="standard">Standard</option><option value="enhanced">Enhanced readability</option></select></label></div><p className="muted">{tr(T,'settings_note','Your preferences are saved on this device for the next visit.')}</p><div className="modal-actions"><button className="btn-primary" onClick={()=>setSettingsOpen(false)}>{tr(T,'close','Close')}</button></div></div></div>}
  {helpOpen&&<div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&setHelpOpen(false)}><div className="modal-card" role="dialog" aria-modal="true" aria-labelledby="help-title"><div className="modal-head"><div><span className="eyebrow">OIL-SIF</span><h2 id="help-title">{tr(T,'quick_help_title','Need help using OIL-SIF?')}</h2></div><button className="close-btn" onClick={()=>setHelpOpen(false)}>×</button></div><div className="help-grid"><div><b>1. {tr(T,'help_report','Report')}</b><p>{tr(T,'help_report_text','Use voice or typing to describe an unsafe condition or near miss.')}</p></div><div><b>2. {tr(T,'help_review','Review')}</b><p>{tr(T,'help_review_text','Use the dashboard to see what needs attention.')}</p></div><div><b>3. {tr(T,'help_assistant','Ask the Assistant')}</b><p>{tr(T,'help_assistant_text','Ask safety questions in plain language.')}</p></div></div><div className="modal-actions"><button className="btn-secondary read-aloud-btn" onClick={speak}>🔊 {tr(T,'read_aloud','Read aloud')}</button>{speaking&&<button className="btn-secondary" onClick={()=>{window.speechSynthesis?.cancel();setSpeaking(false)}}>■ {tr(T,'stop','Stop')}</button>}<button className="btn-primary" onClick={()=>setHelpOpen(false)}>{tr(T,'close','Close')}</button></div></div></div>}
  {statusOpen&&<div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&setStatusOpen(false)}><div className="modal-card"><div className="modal-head"><div><span className="eyebrow">OIL-SIF</span><h2>{tr(T,'system_status','System status')}</h2></div><button className="close-btn" onClick={()=>setStatusOpen(false)}>×</button></div><div className="status-list">{[['API',health?'Operational':'Unavailable'],['SIF classifier',health?.sif_model_loaded?'Loaded':'Unavailable'],['Life-Saving Rule engine',health?.lsr_model_loaded?'Loaded':'Unavailable'],['Voice input','Browser available']].map(x=><div key={x[0]}><span>{x[0]}</span><strong className={x[1]==='Unavailable'?'status-bad':''}><i/> {x[1]}</strong></div>)}</div><p className="muted">{tr(T,'status_note','Status checks describe the application services currently available to this session.')}</p></div></div>}
  <div className="app-body">
   <aside className={`sidebar ${navOpen?'open':''} ${sidebarCollapsed?'collapsed':''}`}><div className="sidebar-heading"><span>{tr(T,'workspace','WORKSPACE')}</span><button className="sidebar-collapse" onClick={()=>setSidebarCollapsed(v=>!v)} aria-label={sidebarCollapsed?tr(T,'expand_sidebar','Expand sidebar'):tr(T,'collapse_sidebar','Collapse sidebar')}>{sidebarCollapsed?'»':'«'}</button><button className="sidebar-close" onClick={()=>setNavOpen(false)}>×</button></div>
    <nav aria-label={tr(T,'main_navigation','Main navigation')}>{items.map(item=>{const is=activePage===item.id;return <button key={item.id} title={sidebarCollapsed?tr(T,item.key,item.key):undefined} className={`nav-item ${is?'active':''}`} onClick={()=>{setActivePage(item.id);setNavOpen(false)}} aria-current={is?'page':undefined}><span className="nav-icon">{item.icon}</span><span><b>{tr(T,item.key,item.key)}</b><small>{tr(T,item.helpKey,'')}</small></span></button>})}</nav>
    <div className="sidebar-section"><label htmlFor="language">{tr(T,'select_lang','Language')}</label><select id="language" value={language} onChange={e=>setLanguage(e.target.value)}>{LANGUAGES.map(l=><option key={l}>{l}</option>)}</select></div>
    <div className="sidebar-help"><div className="help-icon">?</div><div><strong>{tr(T,'need_help','Need help?')}</strong><p>{tr(T,'sidebar_help','Use the Safety Assistant for plain-language guidance.')}</p><button onClick={()=>setHelpOpen(true)}>{tr(T,'open_help','Open help')}</button></div></div>
    <div className="sidebar-bottom"><button className="settings-side-btn" onClick={()=>setSettingsOpen(true)}>⚙ {tr(T,'settings','Settings')}</button><button className="logout-btn" onClick={onLogout}>↪ {tr(T,'sign_out_safely','Sign out safely')}</button></div>
   </aside>
   <main className="main-content"><div className="page-intro"><div><h1>{tr(T,active.key,active.key)}</h1><p>{tr(T,'page_intro','Clear, practical safety information to support informed decisions.')}</p></div><div className="role-badge"><span className="role-dot"/>{roleLabel(role,T)}</div></div>{children}</main>
  </div>
  <footer className="app-footer"><span>OIL-SIF · {tr(T,'platform_name','Safety Intelligence Platform')}</span><span>{tr(T,'ai_disclaimer','AI recommendations support — not replace — qualified HSE judgement.')}</span></footer>
 </div>
}
