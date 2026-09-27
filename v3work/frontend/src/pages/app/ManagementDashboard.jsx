import React,{useEffect,useMemo,useState} from 'react'
import {LineChart,Line,ResponsiveContainer,Tooltip,CartesianGrid,XAxis,YAxis} from 'recharts'
import {Panel,Chip} from '../../components/UI.jsx'
import {api} from '../../api.js'

const LEVELS={
 High:{tone:'red',icon:'●',text:'High SIF precursor density'},
 Moderate:{tone:'amber',icon:'●',text:'Moderate SIF precursor density'},
 Low:{tone:'green',icon:'●',text:'Low SIF precursor density'},
 'No data':{tone:'gray',icon:'●',text:'No live SIF precursor data'}
}
const tr=(T,k,f)=>T?.[k]||f
const formatNumber=n=>Number(n||0).toLocaleString()
const heatTone=r=>r>=.78?'critical':r>=.5?'high':r>=.24?'medium':'low'

export default function ManagementDashboard({T,data,site,onNavigate}){
 const [days,setDays]=useState(30),[sites,setSites]=useState([]),[selectedSite,setSelectedSite]=useState('')
 const [levelFilter,setLevelFilter]=useState('all'),[activity,setActivity]=useState(''),[year,setYear]=useState(null),[playing,setPlaying]=useState(false)
 const [geo,setGeo]=useState(null),[positions,setPositions]=useState({}),[selectedState,setSelectedState]=useState(''),[drill,setDrill]=useState(null)
 const [activityDrill,setActivityDrill]=useState(''),[hazard,setHazard]=useState(''),[barrier,setBarrier]=useState(''),[loading,setLoading]=useState(false)
 const [search,setSearch]=useState(''),[story,setStory]=useState(false),[storyStep,setStoryStep]=useState(0)

 useEffect(()=>{
  api.getManagementGeography().then(setGeo).catch(()=>setGeo(null))
  api.getManagementSites().then(r=>{setSites(r.sites||[]);setSelectedSite(v=>v||r.sites?.[0]?.name||'')}).catch(()=>setSites([]))
  fetch('/state-positions.json').then(r=>r.json()).then(setPositions).catch(()=>setPositions({}))
 },[])
 const years=geo?.years||[]
 useEffect(()=>{if(years.length)setYear(v=>v&&years.some(y=>y.year===v)?v:years[years.length-1].year)},[years.length])
 useEffect(()=>{if(!playing||!years.length)return;const t=setInterval(()=>setYear(cur=>{const i=Math.max(0,years.findIndex(y=>y.year===cur));return years[(i+1)%years.length].year}),1100);return()=>clearInterval(t)},[playing,years])
 const selected=sites.find(x=>x.name===selectedSite), level=selected?.risk_level||'No data'
 const visibleSites=useMemo(()=>levelFilter==='all'?sites:sites.filter(x=>x.risk_level===levelFilter),[sites,levelFilter])
 const yearRecord=years.find(y=>y.year===year)
 const stateRows=useMemo(()=>{
  if(!geo?.states)return []
  const map=activity?geo.activity_states?.[activity]||{}:null
  return geo.states.map(s=>({...s,viewCount:Number(map?map[s.name]||0:yearRecord?.states?.[s.name]||0)})).filter(s=>s.viewCount>0)
 },[geo,activity,yearRecord])
 const searchFiltered=useMemo(()=>{const q=search.trim().toLowerCase();if(!q)return stateRows;return stateRows.filter(s=>s.name.toLowerCase().includes(q)||s.top_activities?.some(a=>String(a.name).toLowerCase().includes(q)))},[stateRows,search])
 const maxVisible=Math.max(1,...searchFiltered.map(s=>s.viewCount)), ranked=useMemo(()=>[...searchFiltered].sort((a,b)=>b.viewCount-a.viewCount).slice(0,6),[searchFiltered])
 const chosen=searchFiltered.find(s=>s.name===selectedState)||ranked[0], totalVisible=searchFiltered.reduce((a,s)=>a+s.viewCount,0)
 const country=geo?.country, activities=geo?.activities||[]
 const trend=useMemo(()=>years.map(y=>({year:String(y.year),reports:Object.values(y.states||{}).reduce((a,v)=>a+Number(v||0),0)})),[years])
 const highStates=ranked.filter(s=>s.viewCount/maxVisible>=.5).length
 const topActivity=chosen?.top_activities?.[0]?.name||'Not available'

 async function loadDrill(next={}){if(!selectedSite)return;setLoading(true);try{const r=await api.getManagementDrilldown({site:selectedSite,...next});setDrill(r);setActivityDrill(next.activity||'');setHazard(next.hazard||'');setBarrier(next.barrier||'')}finally{setLoading(false)}}
 function selectSite(name){setSelectedSite(name);setActivityDrill('');setHazard('');setBarrier('');api.getManagementDrilldown({site:name}).then(setDrill).catch(()=>setDrill(null))}
 const activitiesDrill=drill?.activities||[],hazards=drill?.hazards||[],barriers=drill?.barriers||[],reports=drill?.reports||[]
 const storyTitles=['Geographic overview','Concentration hotspots','Operational pattern','Evidence trail']
 const storyText=[
  `The current geographic view contains ${formatNumber(totalVisible)} records across the selected scope.`,
  chosen?`${chosen.name} is the current leading hotspot with ${formatNumber(chosen.viewCount)} reports in this view.`:'Select a hotspot to inspect concentration.',
  topActivity!== 'Not available'?`${topActivity} is the leading recurring activity associated with the selected state.`:'Activity detail is not available for this selection.',
  selectedSite?`The next step is to verify the underlying reports for ${selectedSite}.`:'Select a site below to open the evidence trail.'
 ]
 return <div className="management-page">
  <div className="management-command-hero">
   <div className="hero-copy"><span className="eyebrow">MANAGEMENT COMMAND CENTER</span><h2>Safety intelligence, made simple.</h2><p>Start with the geographic signal, understand the pattern, then verify the evidence. The interface is designed for quick decisions without requiring technical expertise.</p><div className="hero-badges"><span><i/> System operational</span><span>2015–2025 historical view</span><span>{formatNumber(country?.total_reports)} records</span></div></div>
   <div className="hero-actions"><label>Reporting period<select value={days} onChange={e=>setDays(Number(e.target.value))}><option value={7}>7 days</option><option value={30}>30 days</option><option value={90}>90 days</option><option value={365}>12 months</option></select></label><button className="story-button" onClick={()=>{setStory(true);setStoryStep(0)}}>▶ Start safety briefing</button></div>
  </div>

  <div className="management-kpis">
   <div className="command-kpi"><span>REPORTS IN VIEW</span><strong>{formatNumber(totalVisible)}</strong><small>Current geographic scope</small></div>
   <div className="command-kpi amber"><span>HOTSPOT STATES</span><strong>{highStates}</strong><small>Higher-concentration areas</small></div>
   <div className="command-kpi red"><span>SIF-POTENTIAL REPORTS</span><strong>{formatNumber(data?.overview?.kpis?.sif_potential)}</strong><small>Requires HSE validation</small></div>
   <div className="command-kpi blue"><span>HSE REVIEW QUEUE</span><strong>{formatNumber(data?.overview?.kpis?.awaiting_review)}</strong><small>Human review remains required</small></div>
  </div>

  <div className="management-alert"><div className="alert-icon">!</div><div><strong>Management attention</strong><span>{highStates?`${highStates} geographic area${highStates>1?'s':''} show higher report concentration in the current view.`:'No high-concentration area is currently selected.'}</span></div><button onClick={()=>document.getElementById('geo-intelligence')?.scrollIntoView({behavior:'smooth'})}>Investigate signal →</button></div>

  <Panel title="Geographic safety intelligence" subtitle="A U.S. map built from the supplied 2015–2025 reporting dataset. Glow intensity represents report concentration, not SIF probability." id="geo-intelligence">
   <div className="geo-toolbar"><div className="geo-search"><span>⌕</span><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search a state or activity…" aria-label="Search a state or activity"/>{search&&<button onClick={()=>setSearch('')}>×</button>}</div><label>Activity<select value={activity} onChange={e=>{setActivity(e.target.value);setSelectedState('')}}><option value="">All activities</option>{activities.map(a=><option key={a.name} value={a.name}>{a.name}</option>)}</select></label><div className="map-stat-pill"><span>{activity?'Activity lens':'Historical year'}</span><strong>{activity?'All years':year}</strong></div></div>
   <div className="geo-map-layout geo-map-layout-v2">
    <div className="geo-map-card us-heat-surface">
     <div className="map-grid"/><div className="map-glow"/><div className="map-scanline"/>
     <div className="map-surface-head"><div><span>GEOSPATIAL RISK SURFACE</span><strong>UNITED STATES</strong></div><div className="surface-status"><i/>{playing?'Historical scan active':'Interactive'}</div></div>
     <img className="us-map-outline us-map-v2" src="/us-states-outline.svg" alt="United States state outline"/>
     <div className="map-water-label">REPORT CONCENTRATION</div>
     {searchFiltered.map((s,i)=>{const p=positions[s.name];if(!p)return null;const ratio=s.viewCount/maxVisible;const size=18+Math.sqrt(ratio)*58;const selected=s.name===selectedState;return <React.Fragment key={s.name}><button className={`geo-bubble-v2 ${heatTone(ratio)} ${selected?'selected':''} ${p.inset?'inset':''}`} style={{left:`${p.x*100}%`,top:`${p.y*100}%`,width:size,height:size,'--delay':`${i%15*70}ms`}} onClick={()=>setSelectedState(s.name)} aria-label={`${s.name}, ${formatNumber(s.viewCount)} reports`} title={`${s.name}: ${formatNumber(s.viewCount)} reports`}><span className="bubble-halo"/><span className="bubble-core"/></button>{(selected||i<5)&&<button className={`map-state-tag ${selected?'selected':''}`} style={{left:`calc(${p.x*100}% + ${size/2+8}px)`,top:`calc(${p.y*100}% - 12px)`}} onClick={()=>setSelectedState(s.name)}>{s.name}<b>{formatNumber(s.viewCount)}</b></button>}</React.Fragment>})}
     <div className="surface-legend"><span><i className="legend-dot cool"/>Lower</span><span><i className="legend-dot warm"/>Elevated</span><span><i className="legend-dot hot"/>High concentration</span><span><i className="legend-dot critical"/>Highest</span></div>
     <div className="map-timeline"><button onClick={()=>setPlaying(v=>!v)}>{playing?'Ⅱ':'▶'}</button><input type="range" min={years[0]?.year||2015} max={years[years.length-1]?.year||2025} value={year||2025} disabled={!!activity} onChange={e=>setYear(Number(e.target.value))}/><strong>{activity?'2015–2025':year}</strong></div>
    </div>
    <aside className="geo-intelligence-panel geo-intelligence-v2">
     <div className="intel-header"><span className="eyebrow">STATE INTELLIGENCE</span><strong>{chosen?.name||'Select a hotspot'}</strong></div>
     {chosen?<><div className="intel-score"><div><strong>{formatNumber(chosen.viewCount)}</strong><span>reports in current view</span></div><span className={`heat-badge ${heatTone(chosen.viewCount/maxVisible)}`}>{heatTone(chosen.viewCount/maxVisible)==='critical'?'Highest concentration':'Signal detected'}</span></div><div className="intel-meter"><i style={{width:`${Math.max(5,chosen.viewCount/maxVisible*100)}%`}}/></div><div className="intel-facts"><div><span>Top activity</span><strong>{topActivity}</strong></div><div><span>Overall share</span><strong>{chosen.share||0}%</strong></div><div><span>Federal</span><strong>{formatNumber(chosen.federal_reports)}</strong></div><div><span>State</span><strong>{formatNumber(chosen.state_reports)}</strong></div></div><div className="explain-box"><span>WHY THIS SIGNAL?</span><p>{formatNumber(chosen.viewCount)} reports create a stronger geographic concentration signal than lower-volume states in the current scope. This is a reporting-density indicator, not a prediction of injury probability.</p></div></>:<div className="empty-state">Click a glowing state to see the evidence summary.</div>}
     <div className="hotspot-list">{ranked.map((s,i)=><button key={s.name} className={chosen?.name===s.name?'selected':''} onClick={()=>setSelectedState(s.name)}><b>{String(i+1).padStart(2,'0')}</b><span>{s.name}<small>{formatNumber(s.viewCount)} reports</small></span><i style={{width:`${Math.max(8,s.viewCount/maxVisible*100)}%`}}/></button>)}</div>
    </aside>
   </div>
   <div className="geo-footer"><span><b>{country?.name||'United States'}</b> · {formatNumber(country?.states)} states/areas represented</span><span>{activity?`Filtered: ${activity}`:'All activity groups'}</span><span>Click a hotspot for detail</span></div>
  </Panel>

  <div className="command-grid-two">
   <Panel title="Historical concentration" subtitle="See how reporting volume changes across the supplied historical years."><div className="trend-chart"><ResponsiveContainer width="100%" height={240}><LineChart data={trend}><CartesianGrid stroke="#d9e4ea" strokeDasharray="3 3"/><XAxis dataKey="year" tick={{fontSize:10}}/><YAxis tick={{fontSize:10}} tickFormatter={v=>Number(v).toLocaleString()}/><Tooltip formatter={v=>Number(v).toLocaleString()}/><Line type="monotone" dataKey="reports" stroke="#1f75b5" strokeWidth={3} dot={{r:3}} activeDot={{r:6}}/></LineChart></ResponsiveContainer></div></Panel>
   <Panel title="Quick management actions" subtitle="Common tasks are one click away."><div className="quick-action-grid"><button onClick={()=>window.print()}><span>⎙</span><strong>Print decision brief</strong><small>Prepare a management summary</small></button></div></Panel>
  </div>

  <Panel title="Site risk overview" subtitle="A simple facility-level view. Select a site to open its activity → hazard → barrier → report evidence trail."><div className="site-risk-grid">{visibleSites.map(s=>{const l=LEVELS[s.risk_level]||LEVELS['No data'];return <button key={s.name} className={`site-risk-card ${l.tone} ${selectedSite===s.name?'selected':''}`} onClick={()=>selectSite(s.name)}><div className="site-risk-head"><span>{s.id}</span><span>{l.icon}</span></div><h3>{s.name}</h3><strong>{l.text}</strong><div className="site-risk-stats"><span><b>{formatNumber(s.sif_reports)}</b> SIF reports</span><span><b>{formatNumber(s.total_reports)}</b> reports</span></div><small>{s.source==='live'?'Live submitted reports':'Management demonstration baseline'}</small></button>})}</div><div className="risk-filter"><span>Filter facilities</span>{['all','High','Moderate','Low'].map(x=><button key={x} className={levelFilter===x?'active':''} onClick={()=>setLevelFilter(x)}>{x==='all'?'All sites':x}</button>)}</div></Panel>

  {selected&&<div className="management-selection"><div><span>Selected facility</span><strong>{selected.id} · {selected.name}</strong></div><Chip tone={LEVELS[level]?.tone==='red'?'red':LEVELS[level]?.tone==='amber'?'amber':'green'}>{LEVELS[level]?.icon} {LEVELS[level]?.text}</Chip><button className="btn-secondary" onClick={()=>onNavigate?.('overview')}>View site overview →</button></div>}

  <Panel title="Risk investigation" subtitle="Three simple steps keep the evidence trail understandable for non-technical users."><div className="investigation-guide"><div className="investigation-step"><b>1</b><div><strong>Choose a site</strong><span>Set the management scope.</span></div></div><div className="investigation-step"><b>2</b><div><strong>Find the pattern</strong><span>Identify activities, hazards and failed barriers.</span></div></div><div className="investigation-step"><b>3</b><div><strong>Verify the evidence</strong><span>Open the underlying reports before decisions.</span></div></div></div><div className="drill-breadcrumb"><button className={!activityDrill?'active':''} onClick={()=>loadDrill({})}>All activities</button><span>→</span><button className={!hazard&&activityDrill?'active':''} disabled={!activityDrill} onClick={()=>loadDrill({activity:activityDrill})}>Hazards</button><span>→</span><button className={barrier?'active':''} disabled={!hazard} onClick={()=>loadDrill({activity:activityDrill,hazard})}>Barriers</button><span>→</span><span className="drill-end">Reports</span></div><div className="drill-columns"><div><h4>1 · Activities</h4><div className="drill-list">{activitiesDrill.length?activitiesDrill.map(x=><button key={x.name} className={activityDrill===x.name?'selected':''} onClick={()=>loadDrill({activity:x.name})}><span>{x.name}</span><b>{x.count}</b></button>):<div className="empty-state">Select a site to see activity patterns.</div>}</div></div><div><h4>2 · Hazards</h4><div className="drill-list">{hazards.length?hazards.map(x=><button key={x.name} className={hazard===x.name?'selected':''} onClick={()=>loadDrill({activity:activityDrill,hazard:x.name})}><span>{x.name}</span><b>{x.count}</b></button>):<div className="empty-state">Choose an activity first.</div>}</div></div><div><h4>3 · Failed barriers</h4><div className="drill-list">{barriers.length?barriers.map(x=><button key={x.name} className={barrier===x.name?'selected':''} onClick={()=>loadDrill({activity:activityDrill,hazard,barrier:x.name})}><span>{x.name}</span><b>{x.count}</b></button>):<div className="empty-state">Choose a hazard first.</div>}</div></div></div><div className="drill-report-head"><strong>{loading?'Loading evidence…':`${reports.length} SIF reports found for the current selection`}</strong>{(activityDrill||hazard||barrier)&&<button className="btn-secondary compact" onClick={()=>loadDrill({})}>Reset</button>}</div>{reports.length?<div className="management-report-list">{reports.slice(0,20).map(r=><button key={r.report_id} onClick={()=>onNavigate?.('reports',r.report_id)}><div><strong>{r.report_id}</strong><span>{r.activity_group||'Activity'} · {r.precursor||'Hazard'} · {r.barrier||'Barrier not recorded'}</span></div><Chip tone="red">SIF {Number(r.sif_probability||0).toFixed(1)}%</Chip><span>→</span></button>)}</div>:<div className="empty-state">No live SIF reports match this selection.</div>}</Panel>

  <Panel title="Management priorities" subtitle="A concise decision path that keeps the interface focused."><div className="management-priorities"><div><b>01</b><strong>Watch concentration</strong><span>Use geographic density to identify where attention may be required.</span></div><div><b>02</b><strong>Find the failed barrier</strong><span>Drill through activity and hazard to identify controls that may need restoration.</span></div><div><b>03</b><strong>Validate with HSE</strong><span>Use the review queue and underlying reports before operational decisions.</span></div></div></Panel>

  {story&&<div className="modal-backdrop" onMouseDown={e=>e.target===e.currentTarget&&setStory(false)}><div className="story-modal"><div className="story-top"><span className="eyebrow">EXECUTIVE SAFETY BRIEFING</span><button className="close-btn" onClick={()=>setStory(false)}>×</button></div><div className="story-progress">{storyTitles.map((x,i)=><span className={i===storyStep?'active':i<storyStep?'done':''} key={x}>{i+1}</span>)}</div><div className="story-stage"><span>{storyTitles[storyStep]}</span><h2>{storyTitles[storyStep]}</h2><p>{storyText[storyStep]}</p>{storyStep===0&&<div className="story-stat"><strong>{formatNumber(totalVisible)}</strong><small>records in current map scope</small></div>}{storyStep===1&&chosen&&<div className="story-stat"><strong>{chosen.name}</strong><small>{formatNumber(chosen.viewCount)} reports</small></div>}{storyStep===2&&<div className="story-stat"><strong>{topActivity}</strong><small>leading recurring activity</small></div>}{storyStep===3&&<div className="story-stat"><strong>{selectedSite||'Select a facility'}</strong><small>evidence trail</small></div>}</div><div className="story-actions"><button className="btn-secondary" onClick={()=>setStoryStep(s=>Math.max(0,s-1))} disabled={!storyStep}>← Back</button>{storyStep<3?<button className="btn-primary" onClick={()=>setStoryStep(s=>Math.min(3,s+1))}>Next →</button>:<button className="btn-primary" onClick={()=>{setStory(false);onNavigate?.('reports')}}>Open review queue →</button>}</div></div></div>}
 </div>
}
