import React from 'react'
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell } from 'recharts'

const CHART_COLORS = ['#2563eb','#f59e0b','#dc2626','#0f766e','#7c3aed','#475569']
const FALLBACK = { kpis: { total_reports: 366630, sif_potential: 8585, high_probability: 654, awaiting_review: 10000 }, sif_distribution: [{ band: 'Low SIF probability', count: 357391 }, { band: 'Review zone', count: 10185 }, { band: 'High SIF probability', count: 654 }], sif_trend: [], precursors: [] }
function tr(T, key, fallback) { return T?.[key] || fallback }
function KpiCard({ title, value, subtitle, tone }) { return <div className={`deck-card kpi-card kpi-${tone}`}><div className="kpi-title">{title}</div><div className="kpi-value">{Number(value ?? 0).toLocaleString()}</div><div className="kpi-subtitle">{subtitle}</div></div> }
function SectionHeader({ title, subtitle }) { return <div className="section-header"><h2>{title}</h2><p>{subtitle}</p></div> }

export default function Overview({ T, data, loading, onNavigate }) {
  if (loading) return <div className="loading-state"><div className="loading-spinner" aria-hidden="true" /><strong>{tr(T,'loading_overview','Loading safety overview…')}</strong><p>{tr(T,'loading_overview_text','Preparing the latest summary. This should only take a moment.')}</p></div>
  const d = data || FALLBACK
  const pieData = (d.sif_distribution || []).map(item => ({ name: item.band, value: item.count }))
  const total = Number(d.kpis?.total_reports || 0)
  const high = Number(d.kpis?.high_probability || 0)
  const pending = Number(d.kpis?.awaiting_review || 0)
  const highPct = total ? ((high / total) * 100).toFixed(2) : '0.00'

  return <div className="page-content overview-page">
    <div className="overview-welcome"><div><div className="eyebrow">{tr(T,'safety_intelligence','SAFETY INTELLIGENCE')}</div><h1>{tr(T, 'overview_title', 'OIL-SIF Precursor Intelligence')}</h1><p>{tr(T, 'overview_subtitle', 'A clear view of where serious injury and fatality potential requires attention.')}</p></div><div className="overview-updated"><span className="status-dot" />{tr(T,'data_ready','Data ready')}<small>{tr(T,'review_before_action','Review before operational action')}</small></div></div>

    <div className="quick-actions" aria-label={tr(T,'quick_actions','Quick actions')}>
      <button onClick={() => onNavigate?.('reports')}><span>📋</span><div><strong>{tr(T,'quick_review','Review reports')}</strong><small>{tr(T,'quick_review_help','Find and review safety reports')}</small></div><b>→</b></button>
      <button onClick={() => onNavigate?.('intelligence')}><span>📊</span><div><strong>{tr(T,'quick_intelligence','View risk patterns')}</strong><small>{tr(T,'quick_intelligence_help','See precursors and barriers')}</small></div><b>→</b></button>
      <button onClick={() => onNavigate?.('copilot')}><span>💬</span><div><strong>{tr(T,'quick_assistant','Ask Safety Assistant')}</strong><small>{tr(T,'quick_assistant_help','Ask a question in plain language')}</small></div><b>→</b></button>
    </div>

    <div className="kpi-grid">
      <KpiCard tone="neutral" title={tr(T,'total_reports','Total Reports')} value={d.kpis?.total_reports} subtitle={tr(T,'all_safety_reports','All safety reports in the system')} />
      <KpiCard tone="amber" title={tr(T,'sif_potential','SIF Potential')} value={d.kpis?.sif_potential} subtitle={tr(T,'sif_potential_reports','Reports flagged as SIF potential')} />
      <KpiCard tone="red" title={tr(T,'high_sif_probability','High SIF Probability')} value={d.kpis?.high_probability} subtitle={`${highPct}% ${tr(T,'of_all_reports','of all reports')}`} />
      <KpiCard tone="blue" title={tr(T,'awaiting_hse_review','Awaiting HSE Review')} value={pending} subtitle={tr(T,'pending_human_validation','Reports pending human validation')} />
    </div>

    <div className="attention-strip"><div><strong>⚠️ {tr(T,'attention_needed','Where to focus')}</strong><span>{high.toLocaleString()} {tr(T,'high_probability_reports','reports are in the high-probability band')}.</span></div><button className="btn-secondary" onClick={() => onNavigate?.('reports')}>{tr(T,'review_high_risk','Review high-risk reports')}</button></div>

    <SectionHeader title={tr(T,'sif_risk_overview','SIF Risk Overview')} subtitle={tr(T,'distribution_trend','Distribution and trend of SIF potential across all reports')} />
    <div className="dashboard-two-column">
      <div className="deck-card chart-card"><h3>{tr(T,'sif_probability_distribution','SIF Probability Distribution')}</h3><div className="chart-container"><ResponsiveContainer width="100%" height={280}><PieChart><Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={72} outerRadius={104} paddingAngle={3}>{pieData.map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} stroke="#ffffff" strokeWidth={2} />)}</Pie><Tooltip formatter={value => Number(value).toLocaleString()} /></PieChart></ResponsiveContainer></div><div className="chart-legend">{d.sif_distribution?.map(item => <div className="legend-item" key={item.band}><span className="legend-swatch" style={{background:CHART_COLORS[d.sif_distribution.indexOf(item)%CHART_COLORS.length]}} /><span className="legend-label">{item.band}</span><strong>{Number(item.count).toLocaleString()}</strong></div>)}</div></div>
      <div className="deck-card chart-card"><h3>{tr(T,'sif_probability_trend','SIF Probability Trend')}</h3>{d.sif_trend?.length ? <div className="chart-container"><ResponsiveContainer width="100%" height={320}><AreaChart data={d.sif_trend}><CartesianGrid stroke="#d7e0e7" strokeDasharray="3 3" /><XAxis dataKey="date" tick={{ fontSize: 11 }} interval="preserveStartEnd" /><YAxis tick={{ fontSize: 11 }} /><Tooltip /><Area type="monotone" dataKey="low" name={tr(T,'low_sif_probability','Low SIF probability')} stackId="1" fill={CHART_COLORS[0]} stroke={CHART_COLORS[0]} fillOpacity={0.45} /><Area type="monotone" dataKey="review" name={tr(T,'review_zone','Review zone')} stackId="1" fill={CHART_COLORS[1]} stroke={CHART_COLORS[1]} fillOpacity={0.62} /><Area type="monotone" dataKey="high" name={tr(T,'high_probability_band','High SIF probability')} stackId="1" fill={CHART_COLORS[2]} stroke={CHART_COLORS[2]} fillOpacity={0.82} /></AreaChart></ResponsiveContainer></div> : <div className="empty-chart"><strong>{tr(T,'trend_available','Trend information is available when dated records are present.')}</strong><p>{tr(T,'trend_tip','Use Report Analysis to investigate individual records and current risk status.')}</p><button className="btn-secondary" onClick={() => onNavigate?.('reports')}>{tr(T,'open_reports','Open reports')}</button></div>}</div>
    </div>

    <SectionHeader title={tr(T,'top_recurring_precursors','Top Recurring Precursors')} subtitle={tr(T,'recurring_patterns','Recurring activity, hazard and barrier-failure patterns')} />
    <div className="precursor-grid">{(d.precursors || []).map((item, index) => <div className="deck-card precursor-card" key={item.precursor || index}><div className="precursor-rank">#{item.rank ?? index + 1}</div><div className="precursor-content"><h3>{item.precursor}</h3><div className="precursor-stats"><div><span>{tr(T,'reports','Reports')}</span><strong>{Number(item.total_reports || 0).toLocaleString()}</strong></div><div><span>{tr(T,'sif_reports','SIF Reports')}</span><strong>{Number(item.sif_reports || 0).toLocaleString()}</strong></div><div><span>{tr(T,'sif_density','SIF Density')}</span><strong>{Number(item.sif_density_pct || 0).toFixed(1)}%</strong></div></div></div></div>)}</div>
  </div>
}
