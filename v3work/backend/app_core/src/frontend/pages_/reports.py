import streamlit as st
import pandas as pd

from src.frontend import data_api
from src.frontend.components import page_header, section_heading, ai_analysis_panel


def render():
    page_header("Reports Database", "Searchable, filterable record of all safety reports")

    df = data_api.get_reports()

    section_heading("Filters")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        site_filter = st.multiselect("Site", sorted(df["site"].unique()))
    with c2:
        type_filter = st.multiselect("Report Type", sorted(df["report_type"].unique()))
    with c3:
        risk_filter = st.multiselect("SIF Risk", ["High", "Medium", "Low"])
    with c4:
        rule_filter = st.multiselect("Life-Saving Rule", sorted(df["life_saving_rule"].unique()))

    c5, c6, c7 = st.columns(3)
    with c5:
        activity_filter = st.multiselect("Activity", sorted(df["activity"].unique()))
    with c6:
        status_filter = st.multiselect("Review Status", sorted(df["review_status"].unique()))
    with c7:
        date_range = st.date_input(
            "Date range",
            value=(df["date"].min().date(), df["date"].max().date()),
        )

    search_query = st.text_input("Search report ID or narrative text", placeholder="e.g. OIL-2026-00123, isolation, gas test...")

    filtered = df.copy()
    if site_filter:
        filtered = filtered[filtered["site"].isin(site_filter)]
    if type_filter:
        filtered = filtered[filtered["report_type"].isin(type_filter)]
    if risk_filter:
        filtered = filtered[filtered["sif_band"].isin(risk_filter)]
    if rule_filter:
        filtered = filtered[filtered["life_saving_rule"].isin(rule_filter)]
    if activity_filter:
        filtered = filtered[filtered["activity"].isin(activity_filter)]
    if status_filter:
        filtered = filtered[filtered["review_status"].isin(status_filter)]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["date"].dt.date >= start) & (filtered["date"].dt.date <= end)
        ]
    if search_query:
        q = search_query.lower()
        filtered = filtered[
            filtered["report_id"].str.lower().str.contains(q)
            | filtered["narrative"].str.lower().str.contains(q)
        ]

    section_heading(f"Results ({len(filtered)} reports)")
    display = filtered[[
        "report_id", "date", "site", "report_type", "activity", "sif_score",
        "sif_band", "life_saving_rule", "review_status",
    ]].copy()
    display["date"] = display["date"].dt.strftime("%d %b %Y")
    display.columns = ["Report ID", "Date", "Site", "Report Type", "Activity", "SIF Score", "Risk", "Rule", "Review Status"]
    st.dataframe(display, use_container_width=True, hide_index=True, height=380)

    st.markdown("---")
    section_heading("Open a Report", "Select a report to view its detailed AI analysis")
    if len(filtered) > 0:
        selected_id = st.selectbox("Report ID", ["—"] + filtered["report_id"].tolist())
        if selected_id != "—":
            row = filtered[filtered["report_id"] == selected_id].iloc[0]
            st.markdown(f"**Narrative:** {row['narrative']}")
            result = {
                "sif_potential": row["sif_score"],
                "sif_band": row["sif_band"],
                "model_confidence": 87.0,
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
            ai_analysis_panel(result)
    else:
        st.info("No reports match the current filters.")
