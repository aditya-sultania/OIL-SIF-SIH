import streamlit as st

from src.frontend import data_api, charts
from src.frontend.components import page_header, section_heading, reasoning_flow
from src.frontend.styles import COLORS


def render():
    page_header("Barrier Analysis", "Where safety-critical barriers are failing, and what follows when they do")

    barrier_df = data_api.get_barrier_failures()

    section_heading("Hazard → Barrier → Failure → Consequence", "Illustrative chain for the top failing barrier")
    top = barrier_df.iloc[0]
    df = data_api.get_reports()
    matching = df[df["critical_barrier"] == top["critical_barrier"]].iloc[0]

    reasoning_flow([
        (matching["hazard"], "Hazard present"),
        (top["critical_barrier"], "Required barrier"),
        ("Barrier Status: Failed", f"{top['occurrences']} occurrences in dataset"),
        (matching["barrier_failure"], "Observed failure mode"),
        (matching["potential_consequence"], "Potential consequence"),
    ])

    st.markdown("---")
    section_heading("Top Failed Barriers", "Ranked by number of occurrences across all reports")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(charts.barrier_failure_bar(barrier_df), use_container_width=True, config={"displayModeBar": False})
    with col2:
        for _, row in barrier_df.head(5).iterrows():
            trend_color = COLORS["critical"] if row["trend_pct"] > 0 else COLORS["controlled"]
            arrow = "↑" if row["trend_pct"] > 0 else "↓"
            st.markdown(f"""
                <div class="panel-tight">
                    <div style="font-weight:700; font-size:0.9rem;">{row['critical_barrier']}</div>
                    <div style="font-size:0.78rem; color:{COLORS['text_secondary']}; margin-top:0.2rem;">
                        {int(row['occurrences'])} occurrences &nbsp;•&nbsp; {row['pct_of_high_risk']:.0f}% of all reports
                    </div>
                    <div style="font-size:0.78rem; margin-top:0.3rem;">
                        Top activity: <b>{row['top_activity']}</b> &nbsp;·&nbsp; Top site: <b>{row['top_site']}</b>
                    </div>
                    <div style="color:{trend_color}; font-weight:700; font-size:0.8rem; margin-top:0.3rem;">
                        {arrow} {abs(row['trend_pct']):.0f}% trend
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    section_heading("Barrier Failure Relationship View", "Barriers linked to the activities and hazards they most commonly co-occur with")

    selected_barrier = st.selectbox("Select a barrier", barrier_df["critical_barrier"].tolist())
    subset = df[df["critical_barrier"] == selected_barrier]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Linked Hazards**")
        for hz, cnt in subset["hazard"].value_counts().head(4).items():
            st.markdown(f"- {hz} ({cnt})")
    with c2:
        st.markdown("**Linked Activities**")
        for act, cnt in subset["activity"].value_counts().head(4).items():
            st.markdown(f"- {act} ({cnt})")
    with c3:
        st.markdown("**Linked Sites**")
        for site, cnt in subset["site"].value_counts().head(4).items():
            st.markdown(f"- {site} ({cnt})")
