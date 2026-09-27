import hashlib
import json
import random
from pathlib import Path

import streamlit as st


# ============================================================
# PERSISTENT USER STORE
#
# Demo-grade local JSON store (this is a prototype, not a
# production auth system — swap for a real DB + bcrypt/argon2
# before this ever sees real credentials).
# ============================================================

STORE_PATH = Path(__file__).resolve().parent / "_users.json"

ROLES = ["Employee / Worker", "HSE Officer", "Management"]

ROLE_META = {
    "Employee / Worker": {
        "prefix": "EMP",
        "icon": "🦺",
        "tagline": "Report incidents & view safety guidance",
        "color": "#16a34a",
    },
    "HSE Officer": {
        "prefix": "HSE",
        "icon": "🛡️",
        "tagline": "Full SIF analytics & review queue",
        "color": "#d97706",
    },
    "Management": {
        "prefix": "MGR",
        "icon": "👔",
        "tagline": "Executive risk & decision dashboards",
        "color": "#2563eb",
    },
}


def _hash_password(password, salt="oil-sif-proto"):
    return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()


def _seed_defaults():
    return {
        "EMP-1001": {
            "password": _hash_password("employee123"),
            "role": "Employee / Worker",
            "name": "Demo Employee",
        },
        "HSE-1001": {
            "password": _hash_password("hse123"),
            "role": "HSE Officer",
            "name": "Demo HSE Officer",
        },
        "MGR-1001": {
            "password": _hash_password("management123"),
            "role": "Management",
            "name": "Demo Manager",
        },
    }


def _load_store():
    if not STORE_PATH.exists():
        store = _seed_defaults()
        _save_store(store)
        return store

    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        store = _seed_defaults()
        _save_store(store)
        return store


def _save_store(store):
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)


def _generate_id(role):
    prefix = ROLE_META[role]["prefix"]
    store = _load_store()

    while True:
        candidate = f"{prefix}-{random.randint(1000, 9999)}"
        if candidate not in store:
            return candidate


# ============================================================
# CSS — auth screen only (sidebar hidden, animated hero card)
# ============================================================

