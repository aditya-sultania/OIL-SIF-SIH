import re
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

from chatbot.auth import login, logout, get_role
from chatbot.assistant import answer_question


# ============================================================
# PATHS / MODELS
# ============================================================

ROOT = Path(__file__).resolve().parent

SIF_MODEL = joblib.load(
    ROOT / "SIF_Model_v4_DomainAware.joblib"
)

LSR_MODEL = joblib.load(
    ROOT / "IOGP_Life_Saving_Rule_Classifier_v2.joblib"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="OIL SIF Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

def inject_css():

    st.markdown(
        """
        <style>

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        .hero {
            padding: 1.4rem 1.6rem;
            border-radius: 18px;
            background: linear-gradient(
                135deg,
                #0b1220,
                #16243a
            );
            color: white;
            margin-bottom: 1.2rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 2.1rem;
        }

        .hero p {
            margin: .4rem 0 0;
            color: #cbd5e1;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HERO
# ============================================================

def header(title, subtitle):

    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_all_data():

    master = pd.read_csv(
        ROOT / "SIF_Dashboard_Master_v4.csv",
        low_memory=False
    )

    activity = pd.read_csv(
        ROOT / "SIF_Activity_Ranking_v4.csv"
    )

    lsr = pd.read_csv(
        ROOT / "SIF_LSR_Ranking_v4.csv"
    )

    precursor = pd.read_csv(
        ROOT / "SIF_Precursor_Ranking_v4.csv"
    )

    barrier = pd.read_csv(
        ROOT / "SIF_Barrier_Ranking_v4.csv"
    )

    queue = pd.read_csv(
        ROOT / "SIF_HSE_Review_Queue_v2.csv",
        low_memory=False
    )

    return (
        master,
        activity,
        lsr,
        precursor,
        barrier,
        queue
    )


# ============================================================
# SAFETY / CLASSIFICATION RULES
# ============================================================

HIGH_RISK = {

    "Confined Space":
        r"confined space|asphyxi|hydrogen sulfide|\bh2s\b|oxygen deficient|engulf",

    "Energy / Isolation":
        r"electrocution|electrical shock|arc flash|high voltage|energized|lock[- ]out|tag[- ]out|stored energy",

    "Line of Fire":
        r"caught between|pinned between|crushed between|suspended load|line of fire|struck by",

    "Working at Height":
        r"fall(?:ed|ing)? from|fall from height|roof|scaffold|tower|derrick",

    "Hot Work / Fire":
        r"explosion|flash fire|fireball|uncontrolled release|flammable gas",

    "Excavation":
        r"trench collapse|cave[- ]in|buried in|excavation collapse",

    "Pressure":
        r"high pressure|pressure release|pressurized|rupture",

    "Drowning / Water":
        r"drown(?:ed|ing)?|man overboard|submerged"
}


LSR = {

    "Energy Isolation":
        r"energized|high voltage|electrocution|electrical shock|arc flash|lock[- ]out|tag[- ]out|stored energy|isolation",

    "Hot Work":
        r"hot work|welding|cutting|grinding|flammable|explosion|fire",

    "Confined Space":
        r"confined space|asphyxi|hydrogen sulfide|\bh2s\b|oxygen deficient|engulf",

    "Line of Fire":
        r"line of fire|struck by|caught between|pinned between|crushed between|suspended load|falling object",

    "Working at Height":
        r"fall|roof|scaffold|tower|derrick|elevated platform",

    "Driving / Mobile Equipment":
        r"vehicle|forklift|truck|driving|excavat|mobile equipment",

    "Lifting Operations":
        r"lifting|load|rigging|hoist|crane|suspended load",

    "Excavation":
        r"excavat|trench|cave[- ]in|buried|collapse"
}


PREC = {

    "Energy / isolation":
        r"energized|high voltage|electrocution|electrical shock|arc flash|lock[- ]out|tag[- ]out|stored energy|power cable",

    "Confined space":
        r"confined space|asphyxi|hydrogen sulfide|\bh2s\b|oxygen deficient|engulf",

    "Line of fire":
        r"struck by|caught between|pinned between|crushed between|suspended load|falling object|line of fire",

    "Working at height":
        r"fall(?:ed|ing)? from|fall(?:ed|ing)? off|roof|scaffold|tower|derrick|elevated platform",

    "Hot work / fire":
        r"hot work|welding|cutting|grinding|explosion|flash fire|flammable",

    "Excavation":
        r"excavat|trench|cave[- ]in|buried|collapse",

    "Vehicle / mobile equipment":
        r"forklift|excavator|vehicle|run over|backed over|mobile equipment",

    "Machinery / guarding":
        r"caught in|entangled|unguarded|machine guard|interlock|bypass"
}


ACT = {

    "Maintenance":
        r"maintenance|repair|cleaning|servicing",

    "Material handling / lifting":
        r"lifting|load|rigging|hoist|material handling|crane",

    "Working at height":
        r"fall|roof|scaffold|tower|elevated",

    "Mobile equipment / vehicles":
        r"vehicle|forklift|truck|excavat|transport",

    "Machinery operation":
        r"machin|equipment|caught in|entangled",

    "Excavation":
        r"excavat|trench",

    "Welding / hot work":
        r"weld|cutting|grinding|hot work",

    "Electrical work":
        r"electric|electrical|power cable|energized"
}


BARR = {

    "Isolation failure":
        [
            "isolation",
            "isolat",
            "lock-out",
            "lockout",
            "tag-out",
            "tagout",
            "energized",
            "stored energy"
        ],

    "Permit / authorization failure":
        [
            "permit",
            "authorization",
            "work authorization"
        ],

    "Planning / risk assessment":
        [
            "planning",
            "risk assessment",
            "hazard assessment",
            "jsa",
            "job safety"
        ],

    "Communication failure":
        [
            "communication",
            "communicat",
            "handover",
            "coordination"
        ],

    "Supervision failure":
        [
            "supervision",
            "supervisor",
            "oversight"
        ],

    "Procedure failure":
        [
            "procedure",
            "procedural",
            "instruction",
            "standard"
        ],

    "Training / competency":
        [
            "training",
            "competenc",
            "qualified",
            "qualification"
        ],

    "Inspection / maintenance":
        [
            "inspection",
            "inspect",
            "maintenance",
            "defect",
            "equipment condition"
        ],

    "Safety control bypass":
        [
            "bypass",
            "interlock",
            "guard removed",
            "safety control"
        ]
}


# ============================================================
# HELPERS
# ============================================================

def hits(text, dictionary):

    return [
        key
        for key, pattern in dictionary.items()
        if re.search(pattern, text, re.I)
    ]


def explain(text):

    features = SIF_MODEL.named_steps["features"]
    clf = SIF_MODEL.named_steps["clf"]

    X = features.transform([text]).toarray()[0]

    names = features.get_feature_names_out()

    contributions = X * clf.coef_[0]

    positive = sorted(
        [
            (names[i], float(contributions[i]))
            for i in range(len(contributions))
            if contributions[i] > 0
        ],
        key=lambda x: x[1],
        reverse=True
    )[:8]

    negative = sorted(
        [
            (names[i], float(contributions[i]))
            for i in range(len(contributions))
            if contributions[i] < 0
        ],
        key=lambda x: x[1]
    )[:8]

    return positive, negative


def review_level(probability, high_risk):

    if high_risk or probability >= 0.70:
        return "High Priority"

    if probability >= 0.30:
        return "HSE Review"

    return "Normal"


def analyze(text):

    probability = float(
        SIF_MODEL.predict_proba([text])[0, 1]
    )

    high_risk = hits(
        text,
        HIGH_RISK
    )

    prediction = (
        "SIF Potential"
        if probability >= 0.5 or high_risk
        else "Non-SIF Potential"
    )

    probabilities = LSR_MODEL.predict_proba([text])[0]

    indexes = probabilities.argsort()[::-1][:3]

    lsr_predictions = [
        (
            str(LSR_MODEL.classes_[i]),
            float(probabilities[i])
        )
        for i in indexes
    ]

    precursors = hits(text, PREC)
    activities = hits(text, ACT)
    lsr_keywords = hits(text, LSR)

    barrier_patterns = {
        key: "|".join(
            map(re.escape, values)
        )
        for key, values in BARR.items()
    }

    barriers = hits(
        text,
        barrier_patterns
    )

    return (
        probability,
        prediction,
        high_risk,
        precursors,
        activities,
        lsr_keywords,
        lsr_predictions,
        barriers,
        explain(text)
    )


# ============================================================
# WORKER DASHBOARD
# ============================================================

def worker_dashboard(master, lsr, precursor):

    page = st.sidebar.radio(
        "Workspace",
        [
            "Safety Home",
            "My Safety View"
        ]
    )

    header(
        "🦺 Worker Safety Dashboard",
        "Practical safety intelligence without sensitive management information."
    )

    # --------------------------------------------------------
    # SAFETY HOME
    # --------------------------------------------------------

    if page == "Safety Home":

        sif_count = 0

        if "sif_prediction" in master.columns:

            sif_count = int(
                (
                    master["sif_prediction"]
                    == "SIF Potential"
                ).sum()
            )

        if "precursor" in master.columns:

            common_hazard_series = (
                master["precursor"]
                .dropna()
                .astype(str)
                .value_counts()
            )

        else:
            common_hazard_series = pd.Series(dtype=int)

        top_hazard = (
            common_hazard_series.index[0]
            if len(common_hazard_series)
            else "N/A"
        )

        a, b, c = st.columns(3)

        a.metric(
            "Safety Reports",
            f"{len(master):,}"
        )

        b.metric(
            "Common Hazard",
            top_hazard
        )

        c.metric(
            "SIF-Potential Reports",
            f"{sif_count:,}"
        )

        # ----------------------------------------------------
        # COMMON HAZARDS
        # ----------------------------------------------------

        st.subheader("⚠️ Common Hazards")

        if len(common_hazard_series):

            hazards = (
                common_hazard_series
                .head(8)
                .rename_axis("Hazard")
                .reset_index(name="Reports")
            )

            st.dataframe(
                hazards,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No hazard information available."
            )

        # ----------------------------------------------------
        # LIFE-SAVING RULES
        # ----------------------------------------------------

        st.subheader(
            "🛡️ Top Life-Saving Rules"
        )

        if not lsr.empty:

            st.dataframe(
                lsr.head(8),
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # SAFETY REMINDERS
        # ----------------------------------------------------

        st.subheader(
            "✅ Safety Reminders"
        )

        reminders = [
            "Verify energy isolation before starting maintenance.",
            "Stay outside the line of fire of moving equipment and suspended loads.",
            "Use appropriate protection for work at height.",
            "Maintain separation between pedestrians and mobile equipment.",
            "Report recurring unsafe conditions to HSE."
        ]

        for reminder in reminders:

            st.info(reminder)

    # --------------------------------------------------------
    # MY SAFETY VIEW
    # --------------------------------------------------------

    else:

        st.subheader(
            "My Safety View"
        )

        st.caption(
            "Select an activity to view its recurring safety patterns."
        )

        if "activity_group" not in master.columns:

            st.info(
                "Activity information is unavailable."
            )

            return

        activities = sorted(
            master["activity_group"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_activity = st.selectbox(
            "Activity",
            activities
        )

        filtered = master[
            master["activity_group"]
            .astype(str)
            == selected_activity
        ]

        st.metric(
            "Reports for this activity",
            f"{len(filtered):,}"
        )

        if "precursor" in filtered.columns:

            hazards = (
                filtered["precursor"]
                .dropna()
                .astype(str)
                .value_counts()
                .head(8)
                .rename_axis("Hazard")
                .reset_index(name="Reports")
            )

            st.subheader(
                "Recurring Hazards"
            )

            st.dataframe(
                hazards,
                use_container_width=True,
                hide_index=True
            )

        st.subheader(
            "Recommended Precautions"
        )

        precautions = [
            "Follow the applicable Life-Saving Rules for the task.",
            "Verify critical controls before beginning work.",
            "Maintain awareness of line-of-fire exposures.",
            "Report unsafe conditions and recurring hazards.",
            "Stop work when critical controls are missing."
        ]

        for precaution in precautions:

            st.write(
                "• " + precaution
            )


# ============================================================
# HSE COMMAND CENTER
# ============================================================

def hse_command_center(
    master,
    activity,
    lsr,
    precursor,
    barrier,
    queue
):

    page = st.sidebar.radio(
        "Workspace",
        [
            "HSE Command Center",
            "SIF Queue",
            "Trend & Precursor Lab",
            "AI Safety Assistant"
        ]
    )

    # ========================================================
    # HSE COMMAND CENTER
    # ========================================================

    if page == "HSE Command Center":

        header(
            "🛡️ HSE Safety Officer Command Center",
            "Full SIF analytics, risk prioritization and safety intelligence."
        )

        total = len(master)

        sif_count = int(
            (
                master["sif_prediction"]
                == "SIF Potential"
            ).sum()
        )

        sif_rate = (
            sif_count / total * 100
            if total
            else 0
        )

        mean_probability = (
            master["sif_probability"]
            .mean()
            if "sif_probability" in master.columns
            else 0
        )

        review_count = 0

        if "hse_review_status" in master.columns:

            review_count = int(
                (
                    master["hse_review_status"]
                    == "Review Suggested"
                ).sum()
            )

        a, b, c, d = st.columns(4)

        a.metric(
            "Analyzed Reports",
            f"{total:,}"
        )

        b.metric(
            "SIF Potential",
            f"{sif_count:,}"
        )

        c.metric(
            "SIF Density",
            f"{sif_rate:.2f}%"
        )

        d.metric(
            "Mean SIF Probability",
            f"{mean_probability:.1%}"
        )

        # ----------------------------------------------------
        # RISK DISTRIBUTION
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            risk = (
                master["sif_prediction"]
                .value_counts()
                .rename_axis("Prediction")
                .reset_index(name="Reports")
            )

            st.plotly_chart(
                px.bar(
                    risk,
                    x="Prediction",
                    y="Reports",
                    title="SIF Prediction Distribution"
                ),
                use_container_width=True
            )

        with col2:

            if "precursor" in master.columns:

                precursor_counts = (
                    master["precursor"]
                    .dropna()
                    .astype(str)
                    .value_counts()
                    .head(10)
                    .rename_axis("Precursor")
                    .reset_index(name="Reports")
                )

                st.plotly_chart(
                    px.bar(
                        precursor_counts,
                        x="Reports",
                        y="Precursor",
                        orientation="h",
                        title="Top Precursor Patterns"
                    ),
                    use_container_width=True
                )

        # ----------------------------------------------------
        # TOP ACTIVITIES
        # ----------------------------------------------------

        st.subheader(
            "Top Activity Risk"
        )

        st.dataframe(
            activity.head(10),
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # SIF QUEUE
    # ========================================================

    elif page == "SIF Queue":

        header(
            "📋 SIF Review Queue",
            "Prioritized reports requiring HSE attention."
        )

        if "activity_group" not in master.columns:

            st.warning(
                "Activity information unavailable."
            )

            return

        activities = [
            "All"
        ] + sorted(
            master["activity_group"]
            .dropna()
            .astype(str)
            .unique()
        )

        precursors = [
            "All"
        ] + sorted(
            master["precursor"]
            .dropna()
            .astype(str)
            .unique()
        )

        c1, c2, c3 = st.columns(3)

        selected_activity = c1.selectbox(
            "Activity",
            activities
        )

        selected_precursor = c2.selectbox(
            "Precursor",
            precursors
        )

        minimum_probability = c3.slider(
            "Minimum SIF Probability",
            0.0,
            1.0,
            0.30,
            0.01
        )

        filtered = master.copy()

        if selected_activity != "All":

            filtered = filtered[
                filtered["activity_group"]
                == selected_activity
            ]

        if selected_precursor != "All":

            filtered = filtered[
                filtered["precursor"]
                == selected_precursor
            ]

        filtered = filtered[
            filtered["sif_probability"]
            >= minimum_probability
        ]

        filtered = filtered.sort_values(
            "sif_probability",
            ascending=False
        )

        display_columns = [
            column
            for column in [
                "report_id",
                "date_of_incident",
                "sif_probability",
                "sif_prediction",
                "confidence_band",
                "activity_group",
                "precursor",
                "life_saving_rule",
                "hse_review_status",
                "priority_score"
            ]
            if column in filtered.columns
        ]

        st.dataframe(
            filtered[display_columns].head(500),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing up to 500 of {len(filtered):,} matching reports."
        )

        # ----------------------------------------------------
        # INDIVIDUAL REPORT DRILL-DOWN
        # ----------------------------------------------------

        st.subheader(
            "🔎 Individual Report"
        )

        if "report_id" in filtered.columns and not filtered.empty:

            report_ids = filtered[
                "report_id"
            ].astype(str).tolist()

            selected_report = st.selectbox(
                "Select Report",
                report_ids
            )

            report = filtered[
                filtered["report_id"]
                .astype(str)
                == selected_report
            ].iloc[0]

            st.json(
                report.to_dict()
            )


    # ========================================================
    # TREND & PRECURSOR LAB
    # ========================================================

    elif page == "Trend & Precursor Lab":

        header(
            "📈 Trend & Precursor Lab",
            "Recurring patterns, SIF trends and Life-Saving Rule analysis."
        )

        if "date_of_incident" in master.columns:

            trend_data = master.copy()

            trend_data["date_of_incident"] = pd.to_datetime(
                trend_data["date_of_incident"],
                errors="coerce"
            )

            trend_data = trend_data.dropna(
                subset=["date_of_incident"]
            )

            if not trend_data.empty:

                trend_data["month"] = (
                    trend_data["date_of_incident"]
                    .dt.to_period("M")
                    .dt.to_timestamp()
                )

                monthly = (
                    trend_data
                    .groupby("month")
                    .agg(
                        reports=("report_id", "count"),
                        sif=(
                            "sif_prediction",
                            lambda x:
                            (
                                x == "SIF Potential"
                            ).sum()
                        )
                    )
                    .reset_index()
                )

                st.plotly_chart(
                    px.line(
                        monthly,
                        x="month",
                        y=["reports", "sif"],
                        title="Monthly Report and SIF-Potential Trend"
                    ),
                    use_container_width=True
                )

        # ----------------------------------------------------
        # PRECURSORS
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "Recurring Precursors"
            )

            st.dataframe(
                precursor,
                use_container_width=True,
                hide_index=True
            )

        with col2:

            st.subheader(
                "Life-Saving Rules"
            )

            st.dataframe(
                lsr,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # BARRIERS
        # ----------------------------------------------------

        st.subheader(
            "Barrier Failure Patterns"
        )

        st.dataframe(
            barrier,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # AI SAFETY ASSISTANT
    # ========================================================

    else:

        header(
            "🤖 AI Safety Assistant",
            "Ask natural-language questions about the OIL SIF dataset."
        )

        st.caption(
            "The assistant uses Gemini and dataset tools. "
            "Dataset-derived information is returned from the underlying data rather than invented."
        )

        if "chat_history" not in st.session_state:

            st.session_state.chat_history = []

        if "gemini_chat" not in st.session_state:

            st.session_state.gemini_chat = None

        if st.button(
            "🗑️ Clear Conversation"
        ):

            st.session_state.chat_history = []

            st.session_state.gemini_chat = None

            st.rerun()

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        for role_name, message in st.session_state.chat_history:

            with st.chat_message(role_name):

                st.markdown(message)

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        question = st.chat_input(
            "Ask about incidents, SIF risk, precursors, barriers..."
        )

        if question:

            st.session_state.chat_history.append(
                ("user", question)
            )

            with st.chat_message("user"):

                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner(
                    "Analyzing the SIF dataset..."
                ):

                    answer, chat = answer_question(
                        question,
                        st.session_state.gemini_chat
                    )

                    st.session_state.gemini_chat = chat

                    st.markdown(answer)

            st.session_state.chat_history.append(
                ("assistant", answer)
            )


# ============================================================
# MANAGEMENT DASHBOARD
# ============================================================

def management_dashboard(
    master,
    activity,
    precursor,
    barrier
):

    page = st.sidebar.radio(
        "Workspace",
        [
            "Executive Overview",
            "Risk Ranking",
            "Risk Drill-down",
            "Decision Brief"
        ]
    )

    header(
        "👔 Management Decision Dashboard",
        "High-level safety intelligence for decision-making."
    )

    # ========================================================
    # EXECUTIVE OVERVIEW
    # ========================================================

    if page == "Executive Overview":

        total = len(master)

        sif_count = int(
            (
                master["sif_prediction"]
                == "SIF Potential"
            ).sum()
        )

        sif_rate = (
            sif_count / total * 100
            if total
            else 0
        )

        a, b, c = st.columns(3)

        a.metric(
            "Total Reports",
            f"{total:,}"
        )

        b.metric(
            "SIF-Potential Reports",
            f"{sif_count:,}"
        )

        c.metric(
            "SIF Density",
            f"{sif_rate:.2f}%"
        )

        st.subheader(
            "Activity Risk Overview"
        )

        display = activity.copy()

        if "sif_density_pct" in display.columns:

            def risk_label(value):

                if value >= 50:
                    return "🔴 High"

                if value >= 25:
                    return "🟡 Moderate"

                return "🟢 Lower"

            display["Risk Level"] = (
                display["sif_density_pct"]
                .apply(risk_label)
            )

        columns = [
            column
            for column in [
                "activity_group",
                "total_reports",
                "sif_reports",
                "sif_density_pct",
                "Risk Level"
            ]
            if column in display.columns
        ]

        st.dataframe(
            display[columns],
            use_container_width=True,
            hide_index=True
        )

        if "sif_density_pct" in activity.columns:

            st.plotly_chart(
                px.bar(
                    activity,
                    x="sif_density_pct",
                    y="activity_group",
                    orientation="h",
                    title="SIF Density by Activity"
                ),
                use_container_width=True
            )

    # ========================================================
    # RISK RANKING
    # ========================================================

    elif page == "Risk Ranking":

        st.subheader(
            "Risk Ranking by Activity"
        )

        st.caption(
            "This ranking uses the supplied SIF analytical dataset. "
            "It is not a claim that a site or department is inherently unsafe."
        )

        ranking_columns = [
            column
            for column in [
                "rank",
                "activity_group",
                "total_reports",
                "sif_reports",
                "sif_density_pct",
                "reliability"
            ]
            if column in activity.columns
        ]

        st.dataframe(
            activity[ranking_columns],
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "Leading Precursors"
        )

        st.dataframe(
            precursor.head(10),
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # RISK DRILL-DOWN
    # ========================================================

    elif page == "Risk Drill-down":

        st.subheader(
            "🔎 Risk Drill-down"
        )

        if "activity_group" not in master.columns:

            st.info(
                "Activity information is unavailable."
            )

            return

        activities = sorted(
            master["activity_group"]
            .dropna()
            .astype(str)
            .unique()
        )

        selected_activity = st.selectbox(
            "Activity",
            activities
        )

        filtered = master[
            master["activity_group"]
            .astype(str)
            == selected_activity
        ]

        st.metric(
            "Reports",
            f"{len(filtered):,}"
        )

        if "sif_prediction" in filtered.columns:

            sif_count = int(
                (
                    filtered["sif_prediction"]
                    == "SIF Potential"
                ).sum()
            )

            st.metric(
                "SIF-Potential Reports",
                f"{sif_count:,}"
            )

        # ----------------------------------------------------
        # HAZARDS
        # ----------------------------------------------------

        if "precursor" in filtered.columns:

            st.subheader(
                "Hazard / Precursor"
            )

            hazards = (
                filtered["precursor"]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .rename_axis("Precursor")
                .reset_index(name="Reports")
            )

            st.dataframe(
                hazards,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # BARRIERS
        # ----------------------------------------------------

        if "barrier_theme" in filtered.columns:

            st.subheader(
                "Failed Barriers"
            )

            barriers = (
                filtered["barrier_theme"]
                .dropna()
                .astype(str)
                .value_counts()
                .head(10)
                .rename_axis("Barrier")
                .reset_index(name="Reports")
            )

            st.dataframe(
                barriers,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # SIF REPORTS
        # ----------------------------------------------------

        st.subheader(
            "SIF-Potential Reports"
        )

        sif_reports = filtered[
            filtered["sif_prediction"]
            == "SIF Potential"
        ]

        display_columns = [
            column
            for column in [
                "report_id",
                "sif_probability",
                "sif_prediction",
                "precursor",
                "life_saving_rule"
            ]
            if column in sif_reports.columns
        ]

        st.dataframe(
            sif_reports[display_columns].sort_values(
                "sif_probability",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # DECISION BRIEF
    # ========================================================

    else:

        st.subheader(
            "📋 Decision Brief"
        )

        st.markdown(
            """
            ### Current Safety Priorities
            """
        )

        if not precursor.empty:

            top_precursor = precursor.iloc[0]

            st.warning(
                f"Leading precursor pattern: "
                f"**{top_precursor.get('precursor', 'N/A')}**"
            )

        if not barrier.empty:

            top_barrier = barrier.iloc[0]

            st.info(
                f"Leading barrier theme: "
                f"**{top_barrier.get('barrier_theme', 'N/A')}**"
            )

        st.markdown(
            """
            ### Recommended Management Actions
            """
        )

        actions = [
            "Prioritize HSE review of high-probability SIF reports.",
            "Investigate recurring precursor patterns.",
            "Review critical barrier failures and control effectiveness.",
            "Track changes in SIF density and precursor patterns over time.",
            "Validate analytical indicators against company-specific operational data before making high-consequence decisions."
        ]

        for action in actions:

            st.write(
                "• " + action
            )


# ============================================================
# SIDEBAR HEADER
# ============================================================

def sidebar_header(role):

    st.sidebar.title(
        "🛡️ OIL SIF Intelligence"
    )

    st.sidebar.caption(
        f"Signed in as **{role}**"
    )

    if st.sidebar.button(
        "Sign Out",
        use_container_width=True
    ):

        logout()


# ============================================================
# MAIN
# ============================================================

def main():

    inject_css()

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    if not login():
        return

    role = get_role()

    sidebar_header(role)

    # --------------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------------

    try:

        (
            master,
            activity,
            lsr,
            precursor,
            barrier,
            queue
        ) = load_all_data()

    except Exception as e:

        st.error(
            "Dataset loading failed."
        )

        st.exception(e)

        st.stop()

    # --------------------------------------------------------
    # ROLE ROUTING
    # --------------------------------------------------------

    if role == "Employee / Worker":

        worker_dashboard(
            master,
            lsr,
            precursor
        )

    elif role == "HSE Officer":

        hse_command_center(
            master,
            activity,
            lsr,
            precursor,
            barrier,
            queue
        )

    elif role == "Management":

        management_dashboard(
            master,
            activity,
            precursor,
            barrier
        )

    else:

        st.error(
            "Unknown user role."
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()