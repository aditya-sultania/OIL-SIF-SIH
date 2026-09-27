import React,{useEffect,useMemo,useState} from 'react'
import {Chip,Panel} from '../../components/UI.jsx'
import {api} from '../../api.js'
const tr=(T,k,f)=>T?.[k]||f

function densityTone(value,max){
 const ratio=max?value/max:0
 if(value===0)return 'empty'
 if(ratio>=.82)return 'critical'
 if(ratio>=.58)return 'high'
 if(ratio>=.3)return 'medium'
 return 'low'
}

export default function HseDashboard({T,data,site,onNavigate}){
 const k=data?.overview?.kpis||{}; const queue=data?.queue?.rows||[]; const [filter,setFilter]=useState('attention')
 const [density,setDensity]=useState(null); const [densityMode,setDensityMode]=useState('sif'); const [selectedCell,setSelectedCell]=useState(null)
 const critical=queue.filter(x=>String(x.sif_prediction).toLowerCase().includes('sif')).length||k.high_probability||0
 const shown=useMemo(()=>filter==='attention'?queue.slice(0,8):filter==='critical'?queue.filter(x=>String(x.sif_prediction).toLowerCase().includes('sif')).slice(0,8):queue.slice(0,8),[filter,queue])
 useEffect(()=>{api.getHseDensity().then(setDensity).catch(()=>setDensity(null))},[])
 const maxSif=Math.max(1,...(density?.cells||[]).map(x=>x.sif||0)); const maxTotal=Math.max(1,...(density?.cells||[]).map(x=>x.total||0))
 const selectedInfo=selectedCell&&density?.cells?.find(x=>x.activity===selectedCell.activity&&x.rule===selectedCell.rule)
 return <div className="hse-dashboard">
  <div className="scope-strip"><span>Current facility</span><strong>{site}</strong><small>Live submitted reports and the review workflow use this facility scope.</small></div>
  <div className="action-banner hse-action-banner"><div><span className="eyebrow">HSE ACTION CENTRE</span><h2>{tr(T,'hse_action_title','What needs my attention?')}</h2><p>Review serious-risk observations, validate AI screening and record the next safety action.</p></div><button className="btn-primary" onClick={()=>onNavigate?.('reports')}>Open report review →</button></div>
  <div className="kpi-grid four hse-kpis"><div className="kpi-card critical"><span>🔴 Critical / SIF</span><strong>{Number(critical).toLocaleString()}</strong><small>Potential serious-risk observations</small></div><div className="kpi-card high"><span>🟠 High probability</span><strong>{Number(k.high_probability||0).toLocaleString()}</strong><small>Reports in the high-probability band</small></div><div className="kpi-card review"><span>🟡 Awaiting review</span><strong>{Number(k.awaiting_review||queue.length||0).toLocaleString()}</strong><small>Require human validation</small></div><div className="kpi-card good"><span>🟢 System reports</span><strong>{Number(k.total_reports||0).toLocaleString()}</strong><small>Total reports in the dataset</small></div></div>

  <Panel title="⚠️ HSE priority queue" subtitle="Start with the highest-risk items. AI screening is a triage aid, not the final decision.">
   <div className="filter-pills"><button className={filter==='attention'?'active':''} onClick={()=>setFilter('attention')}>Needs attention</button><button className={filter==='critical'?'active':''} onClick={()=>setFilter('critical')}>Critical / SIF</button><button className={filter==='all'?'active':''} onClick={()=>setFilter('all')}>All queued</button></div>
   <div className="hse-queue">{shown.length?shown.map((r,i)=><button className="hse-row" key={r.report_id||i} onClick={()=>onNavigate?.('reports',r.report_id)}><div className="priority-marker">{String(r.sif_prediction||'').toLowerCase().includes('sif')?'🔴':'🟡'}</div><div><strong>{r.report_id||'Report'}</strong><span>{r.activity_group||'Activity not specified'} · {r.life_saving_rule||'Rule not mapped'}</span><p>{r.report_text||'No narrative available.'}</p></div><Chip tone={String(r.sif_prediction||'').toLowerCase().includes('sif')?'red':'amber'}>{r.hse_review_status||'Pending'}</Chip><span className="row-arrow">→</span></button>):<div className="empty-state">No reports are currently shown.</div>}</div>
   <button className="btn-secondary full-action" onClick={()=>onNavigate?.('reports')}>View full review queue →</button>
  </Panel>

  <Panel title="📊 HSE density matrix" subtitle="A compact view of where review-queue activity and Life-Saving Rule associations concentrate. Click a cell to inspect the corresponding report set.">
   <div className="density-head"><div><span className="eyebrow">REVIEW-QUEUE CONCENTRATION</span><strong>{density?Number(density.total_associations||0).toLocaleString():'—'} rule associations</strong><small>{density?.note||'Loading density data…'}</small></div><div className="density-toggle"><button className={densityMode==='sif'?'active':''} onClick={()=>setDensityMode('sif')}>SIF Density</button><button className={densityMode==='volume'?'active':''} onClick={()=>setDensityMode('volume')}>Report Volume</button></div></div>
   <div className="density-matrix-wrap">
    {density?.activities?.length? <div className="density-matrix" style={{'--cols':density.rules.length}}>
      <div className="density-corner"><span>Activity × rule</span></div>
      {density.rules.map(r=><div className="density-col-label" key={r.name}>{r.name}</div>)}
      {density.activities.map(a=>{
       const cells=density.rules.map(r=>{
        const c=density.cells.find(x=>x.activity===a.name&&x.rule===r.name)||{total:0,sif:0,density:0};
        const value=densityMode==='sif'?Number(c.density||0):Number(c.total||0);
        const max=densityMode==='sif'?100:maxTotal;
        const heat=densityMode==='sif'?Math.min(1,value/100):Math.min(1,value/maxTotal);
        return {rule:r,c,value,max,heat};
       });
       return <React.Fragment key={a.name}>
        <div className="density-row-label"><strong>{a.name}</strong><small>{Number(a.total||0).toLocaleString()} associations</small></div>
        {cells.map(({rule:r,c,value,max,heat})=><button key={`${a.name}-${r.name}`} className={`density-cell ${densityTone(value,max)}`} style={{'--heat':String(heat)}} onClick={()=>{setSelectedCell({activity:a.name,rule:r.name});onNavigate?.('reports',a.name)}} title={`${a.name} · ${r.name}: ${c.sif} SIF / ${c.total} associations`}>
         <strong>{densityMode==='sif'?`${Number(c.density||0).toFixed(1)}%`:Number(c.total||0).toLocaleString()}</strong>
         <small>{Number(c.sif||0).toLocaleString()} SIF</small>
        </button>)}
       </React.Fragment>;
      })}
      <div className="density-legend"><span>Lower</span><i className="density-swatch low"/><i className="density-swatch medium"/><i className="density-swatch high"/><i className="density-swatch critical"/><span>Higher</span></div>
    </div> : <div className="empty-state">Density data is not available yet.</div>}
   </div>
   {selectedInfo&&<div className="density-focus"><div><span>Selected concentration</span><strong>{selectedInfo.activity}</strong><small>{selectedInfo.rule}</small></div><div><span>SIF associations</span><strong>{selectedInfo.sif}</strong></div><div><span>Total associations</span><strong>{selectedInfo.total}</strong></div><div><span>SIF density</span><strong>{selectedInfo.density.toFixed(1)}%</strong></div><button className="btn-secondary compact" onClick={()=>onNavigate?.('reports',selectedInfo.activity)}>Open related reports →</button></div>}
  </Panel>

  <Panel title="🧭 Recommended HSE workflow" subtitle="A simple sequence for consistent human validation."><div className="workflow-grid"><div><b>1</b><strong>Review the narrative</strong><span>Understand what actually happened.</span></div><div><b>2</b><strong>Check the AI reason</strong><span>Use the SIF result and Life-Saving Rule as screening evidence.</span></div><div><b>3</b><strong>Validate on site</strong><span>Confirm the physical barrier and work controls.</span></div><div><b>4</b><strong>Record the action</strong><span>Confirm SIF status and document corrective action.</span></div></div></Panel>
 </div>
}