def _inject_auth_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        section[data-testid="stSidebar"] { display: none; }
        header[data-testid="stHeader"] { background: transparent; }

        .block-container {
            padding-top: 1rem;
            max-width: 900px;
        }

        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        @keyframes gradientShift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes fadeSlideUp {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes floatY {
            0%, 100% { transform: translateY(0px); }
            50%      { transform: translateY(-8px); }
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 0 0 rgba(217,119,6,0.35); }
            50%      { box-shadow: 0 0 0 10px rgba(217,119,6,0); }
        }

        .auth-hero {
            background: linear-gradient(120deg, #061021, #0f2942, #16324f, #0f2942);
            background-size: 300% 300%;
            border-radius: 22px;
            padding: 2.1rem 2.3rem 1.7rem;
            color: white;
            text-align: center;
            margin-bottom: 1.3rem;
            box-shadow: 0 16px 40px -16px rgba(6,16,33,0.6);
            border: 1px solid rgba(242,181,68,0.25);
            animation: fadeSlideUp .6s ease-out, gradientShift 12s ease infinite;
        }
        .auth-hero .badge-icon {
            font-size: 2.6rem;
            display: inline-block;
            animation: floatY 3.2s ease-in-out infinite;
        }
        .auth-hero h1 {
            margin: .5rem 0 .2rem;
            font-size: 1.9rem;
            font-weight: 800;
            letter-spacing: -0.01em;
        }
        .auth-hero p {
            margin: 0;
            color: #c7d2e0;
            font-size: .95rem;
        }

        .auth-card {
            background: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 18px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 10px 28px -14px rgba(15,41,66,0.25);
            animation: fadeSlideUp .7s ease-out;
        }

        .role-card {
            border: 2px solid #e6e9ef;
            border-radius: 16px 16px 0 0;
            padding: 1.1rem .8rem .9rem;
            text-align: center;
            background: #f8fafc;
            transition: all .2s ease;
        }
        .role-card .icon { font-size: 2rem; }
        .role-card .title { font-weight: 700; color: #0f2942; margin-top: .3rem; font-size: .92rem; }
        .role-card .tagline { font-size: .74rem; color: #64748b; margin-top: .15rem; }
        .role-card.selected {
            border-color: #d97706;
            background: #fff7ed;
            animation: pulseGlow 1.8s ease-in-out infinite;
        }

        div[data-testid="column"] .stButton>button {
            border-radius: 0 0 14px 14px !important;
            margin-top: -6px;
            border: 2px solid #e6e9ef;
            border-top: none;
            font-weight: 600;
            transition: transform .15s ease, box-shadow .15s ease;
        }
        div[data-testid="column"] .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px -8px rgba(15,41,66,0.3);
        }

        .stButton>button {
            border-radius: 10px;
            font-weight: 600;
            transition: transform .15s ease, box-shadow .15s ease;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
        }
        .stButton>button[kind="primary"] {
            background: linear-gradient(120deg, #d97706, #b45309);
            border: none;
        }
        .stButton>button[kind="primary"]:hover {
            box-shadow: 0 10px 20px -8px rgba(217,119,6,0.55);
        }

        .id-reveal {
            background: #0f2942;
            color: #f2b544;
            border-radius: 12px;
            padding: .9rem 1.1rem;
            text-align: center;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: .06em;
            margin: .6rem 0 .9rem;
            animation: fadeSlideUp .4s ease-out;
        }

        .demo-hint {
            font-size: .78rem;
            color: #94a3b8;
            text-align: center;
            margin-top: .9rem;
        }
        .demo-hint code {
            background: #f1f5f9;
            padding: .1rem .4rem;
            border-radius: 6px;
            color: #334155;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _role_picker(key_prefix):
    """Renders three illustrated role cards + select buttons. Returns the chosen role (or None)."""
    state_key = f"{key_prefix}_role"
    if state_key not in st.session_state:
        st.session_state[state_key] = None

    cols = st.columns(3)
    for col, role in zip(cols, ROLES):
        meta = ROLE_META[role]
        selected = st.session_state[state_key] == role
        with col:
            st.markdown(
                f"""
                <div class="role-card {'selected' if selected else ''}">
                    <div class="icon">{meta['icon']}</div>
                    <div class="title">{role}</div>
                    <div class="tagline">{meta['tagline']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Selected ✓" if selected else "Select",
                key=f"{key_prefix}_pick_{role}",
                use_container_width=True,
            ):
                st.session_state[state_key] = role
                st.rerun()

    return st.session_state[state_key]


# ============================================================
# LOGIN
# ============================================================

def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "signin"

    if st.session_state.authenticated:
        return True

    _inject_auth_css()

    st.markdown(
        """
        <div class="auth-hero">
            <span class="badge-icon">🛡️</span>
            <h1>OIL SIF Intelligence</h1>
            <p>Serious Injury &amp; Fatality precursor intelligence for the field, HSE, and leadership.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, mid, right = st.columns([1, 3, 1])
    with mid:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        t1, t2 = st.columns(2)
        with t1:
            if st.button(
                "🔐 Sign In",
                use_container_width=True,
                type="primary" if st.session_state.auth_mode == "signin" else "secondary",
            ):
                st.session_state.auth_mode = "signin"
                st.rerun()
        with t2:
            if st.button(
                "🆕 Create Account",
                use_container_width=True,
                type="primary" if st.session_state.auth_mode == "signup" else "secondary",
            ):
                st.session_state.auth_mode = "signup"
                st.rerun()

        st.markdown("###")

        if st.session_state.auth_mode == "signin":
            _render_signin()
        else:
            _render_signup()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="demo-hint">
                Demo accounts — <code>EMP-1001 / employee123</code> ·
                <code>HSE-1001 / hse123</code> ·
                <code>MGR-1001 / management123</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return False


def _render_signin():
    role = _role_picker("signin")

    if role is None:
        st.info("👆 Choose your role to continue.")
        return

    back, _ = st.columns([1, 3])
    with back:
        if st.button("← Back", key="signin_back", use_container_width=True):
            st.session_state.signin_role = None
            st.rerun()

    meta = ROLE_META[role]
    st.markdown(f"**{meta['icon']} Signing in as {role}**")

    user_id = st.text_input(
        "User ID",
        placeholder=f"{meta['prefix']}-1001",
        key="signin_id",
    ).strip().upper()

    password = st.text_input("Password", type="password", key="signin_pw")

    if st.button("Login →", type="primary", use_container_width=True, key="signin_submit"):
        store = _load_store()
        record = store.get(user_id)

        if not user_id or not password:
            st.error("Enter both your User ID and password.")
        elif not record:
            st.error("No account found with that User ID.")
        elif record["role"] != role:
            st.error(f"That User ID is not registered as {role}. Double-check your role selection.")
        elif record["password"] != _hash_password(password):
            st.error("Incorrect password.")
        else:
            st.session_state.authenticated = True
            st.session_state.user_id = user_id
            st.session_state.username = record["name"]
            st.session_state.user_role = record["role"]
            st.toast(f"Welcome back, {record['name']}!", icon=meta["icon"])
            st.rerun()


def _render_signup():
    role = _role_picker("signup")

    if role is None:
        st.info("👆 Choose the role your account should have.")
        return

    back, _ = st.columns([1, 3])
    with back:
        if st.button("← Back", key="signup_back", use_container_width=True):
            st.session_state.signup_role = None
            st.rerun()

    meta = ROLE_META[role]
    st.markdown(f"**{meta['icon']} Creating a {role} account**")

    full_name = st.text_input("Full name", key="signup_name")
    password = st.text_input("Choose a password", type="password", key="signup_pw")
    confirm = st.text_input("Confirm password", type="password", key="signup_pw2")

    if st.button("Create Account", type="primary", use_container_width=True, key="signup_submit"):
        if not full_name.strip():
            st.error("Enter your full name.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            new_id = _generate_id(role)
            store = _load_store()
            store[new_id] = {
                "password": _hash_password(password),
                "role": role,
                "name": full_name.strip(),
            }
            _save_store(store)

            st.success("Account created! This is your permanent User ID — save it, it also shows your role:")
            st.markdown(f'<div class="id-reveal">{new_id}</div>', unsafe_allow_html=True)

            if st.button("Continue to Sign In →", use_container_width=True, key="signup_goto_login"):
                st.session_state.auth_mode = "signin"
                st.session_state.signin_role = role
                st.rerun()


# ============================================================
# LOGOUT
# ============================================================

def logout():
    for key in [
        "authenticated", "user_role", "username", "user_id",
        "auth_mode", "signin_role", "signup_role",
        "gemini_chat", "chat_history",
    ]:
        st.session_state.pop(key, None)

    st.rerun()


# ============================================================
# ROLE HELPERS
# ============================================================

def get_role():
    return st.session_state.get("user_role")


def get_user_id():
    return st.session_state.get("user_id")


def get_display_name():
    return st.session_state.get("username")


def is_employee():
    return get_role() == "Employee / Worker"


def is_hse():
    return get_role() == "HSE Officer"


def is_management():
    return get_role() == "Management"
