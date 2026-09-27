import streamlit as st

from src.frontend import data_api, mock_data
from src.frontend.components import page_header, section_heading
from src.frontend.styles import risk_badge, COLORS


def render():
    page_header("HSE Review", "Reports Awaiting HSE Validation")

    st.markdown(f"""
        <div class="alert-box" style="border-color:{COLORS['accent']}66; background:{COLORS['accent_soft']};">
            <div class="alert-title" style="color:{COLORS['accent']};">👤 Human-in-the-loop safety workflow</div>
            <div class="alert-text">AI flags potential SIF precursors. An HSE officer must confirm, reject, or correct
            each classification before it is treated as validated. The AI does not make autonomous safety decisions.</div>
        </div>
    """, unsafe_allow_html=True)

    pending = data_api.get_pending_reviews(limit=15)

    if len(pending) == 0:
        st.success("No reports are currently awaiting HSE review.")
        return

    section_heading(f"{len(pending)} Reports Pending Validation")

    for _, row in pending.iterrows():
        with st.expander(f"{row['report_id']}  ·  {row['site']}  ·  {row['activity']}  ·  SIF {row['sif_score']:.0f}%", expanded=False):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"""
                    <div class="panel-tight">
                        <div class="kpi-label">AI Classification</div>
                        <div class="kpi-value" style="font-size:1.5rem;">SIF Potential — {row['sif_score']:.0f}%</div>
                        <div style="margin-top:0.4rem;">{risk_badge(row['sif_band'])}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="panel-tight">
                        <div class="kpi-label">AI Reasoning</div>
                        <div style="font-size:0.88rem; color:{COLORS['text_primary']};">
                            Worker potentially exposed to {row['hazard'].lower()} where
                            {row['critical_barrier'].lower()} was reported as ineffective or absent.
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                    <div class="panel-tight">
                        <div class="kpi-label">Suggested Rule</div>
                        <div style="font-weight:700;">{row['life_saving_rule']}</div>
                    </div>
                    <div class="panel-tight">
                        <div class="kpi-label">Suggested Barrier</div>
                        <div style="font-weight:700;">{row['critical_barrier']}</div>
                    </div>
                    <div class="panel-tight">
                        <div class="kpi-label">Suggested Failure</div>
                        <div style="font-weight:700;">{row['barrier_failure']}</div>
                    </div>
                    <div class="panel-tight">
                        <div class="kpi-label">Potential Consequence</div>
                        <div style="font-weight:700;">{row['potential_consequence']}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.caption(f"Report narrative: {row['narrative']}")

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            confirm_key = f"confirm_{row['report_id']}"
            reject_key = f"reject_{row['report_id']}"
            correct_key = f"correct_toggle_{row['report_id']}"

            with btn_col1:
                if st.button("✓ Confirm", key=confirm_key, use_container_width=True):
                    data_api.submit_review_decision(row["report_id"], "Confirm")
                    st.success(f"{row['report_id']} confirmed.")
                    st.rerun()
            with btn_col2:
                if st.button("✕ Reject", key=reject_key, use_container_width=True):
                    data_api.submit_review_decision(row["report_id"], "Reject")
                    st.warning(f"{row['report_id']} rejected.")
                    st.rerun()
            with btn_col3:
                show_correct = st.toggle("✎ Correct", key=correct_key)

            if show_correct:
                st.markdown("###### Correct AI Classification")
                cc1, cc2, cc3 = st.columns(3)
                with cc1:
                    new_band = st.selectbox("SIF Classification", ["High", "Medium", "Low"],
                                             index=["High", "Medium", "Low"].index(row["sif_band"]),
                                             key=f"band_{row['report_id']}")
                    new_rule = st.selectbox(
                        "Life-Saving Rule",
                        sorted(set(p["rule"] for p in mock_data.HAZARD_PROFILES.values())),
                        index=0, key=f"rule_{row['report_id']}",
                    )
                with cc2:
                    new_hazard = st.selectbox("Hazard", list(mock_data.HAZARD_PROFILES.keys()),
                                               index=list(mock_data.HAZARD_PROFILES.keys()).index(row["hazard"]),
                                               key=f"hazard_{row['report_id']}")
                    new_activity = st.selectbox("Activity", mock_data.ACTIVITIES,
                                                 index=mock_data.ACTIVITIES.index(row["activity"]) if row["activity"] in mock_data.ACTIVITIES else 0,
                                                 key=f"activity_{row['report_id']}")
                with cc3:
                    new_barrier = st.text_input("Barrier", value=row["critical_barrier"], key=f"barrier_{row['report_id']}")
                    new_failure = st.text_input("Barrier Failure", value=row["barrier_failure"], key=f"failure_{row['report_id']}")
                new_consequence = st.text_input("Potential Consequence", value=row["potential_consequence"], key=f"cons_{row['report_id']}")

                if st.button("Save Correction", key=f"save_{row['report_id']}", type="primary"):
                    data_api.submit_review_decision(row["report_id"], "Correct", corrected_fields={
                        "sif_band": new_band,
                        "life_saving_rule": new_rule,
                        "hazard": new_hazard,
                        "activity": new_activity,
                        "critical_barrier": new_barrier,
                        "barrier_failure": new_failure,
                        "potential_consequence": new_consequence,
                    })
                    st.success(f"{row['report_id']} updated with HSE-corrected classification.")
                    st.rerun()

            st.caption("Human validation improves future model performance.")
