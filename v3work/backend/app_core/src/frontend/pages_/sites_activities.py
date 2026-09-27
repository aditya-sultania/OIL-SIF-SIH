import streamlit as st

from src.frontend import data_api, charts
from src.frontend.components import page_header, section_heading
from src.frontend.styles import priority_badge


def render():
    page_header("Sites & Activities", "Site-level and activity-level safety intelligence")

    site_risk = data_api.get_site_risk()

    section_heading("Site Risk Ranking")
    display = site_risk.copy()
    display["risk_score"] = display["risk_score"].round(0).astype(int)
    display["emerging_trend_pct"] = display["emerging_trend_pct"].round(0)
    table = display[["site", "total_reports", "high_sif", "risk_score", "emerging_trend_pct", "priority"]].copy()
    table.columns = ["Site", "Total Reports", "High SIF", "Risk Score", "Emerging Trend %", "Priority"]
    st.dataframe(table, use_container_width=True, hide_index=True, height=320)

    st.plotly_chart(charts.site_risk_scatter(site_risk), use_container_width=True, config={"displayModeBar": False})
    st.caption("Bubble size reflects number of high-SIF reports at each site.")

    st.markdown("---")
    section_heading("Site Detail", "Select a site to view its full risk profile")
    selected_site = st.selectbox("Site", site_risk["site"].tolist())
    detail = data_api.get_site_detail(selected_site)
    site_row = site_risk[site_risk["site"] == selected_site].iloc[0]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Reports", int(site_row["total_reports"]))
    c2.metric("Risk Score", f"{site_row['risk_score']:.0f}")
    c3.markdown(f"<div style='padding-top:0.6rem;'>{priority_badge(site_row['priority'])}</div>", unsafe_allow_html=True)

    st.plotly_chart(charts.site_sif_trend(detail["df"]), use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Average SIF score trend at {selected_site}")

    c4, c5, c6, c7 = st.columns(4)
    with c4:
        st.markdown("**Top Activities**")
        for k, v in detail["top_activities"].items():
            st.markdown(f"- {k} ({v})")
    with c5:
        st.markdown("**Top Hazards**")
        for k, v in detail["top_hazards"].items():
            st.markdown(f"- {k} ({v})")
    with c6:
        st.markdown("**Top Life-Saving Rules**")
        for k, v in detail["top_rules"].items():
            st.markdown(f"- {k} ({v})")
    with c7:
        st.markdown("**Recurring Barrier Failures**")
        for k, v in detail["top_failures"].items():
            st.markdown(f"- {k} ({v})")

    st.markdown("---")
    section_heading("Activity Ranking", "Report volume by activity type, across all sites")
    df = data_api.get_reports()
    st.plotly_chart(charts.activity_ranking_bar(df), use_container_width=True, config={"displayModeBar": False})
