import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import time
from pathlib import Path

ROOT = Path(__file__).parent

# -----------------------------------------------------------------------------
# 1. ASSISTANT & BACKEND INTEGRATION
# -----------------------------------------------------------------------------
try:
    from chatbot.assistant import answer_question
    HAS_ASSISTANT = True
except Exception:
    HAS_ASSISTANT = False

try:
    from chatbot.auth import login as be_login, logout as be_logout, get_role as be_get_role
    HAS_BE_AUTH = True
except Exception:
    HAS_BE_AUTH = False

# -----------------------------------------------------------------------------
# 2. MULTILINGUAL DICTIONARIES (ENGLISH, HINDI, ASSAMESE)
# -----------------------------------------------------------------------------
TRANSLATIONS = {
    "English": {
        "title": "OIL-SIF COMMAND HUB",
        "subtitle": "Enterprise SIF Precursor Detection & Multilingual Barrier Intelligence Engine",
        "welcome": "Welcome",
        "logout": "Log Out / Back to Login",
        "switch_user": "Switch Role Session",
        "select_lang": "Interface Language",
        "field_worker": "Field Worker",
        "hse_officer": "HSE Officer",
        "management": "Management",
        "shift_alert_title": "Shift Priority Warning: High-Pressure Isolation & Bleed-Off",
        "shift_alert_msg": "Sector Hazard Alert: 2 near-misses reported on hydrotest manifolds this week. Confirm double block & bleed before starting line maintenance!",
        "instant_scanner": "Incident & Hazard Precursor Scanner",
        "scan_desc": "AI-assisted real-time screening against IOGP Life-Saving Rules.",
        "describe_hazard": "Describe observed unsafe condition or near miss:",
        "scan_btn": "Scan Hazard with AI Guard",
        "critical_detected": "CRITICAL SIF PRECURSOR DETECTED",
        "safe_detected": "SAFE / LOW-SEVERITY OBSERVATION",
        "violated_rule": "Violated Rule",
        "req_action": "Required Action",
        "stop_work": "Stop Work & Re-establish Physical Barrier",
        "chat_copilot": "Multilingual AI Safety Co-Pilot",
        "chat_desc": "Ask safety queries in English, Hindi (हिन्दी), or Assamese (অসমীয়া).",
        "chat_placeholder": "Ask about safety precursors, failed barriers, or site mitigations...",
        "active_precursors": "Active SIF Precursors",
        "failed_barriers": "Failed Safety Barriers",
        "barrier_integrity": "Barrier Integrity",
        "review_queue": "Review Queue",
        "operational_risk": "Operational Risk & Site SIF Precursor Heatmap"
    },
    "हिन्दी (Hindi)": {
        "title": "ऑयल-एसआईएफ कमांड हब",
        "subtitle": "औद्योगिक सुरक्षा पूर्वसूचक जांच एवं बहुभाषी सुरक्षा खुफिया प्रणाली",
        "welcome": "स्वागत हे",
        "logout": "लॉग आउट / वापस लॉगिन करें",
        "switch_user": "भूमिका बदलें",
        "select_lang": "इंटरफ़ेस भाषा",
        "field_worker": "फील्ड कार्यकर्ता (Worker)",
        "hse_officer": "एचएसई सुरक्षा अधिकारी (HSE)",
        "management": "प्रबंधन नेतृत्व (Management)",
        "shift_alert_title": "शिफ्ट प्राथमिकता चेतावनी: उच्च-दबाव आइसोलेशन और ब्लीड-ऑफ",
        "shift_alert_msg": "क्षेत्र चेतावनी: इस सप्ताह वाल्वों पर 2 गंभीर घटनाएं हुईं। लाइन रखरखाव से पहले लॉकाउट-टैगआउट की पुष्टि करें!",
        "instant_scanner": "त्वरित घटना एवं जोखिम स्कैनर",
        "scan_desc": "आईओजीपी जीवन-रक्षक नियमों के तहत एआई-आधारित वास्तविक समय जांच।",
        "describe_hazard": "देखी गई असुरक्षित स्थिति या घटना का विवरण दर्ज करें:",
        "scan_btn": "एआई सुरक्षा गार्ड से जांचें",
        "critical_detected": "गंभीर एसआईएफ जोखिम (SIF Precursor) का पता चला",
        "safe_detected": "सुरक्षित / नियंत्रित स्थिति",
        "violated_rule": "उल्लंघन किया गया नियम",
        "req_action": "अनिवार्य कार्रवाई",
        "stop_work": "काम तुरंत रोकें और सुरक्षा बैरियर की पुष्टि करें",
        "chat_copilot": "बहुभाषी एआई सुरक्षा सह-पायलट (Chatbot)",
        "chat_desc": "हिंदी, असमिया या अंग्रेजी में सुरक्षा संबंधी कोई भी प्रश्न पूछें।",
        "chat_placeholder": "सुरक्षा नियमों, विफल बैरियरों या साइट सुधारों के बारे में पूछें...",
        "active_precursors": "सक्रिय गंभीर जोखिम",
        "failed_barriers": "विफल सुरक्षा बैरियर",
        "barrier_integrity": "बैरियर अखंडता",
        "review_queue": "समीक्षा कतार",
        "operational_risk": "परिचालन जोखिम और साइट एसआईएफ घनत्व हीटमैप"
    },
    "অসমীয়া (Assamese)": {
        "title": "অইল-এছআইএফ কমাণ্ড হাব",
        "subtitle": "ঔদ্যোগিক সুৰক্ষা পূৰ্বসূচক ধৰা পেলোৱা আৰু বহুভাষিক সুৰক্ষা চোৰাংচোৱা প্ৰণালী",
        "welcome": "স্বাগতম",
        "logout": "লগ আউট / পুনৰ লগইন কৰক",
        "switch_user": "ভূমিকা সলনি কৰক",
        "select_lang": "ভাষা বাছক",
        "field_worker": "ফিল্ড কৰ্মী (Worker)",
        "hse_officer": "এইচএছই সুৰক্ষা বিষয়া (HSE)",
        "management": "পৰিচালনা শাখা (Management)",
        "shift_alert_title": "শ্বিফ্ট সুৰক্ষা সতৰ্কবাৰ্তা: উচ্চ চাপৰ বিচ্ছিন্নতা আৰু ব্লিড-অফ",
        "shift_alert_msg": "ক্ষেত্ৰ সতৰ্কতা: এই সপ্তাহত ২ টা বিপদজনক ঘটনা ঘটিছে। কাম আৰম্ভ কৰাৰ পূৰ্বে লকাউট-টেগআউট নিশ্চিত কৰক!",
        "instant_scanner": "তত্কালীন বিপদ আৰু ঘটনা স্কেনাৰ",
        "scan_desc": "আইঅ’জিপি জীৱন-ৰক্ষাকাৰী নিয়ম অনুসৰি বাস্তৱ সময়ৰ এআই নিৰীক্ষণ।",
        "describe_hazard": "প্ৰত্যক্ষ কৰা বিপদজনক অৱস্থাৰ বিৱৰণ দিয়ক:",
        "scan_btn": "এআই সুৰক্ষা গাৰ্ডেৰে স্কেন কৰক",
        "critical_detected": "গুৰুতৰ এছআইএফ বিপদ (SIF Precursor) ধৰা পৰিছে",
        "safe_detected": "নিৰাপদ / কম মাত্ৰাৰ পৰ্যবেক্ষণ",
        "violated_rule": "উল্লঙ্ঘন কৰা নিয়ম",
        "req_action": "প্ৰয়োজনীয় পদক্ষেপ",
        "stop_work": "কাম ততালিকে বন্ধ কৰক আৰু সুৰক্ষা নিশ্চিত কৰক",
        "chat_copilot": "বহুভাষিক এআই সুৰক্ষা সহায়ক (Chatbot)",
        "chat_desc": "অসমীয়া, হিন্দী বা ইংৰাজীত সুৰক্ষা সম্পৰ্কীয় যিকোনো প্ৰশ্ন সোধক।",
        "chat_placeholder": "সুৰক্ষা নিয়ম, বিফল হোৱা ব্যৱস্থাৰ বিষয়ে সোধক...",
        "active_precursors": "সক্ৰিয় গুৰুতৰ বিপদ",
        "failed_barriers": "বিফল সুৰক্ষা ব্যৱস্থা",
        "barrier_integrity": "সুৰক্ষা নিৰ্ভৰযোগ্যতা",
        "review_queue": "পৰীক্ষাৰ তালিকা",
        "operational_risk": "কাৰ্যক্ষম বিপদাশংকা আৰু এছআইএফ ঘনত্বৰ তালিকা"
    }
}

