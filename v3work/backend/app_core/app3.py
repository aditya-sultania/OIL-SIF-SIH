import re
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from chatbot.auth import (
    login,
    logout,
    get_role,
    get_display_name,
    ROLE_META,
)
from chatbot.assistant import answer_question
from chatbot.gemini_chat import translate_text


# ============================================================
# PATHS / MODELS
# ============================================================

ROOT = Path(__file__).resolve().parent

SIF_MODEL = joblib.load(ROOT / "SIF_Model_v4_DomainAware.joblib")
LSR_MODEL = joblib.load(ROOT / "IOGP_Life_Saving_Rule_Classifier_v2.joblib")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OIL SIF Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

LANGUAGES = [
    "English", "Hindi", "Assamese", "Bengali", "Odia", "Tamil",
    "Telugu", "Marathi", "Gujarati", "Punjabi", "Spanish", "French",
]


# ============================================================
# THEME / CSS
# ============================================================

def inject_css(theme="dark"):

    if theme == "dark":
        app_bg = "linear-gradient(160deg,#05070f 0%,#0b1220 45%,#141a2e 100%)"
        sidebar_bg = "linear-gradient(180deg,#0b1220,#111827)"
        text_color = "#e2e8f0"
        muted = "#94a3b8"
        card_bg = "rgba(255,255,255,0.045)"
        card_border = "rgba(148,163,184,0.16)"
    else:
        app_bg = "linear-gradient(160deg,#f8fafc 0%,#eef2ff 55%,#f5f3ff 100%)"
        sidebar_bg = "linear-gradient(180deg,#ffffff,#f1f5f9)"
        text_color = "#0f172a"
        muted = "#475569"
        card_bg = "rgba(15,23,42,0.035)"
        card_border = "rgba(15,23,42,0.10)"

    st.markdown(
        f"""
        <style>

        @keyframes fadeInUp {{
            from {{opacity: 0; transform: translateY(16px);}}
            to {{opacity: 1; transform: translateY(0);}}
        }}
        @keyframes gradientShift {{
            0% {{background-position: 0% 50%;}}
            50% {{background-position: 100% 50%;}}
            100% {{background-position: 0% 50%;}}
        }}
        @keyframes pulseGlow {{
            0% {{box-shadow: 0 0 0 0 rgba(99,102,241,0.35);}}
            70% {{box-shadow: 0 0 0 12px rgba(99,102,241,0);}}
            100% {{box-shadow: 0 0 0 0 rgba(99,102,241,0);}}
        }}

        [data-testid="stAppViewContainer"] {{
            background: {app_bg};
            color: {text_color};
        }}

        [data-testid="stSidebar"] {{
            background: {sidebar_bg};
            border-right: 1px solid {card_border};
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        .block-container {{
            padding-top: 1.1rem;
            padding-bottom: 3rem;
            animation: fadeInUp .45s ease;
        }}

        h1, h2, h3, h4, p, span, label, .stMarkdown {{
            color: {text_color};
        }}

        .hero {{
            padding: 1.5rem 1.8rem;
            border-radius: 20px;
            background: linear-gradient(120deg, var(--accent-1), var(--accent-2), var(--accent-3));
            background-size: 220% 220%;
            animation: gradientShift 10s ease infinite, fadeInUp .5s ease;
            color: white;
            margin-bottom: 1.3rem;
            box-shadow: 0 16px 40px rgba(0,0,0,0.28);
        }}
        .hero h1 {{
            margin: 0;
            font-size: 2.05rem;
            color: white !important;
        }}
        .hero p {{
            margin: .45rem 0 0;
            color: rgba(255,255,255,0.9) !important;
            font-size: 1rem;
        }}

        .profile-card {{
            padding: .9rem 1rem;
            border-radius: 16px;
            background: {card_bg};
            border: 1px solid {card_border};
            margin-bottom: .8rem;
            animation: fadeInUp .5s ease;
        }}
        .profile-avatar {{
            font-size: 1.8rem;
            display: inline-block;
            margin-right: .5rem;
        }}
        .profile-name {{
            font-weight: 700;
            font-size: 1.02rem;
        }}
        .profile-role {{
            font-size: .8rem;
            color: {muted};
        }}

        .metric-card {{
            padding: 1rem 1.1rem;
            border-radius: 16px;
            background: {card_bg};
            border: 1px solid {card_border};
            transition: transform .18s ease, box-shadow .18s ease;
            animation: fadeInUp .5s ease;
            height: 100%;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 14px 30px rgba(0,0,0,0.20);
        }}
        .metric-icon {{
            font-size: 1.4rem;
        }}
        .metric-value {{
            font-size: 1.7rem;
            font-weight: 800;
            margin-top: .15rem;
        }}
        .metric-label {{
            font-size: .82rem;
            color: {muted};
            text-transform: uppercase;
            letter-spacing: .04em;
        }}

        .chip {{
            display: inline-block;
            padding: .28rem .75rem;
            margin: .18rem .25rem .18rem 0;
            border-radius: 999px;
            font-size: .8rem;
            font-weight: 600;
            color: white;
            animation: fadeInUp .4s ease;
        }}

        .badge-lg {{
            display: inline-block;
            padding: .5rem 1.1rem;
            border-radius: 12px;
            font-size: 1.05rem;
            font-weight: 800;
            color: white;
            animation: pulseGlow 2.4s infinite;
        }}

        .glass-panel {{
            padding: 1.2rem 1.4rem;
            border-radius: 18px;
            background: {card_bg};
            border: 1px solid {card_border};
            animation: fadeInUp .5s ease;
            margin-bottom: 1rem;
        }}

        div[role="radiogroup"] > label {{
            background: {card_bg};
            border: 1px solid {card_border};
            padding: .5rem .9rem;
            border-radius: 12px;
            margin-bottom: .35rem;
            transition: all .15s ease;
            width: 100%;
        }}
        div[role="radiogroup"] > label:hover {{
            border-color: var(--accent-2);
            transform: translateX(2px);
        }}

        .stButton>button {{
            border-radius: 12px;
            font-weight: 600;
            transition: transform .15s ease;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
        }}

        [data-testid="stChatMessage"] {{
            animation: fadeInUp .35s ease;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


ROLE_ACCENTS = {
    "Employee / Worker": ("#059669", "#10b981", "#34d399"),
    "HSE Officer": ("#b45309", "#f59e0b", "#fbbf24"),
    "Management": ("#4338ca", "#6366f1", "#818cf8"),
    None: ("#1e293b", "#334155", "#475569"),
}


def set_role_accent(role):
    a1, a2, a3 = ROLE_ACCENTS.get(role, ROLE_ACCENTS[None])
    st.markdown(
        f"<style>:root {{ --accent-1:{a1}; --accent-2:{a2}; --accent-3:{a3}; }}</style>",
        unsafe_allow_html=True,
    )


def header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card_html(label, value, icon, color):
    return f"""
    <div class="metric-card" style="border-top:3px solid {color};">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value, icon, color) in zip(cols, items):
        with col:
            st.markdown(metric_card_html(label, value, icon, color), unsafe_allow_html=True)


