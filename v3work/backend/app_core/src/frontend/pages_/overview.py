import streamlit as st
import plotly.graph_objects as go

from src.frontend import data_api, charts
from src.frontend.components import page_header, section_heading, kpi_card, precursor_card
from src.frontend.styles import COLORS, risk_badge, status_badge, priority_badge


def render():
    page_header(
        "OIL SIF Precursor Intelligence",
        "Proactive identification of conditions with serious injury and fatality potential",
    )

    df = data_api.get_reports()
    site_risk = data_api.get_site_risk()
    precursors = data_api.get_precursor_patterns()
    pending = data_api.get_pending_reviews()

    total_reports = len(df)
    high_sif = int((df["sif_band"] == "High").sum())
    emerging_count = int((precursors["trend_pct"] > 20).sum())
    awaiting_review = len(pending)

    # naive trend vs prior period for KPI deltas
    import pandas as pd
    cutoff = df["date"].max() - pd.Timedelta(days=30)
    recent = df[df["date"] >= cutoff]
    older = df[df["date"] < cutoff]
    recent_high = (recent["sif_band"] == "High").sum()
    older_high = (older["sif_band"] == "High").sum()
    high_sif_trend = ((recent_high - older_high) / older_high * 100) if older_high else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Reports", f"{total_reports:,}", "All safety reports in the system")
    with c2:
        kpi_card("High SIF Potential", f"{high_sif:,}", "Reports flagged as high SIF risk", trend=high_sif_trend)
    with c3:
        kpi_card("Emerging Precursors", f"{emerging_count}", "Patterns trending upward >20%", trend=emerging_count * 4)
    with c4:
        kpi_card("Awaiting HSE Review", f"{awaiting_review}", "Reports pending human validation",
                 trend=None)

    section_heading("SIF Risk Overview", "Distribution and trend of SIF potential across all reports")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(charts.sif_distribution_donut(df), use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.plotly_chart(charts.sif_trend_chart(df), use_container_width=True, config={"displayModeBar": False})

    section_heading("Top Recurring Precursors", "Recurring activity + hazard + barrier-failure combinations")
    top_precursors = precursors.head(4)
    for _, row in top_precursors.iterrows():
        cols = st.columns([5, 1])
        with cols[0]:
            precursor_card(row["pattern"], row["frequency"], row["risk_density"], row["trend_pct"])
        with cols[1]:
            st.button("View details →", key=f"ov_prec_{row['pattern'][:20]}", use_container_width=True)

    section_heading("Sites Requiring Attention", "Ranked by SIF risk score and emerging trend")
    top_sites = site_risk.head(6)
    header_cols = st.columns([2.5, 1.2, 1.4, 1.4, 1.2])
    for c, label in zip(header_cols, ["Site", "SIF Risk", "High-Risk Reports", "Emerging Trend", "Priority"]):
        c.markdown(f"<div style='color:{COLORS['text_secondary']}; font-size:0.78rem; font-weight:700; text-transform:uppercase;'>{label}</div>", unsafe_allow_html=True)
    for _, row in top_sites.iterrows():
        cols = st.columns([2.5, 1.2, 1.4, 1.4, 1.2])
        cols[0].markdown(f"**{row['site']}**")
        cols[1].markdown(f"{row['risk_score']:.0f}")
        cols[2].markdown(f"{int(row['high_sif'])}")
        trend_color = COLORS["critical"] if row["emerging_trend_pct"] > 0 else COLORS["controlled"]
        arrow = "↑" if row["emerging_trend_pct"] > 0 else "↓"
        cols[3].markdown(f"<span style='color:{trend_color}; font-weight:600;'>{arrow} {abs(row['emerging_trend_pct']):.0f}%</span>", unsafe_allow_html=True)
        cols[4].markdown(priority_badge(row["priority"]), unsafe_allow_html=True)

    section_heading("Recent High-Risk Reports", "Most recent reports with High SIF potential")
    recent_high_risk = df[df["sif_band"] == "High"].sort_values("date", ascending=False).head(6)
    display_df = recent_high_risk[["report_id", "date", "site", "activity", "sif_score", "life_saving_rule", "review_status"]].copy()
    display_df["date"] = display_df["date"].dt.strftime("%d %b %Y")
    display_df.columns = ["Report ID", "Date", "Site", "Activity", "SIF Score", "Life-Saving Rule", "Review Status"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
