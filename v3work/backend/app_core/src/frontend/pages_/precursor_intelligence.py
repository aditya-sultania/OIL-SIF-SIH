import streamlit as st

from src.frontend import data_api, charts
from src.frontend.components import page_header, section_heading, precursor_card, alert_box
from src.frontend.styles import COLORS


def render():
    page_header(
        "Recurring SIF Precursor Intelligence",
        "Recurring precursor patterns discovered from safety reports",
    )

    df = data_api.get_reports()
    precursors = data_api.get_precursor_patterns()

    section_heading("Ranked Precursor Patterns", "Activity + Hazard + Barrier-Failure combinations, ranked by frequency")

    for _, row in precursors.head(10).iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            precursor_card(row["pattern"], row["frequency"], row["risk_density"], row["trend_pct"])
        with col2:
            st.markdown(f"""
                <div class="panel-tight" style="text-align:center;">
                    <div class="kpi-label">Avg SIF</div>
                    <div style="font-weight:800; font-size:1.1rem; color:{COLORS['text_primary']};">{row['avg_sif']:.0f}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    section_heading("Emerging Risk Detection", "Statistically significant upward trends in precursor frequency")

    emerging = precursors[precursors["trend_pct"] >= 25].sort_values("trend_pct", ascending=False)

    if len(emerging) == 0:
        st.info("No emerging precursor trends exceeding the +25% threshold in the current period.")
    else:
        top = emerging.iloc[0]
        alert_box(
            "Emerging SIF Precursor",
            f"<b>{top['hazard']}</b> related precursors increased "
            f"<b>{top['trend_pct']:.0f}%</b> over the last period, concentrated in "
            f"<b>{top['activity']}</b> activities. Rule affected: <b>{top['rule']}</b>.",
        )

        site_options = sorted(df["site"].unique())
        default_site = "Baghjan EPS" if "Baghjan EPS" in site_options else site_options[0]
        col1, col2 = st.columns(2)
        with col1:
            site_filter = st.selectbox("Site", site_options, index=site_options.index(default_site))
        with col2:
            hazard_filter = st.selectbox("Hazard", sorted(df["hazard"].unique()),
                                          index=sorted(df["hazard"].unique()).index(top["hazard"]) if top["hazard"] in df["hazard"].unique() else 0)

        st.plotly_chart(
            charts.precursor_trend_chart(df, site=site_filter, hazard=hazard_filter),
            use_container_width=True, config={"displayModeBar": False},
        )
        st.caption(f"Weekly report frequency — {hazard_filter} at {site_filter}")

        st.markdown("##### Other emerging patterns")
        other_cols = st.columns(min(3, max(1, len(emerging) - 1))) if len(emerging) > 1 else None
        for i, (_, row) in enumerate(emerging.iloc[1:4].iterrows()):
            with (other_cols[i] if other_cols else st.container()):
                st.markdown(f"""
                    <div class="panel-tight">
                        <div style="font-size:0.82rem; font-weight:700;">{row['hazard']}</div>
                        <div style="font-size:0.78rem; color:{COLORS['text_secondary']};">{row['activity']}</div>
                        <div style="color:{COLORS['critical']}; font-weight:700; margin-top:0.3rem;">↑ {row['trend_pct']:.0f}%</div>
                    </div>
                """, unsafe_allow_html=True)
