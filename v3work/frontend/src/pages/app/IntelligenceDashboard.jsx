import React,{useMemo,useState} from 'react'
import {Panel} from '../../components/UI.jsx'
const tr=(T,k,f)=>T?.[k]||f

// Plain-language explanations shown with each Life-Saving Rule so the HSE
// intelligence view explains the control intent instead of only naming the rule.
const LSR_DETAILS={
 'Driving / Mobile Equipment': {
   description:'Control the risks created by driving and operating mobile equipment, especially vehicle–pedestrian interaction, distraction and loss of control.',
   controls:'Use seat belts, follow site speed and traffic rules, stay focused, use designated routes and keep pedestrians separated from moving equipment.'
 },
 'Safe Driving': {
   description:'Control the risks created by driving and operating mobile equipment, especially vehicle–pedestrian interaction, distraction and loss of control.',
   controls:'Use seat belts, follow site speed and traffic rules, stay focused, use designated routes and keep pedestrians separated from moving equipment.'
 },
 'Lifting Operations': {
   description:'Prevent people from being struck by, trapped under, or exposed to a dropped or uncontrolled load during lifting.',
   controls:'Plan the lift, inspect lifting gear, use competent personnel and establish an exclusion zone before the load is moved.'
 },
 'Line of Fire': {
   description:'Keep people out of locations where they could be struck, crushed, caught, released or otherwise exposed to stored or moving energy.',
   controls:'Identify the line of fire, establish exclusion zones and never place yourself between moving equipment, loads or other sources of energy.'
 },
 'Working at Height': {
   description:'Prevent serious injury from falls when work is performed where a person could fall from one level to another.',
   controls:'Use suitable access and fall-protection systems, verify anchorage and inspect equipment before starting work.'
 },
 'Hot Work': {
   description:'Prevent fires and explosions when welding, cutting, grinding or other work can create an ignition source.',
   controls:'Obtain the required permit, isolate combustible or hydrocarbon sources, gas-test the area and maintain the required fire-watch controls.'
 },
 'Excavation': {
   description:'Prevent collapse, buried-service strikes and other serious exposures when ground is opened or disturbed.',
   controls:'Obtain authorization, locate underground services, assess ground stability and provide suitable support, access and exclusion controls.'
 },
 'Energy Isolation': {
   description:'Prevent unexpected release of electrical, mechanical, hydraulic, pneumatic, pressure, chemical or other hazardous energy.',
   controls:'Identify all energy sources, isolate and lock/tag them, release stored energy and verify zero energy before work begins.'
 },
 'Confined Space': {
   description:'Prevent fatal exposure to toxic atmospheres, oxygen deficiency, engulfment and other hazards in spaces not designed for continuous occupancy.',
   controls:'Authorize the entry, isolate hazards, test and monitor the atmosphere, maintain communication and have rescue arrangements ready.'
 }
}
export default function IntelligenceDashboard({T,data,onNavigate}){
 const barriers=data?.barriers?.rows||[],lsr=data?.lsr?.rows||[],activities=data?.activities?.rows||[],precursors=data?.precursor?.rows||[]
 const [selected,setSelected]=useState(null),[facility,setFacility]=useState('All facilities')
 const topPrecursors=useMemo(()=>precursors.slice(0,8),[precursors])
 const total=topPrecursors.reduce((s,x)=>s+Number(x.total_reports||0),0)||1
 return <div className="intelligence-page"><div className="intel-hero"><div><span className="eyebrow">PRECURSOR INTELLIGENCE</span><h2>Find recurring patterns before they become serious events.</h2><p>Use the cards and rankings below to move from a pattern → activity → barrier → related reports.</p></div><div className="hero-control"><label>Facility view</label><select value={facility} onChange={e=>setFacility(e.target.value)}><option>All facilities</option><option>Offshore Platform Alpha</option><option>Refinery Complex Beta</option><option>Pipeline Sector 4</option><option>Depot Terminal C</option></select></div></div>
 <div className="insight-strip"><div><b>1</b><span>Identify a recurring precursor</span></div><div><b>2</b><span>Open the related activity or barrier</span></div><div><b>3</b><span>Send the evidence to report review</span></div></div>
 <Panel title="🔥 Top recurring precursor patterns" subtitle="Ranked by the available SIF-precursor dataset. Click a card to explore it."><div className="pattern-grid">{topPrecursors.map((x,i)=><button className={`pattern-card ${selected?.precursor===x.precursor?'selected':''}`} key={i} onClick={()=>setSelected(x)}><div className="pattern-top"><b>#{x.rank||i+1}</b><span>{Number(x.sif_density_pct||0).toFixed(1)}% SIF density</span></div><h3>{x.precursor||'Unknown precursor'}</h3><div className="bar-track"><i style={{width:`${Math.min(100,(Number(x.total_reports||0)/total)*100)}%`}}/></div><small>{Number(x.total_reports||0).toLocaleString()} reports · {Number(x.sif_reports||0).toLocaleString()} SIF reports</small></button>)}</div></Panel>
 {selected&&<Panel title={`🔎 Pattern drill-down: ${selected.precursor}`} subtitle="Use this as an evidence-led starting point for HSE intervention."><div className="drill-summary"><div><span>Reports</span><strong>{Number(selected.total_reports||0).toLocaleString()}</strong></div><div><span>SIF reports</span><strong>{Number(selected.sif_reports||0).toLocaleString()}</strong></div><div><span>SIF density</span><strong>{Number(selected.sif_density_pct||0).toFixed(1)}%</strong></div></div><div className="drill-actions"><button className="btn-primary" onClick={()=>onNavigate?.('reports',selected.precursor)}>View related reports →</button><button className="btn-secondary" onClick={()=>window.speechSynthesis?.speak(new SpeechSynthesisUtterance(`The selected precursor is ${selected.precursor}. It has ${selected.sif_reports||0} SIF reports out of ${selected.total_reports||0} reports.`))}>🔊 Read summary</button></div></Panel>}
 <div className="two-col-panels"><Panel title="🛡️ Barrier health" subtitle="Barriers most associated with observed failures."><div className="rank-list">{barriers.slice(0,7).map((x,i)=><button key={i} onClick={()=>onNavigate?.('reports',x.barrier_theme||x.critical_barrier)}><span className="rank-num">{i+1}</span><div><strong>{x.barrier_theme||x.critical_barrier||'Unknown barrier'}</strong><small>{Number(x.sif_reports||0).toLocaleString()} SIF reports · {Number(x.sif_density_pct||0).toFixed(1)}% density</small></div><span>→</span></button>)}</div></Panel><Panel title="🧭 Life-Saving Rules" subtitle="Rules with the strongest presence in the dataset. Each rule includes the control intent and the practical checks HSE should look for."><div className="rank-list lsr-list">{lsr.slice(0,8).map((x,i)=>{const rule=x.life_saving_rule||x.rule||'Unknown rule'; const detail=LSR_DETAILS[rule]||{description:'A critical safety control intended to prevent a serious injury or fatality exposure.',controls:'Confirm the applicable site procedure, verify the physical controls and stop work if the required barrier is missing.'}; return <button className="lsr-rule-card" key={i} onClick={()=>onNavigate?.('reports',rule)}><span className="rank-num">{i+1}</span><div className="lsr-rule-copy"><div className="lsr-rule-head"><strong>{rule}</strong><small>{Number(x.sif_reports||x.high_sif_count||0).toLocaleString()} SIF reports</small></div><p>{detail.description}</p><span className="lsr-controls"><b>Key controls:</b> {detail.controls}</span></div><span className="lsr-arrow">→</span></button>})}</div></Panel></div>
 <Panel title="⚙️ Activity risk ranking" subtitle="Click an activity to move directly to its reports."><div className="activity-ranking">{activities.slice(0,10).map((x,i)=><button key={i} onClick={()=>onNavigate?.('reports',x.activity_group||x.Activity)}><span className="rank-num">{i+1}</span><strong>{x.activity_group||x.Activity||'Unknown activity'}</strong><div className="mini-meter"><i style={{width:`${Math.min(100,Number(x.sif_density_pct||0))}%`}}/></div><span>{Number(x.sif_density_pct||0).toFixed(1)}%</span><b>→</b></button>)}</div></Panel>
 </div>
}