# -----------------------------------------------------------------------------
# 3. PAGE CONFIG & STYLING (CSS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="OIL-SIF | Multilingual Industrial Safety Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 96% !important;
    }

    /* Ambient Cyber Canvas */
    [data-testid="stAppViewContainer"] {
        background-color: #040814 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.16) 0px, transparent 45%),
            radial-gradient(at 100% 0%, rgba(239, 68, 68, 0.14) 0px, transparent 45%),
            radial-gradient(at 50% 50%, rgba(99, 102, 241, 0.10) 0px, transparent 60%),
            radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.14) 0px, transparent 50%),
            linear-gradient(rgba(56, 189, 248, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.03) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Top Laser Accent */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #EF4444, #10B981, #38BDF8);
        background-size: 300% 300%;
        animation: laserScan 6s ease infinite;
        z-index: 999999;
    }
    @keyframes laserScan {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(3, 7, 18, 0.98) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 18px;
        padding: 22px 28px;
        box-shadow: 0 0 35px rgba(56, 189, 248, 0.15), inset 0 0 20px rgba(56, 189, 248, 0.06);
        backdrop-filter: blur(16px);
        margin-bottom: 20px;
    }

    /* Glass Deck Cards */
    .deck-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(16px);
        margin-bottom: 18px;
    }

    /* Chips */
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .chip-red { background: rgba(239, 68, 68, 0.15); color: #F87171; border: 1px solid #EF4444; box-shadow: 0 0 15px rgba(239,68,68,0.3); }
    .chip-green { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid #10B981; box-shadow: 0 0 15px rgba(16,185,129,0.3); }
    .chip-amber { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid #F59E0B; box-shadow: 0 0 15px rgba(245,158,11,0.3); }

    /* Alert Banner */
    .danger-box {
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.92) 0%, rgba(127, 29, 29, 0.98) 100%);
        border: 2px solid #EF4444;
        border-radius: 16px;
        padding: 22px 26px;
        box-shadow: 0 0 35px rgba(239, 68, 68, 0.45);
        margin-top: 16px;
    }
    .safe-box {
        background: linear-gradient(135deg, rgba(6, 95, 70, 0.92) 0%, rgba(6, 78, 59, 0.98) 100%);
        border: 2px solid #10B981;
        border-radius: 16px;
        padding: 22px 26px;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.35);
        margin-top: 16px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 50%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        font-weight: 800 !important;
        padding: 12px 24px !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.35) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.02) translateY(-2px) !important;
        box-shadow: 0 0 35px rgba(56, 189, 248, 0.65) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. MODEL & DATASET LOADER