def chip(text, color="#6366f1"):
    return f'<span class="chip" style="background:{color};">{text}</span>'


def chips_row(items, color="#6366f1", empty_text="None detected"):
    if not items:
        st.caption(empty_text)
        return
    st.markdown("".join(chip(i, color) for i in items), unsafe_allow_html=True)


def badge_large(text, color):
    st.markdown(
        f'<span class="badge-lg" style="background:{color};">{text}</span>',
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_all_data():

    master = pd.read_csv(ROOT / "SIF_Dashboard_Master_v4.csv", low_memory=False)
    activity = pd.read_csv(ROOT / "SIF_Activity_Ranking_v4.csv")
    lsr = pd.read_csv(ROOT / "SIF_LSR_Ranking_v4.csv")
    precursor = pd.read_csv(ROOT / "SIF_Precursor_Ranking_v4.csv")
    barrier = pd.read_csv(ROOT / "SIF_Barrier_Ranking_v4.csv")
    queue = pd.read_csv(ROOT / "SIF_HSE_Review_Queue_v2.csv", low_memory=False)

    return master, activity, lsr, precursor, barrier, queue


# ============================================================
# SAFETY / CLASSIFICATION RULES
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


# ============================================================
# HELPERS
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
        probability, prediction, high_risk, precursors, activities,
        lsr_keywords, lsr_predictions, barriers, explain(text),
    )


