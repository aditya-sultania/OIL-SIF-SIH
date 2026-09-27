"""
styles.py
---------
Centralized visual design system for the OIL SIF Precursor Intelligence
Platform. Restrained industrial/enterprise palette — risk colors are used
purposefully (see COLORS below), never decoratively.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# COLOR SYSTEM — semantic, not decorative
# ---------------------------------------------------------------------------
COLORS = {
    "bg": "#0B1220",
    "bg_panel": "#111A2C",
    "bg_panel_alt": "#0E1727",
    "border": "#22304A",
    "border_soft": "#1A2740",
    "text_primary": "#E7ECF4",
    "text_secondary": "#93A1B8",
    "text_muted": "#5D6B85",
    "accent": "#2F7DE1",          # neutral / informational blue
    "accent_soft": "#173252",
    "critical": "#E5484D",        # high SIF risk
    "critical_soft": "#3A1518",
    "elevated": "#F2994A",        # medium risk
    "elevated_soft": "#3A2410",
    "controlled": "#3DBE7A",      # low risk / controlled
    "controlled_soft": "#123321",
    "warning": "#E9C46A",         # emerging trend / warning
    "warning_soft": "#332B10",
}


def inject_css():
    c = COLORS
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .stApp {{
            background: {c['bg']};
            color: {c['text_primary']};
        }}

        section[data-testid="stSidebar"] {{
            background: {c['bg_panel_alt']};
            border-right: 1px solid {c['border']};
        }}
        section[data-testid="stSidebar"] .stRadio label {{
            font-size: 0.92rem;
        }}

        #MainMenu, footer, header[data-testid="stHeader"] {{
            visibility: hidden;
            height: 0;
        }}

        .block-container {{
            padding-top: 1.6rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }}

        h1, h2, h3, h4 {{
            font-family: 'Inter', sans-serif;
            color: {c['text_primary']};
            letter-spacing: -0.01em;
        }}

        /* ---------- Header block ---------- */
        .app-header-title {{
            font-size: 1.9rem;
            font-weight: 800;
            margin-bottom: 0.15rem;
            color: {c['text_primary']};
        }}
        .app-header-subtitle {{
            font-size: 0.98rem;
            color: {c['text_secondary']};
            margin-bottom: 1.4rem;
            font-weight: 400;
        }}

        /* ---------- Section headers ---------- */
        .section-heading {{
            font-size: 1.05rem;
            font-weight: 700;
            color: {c['text_primary']};
            margin: 1.6rem 0 0.7rem 0;
            padding-bottom: 0.4rem;
            border-bottom: 1px solid {c['border']};
        }}
        .section-subtext {{
            font-size: 0.85rem;
            color: {c['text_secondary']};
            margin-top: -0.5rem;
            margin-bottom: 0.8rem;
        }}

        /* ---------- KPI cards ---------- */
        .kpi-card {{
            background: {c['bg_panel']};
            border: 1px solid {c['border']};
            border-radius: 10px;
            padding: 1.05rem 1.2rem;
            height: 100%;
        }}
        .kpi-label {{
            font-size: 0.76rem;
            font-weight: 600;
            color: {c['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.45rem;
        }}
        .kpi-value {{
            font-size: 1.9rem;
            font-weight: 800;
            font-family: 'IBM Plex Mono', monospace;
            color: {c['text_primary']};
            line-height: 1.1;
        }}
        .kpi-desc {{
            font-size: 0.78rem;
            color: {c['text_muted']};
            margin-top: 0.3rem;
        }}
        .kpi-trend {{
            font-size: 0.78rem;
            font-weight: 600;
            margin-top: 0.5rem;
            display: inline-block;
        }}

        /* ---------- Badges ---------- */
        .badge {{
            display: inline-block;
            padding: 0.16rem 0.6rem;
            border-radius: 5px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }}
        .badge-critical {{ background: {c['critical_soft']}; color: {c['critical']}; border: 1px solid {c['critical']}55; }}
        .badge-elevated {{ background: {c['elevated_soft']}; color: {c['elevated']}; border: 1px solid {c['elevated']}55; }}
        .badge-controlled {{ background: {c['controlled_soft']}; color: {c['controlled']}; border: 1px solid {c['controlled']}55; }}
        .badge-info {{ background: {c['accent_soft']}; color: {c['accent']}; border: 1px solid {c['accent']}55; }}
        .badge-warning {{ background: {c['warning_soft']}; color: {c['warning']}; border: 1px solid {c['warning']}55; }}
        .badge-neutral {{ background: {c['bg_panel_alt']}; color: {c['text_secondary']}; border: 1px solid {c['border']}; }}

        /* ---------- Generic panel/card ---------- */
        .panel {{
            background: {c['bg_panel']};
            border: 1px solid {c['border']};
            border-radius: 10px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.9rem;
        }}
        .panel-tight {{
            background: {c['bg_panel']};
            border: 1px solid {c['border']};
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.6rem;
        }}

        /* ---------- Precursor / list rows ---------- */
        .precursor-row {{
            background: {c['bg_panel']};
            border: 1px solid {c['border']};
            border-left: 3px solid {c['critical']};
            border-radius: 8px;
            padding: 0.85rem 1.1rem;
            margin-bottom: 0.6rem;
        }}
        .precursor-row.medium {{ border-left-color: {c['elevated']}; }}
        .precursor-row.low {{ border-left-color: {c['controlled']}; }}
        .precursor-title {{
            font-weight: 700;
            font-size: 0.94rem;
            color: {c['text_primary']};
            margin-bottom: 0.25rem;
        }}
        .precursor-meta {{
            font-size: 0.8rem;
            color: {c['text_secondary']};
        }}

        /* ---------- Reasoning flow ---------- */
        .flow-step {{
            background: {c['bg_panel']};
            border: 1px solid {c['border']};
            border-radius: 8px;
            padding: 0.7rem 1rem;
            text-align: center;
            font-size: 0.86rem;
            font-weight: 600;
            color: {c['text_primary']};
        }}
        .flow-step-sub {{
            font-size: 0.74rem;
            font-weight: 400;
            color: {c['text_secondary']};
            margin-top: 0.2rem;
        }}
        .flow-arrow {{
            text-align: center;
            color: {c['text_muted']};
            font-size: 1.1rem;
            padding: 0.1rem 0;
        }}

        /* ---------- Alert box (emerging risk) ---------- */
        .alert-box {{
            background: {c['warning_soft']};
            border: 1px solid {c['warning']}66;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
        }}
        .alert-title {{
            font-weight: 700;
            color: {c['warning']};
            font-size: 0.95rem;
            margin-bottom: 0.3rem;
        }}
        .alert-text {{
            color: {c['text_primary']};
            font-size: 0.88rem;
        }}

        /* ---------- AI analysis banner ---------- */
        .ai-note {{
            font-size: 0.78rem;
            color: {c['text_muted']};
            font-style: italic;
            margin-top: 0.4rem;
        }}

        /* ---------- Sidebar footer ---------- */
        .sidebar-footer {{
            position: fixed;
            bottom: 0;
            padding: 1rem 1.3rem 1.3rem 1.3rem;
            font-size: 0.76rem;
            color: {c['text_muted']};
            border-top: 1px solid {c['border']};
            width: 100%;
        }}
        .status-dot {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: {c['controlled']};
            margin-right: 5px;
        }}

        /* ---------- Streamlit widget overrides ---------- */
        div[data-testid="stMetric"] {{
            background: {c['bg_panel']};
            border: 1px solid {c['border']};
            border-radius: 10px;
            padding: 0.8rem 1rem;
        }}
        .stButton button {{
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        div[data-testid="stDataFrame"] {{
            border: 1px solid {c['border']};
            border-radius: 8px;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {c['bg_panel']};
            border-radius: 6px 6px 0 0;
            padding: 0.4rem 1rem;
        }}
        hr {{
            border-color: {c['border']};
        }}
    </style>
    """, unsafe_allow_html=True)


def risk_badge(band: str) -> str:
    """Returns HTML for a risk badge given a band string (High/Medium/Low)."""
    band = (band or "").lower()
    if band == "high":
        return f'<span class="badge badge-critical">High SIF Risk</span>'
    elif band == "medium":
        return f'<span class="badge badge-elevated">Medium SIF Risk</span>'
    else:
        return f'<span class="badge badge-controlled">Low SIF Risk</span>'


def status_badge(status: str) -> str:
    status_map = {
        "Pending": "badge-warning",
        "Confirmed": "badge-controlled",
        "Corrected": "badge-info",
        "Rejected": "badge-neutral",
    }
    cls = status_map.get(status, "badge-neutral")
    return f'<span class="badge {cls}">{status}</span>'


def priority_badge(priority: str) -> str:
    priority_map = {
        "Critical": "badge-critical",
        "Elevated": "badge-elevated",
        "Monitor": "badge-controlled",
    }
    cls = priority_map.get(priority, "badge-neutral")
    return f'<span class="badge {cls}">{priority}</span>'