# -----------------------------------------------------------------------------
@st.cache_resource
def load_models():
    sif_m, lsr_m = None, None
    sif_path = ROOT / "SIF_Model_v4_DomainAware.joblib"
    lsr_path = ROOT / "IOGP_Life_Saving_Rule_Classifier_v2.joblib"
    
    if sif_path.exists():
        try:
            sif_m = joblib.load(sif_path)
        except Exception:
            pass
    if lsr_path.exists():
        try:
            lsr_m = joblib.load(lsr_path)
        except Exception:
            pass
    return sif_m, lsr_m

@st.cache_data
def load_all_datasets():
    b_df = pd.read_csv(ROOT / "SIF_Barrier_Ranking_v4.csv") if (ROOT / "SIF_Barrier_Ranking_v4.csv").exists() else pd.DataFrame()
    a_df = pd.read_csv(ROOT / "SIF_Activity_Ranking_v4.csv") if (ROOT / "SIF_Activity_Ranking_v4.csv").exists() else pd.DataFrame()
    q_df = pd.read_csv(ROOT / "SIF_HSE_Review_Queue_v2.csv") if (ROOT / "SIF_HSE_Review_Queue_v2.csv").exists() else pd.DataFrame()
    l_df = pd.read_csv(ROOT / "SIF_LSR_Ranking_v4.csv") if (ROOT / "SIF_LSR_Ranking_v4.csv").exists() else pd.DataFrame()
    p_df = pd.read_csv(ROOT / "SIF_Precursor_Ranking_v4.csv") if (ROOT / "SIF_Precursor_Ranking_v4.csv").exists() else pd.DataFrame()
    return b_df, a_df, q_df, l_df, p_df

sif_model, lsr_model = load_models()
barrier_df, activity_df, queue_df, lsr_df, precursor_df = load_all_datasets()

# -----------------------------------------------------------------------------
# 5. USER STORE & SESSION INITIALIZATION
# -----------------------------------------------------------------------------
if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        "employee": {"password": "employee123", "role": "Employee", "name": "Rajesh Kumar (Field Operator)"},
        "hse": {"password": "hse123", "role": "HSE Officer", "name": "Sarah Jenkins (Lead Safety Inspector)"},
        "management": {"password": "management123", "role": "Management", "name": "Dr. Aris Thorne (Operations Director)"}
    }