def recommended_action(level, high_risk):
    if level == "High Priority":
        return "🚨 Stop work if the hazard is still present. Escalate immediately to HSE for priority investigation and verify critical controls before resuming."
    if level == "HSE Review":
        return "🟡 Flag for HSE review. Verify the relevant Life-Saving Rule controls were in place and close out any barrier gaps found."
    return "🟢 Log for routine tracking. No immediate escalation required, but continue monitoring for recurrence."


def simple_explanation(prediction, precursors, activities, lsr_keywords, barriers):
    parts = []

    if activities:
        parts.append(f"work involving **{', '.join(activities).lower()}**")
    if precursors:
        parts.append(f"hazard signals for **{', '.join(precursors).lower()}**")
    if lsr_keywords:
        parts.append(f"possible **{', '.join(lsr_keywords)}** Life-Saving Rule relevance")
    if barriers:
        parts.append(f"indications of **{', '.join(barriers).lower()}**")

    if not parts:
        return f"The model classified this report as **{prediction}**, with no strong keyword-based hazard signals detected in the text."

    return f"The model classified this report as **{prediction}**, based on " + "; ".join(parts) + "."


def gauge_chart(probability, theme="dark"):
    color = "#ef4444" if probability >= 0.7 else "#f59e0b" if probability >= 0.3 else "#10b981"
    font_color = "#e2e8f0" if theme == "dark" else "#0f172a"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(probability * 100, 1),
        number={"suffix": "%", "font": {"size": 34, "color": font_color}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": font_color},
            "bar": {"color": color},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, 30], "color": "rgba(16,185,129,0.25)"},
                {"range": [30, 70], "color": "rgba(245,158,11,0.25)"},
                {"range": [70, 100], "color": "rgba(239,68,68,0.25)"},
            ],
        },
        title={"text": "SIF Probability", "font": {"color": font_color}},
    ))
    fig.update_layout(
        height=250, margin=dict(l=20, r=20, t=45, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font={"color": font_color},
    )
    return fig


# ============================================================
# ANALYZE & EXPLAIN (XAI) — the feature that was missing
# ============================================================

def analyze_explain_page(theme, simple_mode=False):

    header(
        "🔬 Analyze & Explain" if not simple_mode else "🔎 Quick Safety Check",
        "Paste an incident / hazard description to get an instant SIF assessment."
        if not simple_mode else
        "Describe a hazard or unsafe act to get instant, easy-to-read safety guidance.",
    )

    default_text = st.session_state.get("analyze_sample", "")

    text = st.text_area(
        "Report / observation text",
        value=default_text,
        height=140,
        placeholder="e.g. Worker was performing hot work near a confined space without verified isolation...",
    )

    c1, c2 = st.columns([1, 3])
    run = c1.button("🔍 Analyze", type="primary", use_container_width=True)

    if not run:
        st.info("Enter a description above and click **Analyze** to see the assessment.")
        return

    if not text or not text.strip():
        st.warning("Please enter some text to analyze.")
        return

    with st.spinner("Running SIF model, LSR classifier and rule-based checks..."):
        (
            probability, prediction, high_risk, precursors, activities,
            lsr_keywords, lsr_predictions, barriers, (positive, negative),
        ) = analyze(text)

    level = review_level(probability, high_risk)
    level_color = {"High Priority": "#ef4444", "HSE Review": "#f59e0b", "Normal": "#10b981"}[level]
    pred_color = "#ef4444" if prediction == "SIF Potential" else "#10b981"

    st.markdown("<br>", unsafe_allow_html=True)

    if high_risk:
        st.error(f"⚠️ **High-Risk Safety Backstop triggered:** {', '.join(high_risk)}. This overrides the raw model score.")

    top_row = st.columns([1, 1, 1]) if not simple_mode else st.columns([1, 1])

    with top_row[0]:
        st.markdown("**Prediction**")
        badge_large(prediction, pred_color)

    with top_row[1]:
        st.markdown("**Review Priority**")
        badge_large(level, level_color)

    if not simple_mode:
        with top_row[2]:
            st.plotly_chart(gauge_chart(probability, theme), use_container_width=True)

    st.markdown("---")
    st.subheader("🗣️ Plain-language explanation")
    st.markdown(simple_explanation(prediction, precursors, activities, lsr_keywords, barriers))

    st.subheader("✅ Recommended action")
    st.success(recommended_action(level, high_risk))

    st.subheader("🏷️ Detected signals")
    d1, d2 = st.columns(2)
    with d1:
        st.caption("Activity")
        chips_row(activities, "#6366f1")
        st.caption("Precursor")
        chips_row(precursors, "#f59e0b")
    with d2:
        st.caption("Life-Saving Rule keywords")
        chips_row(lsr_keywords, "#ef4444")
        st.caption("Barrier theme")
        chips_row(barriers, "#0ea5e9")

    if lsr_predictions:
        st.subheader("🛡️ Most likely Life-Saving Rule (model)")
        lsr_df = pd.DataFrame(lsr_predictions, columns=["Life-Saving Rule", "Confidence"])
        st.plotly_chart(
            px.bar(lsr_df, x="Confidence", y="Life-Saving Rule", orientation="h",
                   range_x=[0, 1], color="Confidence", color_continuous_scale="Oranges"),
            use_container_width=True,
        )

    if not simple_mode:
        with st.expander("🧪 Technical XAI — model feature contributions"):
            pcol, ncol = st.columns(2)

            with pcol:
                st.caption("Pushes toward SIF Potential")
                if positive:
                    pdf = pd.DataFrame(positive, columns=["term", "weight"])
                    st.plotly_chart(
                        px.bar(pdf, x="weight", y="term", orientation="h", color_discrete_sequence=["#ef4444"]),
                        use_container_width=True,
                    )
                else:
                    st.caption("No positive contributions found.")

            with ncol:
                st.caption("Pushes toward Non-SIF")
                if negative:
                    ndf = pd.DataFrame(negative, columns=["term", "weight"])
                    st.plotly_chart(
                        px.bar(ndf, x="weight", y="term", orientation="h", color_discrete_sequence=["#10b981"]),
                        use_container_width=True,
                    )
                else:
                    st.caption("No negative contributions found.")

            st.caption(
                "These weights come from the linear SIF model's coefficients and are a "
                "development-stage indicator, not a certified causal explanation."
            )


# ============================================================
# WORKER DASHBOARD
# ============================================================

def worker_dashboard(master, lsr, precursor, theme):

    page = st.sidebar.radio(
        "Workspace",
        ["🏠 Safety Home", "📊 My Safety View", "🔎 Quick Safety Check"],
    )

    if page == "🏠 Safety Home":

        header("🦺 Worker Safety Dashboard", "Practical safety intelligence without sensitive management information.")

        sif_count = int((master["sif_prediction"] == "SIF Potential").sum()) if "sif_prediction" in master.columns else 0

        if "precursor" in master.columns:
            common_hazard_series = master["precursor"].dropna().astype(str).value_counts()
        else:
            common_hazard_series = pd.Series(dtype=int)

        top_hazard = common_hazard_series.index[0] if len(common_hazard_series) else "N/A"

        metric_row([
            ("Safety Reports", f"{len(master):,}", "📄", "#10b981"),
            ("Common Hazard", top_hazard, "⚠️", "#f59e0b"),
            ("SIF-Potential Reports", f"{sif_count:,}", "🚨", "#ef4444"),
        ])

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.subheader("⚠️ Common Hazards")
            if len(common_hazard_series):
                hazards = common_hazard_series.head(8).rename_axis("Hazard").reset_index(name="Reports")
                st.dataframe(hazards, use_container_width=True, hide_index=True)
            else:
                st.info("No hazard information available.")

            st.subheader("🛡️ Top Life-Saving Rules")
            if not lsr.empty:
                st.dataframe(lsr.head(8), use_container_width=True, hide_index=True)

        with col2:
            st.subheader("✅ Safety Reminders")
            reminders = [
                "Verify energy isolation before starting maintenance.",
                "Stay outside the line of fire of moving equipment and suspended loads.",
                "Use appropriate protection for work at height.",
                "Maintain separation between pedestrians and mobile equipment.",
                "Report recurring unsafe conditions to HSE.",
            ]
            for reminder in reminders:
                st.info(reminder)

    elif page == "📊 My Safety View":

        header("📊 My Safety View", "Select an activity to view its recurring safety patterns.")

        if "activity_group" not in master.columns:
            st.info("Activity information is unavailable.")
            return

        activities = sorted(master["activity_group"].dropna().astype(str).unique())
        selected_activity = st.selectbox("Activity", activities)

        filtered = master[master["activity_group"].astype(str) == selected_activity]

        metric_row([("Reports for this activity", f"{len(filtered):,}", "📄", "#6366f1")])

        if "precursor" in filtered.columns:
            hazards = (
                filtered["precursor"].dropna().astype(str).value_counts()
                .head(8).rename_axis("Hazard").reset_index(name="Reports")
            )
            st.subheader("Recurring Hazards")
            st.dataframe(hazards, use_container_width=True, hide_index=True)

        st.subheader("Recommended Precautions")
        for precaution in [
            "Follow the applicable Life-Saving Rules for the task.",
            "Verify critical controls before beginning work.",
            "Maintain awareness of line-of-fire exposures.",
            "Report unsafe conditions and recurring hazards.",
            "Stop work when critical controls are missing.",
        ]:
            st.write("• " + precaution)

    else:
        analyze_explain_page(theme, simple_mode=True)


# ============================================================
# HSE COMMAND CENTER
# ============================================================

def hse_command_center(master, activity, lsr, precursor, barrier, queue, theme):

    page = st.sidebar.radio(
        "Workspace",
        ["🛡️ Command Center", "📋 SIF Queue", "📈 Trend & Precursor Lab", "🔬 Analyze & Explain", "🤖 AI Safety Assistant"],
    )

    if page == "🛡️ Command Center":

        header("🛡️ HSE Safety Officer Command Center", "Full SIF analytics, risk prioritization and safety intelligence.")

        total = len(master)
        sif_count = int((master["sif_prediction"] == "SIF Potential").sum())
        sif_rate = sif_count / total * 100 if total else 0
        mean_probability = master["sif_probability"].mean() if "sif_probability" in master.columns else 0

        metric_row([
            ("Analyzed Reports", f"{total:,}", "📄", "#f59e0b"),
            ("SIF Potential", f"{sif_count:,}", "🚨", "#ef4444"),
            ("SIF Density", f"{sif_rate:.2f}%", "📉", "#0ea5e9"),
            ("Mean SIF Probability", f"{mean_probability:.1%}", "🎯", "#8b5cf6"),
        ])

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            risk = master["sif_prediction"].value_counts().rename_axis("Prediction").reset_index(name="Reports")
            st.plotly_chart(
                px.bar(risk, x="Prediction", y="Reports", title="SIF Prediction Distribution",
                       color="Prediction", color_discrete_sequence=["#ef4444", "#10b981"]),
                use_container_width=True,
            )

        with col2:
            if "precursor" in master.columns:
                precursor_counts = (
                    master["precursor"].dropna().astype(str).value_counts()
                    .head(10).rename_axis("Precursor").reset_index(name="Reports")
                )
                st.plotly_chart(
                    px.bar(precursor_counts, x="Reports", y="Precursor", orientation="h",
                           title="Top Precursor Patterns", color="Reports", color_continuous_scale="Oranges"),
                    use_container_width=True,
                )

        st.subheader("Top Activity Risk")
        st.dataframe(activity.head(10), use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Export Activity Ranking (CSV)",
            activity.to_csv(index=False).encode("utf-8"),
            file_name="activity_ranking.csv",
            mime="text/csv",
        )

    elif page == "📋 SIF Queue":

        header("📋 SIF Review Queue", "Prioritized reports requiring HSE attention.")

        if "activity_group" not in master.columns:
            st.warning("Activity information unavailable.")
            return

        activities = ["All"] + sorted(master["activity_group"].dropna().astype(str).unique())
        precursors = ["All"] + sorted(master["precursor"].dropna().astype(str).unique())

        c1, c2, c3 = st.columns(3)
        selected_activity = c1.selectbox("Activity", activities)
        selected_precursor = c2.selectbox("Precursor", precursors)
        minimum_probability = c3.slider("Minimum SIF Probability", 0.0, 1.0, 0.30, 0.01)

        filtered = master.copy()

        if selected_activity != "All":
            filtered = filtered[filtered["activity_group"] == selected_activity]
        if selected_precursor != "All":
            filtered = filtered[filtered["precursor"] == selected_precursor]

        filtered = filtered[filtered["sif_probability"] >= minimum_probability]
        filtered = filtered.sort_values("sif_probability", ascending=False)

        display_columns = [c for c in [
            "report_id", "date_of_incident", "sif_probability", "sif_prediction",
            "confidence_band", "activity_group", "precursor", "life_saving_rule",
            "hse_review_status", "priority_score",
        ] if c in filtered.columns]

        st.dataframe(filtered[display_columns].head(500), use_container_width=True, hide_index=True)
        st.caption(f"Showing up to 500 of {len(filtered):,} matching reports.")

        st.download_button(
            "⬇️ Export filtered queue (CSV)",
            filtered[display_columns].to_csv(index=False).encode("utf-8"),
            file_name="sif_queue_filtered.csv",
            mime="text/csv",
        )

        st.subheader("🔎 Individual Report")

        if "report_id" in filtered.columns and not filtered.empty:
            report_ids = filtered["report_id"].astype(str).tolist()
            selected_report = st.selectbox("Select Report", report_ids)
            report = filtered[filtered["report_id"].astype(str) == selected_report].iloc[0]
            st.json(report.to_dict())

            report_text = report.get("report_text") if "report_text" in filtered.columns else None
            if report_text and st.button("🔬 Run full Analyze & Explain on this report"):
                st.session_state["analyze_sample"] = str(report_text)
                st.session_state["_jump_to_analyze"] = True
                st.info("Sample loaded — open **Analyze & Explain** from the sidebar to view it.")

    elif page == "📈 Trend & Precursor Lab":

        header("📈 Trend & Precursor Lab", "Recurring patterns, SIF trends and Life-Saving Rule analysis.")

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
                st.plotly_chart(
                    px.line(monthly, x="month", y=["reports", "sif"], title="Monthly Report and SIF-Potential Trend",
                            color_discrete_sequence=["#6366f1", "#ef4444"]),
                    use_container_width=True,
                )

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Recurring Precursors")
            st.dataframe(precursor, use_container_width=True, hide_index=True)
        with col2:
            st.subheader("Life-Saving Rules")
            st.dataframe(lsr, use_container_width=True, hide_index=True)

        st.subheader("Barrier Failure Patterns")
        st.dataframe(barrier, use_container_width=True, hide_index=True)

    elif page == "🔬 Analyze & Explain":

        if st.session_state.get("_jump_to_analyze"):
            st.session_state["_jump_to_analyze"] = False

        analyze_explain_page(theme, simple_mode=False)

    else:
        ai_safety_assistant()


# ============================================================
# AI SAFETY ASSISTANT (multilingual)
# ============================================================

def ai_safety_assistant():

    header("🤖 AI Safety Assistant", "Ask natural-language questions about the OIL SIF dataset — in any language.")

    st.caption(
        "The assistant uses Gemini and dataset tools. "
        "Dataset-derived information is returned from the underlying data rather than invented."
    )

    top1, top2 = st.columns([2, 1])

    with top2:
        language = st.selectbox(
            "🌐 Reply language",
            LANGUAGES,
            index=LANGUAGES.index(st.session_state.get("chat_language", "English")),
            key="chat_language_select",
        )
        st.session_state.chat_language = language

    with top1:
        if st.button("🗑️ Clear Conversation"):
            st.session_state.chat_history = []
            st.session_state.gemini_chat = None
            st.rerun()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = None

    for i, (role_name, message) in enumerate(st.session_state.chat_history):
        with st.chat_message(role_name):
            st.markdown(message)
            if role_name == "assistant":
                with st.popover("🌐 Translate this reply"):
                    target = st.selectbox(
                        "Translate to", LANGUAGES, key=f"translate_target_{i}",
                    )
                    if st.button("Translate", key=f"translate_btn_{i}"):
                        with st.spinner("Translating..."):
                            translated = translate_text(message, target)
                        st.markdown(f"**{target}:**\n\n{translated}")

    question = st.chat_input("Ask about incidents, SIF risk, precursors, barriers... (any language)")

    if question:
        st.session_state.chat_history.append(("user", question))
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing the SIF dataset..."):
                answer, chat = answer_question(
                    question, st.session_state.gemini_chat, language=st.session_state.chat_language,
                )
                st.session_state.gemini_chat = chat
                st.markdown(answer)

        st.session_state.chat_history.append(("assistant", answer))


# ============================================================
# MANAGEMENT DASHBOARD
# ============================================================

def management_dashboard(master, activity, precursor, barrier):

    page = st.sidebar.radio(
        "Workspace",
        ["👔 Executive Overview", "🏆 Risk Ranking", "🔎 Risk Drill-down", "📋 Decision Brief"],
    )

    header("👔 Management Decision Dashboard", "High-level safety intelligence for decision-making.")

    if page == "👔 Executive Overview":

        total = len(master)
        sif_count = int((master["sif_prediction"] == "SIF Potential").sum())
        sif_rate = sif_count / total * 100 if total else 0

        metric_row([
            ("Total Reports", f"{total:,}", "📄", "#6366f1"),
            ("SIF-Potential Reports", f"{sif_count:,}", "🚨", "#ef4444"),
            ("SIF Density", f"{sif_rate:.2f}%", "📉", "#8b5cf6"),
        ])

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Activity Risk Overview")

        display = activity.copy()

        if "sif_density_pct" in display.columns:
            def risk_label(value):
                if value >= 50:
                    return "🔴 High"
                if value >= 25:
                    return "🟡 Moderate"
                return "🟢 Lower"
            display["Risk Level"] = display["sif_density_pct"].apply(risk_label)

        columns = [c for c in ["activity_group", "total_reports", "sif_reports", "sif_density_pct", "Risk Level"] if c in display.columns]
        st.dataframe(display[columns], use_container_width=True, hide_index=True)

        if "sif_density_pct" in activity.columns:
            st.plotly_chart(
                px.bar(activity, x="sif_density_pct", y="activity_group", orientation="h",
                       title="SIF Density by Activity", color="sif_density_pct", color_continuous_scale="Purples"),
                use_container_width=True,
            )

        st.download_button(
            "⬇️ Export Executive Summary (CSV)",
            display[columns].to_csv(index=False).encode("utf-8"),
            file_name="executive_activity_overview.csv",
            mime="text/csv",
        )

    elif page == "🏆 Risk Ranking":

        st.subheader("Risk Ranking by Activity")
        st.caption("This ranking uses the supplied SIF analytical dataset. It is not a claim that a site or department is inherently unsafe.")

        ranking_columns = [c for c in ["rank", "activity_group", "total_reports", "sif_reports", "sif_density_pct", "reliability"] if c in activity.columns]
        st.dataframe(activity[ranking_columns], use_container_width=True, hide_index=True)

        st.subheader("Leading Precursors")
        st.dataframe(precursor.head(10), use_container_width=True, hide_index=True)

    elif page == "🔎 Risk Drill-down":

        st.subheader("🔎 Risk Drill-down")

        if "activity_group" not in master.columns:
            st.info("Activity information is unavailable.")
            return

        activities = sorted(master["activity_group"].dropna().astype(str).unique())
        selected_activity = st.selectbox("Activity", activities)

        filtered = master[master["activity_group"].astype(str) == selected_activity]

        metric_row([("Reports", f"{len(filtered):,}", "📄", "#6366f1")])

        if "sif_prediction" in filtered.columns:
            sif_count = int((filtered["sif_prediction"] == "SIF Potential").sum())
            metric_row([("SIF-Potential Reports", f"{sif_count:,}", "🚨", "#ef4444")])

        if "precursor" in filtered.columns:
            st.subheader("Hazard / Precursor")
            hazards = filtered["precursor"].dropna().astype(str).value_counts().head(10).rename_axis("Precursor").reset_index(name="Reports")
            st.dataframe(hazards, use_container_width=True, hide_index=True)

        if "barrier_theme" in filtered.columns:
            st.subheader("Failed Barriers")
            barriers = filtered["barrier_theme"].dropna().astype(str).value_counts().head(10).rename_axis("Barrier").reset_index(name="Reports")
            st.dataframe(barriers, use_container_width=True, hide_index=True)

        st.subheader("SIF-Potential Reports")
        sif_reports = filtered[filtered["sif_prediction"] == "SIF Potential"]
        display_columns = [c for c in ["report_id", "sif_probability", "sif_prediction", "precursor", "life_saving_rule"] if c in sif_reports.columns]
        st.dataframe(sif_reports[display_columns].sort_values("sif_probability", ascending=False), use_container_width=True, hide_index=True)

    else:
        st.subheader("📋 Decision Brief")
        st.markdown("### Current Safety Priorities")

        if not precursor.empty:
            top_precursor = precursor.iloc[0]
            st.warning(f"Leading precursor pattern: **{top_precursor.get('precursor', 'N/A')}**")

        if not barrier.empty:
            top_barrier = barrier.iloc[0]
            st.info(f"Leading barrier theme: **{top_barrier.get('barrier_theme', 'N/A')}**")

        st.markdown("### Recommended Management Actions")
        for action in [
            "Prioritize HSE review of high-probability SIF reports.",
            "Investigate recurring precursor patterns.",
            "Review critical barrier failures and control effectiveness.",
            "Track changes in SIF density and precursor patterns over time.",
            "Validate analytical indicators against company-specific operational data before making high-consequence decisions.",
        ]:
            st.write("• " + action)


# ============================================================
# SIDEBAR HEADER
# ============================================================

def sidebar_header(role):

    meta = ROLE_META.get(role, {"icon": "👤", "color": "#6366f1"})

    st.sidebar.markdown(
        f"""
        <div class="profile-card">
            <span class="profile-avatar">{meta['icon']}</span>
            <span class="profile-name">{get_display_name()}</span><br>
            <span class="profile-role">{role}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    theme_toggle = st.sidebar.toggle("🌙 Dark mode", value=(st.session_state.get("theme", "dark") == "dark"))
    st.session_state.theme = "dark" if theme_toggle else "light"

    st.sidebar.divider()

    if st.sidebar.button("🚪 Sign Out", use_container_width=True):
        logout()


# ============================================================
# MAIN
# ============================================================

def main():

    if not login():
        return

    theme = st.session_state.get("theme", "dark")
    role = get_role()

    inject_css(theme)
    set_role_accent(role)

    sidebar_header(role)

    try:
        master, activity, lsr, precursor, barrier, queue = load_all_data()
    except Exception as e:
        st.error("Dataset loading failed.")
        st.exception(e)
        st.stop()

    if role == "Employee / Worker":
        worker_dashboard(master, lsr, precursor, theme)
    elif role == "HSE Officer":
        hse_command_center(master, activity, lsr, precursor, barrier, queue, theme)
    elif role == "Management":
        management_dashboard(master, activity, precursor, barrier)
    else:
        st.error("Unknown user role.")


if __name__ == "__main__":
    main()
