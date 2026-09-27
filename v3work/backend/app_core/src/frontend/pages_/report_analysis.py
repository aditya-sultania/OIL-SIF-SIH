import streamlit as st

from src.frontend import data_api
from src.frontend.components import page_header, section_heading, ai_analysis_panel
from src.frontend.styles import COLORS


def render():
    page_header("Report Analysis", "Submit a safety report for AI-assisted structured analysis")

    section_heading("Submit a Report")
    input_mode = st.radio(
        "Input method", ["Paste report text", "Select a sample report", "Upload a report"],
        horizontal=True, label_visibility="collapsed",
    )

    report_text = ""
    if input_mode == "Paste report text":
        report_text = st.text_area(
            "Report text",
            placeholder="Describe the unsafe act, unsafe condition, near miss, or incident...",
            height=140,
        )
    elif input_mode == "Select a sample report":
        samples = data_api.SAMPLE_REPORTS
        labels = [s["label"] for s in samples]
        choice = st.selectbox("Sample reports", labels)
        report_text = next(s["text"] for s in samples if s["label"] == choice)
        st.text_area("Report preview", value=report_text, height=120, disabled=True)
    else:
        uploaded = st.file_uploader("Upload a report (.txt)", type=["txt"])
        if uploaded is not None:
            report_text = uploaded.read().decode("utf-8", errors="ignore")
            st.text_area("Report preview", value=report_text, height=120, disabled=True)
        else:
            st.caption("Accepted format: plain text (.txt). PDF/scanned form ingestion is a future backend integration point.")

    analyze_clicked = st.button("Run AI Analysis", type="primary", disabled=not report_text.strip())

    if analyze_clicked and report_text.strip():
        with st.spinner("Analyzing report..."):
            result = data_api.analyze_report(report_text)
        st.session_state["last_analysis"] = result

    if "last_analysis" in st.session_state:
        st.markdown("---")
        section_heading("AI Analysis", "AI-assessed classification — this is a suggestion, not a final safety determination")
        ai_analysis_panel(st.session_state["last_analysis"])

        st.markdown(f"""
            <div class="ai-note" style="margin-top:1rem;">
                This output is AI-assessed and requires HSE validation before being treated as confirmed.
                Route this report to <b>HSE Review</b> to confirm, reject, or correct the classification.
            </div>
        """, unsafe_allow_html=True)