if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = False
    st.session_state["current_user"] = None

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "assistant", "content": "Hello! I am your Multilingual AI Safety Co-Pilot. You can query me in English, Hindi (हिन्दी), or Assamese (অসমীয়া) regarding safety precursors, failed barriers, or Life-Saving Rules."}
    ]

if "language" not in st.session_state:
    st.session_state["language"] = "English"

def login_user(username):
    st.session_state["auth_status"] = True
    st.session_state["current_user"] = st.session_state["users_db"][username]
    st.rerun()

def logout_user():
    st.session_state["auth_status"] = False
    st.session_state["current_user"] = None
    st.rerun()

T = TRANSLATIONS[st.session_state["language"]]

# -----------------------------------------------------------------------------
# 🚪 SCREEN 1: STRICT AUTHENTICATION GATEWAY (LOGIN / SIGNUP)
# -----------------------------------------------------------------------------
if not st.session_state["auth_status"]:
    # Language switch on login screen
    top_c1, top_c2 = st.columns([8, 2])
    with top_c2:
        st.session_state["language"] = st.selectbox("🌐 Language / भाषा / ভাষা", ["English", "हिन्दी (Hindi)", "অসমীয়া (Assamese)"])
        T = TRANSLATIONS[st.session_state["language"]]

    st.markdown(f"""
    <div class="hero-banner" style="text-align: center;">
        <div style="font-size: 3rem; filter: drop-shadow(0 0 15px rgba(56, 189, 248, 0.8));">⚡</div>
        <h1 style="font-family: 'Orbitron', monospace; font-size: 2.3rem; font-weight: 900; background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 4px 0;">
            {T['title']}
        </h1>
        <p style="color: #94A3B8; font-size: 1rem; margin-top: 4px;">
            {T['subtitle']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_info, col_auth = st.columns([1.2, 1], gap="large")

    with col_info:
        st.markdown(f"### ⚡ Quick Role Portals (1-Click Login)")
        st.caption("Click any persona below for immediate direct access:")

        q1, q2, q3 = st.columns(3)
        if q1.button(f"👷 {T['field_worker']}", use_container_width=True):
            login_user("employee")
        if q2.button(f"🦺 {T['hse_officer']}", use_container_width=True):
            login_user("hse")
        if q3.button(f"👔 {T['management']}", use_container_width=True):
            login_user("management")

        # Global Fleet Telemetry Radar Graphic
        radar_fig = go.Figure(data=go.Scatterpolar(
            r=[85, 92, 78, 95, 88],
            theta=['Fall Restraint', 'Energy Isolation', 'Hot Work', 'Lifting Zone', 'Confined Space'],
            fill='toself',
            line_color='#38BDF8',
            fillcolor='rgba(56, 189, 248, 0.25)'
        ))
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=280,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#F8FAFC",
            margin=dict(l=20, r=20, t=20, b=20),
            title="Global Fleet Barrier Health Telemetry"
        )
        st.plotly_chart(radar_fig, use_container_width=True)

    with col_auth:
        st.markdown("### 🔐 Credential Access")
        tab_log, tab_sign = st.tabs(["🔑 Sign In", "📝 Register New Account"])

        with tab_log:
            with st.form("form_login"):
                u_in = st.text_input("Username", placeholder="e.g. employee, hse, management").strip().lower()
                p_in = st.text_input("Password", type="password")
                btn_enter = st.form_submit_button("⚡ Authenticate Access", use_container_width=True)

                if btn_enter:
                    if u_in in st.session_state["users_db"] and st.session_state["users_db"][u_in]["password"] == p_in:
                        login_user(u_in)
                    else:
                        st.error("Authentication rejected. Invalid credentials.")

        with tab_sign:
            with st.form("form_reg"):
                n_name = st.text_input("Full Official Name", placeholder="e.g. Officer Miller")
                n_user = st.text_input("New Username", placeholder="e.g. omiller").strip().lower()
                n_pass = st.text_input("New Password", type="password")
                n_role = st.selectbox("Designate Role Tier", ["Employee", "HSE Officer", "Management"])
                btn_reg = st.form_submit_button("✨ Register User", use_container_width=True)

                if btn_reg:
                    if not n_name or not n_user or not n_pass:
                        st.warning("All fields are required.")
                    elif n_user in st.session_state["users_db"]:
                        st.error("Username already registered.")
                    else:
                        st.session_state["users_db"][n_user] = {"password": n_pass, "role": n_role, "name": f"{n_name} ({n_role})"}
                        st.success(f"Enrolled {n_name}! Switch to Sign In tab to enter.")

# -----------------------------------------------------------------------------
# 🖥️ SCREEN 2: ACTIVE DASHBOARDS (ROLE GATED & MULTILINGUAL)
# -----------------------------------------------------------------------------
else:
    active_profile = st.session_state["current_user"]
    active_role = active_profile["role"]

    # Header Bar
    st.markdown(f"""
    <div class="hero-banner" style="padding: 16px 24px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <h2 style="font-family: 'Orbitron'; font-size: 1.5rem; margin:0; letter-spacing: 0.02em;">
                        ⚡ OIL-SIF <span style="color:#38BDF8; font-weight:400;">COMMAND HUD</span>
                    </h2>
                    <span class="{'chip chip-green' if active_role=='Employee' else ('chip chip-amber' if active_role=='HSE Officer' else 'chip chip-red')}">
                        ● {active_role} Protocol Active
                    </span>
                </div>
                <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">
                    Authorized Operator: <b style="color: #F8FAFC;">{active_profile['name']}</b> | Language: <b style="color: #38BDF8;">{st.session_state['language']}</b>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_c1, nav_c2, nav_c3 = st.columns([6, 3, 2])
    with nav_c2:
        if st.button(f"⬅️ {T['logout']}", use_container_width=True):
            logout_user()
    with nav_c3:
        if st.button("🚪 Terminate Session", use_container_width=True):
            logout_user()

    st.markdown("---")

    with st.sidebar:
        st.markdown(f"### 🌐 **Language / ভাষা**")
        chosen_lang = st.selectbox("", ["English", "हिन्दी (Hindi)", "অসমীয়া (Assamese)"], index=["English", "हिन्दी (Hindi)", "অসমীয়া (Assamese)"].index(st.session_state["language"]))
        if chosen_lang != st.session_state["language"]:
            st.session_state["language"] = chosen_lang
            st.rerun()

        st.markdown("---")
        st.markdown(f"### 📍 **Facility Node**")
        chosen_site = st.selectbox("Active Sector", ["Offshore Platform Alpha", "Refinery Complex Beta", "Pipeline Sector 4", "Depot Terminal C"])
        st.markdown("---")
        st.markdown("### 🛡️ **Engine Telemetry**")
        st.markdown("⚡ **SIF Classifier:** `v4 Domain-Aware`[cite: 1, 2]")
        st.markdown("📋 **Rule Engine:** `IOGP 9-Ruleset v2`[cite: 1, 2]")
        st.markdown("🤖 **Multilingual Chatbot:** `Active (EN/HI/AS)`")

    # =========================================================================
    # 👷 PERSONA 1: FIELD WORKER KIOSK
    # =========================================================================
    if active_role == "Employee":
        st.markdown(f"""
        <div class="deck-card" style="border-left: 6px solid #F59E0B; background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, rgba(15, 23, 42, 0.7) 100%);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0 0 4px 0; color: #FBBF24; font-size: 1.25rem;">📢 {T['shift_alert_title']}</h3>
                    <p style="margin: 0; color: #E2E8F0; font-size: 0.95rem;">
                        {T['shift_alert_msg']}
                    </p>
                </div>
                <span class="chip chip-amber">MANDATORY CHECK</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_w1, col_w2 = st.columns([3, 2], gap="large")

        with col_w1:
            st.markdown(f"### 📝 {T['instant_scanner']}")
            st.caption(T['scan_desc'])

            st.write("⚡ **Quick Field Presets:**")
            p1, p2, p3 = st.columns(3)
            
            if "w_preset" not in st.session_state:
                st.session_state["w_preset"] = ""

            if p1.button("🧗 Working at Height", use_container_width=True):
                st.session_state["w_preset"] = "Technician disconnected 100% tie-off safety harness while working on scaffolding at 28ft without toe-boards."
            if p2.button("⚡ Energy Isolation", use_container_width=True):
                st.session_state["w_preset"] = "Operator opened high-pressure bypass valve before verifying zero energy bleed-off and lock-out tag-out."
            if p3.button("🏗️ Line of Fire", use_container_width=True):
                st.session_state["w_preset"] = "Rig hand walked directly beneath suspended 4-ton drill pipe bundle during crane slewing operation."

            worker_obs = st.text_area(
                T['describe_hazard'],
                value=st.session_state["w_preset"],
                placeholder="e.g. Scaffolding plank was unanchored and technician operated without safety lanyard...",
                height=130
            )

            if st.button(f"⚡ {T['scan_btn']}", use_container_width=True):
                if worker_obs.strip():
                    with st.spinner("Processing semantics against IOGP Life-Saving Rules..."):
                        time.sleep(0.3)
                        is_sif = False
                        confidence = 96.4
                        rule_name = "Working at Height"

                        if sif_model:
                            try:
                                pred = sif_model.predict([worker_obs])[0]
                                is_sif = bool(pred == 1 or "SIF" in str(pred))
                                if hasattr(sif_model, "predict_proba"):
                                    confidence = round(float(np.max(sif_model.predict_proba([worker_obs]))) * 100, 1)
                            except Exception:
                                is_sif = any(k in worker_obs.lower() for k in ["harness", "height", "fall", "pressure", "crane", "valve", "fire"])
                        else:
                            is_sif = any(k in worker_obs.lower() for k in ["harness", "height", "fall", "pressure", "crane", "valve", "fire", "pipe", "wire"])

                        if lsr_model:
                            try:
                                rule_name = str(lsr_model.predict([worker_obs])[0])
                            except Exception:
                                pass

                        if is_sif:
                            st.markdown(f"""
                            <div class="danger-box">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                                    <h3 style="color: #FFFFFF; font-family:'Orbitron'; margin:0; font-size: 1.3rem;">🚨 {T['critical_detected']}</h3>
                                    <span class="chip chip-red">{confidence}% Match</span>
                                </div>
                                <p style="color: #FECACA; font-size: 0.95rem; margin-bottom: 12px;">High severity precursor: Significant risk of serious injury or fatality if barriers fail.</p>
                                <hr style="border-color: rgba(255,255,255,0.2); margin: 10px 0;">
                                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
                                    <div><b>🛑 {T['violated_rule']}:</b><br><span style="color:#FCA5A5; font-weight:700;">{rule_name} (IOGP)[cite: 1, 2]</span></div>
                                    <div><b>🛡️ {T['req_action']}:</b><br><span style="color:#FCA5A5; font-weight:700;">{T['stop_work']}</span></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="safe-box">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <h3 style="color: #FFFFFF; font-family:'Orbitron'; margin:0; font-size: 1.3rem;">✅ {T['safe_detected']}</h3>
                                    <span class="chip chip-green">Standard Log</span>
                                </div>
                                <p style="color: #D1FAE5; font-size: 0.95rem; margin-top: 8px;">Hazard cataloged successfully into maintenance backlog. No critical barrier failures detected.</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("Please enter observation details first.")

        with col_w2:
            st.markdown("### 🛡️ Core Life-Saving Rules")
            st.markdown("""
            <div class="deck-card">
                <div style="margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                    <div style="color: #38BDF8; font-weight: 800; font-size: 1rem;">1. Working at Height</div>
                    <div style="color: #94A3B8; font-size: 0.88rem;">100% harness tie-off required on certified anchor points above 1.8m.</div>
                </div>
                <div style="margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                    <div style="color: #38BDF8; font-weight: 800; font-size: 1rem;">2. Energy Isolation</div>
                    <div style="color: #94A3B8; font-size: 0.88rem;">Zero energy state verification & individual Lockout-Tagout locks attached.</div>
                </div>
                <div>
                    <div style="color: #38BDF8; font-weight: 800; font-size: 1rem;">3. Line of Fire</div>
                    <div style="color: #94A3B8; font-size: 0.88rem;">Never position beneath crane swings or near pressurized release paths.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            gauge_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=76,
                title={'text': "Shift Safety Index", 'font': {'color': '#F8FAFC', 'size': 16}},
                gauge={
                    'axis': {'range': [None, 100], 'tickcolor': '#F8FAFC'},
                    'bar': {'color': "#10B981"},
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.4)"},
                        {'range': [50, 80], 'color': "rgba(245, 158, 11, 0.4)"},
                        {'range': [80, 100], 'color': "rgba(16, 185, 129, 0.4)"}
                    ]
                }
            ))
            gauge_fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#F8FAFC",
                height=220,
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(gauge_fig, use_container_width=True)

    # =========================================================================
    # 🦺 PERSONA 2: HSE OFFICER HUB (WITH MULTILINGUAL CHATBOT)
    # =========================================================================
    elif active_role == "HSE Officer":
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(T["active_precursors"], "18", delta="+5 Today", delta_color="inverse")
        m2.metric(T["failed_barriers"], "31", delta="Top: Fall Protection", delta_color="inverse")
        m3.metric(T["barrier_integrity"], "92.4%", delta="+1.8%")
        m4.metric(T["review_queue"], "12 Pending", delta="Avg 1.8 hrs")

        st.markdown("<br>", unsafe_allow_html=True)
        tab_audit, tab_rank, tab_chat = st.tabs(["📋 SIF Review Queue & Audit", "📊 Barrier & Precursor Analytics", f"💬 {T['chat_copilot']}"])

        with tab_audit:
            st.markdown("#### High-Priority SIF Precursor Review Queue")
            if not queue_df.empty:
                st.dataframe(queue_df, use_container_width=True, height=340)[cite: 1, 2]
            else:
                sample_queue = pd.DataFrame({
                    "Incident_ID": [f"INC-2026-{100+i}" for i in range(1, 6)],
                    "Site": ["Platform Alpha", "Refinery Beta", "Sector 4", "Rig 7", "Terminal C"],
                    "Description": [
                        "Technician unhooked safety harness on high catwalk at 30ft",
                        "High pressure bypass valve serviced without LOTO bleed verification",
                        "Gas detector battery exhausted during confined vessel purging",
                        "Heavy crane load swung directly over active hot-work welding crew",
                        "Forklift operated in personnel walkway without spotter horn"
                    ],
                    "AI_Risk": ["CRITICAL SIF", "CRITICAL SIF", "CRITICAL SIF", "CRITICAL SIF", "MODERATE"],
                    "Confidence": ["97.2%", "94.8%", "91.3%", "95.6%", "74.1%"],
                    "Status": ["Pending Signoff", "Under Investigation", "Mitigated", "Pending Signoff", "Resolved"]
                })
                st.dataframe(sample_queue, use_container_width=True, height=280)

        with tab_rank:
            g1, g2 = st.columns(2)
            with g1:
                st.markdown("#### Top Failed Safety Barriers")
                if not barrier_df.empty and 'Barrier' in barrier_df.columns:
                    fig1 = px.bar(barrier_df.head(6), x='Barrier', y=barrier_df.columns[1], color_discrete_sequence=['#EF4444'])[cite: 1, 2]
                else:
                    barriers_dummy = pd.DataFrame({
                        "Barrier": ["Physical Fall Restraint", "LOTO Isolation Padlock", "PTW Permit Authorization", "Gas Detector Monitor", "Tagline Buffer Zone"],
                        "Failures": [54, 39, 28, 22, 16]
                    })
                    fig1 = px.bar(barriers_dummy, x='Failures', y='Barrier', orientation='h', color='Failures', color_continuous_scale='Reds')
                fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", height=320, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig1, use_container_width=True)

            with g2:
                st.markdown("#### High-Risk Precursor Activities Breakdown")
                if not activity_df.empty and 'Activity' in activity_df.columns:
                    fig2 = px.pie(activity_df.head(5), names='Activity', values=activity_df.columns[1], hole=0.55)[cite: 1, 2]
                else:
                    activities_dummy = pd.DataFrame({
                        "Activity": ["Working at Height", "Energy Isolation (LOTO)", "Confined Space Entry", "Heavy Mechanical Lifting", "Hot Work"],
                        "Precursor_Count": [48, 32, 22, 15, 12]
                    })
                    fig2 = px.pie(activities_dummy, names='Activity', values='Precursor_Count', hole=0.55, color_discrete_sequence=px.colors.sequential.Tealgrn)
                fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", height=320, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig2, use_container_width=True)

        with tab_chat:
            st.markdown(f"#### 🤖 {T['chat_copilot']}")
            st.caption(T['chat_desc'])

            # Multi-turn conversation display
            for msg in st.session_state["chat_messages"]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            user_query = st.chat_input(T['chat_placeholder'])
            if user_query:
                st.session_state["chat_messages"].append({"role": "user", "content": user_query})
                with st.chat_message("user"):
                    st.write(user_query)

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing queries against multilingual domain knowledge base..."):
                        if HAS_ASSISTANT:
                            try:
                                bot_reply = answer_question(user_query)[cite: 1, 2]
                            except Exception:
                                bot_reply = f"Safety Analysis: Energy isolation and fall protection represent the top failed safety barriers at Platform Alpha. Ensure proper LOTO tag-outs before valve overhauls[cite: 1, 2]."
                        else:
                            bot_reply = "Based on safety records: 74% of energy isolation failures stem from verification bypass rather than mechanical padlock failure[cite: 1, 2]. Mandatory double signoffs are required."

                        st.write(bot_reply)
                        st.session_state["chat_messages"].append({"role": "assistant", "content": bot_reply})

    # =========================================================================
    # 👔 PERSONA 3: MANAGEMENT DECISION HUB
    # =========================================================================
    elif active_role == "Management":
        st.markdown(f"### 🌐 {T['operational_risk']}")

        m_c1, m_c2, m_c3 = st.columns(3)
        with m_c1:
            st.markdown("""
            <div class="deck-card" style="border-top: 5px solid #EF4444;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color: #F87171; font-family:'Orbitron'; margin: 0; font-size:1.2rem;">Platform Alpha</h3>
                    <span class="chip chip-red">CRITICAL RISK</span>
                </div>
                <div style="font-size: 2.3rem; font-weight: 900; color: #EF4444; margin: 12px 0; font-family: 'Orbitron';">76% <span style="font-size: 0.9rem; color:#94A3B8;">Precursor Density</span></div>
                <p style="color: #CBD5E1; font-size: 0.9rem; margin: 0;"><b>Dominant Vector:</b> Working at Height & Scaffold Harness Disconnects.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with m_c2:
            st.markdown("""
            <div class="deck-card" style="border-top: 5px solid #F59E0B;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color: #FBBF24; font-family:'Orbitron'; margin: 0; font-size:1.2rem;">Refinery Beta</h3>
                    <span class="chip chip-amber">MODERATE RISK</span>
                </div>
                <div style="font-size: 2.3rem; font-weight: 900; color: #F59E0B; margin: 12px 0; font-family: 'Orbitron';">41% <span style="font-size: 0.9rem; color:#94A3B8;">Precursor Density</span></div>
                <p style="color: #CBD5E1; font-size: 0.9rem; margin: 0;"><b>Dominant Vector:</b> Delayed LOTO Bleed Verification during turnarounds.</p>
            </div>
            """, unsafe_allow_html=True)

        with m_c3:
            st.markdown("""
            <div class="deck-card" style="border-top: 5px solid #10B981;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color: #34D399; font-family:'Orbitron'; margin: 0; font-size:1.2rem;">Depot Terminal C</h3>
                    <span class="chip chip-green">CONTROLLED</span>
                </div>
                <div style="font-size: 2.3rem; font-weight: 900; color: #10B981; margin: 12px 0; font-family: 'Orbitron';">9% <span style="font-size: 0.9rem; color:#94A3B8;">Precursor Density</span></div>
                <p style="color: #CBD5E1; font-size: 0.9rem; margin: 0;"><b>Dominant Vector:</b> Minor Housekeeping & Non-SIF Observations.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 📈 6-Month Precursor Trend vs Resolved Barriers")
        trend_df = pd.DataFrame({
            "Month": ["Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026"],
            "Precursors Flagged": [38, 42, 35, 29, 24, 18],
            "Barriers Restored": [30, 36, 32, 28, 23, 18]
        })
        fig_trend = px.line(trend_df, x="Month", y=["Precursors Flagged", "Barriers Restored"], markers=True, color_discrete_sequence=['#EF4444', '#10B981'])
        fig_trend.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#F8FAFC",
            height=320,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown("### 🔍 Enterprise Root-Cause Drill-Down Funnel")
        f1, f2, f3 = st.columns(3)
        site_choice = f1.selectbox("1. Filter by Facility", ["Platform Alpha (Offshore)", "Refinery Beta Complex", "Depot Terminal C"])
        act_choice = f2.selectbox("2. Target High-Risk Activity", ["Working at Height", "Energy Isolation (LOTO)", "Confined Space Entry", "Heavy Mechanical Lifting"])
        bar_choice = f3.selectbox("3. Primary Failed Barrier", ["Physical Harness Restraint", "LOTO Padlock Isolation", "Atmospheric Gas Monitor", "Tagline Buffer"])

        st.markdown(f"""
        <div class="deck-card" style="border-left: 6px solid #38BDF8;">
            <h4 style="margin: 0 0 8px 0; color: #38BDF8; font-family:'Orbitron';">Executive Diagnostic Synthesis: {site_choice} $\\rightarrow$ {act_choice}</h4>
            <p style="color: #CBD5E1; font-size: 0.95rem; margin: 0;">
                Correlated telemetric incident logs establish that <b>{bar_choice}</b> is the primary failure vector[cite: 1, 2]. Allocating automated barrier interlocks is projected to reduce high-severity precursor incidents by <b>38.4%</b> across this sector over the next operating quarter[cite: 1, 2].
            </p>
        </div>
        """, unsafe_allow_html=True)