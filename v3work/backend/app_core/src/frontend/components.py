"""
components.py
-------------
Reusable UI building blocks shared across pages.
"""

import streamlit as st
from src.frontend.styles import COLORS, risk_badge, status_badge, priority_badge


def page_header(title, subtitle=None):
    st.markdown(f'<div class="app-header-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="app-header-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def section_heading(title, subtext=None):
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
    if subtext:
        st.markdown(f'<div class="section-subtext">{subtext}</div>', unsafe_allow_html=True)


def kpi_card(label, value, desc=None, trend=None, trend_positive_is_bad=True):
    """
    trend: numeric percentage change, e.g. +12.4 or -6.1 (string or float ok)
    trend_positive_is_bad: for safety metrics, a rising number is often bad (more high-risk reports),
    so color logic is inverted by default.
    """
    trend_html = ""
    if trend is not None:
        try:
            trend_val = float(trend)
        except (TypeError, ValueError):
            trend_val = 0
        is_bad = (trend_val > 0) if trend_positive_is_bad else (trend_val < 0)
        color = COLORS["critical"] if is_bad and trend_val != 0 else (
            COLORS["controlled"] if trend_val != 0 else COLORS["text_muted"]
        )
        arrow = "▲" if trend_val > 0 else ("▼" if trend_val < 0 else "—")
        trend_html = f'<div class="kpi-trend" style="color:{color};">{arrow} {abs(trend_val):.1f}% vs prior period</div>'

    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {f'<div class="kpi-desc">{desc}</div>' if desc else ''}
            {trend_html}
        </div>
    """, unsafe_allow_html=True)


def precursor_card(title, frequency, risk_density, trend_pct):
    density_class = "low"
    if str(risk_density).lower() == "high":
        density_class = ""  # default red border
    elif str(risk_density).lower() == "medium":
        density_class = "medium"

    trend_html = ""
    if trend_pct is not None:
        color = COLORS["critical"] if trend_pct > 0 else COLORS["controlled"]
        arrow = "↑" if trend_pct > 0 else ("↓" if trend_pct < 0 else "→")
        trend_html = f'<span style="color:{color}; font-weight:700;">{arrow} {abs(trend_pct):.0f}% vs previous period</span>'

    st.markdown(f"""
        <div class="precursor-row {density_class}">
            <div class="precursor-title">{title}</div>
            <div class="precursor-meta">{frequency} reports &nbsp;•&nbsp; {risk_density} SIF density
            {' &nbsp;•&nbsp; ' + trend_html if trend_html else ''}
            </div>
        </div>
    """, unsafe_allow_html=True)


def reasoning_flow(steps):
    """
    steps: list of (title, subtitle) tuples, rendered top-to-bottom with arrows.
    """
    for i, (title, subtitle) in enumerate(steps):
        st.markdown(f"""
            <div class="flow-step">{title}
                <div class="flow-step-sub">{subtitle}</div>
            </div>
        """, unsafe_allow_html=True)
        if i < len(steps) - 1:
            st.markdown('<div class="flow-arrow">↓</div>', unsafe_allow_html=True)


def alert_box(title, text):
    st.markdown(f"""
        <div class="alert-box">
            <div class="alert-title">🚨 {title}</div>
            <div class="alert-text">{text}</div>
        </div>
    """, unsafe_allow_html=True)


def ai_analysis_panel(result):
    """Renders the full AI analysis result for a single report."""
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown(f"""
            <div class="panel">
                <div class="kpi-label">AI-Assessed SIF Potential</div>
                <div class="kpi-value">{result['sif_potential']:.0f}%</div>
                <div style="margin-top:0.5rem;">{risk_badge(result['sif_band'])}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="panel">
                <div class="kpi-label">Model Confidence</div>
                <div class="kpi-value">{result['model_confidence']:.0f}%</div>
                <div class="ai-note">Requires HSE validation</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="panel">
                <div class="kpi-label">Why is this report considered high risk?</div>
                <div style="font-size:0.92rem; color:{COLORS['text_primary']}; margin-top:0.3rem;">
                    {result['why_high_risk']}
                </div>
            </div>
        """, unsafe_allow_html=True)

    section_heading("Structured Extraction", "AI-suggested classification — pending HSE review")
    c1, c2, c3 = st.columns(3)
    fields_left = [("Report Type", result["report_type"]), ("Activity", result["activity"]), ("Location", result["location"])]
    fields_mid = [("Hazard", result["hazard"]), ("Life-Saving Rule", result["life_saving_rule"]), ("Critical Barrier", result["critical_barrier"])]
    fields_right = [("Barrier Failure", result["barrier_failure"]), ("Potential Consequence", result["potential_consequence"])]

    def render_fields(col, fields):
        with col:
            for label, val in fields:
                st.markdown(f"""
                    <div class="panel-tight">
                        <div class="kpi-label">{label}</div>
                        <div style="font-size:0.95rem; font-weight:600; color:{COLORS['text_primary']};">{val}</div>
                    </div>
                """, unsafe_allow_html=True)

    render_fields(c1, fields_left)
    render_fields(c2, fields_mid)
    render_fields(c3, fields_right)

    section_heading("Reasoning Flow")
    reasoning_flow([
        ("REPORT", "Raw safety report text"),
        ("HAZARD", result["hazard"]),
        ("BARRIER", result["critical_barrier"]),
        ("BARRIER FAILURE", result["barrier_failure"]),
        ("EXPOSURE", f"{result['activity']} at {result['location']}"),
        ("POTENTIAL CONSEQUENCE", result["potential_consequence"]),
    ])


def report_row_html(report):
    """Compact single-row summary used in tables/lists outside st.dataframe."""
    return f"""
        <div class="panel-tight" style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <b>{report['report_id']}</b> &nbsp;·&nbsp; {report['site']} &nbsp;·&nbsp; {report['activity']}
            </div>
            <div>{risk_badge(report['sif_band'])} {status_badge(report['review_status'])}</div>
        </div>
    """


def sidebar_footer():
    st.markdown(f"""
        <div class="sidebar-footer">
            <div style="font-weight:700; color:{COLORS['text_primary']}; font-size:0.85rem;">OIL SIF Intelligence</div>
            <div>AI-assisted HSE platform</div>
            <div style="margin-top:0.4rem;"><span class="status-dot"></span>System operational · Mock data mode</div>
        </div>
    """, unsafe_allow_html=True)
