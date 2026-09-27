import streamlit as st

from src.frontend import data_api, charts
from src.frontend.components import page_header, section_heading
from src.frontend.styles import COLORS


def render():
    page_header("IOGP Life-Saving Rules", "Rule-level analytics across all safety reports (a report may map to multiple rules)")

    lsr_df = data_api.get_lsr_statistics()

    section_heading("Life-Saving Rule Summary")
    col1, col2 = st.columns([2, 3])
    with col1:
        display = lsr_df.copy()
        display["avg_sif"] = display["avg_sif"].round(0).astype(int)
        display.columns = ["Rule", "Reports", "Avg SIF", "High SIF Count", "Top Failed Barrier"]
        st.dataframe(display, use_container_width=True, hide_index=True, height=340)
    with col2:
        st.plotly_chart(charts.lsr_bar(lsr_df), use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    section_heading("Rule Drill-Down")
    selected_rule = st.selectbox("Select a Life-Saving Rule", lsr_df["rule"].tolist())
    detail = data_api.get_rule_detail(selected_rule)

    st.markdown(f"**{detail['count']} reports** reference this rule (as primary or secondary)")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Associated Hazards**")
        for hz, cnt in detail["hazards"].items():
            st.markdown(f"- {hz} ({cnt})")
    with c2:
        st.markdown("**Associated Activities**")
        for act, cnt in detail["activities"].items():
            st.markdown(f"- {act} ({cnt})")
    with c3:
        st.markdown("**Sites Most Affected**")
        for site, cnt in detail["sites"].items():
            st.markdown(f"- {site} ({cnt})")

    c4, c5 = st.columns(2)
    with c4:
        st.markdown("**Common Barrier Failures**")
        for fail, cnt in detail["barrier_failures"].items():
            st.markdown(f"- {fail} ({cnt})")
    with c5:
        st.markdown("**Potential Consequences**")
        for cons, cnt in detail["consequences"].items():
            st.markdown(f"- {cons} ({cnt})")
