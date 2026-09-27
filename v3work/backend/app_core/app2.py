import re
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from chatbot.auth import login, logout, get_role, get_user_id
from chatbot.assistant import answer_question


# ============================================================
# PATHS / MODELS
# ============================================================

ROOT = Path(__file__).resolve().parent


@st.cache_resource(show_spinner=False)
def load_models():
    sif_model = joblib.load(ROOT / "SIF_Model_v4_DomainAware.joblib")
    lsr_model = joblib.load(ROOT / "IOGP_Life_Saving_Rule_Classifier_v2.joblib")
    return sif_model, lsr_model


SIF_MODEL, LSR_MODEL = load_models()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OIL SIF Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = [
    "#d97706", "#0f2942", "#0ea5e9", "#16a34a",
    "#dc2626", "#7c3aed", "#64748b", "#facc15",
]


# ============================================================
# THEME / CSS
# ============================================================

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
        }

        .block-container {
            padding-top: 1.1rem;
            padding-bottom: 3rem;
            max-width: 1300px;
        }

        /* ---------- HERO ---------- */
        .hero {
            padding: 1.7rem 2rem;
            border-radius: 20px;
            background: linear-gradient(120deg, #061021 0%, #0f2942 55%, #16324f 100%);
            color: #ffffff;
            margin-bottom: 1.4rem;
            box-shadow: 0 12px 30px -12px rgba(6, 16, 33, 0.55);
            border: 1px solid rgba(217, 119, 6, 0.25);
            position: relative;
            overflow: hidden;
        }
        .hero::after {
            content: "";
            position: absolute;
            top: -60px; right: -60px;
            width: 220px; height: 220px;
            background: radial-gradient(circle, rgba(217,119,6,0.28) 0%, rgba(217,119,6,0) 70%);
        }
        .hero-eyebrow {
            text-transform: uppercase;
            letter-spacing: .14em;
            font-size: .72rem;
            font-weight: 700;
            color: #f2b544;
            margin: 0 0 .35rem 0;
        }
        .hero h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.01em;
        }
        .hero p {
            margin: .5rem 0 0;
            color: #c7d2e0;
            font-size: .98rem;
            max-width: 780px;
        }

        /* ---------- CARDS ---------- */
        .metric-card {
            background: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 16px;
            padding: 1.05rem 1.2rem;
            box-shadow: 0 4px 14px -8px rgba(15,41,66,0.18);
            height: 100%;
        }
        .metric-card .label {
            font-size: .74rem;
            text-transform: uppercase;
            letter-spacing: .08em;
            font-weight: 700;
            color: #64748b;
            margin-bottom: .3rem;
        }
        .metric-card .value {
            font-size: 1.65rem;
            font-weight: 800;
            color: #0f2942;
            line-height: 1.1;
        }
        .metric-card .sub {
            font-size: .78rem;
            color: #94a3b8;
            margin-top: .25rem;
        }

        .section-card {
            background: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 16px;
            padding: 1.1rem 1.3rem 1.3rem;
            margin-bottom: 1.1rem;
            box-shadow: 0 4px 14px -10px rgba(15,41,66,0.15);
        }
        .section-title {
            font-size: 1.02rem;
            font-weight: 700;
            color: #0f2942;
            margin-bottom: .65rem;
            display: flex;
            align-items: center;
            gap: .45rem;
        }

        /* ---------- BADGES / PILLS ---------- */
        .pill {
            display: inline-block;
            padding: .3rem .8rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: .8rem;
            margin: .12rem .3rem .12rem 0;
        }
        .pill-high   { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
        .pill-medium { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
        .pill-low    { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
        .pill-neutral{ background: #e2e8f0; color: #334155; border: 1px solid #cbd5e1; }
        .pill-info   { background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }

        .chip {
            display: inline-block;
            padding: .28rem .7rem;
            border-radius: 8px;
            background: #0f2942;
            color: #f2b544;
            font-weight: 600;
            font-size: .78rem;
            margin: .18rem .32rem .18rem 0;
            border: 1px solid rgba(242,181,68,0.35);
        }
        .chip-muted {
            background: #f1f5f9;
            color: #475569;
            border: 1px solid #e2e8f0;
        }

        .reminder-box {
            background: #fff7ed;
            border-left: 4px solid #d97706;
            border-radius: 10px;
            padding: .7rem .95rem;
            margin-bottom: .55rem;
            color: #7c2d12;
            font-size: .92rem;
        }

        /* ---------- SIDEBAR ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1220 0%, #0f2942 100%);
        }
        section[data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        section[data-testid="stSidebar"] .stRadio label {
            font-weight: 500;
        }
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.12);
        }
        .sidebar-brand {
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.01em;
            margin-bottom: 0;
        }
        .sidebar-role {
            display: inline-block;
            margin-top: .4rem;
            padding: .22rem .65rem;
            border-radius: 999px;
            background: rgba(242,181,68,0.16);
            border: 1px solid rgba(242,181,68,0.4);
            color: #f2b544 !important;
            font-size: .76rem;
            font-weight: 700;
        }

        /* ---------- MISC ---------- */
        div[data-testid="stMetricValue"] { color: #0f2942; }
        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
        }
        .stButton>button[kind="primary"] {
            background: #d97706;
            border-color: #d97706;
        }
        .stButton>button[kind="primary"]:hover {
            background: #b45309;
            border-color: #b45309;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header(title, subtitle, eyebrow=None):
    eyebrow_html = f'<p class="hero-eyebrow">{eyebrow}</p>' if eyebrow else ""
    st.markdown(
        f"""
        <div class="hero">
            {eyebrow_html}
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def metric_card(col, label, value, sub=None):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
                {f'<div class="sub">{sub}</div>' if sub else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )


def risk_pill(text, level):
    css_class = {
        "High": "pill-high",
        "Medium": "pill-medium",
        "Low": "pill-low",
        "Info": "pill-info",
    }.get(level, "pill-neutral")
    return f'<span class="pill {css_class}">{text}</span>'


def chip_row(items, muted=False):
    if not items:
        st.caption("None detected in the supplied text.")
        return
    cls = "chip chip-muted" if muted else "chip"
    html = "".join(f'<span class="{cls}">{item}</span>' for item in items)
    st.markdown(html, unsafe_allow_html=True)


def download_csv_button(df, label, filename):
    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_all_data():
    master = pd.read_csv(ROOT / "SIF_Dashboard_Master_v4.csv", low_memory=False)
    activity = pd.read_csv(ROOT / "SIF_Activity_Ranking_v4.csv")
    lsr = pd.read_csv(ROOT / "SIF_LSR_Ranking_v4.csv")
    precursor = pd.read_csv(ROOT / "SIF_Precursor_Ranking_v4.csv")
    barrier = pd.read_csv(ROOT / "SIF_Barrier_Ranking_v4.csv")
    queue = pd.read_csv(ROOT / "SIF_HSE_Review_Queue_v2.csv", low_memory=False)
    return master, activity, lsr, precursor, barrier, queue


# ============================================================
# SAFETY / CLASSIFICATION RULES  (unchanged detection logic)
# ============================================================

HIGH_RISK = {
    "Confined Space": r"confined space|asphyxi|hydrogen sulfide|\bh2s\b|oxygen deficient|engulf",
    "Energy / Isolation": r"electrocution|electrical shock|arc flash|high voltage|energized|lock[- ]out|tag[- ]out|stored energy",
    "Line of Fire": r"caught between|pinned between|crushed between|suspended load|line of fire|struck by",
    "Working at Height": r"fall(?:ed|ing)? from|fall from height|roof|scaffold|tower|derrick",
    "Hot Work / Fire": r"explosion|flash fire|fireball|uncontrolled release|flammable gas",
    "Excavation": r"trench collapse|cave[- ]in|buried in|excavation collapse",
    "Pressure": r"high pressure|pressure release|pressurized|rupture",
    "Drowning / Water": r"drown(?:ed|ing)?|man overboard|submerged",
}

LSR = {
    "Energy Isolation": r"energized|high voltage|electrocution|electrical shock|arc flash|lock[- ]out|tag[- ]out|stored energy|isolation",
    "Hot Work": r"hot work|welding|cutting|grinding|flammable|explosion|fire",
    "Confined Space": r"confined space|asphyxi|hydrogen sulfide|\bh2s\b|oxygen deficient|engulf",
    "Line of Fire": r"line of fire|struck by|caught between|pinned between|crushed between|suspended load|falling object",
    "Working at Height": r"fall|roof|scaffold|tower|derrick|elevated platform",
    "Driving / Mobile Equipment": r"vehicle|forklift|truck|driving|excavat|mobile equipment",
    "Lifting Operations": r"lifting|load|rigging|hoist|crane|suspended load",
    "Excavation": r"excavat|trench|cave[- ]in|buried|collapse",
}

PREC = {
    "Energy / isolation": r"energized|high voltage|electrocution|electrical shock|arc flash|lock[- ]out|tag[- ]out|stored energy|power cable",
    "Confined space": r"confined space|asphyxi|hydrogen sulfide|\bh2s\b|oxygen deficient|engulf",
    "Line of fire": r"struck by|caught between|pinned between|crushed between|suspended load|falling object|line of fire",
    "Working at height": r"fall(?:ed|ing)? from|fall(?:ed|ing)? off|roof|scaffold|tower|derrick|elevated platform",
    "Hot work / fire": r"hot work|welding|cutting|grinding|explosion|flash fire|flammable",
    "Excavation": r"excavat|trench|cave[- ]in|buried|collapse",
    "Vehicle / mobile equipment": r"forklift|excavator|vehicle|run over|backed over|mobile equipment",
    "Machinery / guarding": r"caught in|entangled|unguarded|machine guard|interlock|bypass",
}

ACT = {
    "Maintenance": r"maintenance|repair|cleaning|servicing",
    "Material handling / lifting": r"lifting|load|rigging|hoist|material handling|crane",
    "Working at height": r"fall|roof|scaffold|tower|elevated",
    "Mobile equipment / vehicles": r"vehicle|forklift|truck|excavat|transport",
    "Machinery operation": r"machin|equipment|caught in|entangled",
    "Excavation": r"excavat|trench",
    "Welding / hot work": r"weld|cutting|grinding|hot work",
    "Electrical work": r"electric|electrical|power cable|energized",
}

BARR = {
    "Isolation failure": ["isolation", "isolat", "lock-out", "lockout", "tag-out", "tagout", "energized", "stored energy"],
    "Permit / authorization failure": ["permit", "authorization", "work authorization"],
    "Planning / risk assessment": ["planning", "risk assessment", "hazard assessment", "jsa", "job safety"],
    "Communication failure": ["communication", "communicat", "handover", "coordination"],
    "Supervision failure": ["supervision", "supervisor", "oversight"],
    "Procedure failure": ["procedure", "procedural", "instruction", "standard"],
    "Training / competency": ["training", "competenc", "qualified", "qualification"],
    "Inspection / maintenance": ["inspection", "inspect", "maintenance", "defect", "equipment condition"],
    "Safety control bypass": ["bypass", "interlock", "guard removed", "safety control"],
}

RECOMMENDED_ACTIONS = {
    "Energy / isolation": "Verify lock-out / tag-out and confirm a zero-energy state before any work resumes.",
    "Confined space": "Confirm atmospheric testing, continuous monitoring and an active rescue plan before entry.",
    "Line of fire": "Establish exclusion zones and remove personnel from the line of fire of moving or suspended loads.",
    "Working at height": "Verify fall-protection, anchor points and a rescue plan before work at height continues.",
    "Hot work / fire": "Confirm an active hot-work permit, fire watch and gas testing before ignition sources are used.",
    "Excavation": "Verify shoring/benching, atmospheric testing and safe access/egress before excavation work continues.",
    "Vehicle / mobile equipment": "Separate pedestrians from mobile equipment and confirm spotter / traffic-management controls.",
    "Machinery / guarding": "Verify machine guarding and interlocks are fitted and have not been bypassed.",
}


# ============================================================
# ANALYSIS HELPERS
# ============================================================

def hits(text, dictionary):
    return [key for key, pattern in dictionary.items() if re.search(pattern, text, re.I)]


def explain(text):
    features = SIF_MODEL.named_steps["features"]
    clf = SIF_MODEL.named_steps["clf"]

    X = features.transform([text]).toarray()[0]
    names = features.get_feature_names_out()
    contributions = X * clf.coef_[0]

    positive = sorted(
        [(names[i], float(contributions[i])) for i in range(len(contributions)) if contributions[i] > 0],
        key=lambda x: x[1], reverse=True,
    )[:8]

    negative = sorted(
        [(names[i], float(contributions[i])) for i in range(len(contributions)) if contributions[i] < 0],
        key=lambda x: x[1],
    )[:8]

    return positive, negative


def review_level(probability, high_risk):
    if high_risk or probability >= 0.70:
        return "High Priority"
    if probability >= 0.30:
        return "HSE Review"
    return "Normal"


def analyze(text):
    probability = float(SIF_MODEL.predict_proba([text])[0, 1])
    high_risk = hits(text, HIGH_RISK)

    prediction = "SIF Potential" if probability >= 0.5 or high_risk else "Non-SIF Potential"

    probabilities = LSR_MODEL.predict_proba([text])[0]
    indexes = probabilities.argsort()[::-1][:3]
    lsr_predictions = [(str(LSR_MODEL.classes_[i]), float(probabilities[i])) for i in indexes]

    precursors = hits(text, PREC)
    activities = hits(text, ACT)
    lsr_keywords = hits(text, LSR)

    barrier_patterns = {key: "|".join(map(re.escape, values)) for key, values in BARR.items()}
    barriers = hits(text, barrier_patterns)

    return (
        probability, prediction, high_risk, precursors,
        activities, lsr_keywords, lsr_predictions, barriers, explain(text),
    )


def plain_explanation(probability, prediction, high_risk):
    if prediction == "SIF Potential":
        line = f"The model estimates a **{probability:.0%} probability** that this event could have led to a Serious Injury or Fatality (SIF)."
    else:
        line = f"The model estimates a **{probability:.0%} probability** of SIF potential, below the SIF-Potential threshold."

    if high_risk:
        line += (
            " The wording also matches known **high-risk safety-critical patterns** "
            f"({', '.join(high_risk)}), so this is flagged as SIF Potential regardless of the raw "
            "probability — this is the safety backstop rule."
        )
    return line


def recommended_action(prediction, precursors, review_lvl):
    actions = []

    if review_lvl == "High Priority":
        actions.append("Escalate to HSE / Emergency Response immediately and stop the activity if the condition is still present.")

    for p in precursors:
        if p in RECOMMENDED_ACTIONS:
            actions.append(RECOMMENDED_ACTIONS[p])

    if not actions:
        if prediction == "SIF Potential":
            actions.append("Route to HSE review to confirm whether critical controls were missing or degraded.")
        else:
            actions.append("Log for trend monitoring; no immediate escalation required.")

    # de-duplicate while preserving order
    seen = set()
    unique_actions = []
    for a in actions:
        if a not in seen:
            unique_actions.append(a)
            seen.add(a)

    return unique_actions


def sif_gauge(probability, review_lvl):
    color = {"High Priority": "#dc2626", "HSE Review": "#d97706", "Normal": "#16a34a"}[review_lvl]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%", "font": {"size": 34, "color": "#0f2942"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": color, "thickness": 0.32},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 30], "color": "#dcfce7"},
                    {"range": [30, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#fee2e2"},
                ],
                "threshold": {"line": {"color": "#0f2942", "width": 3}, "thickness": 0.85, "value": probability * 100},
            },
        )
    )
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=10, b=10))
    return fig


def render_analysis_workbench(key_prefix, show_advanced_default=False):
    """Reusable live SIF / LSR / XAI analysis workbench.

    Wires SIF_MODEL + LSR_MODEL (already loaded) directly into the UI so the
    'Analyze' step from the project workflow is actually reachable, with a
    plain-language read-out plus a technical XAI section for HSE users.
    """

    example_text = (
        "Technician was performing maintenance on an energized panel without "
        "confirming lock-out tag-out. Contact with live conductor caused an "
        "electrical shock and the worker fell from the platform."
    )

    text = st.text_area(
        "Incident / observation narrative",
        placeholder=example_text,
        height=140,
        key=f"{key_prefix}_text",
    )

    c1, c2 = st.columns([1, 5])
    with c1:
        run = st.button("🔍 Analyze", type="primary", use_container_width=True, key=f"{key_prefix}_run")
    with c2:
        if st.button("Use example text", use_container_width=True, key=f"{key_prefix}_example"):
            st.session_state[f"{key_prefix}_text"] = example_text
            st.rerun()

    if not run:
        return

    if not text or not text.strip():
        st.warning("Enter an incident narrative before running the analysis.")
        return

    with st.spinner("Scoring narrative against the SIF and Life-Saving Rule models..."):
        (
            probability, prediction, high_risk, precursors,
            activities, lsr_keywords, lsr_predictions, barriers, (positive, negative),
        ) = analyze(text)

    review_lvl = review_level(probability, high_risk)
    level_ui = {"High Priority": "High", "HSE Review": "Medium", "Normal": "Low"}[review_lvl]

    st.success("Analysis complete.")

    # ---------------- headline row ----------------
    g1, g2 = st.columns([1, 2])

    with g1:
        st.plotly_chart(sif_gauge(probability, review_lvl), use_container_width=True, config={"displayModeBar": False})

    with g2:
        st.markdown(
            f"""
            {risk_pill(prediction, "High" if prediction == "SIF Potential" else "Low")}
            {risk_pill(f"Review level: {review_lvl}", level_ui)}
            {risk_pill("⚠ High-risk backstop triggered", "High") if high_risk else risk_pill("No safety backstop triggered", "Low")}
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        st.markdown(plain_explanation(probability, prediction, high_risk))

    st.markdown("---")

    # ---------------- detected tags ----------------
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        section_title("Detected activity")
        chip_row(activities)
    with d2:
        section_title("Precursor pattern")
        chip_row(precursors)
    with d3:
        section_title("Life-Saving Rule keywords")
        chip_row(lsr_keywords)
    with d4:
        section_title("Barrier failure signal")
        chip_row(barriers, muted=True)

    st.markdown("###")

    # ---------------- LSR model prediction ----------------
    section_title("🛡️ Top predicted Life-Saving Rules")
    lsr_df = pd.DataFrame(lsr_predictions, columns=["Life-Saving Rule", "Confidence"])
    st.plotly_chart(
        px.bar(
            lsr_df.sort_values("Confidence"),
            x="Confidence", y="Life-Saving Rule", orientation="h",
            text=lsr_df.sort_values("Confidence")["Confidence"].map(lambda v: f"{v:.0%}"),
        ).update_layout(height=220, margin=dict(l=10, r=10, t=10, b=10), xaxis_tickformat=".0%"),
        use_container_width=True,
    )

    # ---------------- recommended action ----------------
    section_title("✅ Recommended HSE action")
    for action in recommended_action(prediction, precursors, review_lvl):
        st.markdown(f'<div class="reminder-box">{action}</div>', unsafe_allow_html=True)

    # ---------------- technical XAI ----------------
    with st.expander("🧪 Technical XAI — model feature contributions", expanded=show_advanced_default):
        st.caption(
            "Linear-model term contributions toward the SIF-Potential score. "
            "Positive terms push the prediction toward SIF Potential; negative terms push away from it."
        )

        xc1, xc2 = st.columns(2)

        with xc1:
            st.markdown("**Pushes toward SIF Potential**")
            if positive:
                pos_df = pd.DataFrame(positive, columns=["Term", "Contribution"])
                st.plotly_chart(
                    px.bar(
                        pos_df.sort_values("Contribution"),
                        x="Contribution", y="Term", orientation="h",
                        color_discrete_sequence=["#dc2626"],
                    ).update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10)),
                    use_container_width=True,
                )
            else:
                st.caption("No positive contributing terms found.")

        with xc2:
            st.markdown("**Pushes away from SIF Potential**")
            if negative:
                neg_df = pd.DataFrame(negative, columns=["Term", "Contribution"])
                st.plotly_chart(
                    px.bar(
                        neg_df.sort_values("Contribution"),
                        x="Contribution", y="Term", orientation="h",
                        color_discrete_sequence=["#16a34a"],
                    ).update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10)),
                    use_container_width=True,
                )
            else:
                st.caption("No negative contributing terms found.")

        st.markdown("**Raw probabilities**")
        st.json(
            {
                "sif_probability": round(probability, 4),
                "sif_prediction": prediction,
                "review_level": review_lvl,
                "high_risk_categories": high_risk,
                "lsr_top3": [{"rule": r, "confidence": round(p, 4)} for r, p in lsr_predictions],
            }
        )


# ============================================================
# WORKER DASHBOARD
# ============================================================

def worker_dashboard(master, lsr, precursor):
    page = st.sidebar.radio(
        "Workspace",
        ["Safety Home", "My Safety View", "Report & Analyze Incident"],
    )

    if page == "Safety Home":
        header(
            "🦺 Worker Safety Dashboard",
            "Practical safety intelligence without sensitive management information.",
            eyebrow="Employee / Worker",
        )

        sif_count = 0
        if "sif_prediction" in master.columns:
            sif_count = int((master["sif_prediction"] == "SIF Potential").sum())

        common_hazard_series = (
            master["precursor"].dropna().astype(str).value_counts()
            if "precursor" in master.columns else pd.Series(dtype=int)
        )
        top_hazard = common_hazard_series.index[0] if len(common_hazard_series) else "N/A"

        a, b, c = st.columns(3)
        metric_card(a, "Safety Reports", f"{len(master):,}")
        metric_card(b, "Common Hazard", top_hazard)
        metric_card(c, "SIF-Potential Reports", f"{sif_count:,}")

        st.markdown("###")

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_title("⚠️ Common Hazards")
            if len(common_hazard_series):
                hazards = common_hazard_series.head(8).rename_axis("Hazard").reset_index(name="Reports")
                st.dataframe(hazards, use_container_width=True, hide_index=True)
            else:
                st.info("No hazard information available.")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_title("🛡️ Top Life-Saving Rules")
            if not lsr.empty:
                st.dataframe(lsr.head(8), use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_title("✅ Safety Reminders")
            reminders = [
                "Verify energy isolation before starting maintenance.",
                "Stay outside the line of fire of moving equipment and suspended loads.",
                "Use appropriate protection for work at height.",
                "Maintain separation between pedestrians and mobile equipment.",
                "Report recurring unsafe conditions to HSE.",
            ]
            for reminder in reminders:
                st.markdown(f'<div class="reminder-box">{reminder}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "My Safety View":
        header(
            "My Safety View",
            "Select an activity to view its recurring safety patterns.",
            eyebrow="Employee / Worker",
        )

        if "activity_group" not in master.columns:
            st.info("Activity information is unavailable.")
            return

        activities = sorted(master["activity_group"].dropna().astype(str).unique())
        selected_activity = st.selectbox("Activity", activities)

        filtered = master[master["activity_group"].astype(str) == selected_activity]

        st.metric("Reports for this activity", f"{len(filtered):,}")

        col1, col2 = st.columns(2)

        with col1:
            if "precursor" in filtered.columns:
                hazards = (
                    filtered["precursor"].dropna().astype(str).value_counts()
                    .head(8).rename_axis("Hazard").reset_index(name="Reports")
                )
                section_title("Recurring Hazards")
                st.dataframe(hazards, use_container_width=True, hide_index=True)

        with col2:
            section_title("Recommended Precautions")
            precautions = [
                "Follow the applicable Life-Saving Rules for the task.",
                "Verify critical controls before beginning work.",
                "Maintain awareness of line-of-fire exposures.",
                "Report unsafe conditions and recurring hazards.",
                "Stop work when critical controls are missing.",
            ]
            for precaution in precautions:
                st.write("• " + precaution)

    else:  # Report & Analyze Incident
        header(
            "📝 Report & Analyze Incident",
            "Describe what happened in plain language and get an instant AI-assisted safety read-out before you file a formal report.",
            eyebrow="Employee / Worker",
        )
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        render_analysis_workbench(key_prefix="worker", show_advanced_default=False)
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# HSE COMMAND CENTER
# ============================================================

def hse_command_center(master, activity, lsr, precursor, barrier, queue):
    page = st.sidebar.radio(
        "Workspace",
        ["HSE Command Center", "SIF Queue", "Trend & Precursor Lab", "Analyze / XAI", "AI Safety Assistant"],
    )

    # ========================================================
    # HSE COMMAND CENTER
    # ========================================================
    if page == "HSE Command Center":
        header(
            "🛡️ HSE Safety Officer Command Center",
            "Full SIF analytics, risk prioritization and safety intelligence.",
            eyebrow="HSE Officer",
        )

        total = len(master)
        sif_count = int((master["sif_prediction"] == "SIF Potential").sum())
        sif_rate = sif_count / total * 100 if total else 0
        mean_probability = master["sif_probability"].mean() if "sif_probability" in master.columns else 0

        review_count = 0
        if "hse_review_status" in master.columns:
            review_count = int((master["hse_review_status"] == "Review Suggested").sum())

        a, b, c, d = st.columns(4)
        metric_card(a, "Analyzed Reports", f"{total:,}")
        metric_card(b, "SIF Potential", f"{sif_count:,}")
        metric_card(c, "SIF Density", f"{sif_rate:.2f}%")
        metric_card(d, "Mean SIF Probability", f"{mean_probability:.1%}", sub=f"{review_count:,} flagged for review")

        st.markdown("###")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            risk = master["sif_prediction"].value_counts().rename_axis("Prediction").reset_index(name="Reports")
            st.plotly_chart(
                px.bar(risk, x="Prediction", y="Reports", title="SIF Prediction Distribution", color="Prediction"),
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            if "precursor" in master.columns:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                precursor_counts = (
                    master["precursor"].dropna().astype(str).value_counts()
                    .head(10).rename_axis("Precursor").reset_index(name="Reports")
                )
                st.plotly_chart(
                    px.bar(precursor_counts, x="Reports", y="Precursor", orientation="h", title="Top Precursor Patterns"),
                    use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("Top Activity Risk")
        st.dataframe(activity.head(10), use_container_width=True, hide_index=True)
        download_csv_button(activity, "⬇️ Download activity ranking (CSV)", "activity_ranking.csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # SIF QUEUE
    # ========================================================
    elif page == "SIF Queue":
        header(
            "📋 SIF Review Queue",
            "Prioritized reports requiring HSE attention.",
            eyebrow="HSE Officer",
        )

        if "activity_group" not in master.columns:
            st.warning("Activity information unavailable.")
            return

        activities = ["All"] + sorted(master["activity_group"].dropna().astype(str).unique())
        precursors = ["All"] + sorted(master["precursor"].dropna().astype(str).unique())

        c1, c2, c3 = st.columns(3)
        selected_activity = c1.selectbox("Activity", activities)
        selected_precursor = c2.selectbox("Precursor", precursors)
        minimum_probability = c3.slider("Minimum SIF Probability", 0.0, 1.0, 0.30, 0.01)

        search_term = st.text_input("🔎 Free-text search in report narrative (optional)")

        filtered = master.copy()

        if selected_activity != "All":
            filtered = filtered[filtered["activity_group"] == selected_activity]

        if selected_precursor != "All":
            filtered = filtered[filtered["precursor"] == selected_precursor]

        filtered = filtered[filtered["sif_probability"] >= minimum_probability]

        if search_term and "report_text" in filtered.columns:
            filtered = filtered[filtered["report_text"].astype(str).str.contains(search_term, case=False, na=False)]

        filtered = filtered.sort_values("sif_probability", ascending=False)

        display_columns = [
            column for column in [
                "report_id", "date_of_incident", "sif_probability", "sif_prediction",
                "confidence_band", "activity_group", "precursor", "life_saving_rule",
                "hse_review_status", "priority_score",
            ]
            if column in filtered.columns
        ]

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.dataframe(filtered[display_columns].head(500), use_container_width=True, hide_index=True)
        st.caption(f"Showing up to 500 of {len(filtered):,} matching reports.")
        download_csv_button(filtered[display_columns], "⬇️ Download filtered queue (CSV)", "sif_review_queue_filtered.csv")
        st.markdown("</div>", unsafe_allow_html=True)

        section_title("🔎 Individual Report")

        if "report_id" in filtered.columns and not filtered.empty:
            report_ids = filtered["report_id"].astype(str).tolist()
            selected_report = st.selectbox("Select Report", report_ids)

            report = filtered[filtered["report_id"].astype(str) == selected_report].iloc[0]

            rc1, rc2 = st.columns([2, 1])
            with rc1:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                if "report_text" in report:
                    st.write(report["report_text"])
                st.markdown("</div>", unsafe_allow_html=True)
            with rc2:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.json(report.to_dict())
                st.markdown("</div>", unsafe_allow_html=True)

            if "report_text" in report and isinstance(report["report_text"], str):
                if st.button("🔍 Run live Analyze / XAI on this report"):
                    st.session_state["hse_analyze_text"] = report["report_text"]
                    st.session_state["_jump_to_analyze"] = True
                    st.info("Text loaded. Switch to the **Analyze / XAI** workspace tab in the sidebar to view it.")

    # ========================================================
    # TREND & PRECURSOR LAB
    # ========================================================
    elif page == "Trend & Precursor Lab":
        header(
            "📈 Trend & Precursor Lab",
            "Recurring patterns, SIF trends and Life-Saving Rule analysis.",
            eyebrow="HSE Officer",
        )

        if "date_of_incident" in master.columns:
            trend_data = master.copy()
            trend_data["date_of_incident"] = pd.to_datetime(trend_data["date_of_incident"], errors="coerce")
            trend_data = trend_data.dropna(subset=["date_of_incident"])

            if not trend_data.empty:
                trend_data["month"] = trend_data["date_of_incident"].dt.to_period("M").dt.to_timestamp()
                monthly = (
                    trend_data.groupby("month").agg(
                        reports=("report_id", "count"),
                        sif=("sif_prediction", lambda x: (x == "SIF Potential").sum()),
                    ).reset_index()
                )

                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.plotly_chart(
                    px.line(monthly, x="month", y=["reports", "sif"], title="Monthly Report and SIF-Potential Trend"),
                    use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_title("Recurring Precursors")
            st.dataframe(precursor, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_title("Life-Saving Rules")
            st.dataframe(lsr, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("Barrier Failure Patterns")
        st.dataframe(barrier, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # ANALYZE / XAI  (previously defined but never wired into the UI)
    # ========================================================
    elif page == "Analyze / XAI":
        header(
            "🧪 Analyze / XAI",
            "Run any incident narrative through the SIF and Life-Saving Rule models and inspect the model's reasoning.",
            eyebrow="HSE Officer",
        )

        if st.session_state.get("_jump_to_analyze") and st.session_state.get("hse_analyze_text"):
            st.session_state["analyze_text"] = st.session_state["hse_analyze_text"]
            st.session_state["_jump_to_analyze"] = False

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        render_analysis_workbench(key_prefix="analyze", show_advanced_default=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # AI SAFETY ASSISTANT
    # ========================================================
    else:
        header(
            "🤖 AI Safety Assistant",
            "Ask natural-language questions about the OIL SIF dataset.",
            eyebrow="HSE Officer",
        )

        st.caption(
            "The assistant uses Gemini and dataset tools. "
            "Dataset-derived information is returned from the underlying data rather than invented."
        )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "gemini_chat" not in st.session_state:
            st.session_state.gemini_chat = None

        if st.button("🗑️ Clear Conversation"):
            st.session_state.chat_history = []
            st.session_state.gemini_chat = None
            st.rerun()

        for role_name, message in st.session_state.chat_history:
            with st.chat_message(role_name):
                st.markdown(message)

        question = st.chat_input("Ask about incidents, SIF risk, precursors, barriers...")

        if question:
            st.session_state.chat_history.append(("user", question))
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing the SIF dataset..."):
                    answer, chat = answer_question(question, st.session_state.gemini_chat)
                    st.session_state.gemini_chat = chat
                    st.markdown(answer)

            st.session_state.chat_history.append(("assistant", answer))


# ============================================================
# MANAGEMENT DASHBOARD
# ============================================================

def management_dashboard(master, activity, precursor, barrier):
    page = st.sidebar.radio(
        "Workspace",
        ["Executive Overview", "Risk Ranking", "Risk Drill-down", "Decision Brief"],
    )

    header(
        "👔 Management Decision Dashboard",
        "High-level safety intelligence for decision-making.",
        eyebrow="Management",
    )

    # ========================================================
    # EXECUTIVE OVERVIEW
    # ========================================================
    if page == "Executive Overview":
        total = len(master)
        sif_count = int((master["sif_prediction"] == "SIF Potential").sum())
        sif_rate = sif_count / total * 100 if total else 0

        a, b, c = st.columns(3)
        metric_card(a, "Total Reports", f"{total:,}")
        metric_card(b, "SIF-Potential Reports", f"{sif_count:,}")
        metric_card(c, "SIF Density", f"{sif_rate:.2f}%")

        st.markdown("###")

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("Activity Risk Overview")

        display = activity.copy()
        if "sif_density_pct" in display.columns:
            def risk_label(value):
                if value >= 50:
                    return "🔴 High"
                if value >= 25:
                    return "🟡 Moderate"
                return "🟢 Lower"
            display["Risk Level"] = display["sif_density_pct"].apply(risk_label)

        columns = [
            column for column in ["activity_group", "total_reports", "sif_reports", "sif_density_pct", "Risk Level"]
            if column in display.columns
        ]
        st.dataframe(display[columns], use_container_width=True, hide_index=True)
        download_csv_button(display[columns], "⬇️ Download activity risk overview (CSV)", "activity_risk_overview.csv")
        st.markdown("</div>", unsafe_allow_html=True)

        if "sif_density_pct" in activity.columns:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.plotly_chart(
                px.bar(activity, x="sif_density_pct", y="activity_group", orientation="h", title="SIF Density by Activity"),
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # RISK RANKING
    # ========================================================
    elif page == "Risk Ranking":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("Risk Ranking by Activity")
        st.caption(
            "This ranking uses the supplied SIF analytical dataset. "
            "It is not a claim that a site or department is inherently unsafe."
        )

        ranking_columns = [
            column for column in ["rank", "activity_group", "total_reports", "sif_reports", "sif_density_pct", "reliability"]
            if column in activity.columns
        ]
        st.dataframe(activity[ranking_columns], use_container_width=True, hide_index=True)
        download_csv_button(activity[ranking_columns], "⬇️ Download ranking (CSV)", "risk_ranking.csv")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("Leading Precursors")
        st.dataframe(precursor.head(10), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # RISK DRILL-DOWN
    # ========================================================
    elif page == "Risk Drill-down":
        section_title("🔎 Risk Drill-down")

        if "activity_group" not in master.columns:
            st.info("Activity information is unavailable.")
            return

        activities = sorted(master["activity_group"].dropna().astype(str).unique())
        selected_activity = st.selectbox("Activity", activities)

        filtered = master[master["activity_group"].astype(str) == selected_activity]

        m1, m2 = st.columns(2)
        metric_card(m1, "Reports", f"{len(filtered):,}")

        if "sif_prediction" in filtered.columns:
            sif_count = int((filtered["sif_prediction"] == "SIF Potential").sum())
            metric_card(m2, "SIF-Potential Reports", f"{sif_count:,}")

        st.markdown("###")

        col1, col2 = st.columns(2)

        with col1:
            if "precursor" in filtered.columns:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                section_title("Hazard / Precursor")
                hazards = (
                    filtered["precursor"].dropna().astype(str).value_counts()
                    .head(10).rename_axis("Precursor").reset_index(name="Reports")
                )
                st.dataframe(hazards, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            if "barrier_theme" in filtered.columns:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                section_title("Failed Barriers")
                barriers = (
                    filtered["barrier_theme"].dropna().astype(str).value_counts()
                    .head(10).rename_axis("Barrier").reset_index(name="Reports")
                )
                st.dataframe(barriers, use_container_width=True, hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("SIF-Potential Reports")

        sif_reports = filtered[filtered["sif_prediction"] == "SIF Potential"]

        display_columns = [
            column for column in ["report_id", "sif_probability", "sif_prediction", "precursor", "life_saving_rule"]
            if column in sif_reports.columns
        ]
        st.dataframe(
            sif_reports[display_columns].sort_values("sif_probability", ascending=False),
            use_container_width=True, hide_index=True,
        )
        download_csv_button(sif_reports[display_columns], "⬇️ Download SIF-potential reports (CSV)", f"sif_reports_{selected_activity}.csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # DECISION BRIEF
    # ========================================================
    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("📋 Current Safety Priorities")

        if not precursor.empty:
            top_precursor = precursor.iloc[0]
            st.warning(f"Leading precursor pattern: **{top_precursor.get('precursor', 'N/A')}**")

        if not barrier.empty:
            top_barrier = barrier.iloc[0]
            st.info(f"Leading barrier theme: **{top_barrier.get('barrier_theme', 'N/A')}**")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_title("Recommended Management Actions")

        actions = [
            "Prioritize HSE review of high-probability SIF reports.",
            "Investigate recurring precursor patterns.",
            "Review critical barrier failures and control effectiveness.",
            "Track changes in SIF density and precursor patterns over time.",
            "Validate analytical indicators against company-specific operational data before making high-consequence decisions.",
        ]
        for action in actions:
            st.markdown(f'<div class="reminder-box">{action}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# SIDEBAR HEADER
# ============================================================

ROLE_ICON = {
    "Employee / Worker": "🦺",
    "HSE Officer": "🛡️",
    "Management": "👔",
}


def sidebar_header(role, username, user_id):
    icon = ROLE_ICON.get(role, "🛡️")

    st.sidebar.markdown(
        f"""
        <p class="sidebar-brand">{icon} OIL SIF Intelligence</p>
        <span class="sidebar-role">{role}</span>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.caption(f"**{username}**  ·  ID `{user_id}`")
    st.sidebar.caption(datetime.now().strftime("%d %b %Y"))
    st.sidebar.markdown("---")

    if st.sidebar.button("Sign Out", use_container_width=True):
        logout()


# ============================================================
# MAIN
# ============================================================

def main():
    inject_css()

    if not login():
        return

    role = get_role()
    username = st.session_state.get("username", "user")
    user_id = get_user_id() or "—"

    sidebar_header(role, username, user_id)

    try:
        master, activity, lsr, precursor, barrier, queue = load_all_data()
    except Exception as e:
        st.error("Dataset loading failed.")
        st.exception(e)
        st.stop()

    if role == "Employee / Worker":
        worker_dashboard(master, lsr, precursor)
    elif role == "HSE Officer":
        hse_command_center(master, activity, lsr, precursor, barrier, queue)
    elif role == "Management":
        management_dashboard(master, activity, precursor, barrier)
    else:
        st.error("Unknown user role.")


if __name__ == "__main__":
    main()
