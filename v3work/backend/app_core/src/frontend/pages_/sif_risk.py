import streamlit as st

from src.frontend import data_api, charts
from src.frontend.components import page_header, section_heading, ai_analysis_panel
from src.frontend.styles import risk_badge, status_badge


def render():
    page_header("SIF Risk Analytics", "Detailed serious injury / fatality potential analysis across all reports")

    df = data_api.get_reports()

    section_heading("Risk Distribution & Trend")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.plotly_chart(charts.sif_distribution_donut(df), use_container_width=True, config={"displayModeBar": False})
    with c2:
        st.plotly_chart(charts.sif_trend_chart(df), use_container_width=True, config={"displayModeBar": False})

    section_heading("Risk by Dimension")
    tab1, tab2, tab3, tab4 = st.tabs(["By Report Type", "By Activity", "By Site", "By Hazard"])
    with tab1:
        st.plotly_chart(charts.report_volume_by_type(df), use_container_width=True, config={"displayModeBar": False})
    with tab2:
        st.plotly_chart(charts.risk_by_category_bar(df, "activity"), use_container_width=True, config={"displayModeBar": False})
    with tab3:
        st.plotly_chart(charts.risk_by_category_bar(df, "site"), use_container_width=True, config={"displayModeBar": False})
    with tab4:
        st.plotly_chart(charts.risk_by_category_bar(df, "hazard"), use_container_width=True, config={"displayModeBar": False})

    section_heading("High Risk Reports", "Select a report to view its full AI analysis")
    high_risk = df[df["sif_band"] == "High"].sort_values("sif_score", ascending=False)
    display = high_risk[["report_id", "site", "activity", "sif_score", "hazard", "life_saving_rule", "review_status"]].head(30).copy()
    display.columns = ["Report ID", "Site", "Activity", "SIF Score", "Main Hazard", "Life-Saving Rule", "Status"]

    st.dataframe(display, use_container_width=True, hide_index=True, height=320)

    st.caption("Select a report ID below to open its detailed AI analysis.")
    selected_id = st.selectbox("Open report", ["—"] + display["Report ID"].tolist())
    if selected_id != "—":
        row = df[df["report_id"] == selected_id].iloc[0]
        result = {
            "sif_potential": row["sif_score"],
            "sif_band": row["sif_band"],
            "model_confidence": 88.0,
            "report_type": row["report_type"],
            "activity": row["activity"],
            "location": row["site"],
            "hazard": row["hazard"],
            "life_saving_rule": row["life_saving_rule"],
            "critical_barrier": row["critical_barrier"],
            "barrier_failure": row["barrier_failure"],
            "potential_consequence": row["potential_consequence"],
            "why_high_risk": (
                f"Report describes exposure to {row['hazard'].lower()} where the required control "
                f"({row['critical_barrier'].lower()}) was reported as ineffective or absent."
            ),
        }
        st.markdown("---")
        section_heading(f"Detailed Analysis — {selected_id}")
        ai_analysis_panel(result)
