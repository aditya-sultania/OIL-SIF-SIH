import hashlib
import json
import os
import time
from pathlib import Path

import streamlit as st

# ============================================================
# STORAGE
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
USER_DB = ROOT / "users_db.json"

ROLES = ["Employee / Worker", "HSE Officer", "Management"]

ROLE_META = {
    "Employee / Worker": {"icon": "🦺", "color": "#10b981"},
    "HSE Officer":       {"icon": "🛡️", "color": "#f59e0b"},
    "Management":        {"icon": "👔", "color": "#6366f1"},
}

# Seed / default demo accounts so existing credentials keep working.
_DEFAULT_USERS = {
    "employee": {
        "password_plain_seed": "employee123",
        "role": "Employee / Worker",
        "name": "Safety Employee",
    },
    "hse": {
        "password_plain_seed": "hse123",
        "role": "HSE Officer",
        "name": "HSE Safety Officer",
    },
    "management": {
        "password_plain_seed": "management123",
        "role": "Management",
        "name": "Management User",
    },
}


def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def _new_salt() -> str:
    return os.urandom(16).hex()


def _seed_users_if_missing():
    if USER_DB.exists():
        return

    users = {}

    for username, meta in _DEFAULT_USERS.items():
        salt = _new_salt()
        users[username] = {
            "salt": salt,
            "password_hash": _hash_password(meta["password_plain_seed"], salt),
            "role": meta["role"],
            "name": meta["name"],
            "created_at": time.time(),
        }

    _write_users(users)


def _read_users() -> dict:
    _seed_users_if_missing()

    try:
        with open(USER_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _write_users(users: dict):
    with open(USER_DB, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


# ============================================================
# PUBLIC ACCOUNT HELPERS
# ============================================================

def user_exists(username: str) -> bool:
    return username.strip().lower() in _read_users()


def create_user(username: str, password: str, name: str, role: str):
    username = username.strip().lower()
    users = _read_users()

    if not username or not password:
        return False, "Username and password are required."

    if username in users:
        return False, "That username is already taken."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if role not in ROLES:
        return False, "Please choose a valid role."

    salt = _new_salt()

    users[username] = {
        "salt": salt,
        "password_hash": _hash_password(password, salt),
        "role": role,
        "name": name.strip() or username.title(),
        "created_at": time.time(),
    }

    _write_users(users)

    return True, "Account created. You can log in now."


def verify_credentials(username: str, password: str):
    username = username.strip().lower()
    users = _read_users()

    user = users.get(username)

    if not user:
        return None

    if _hash_password(password, user["salt"]) == user["password_hash"]:
        return user

    return None


# ============================================================
# SESSION STATE
# ============================================================

def _init_session():
    defaults = {
        "authenticated": False,
        "user_role": None,
        "username": None,
        "display_name": None,
        "auth_mode": "Login",
        "theme": "dark",
        "chat_language": "English",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# LOGIN / SIGNUP UI
# ============================================================

def login():
    _init_session()

    if st.session_state.authenticated:
        return True

    _render_auth_page()

    return False


def _render_auth_page():

    st.markdown(
        """
        <style>
        .auth-hero {
            text-align: center;
            padding: 2.2rem 1rem 1.4rem;
            border-radius: 22px;
            margin-bottom: 1.4rem;
            background: linear-gradient(120deg, #0f172a 0%, #1e293b 45%, #312e81 100%);
            background-size: 200% 200%;
            animation: gradientShift 8s ease infinite, fadeInUp .6s ease;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 18px 45px rgba(2, 6, 23, 0.45);
        }
        .auth-hero h1 {
            font-size: 2.3rem;
            margin: 0;
            background: linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        .auth-hero p {
            color: #cbd5e1;
            margin-top: .5rem;
            font-size: 1.02rem;
        }
        .role-chip {
            display: inline-block;
            padding: .25rem .7rem;
            margin: .15rem;
            border-radius: 999px;
            font-size: .78rem;
            font-weight: 600;
            color: white;
        }
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        @keyframes fadeInUp {
            from {opacity: 0; transform: translateY(14px);}
            to {opacity: 1; transform: translateY(0);}
        }
        .auth-card {
            animation: fadeInUp .5s ease;
            padding: 1.6rem 1.8rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(148,163,184,0.18);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="auth-hero">
            <h1>🛡️ OIL SIF Intelligence</h1>
            <p>Serious Injury &amp; Fatality Precursor Intelligence Platform</p>
            <span class="role-chip" style="background:#10b981;">🦺 Employee</span>
            <span class="role-chip" style="background:#f59e0b;">🛡️ HSE Officer</span>
            <span class="role-chip" style="background:#6366f1;">👔 Management</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, mid, right = st.columns([1, 1.4, 1])

    with mid:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔑 Login", "🆕 Create Account"])

        with tab_login:
            _login_form()

        with tab_signup:
            _signup_form()

        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("ℹ️ Demo credentials (for evaluators)"):
            st.code(
                "employee / employee123\n"
                "hse / hse123\n"
                "management / management123",
                language="text",
            )


def _login_form():
    username = st.text_input("Username", key="login_username", placeholder="e.g. hse")

    show_pw = st.toggle("Show password", key="login_show_pw")
    password = st.text_input(
        "Password",
        key="login_password",
        type="default" if show_pw else "password",
        placeholder="••••••••",
    )

    st.checkbox("Remember me on this device", value=True, key="login_remember")

    if st.button("Login", type="primary", use_container_width=True, key="login_btn"):
        if not username or not password:
            st.error("Please enter both username and password.")
            return

        user = verify_credentials(username, password)

        if user:
            st.session_state.authenticated = True
            st.session_state.username = username.strip().lower()
            st.session_state.user_role = user["role"]
            st.session_state.display_name = user.get("name", username.title())
            st.toast(f"Welcome back, {st.session_state.display_name}! 👋", icon="✅")
            st.balloons()
            time.sleep(0.4)
            st.rerun()
        else:
            st.error("Invalid username or password.")

    st.caption("Don't have an account? Use the **Create Account** tab. →")


def _signup_form():
    name = st.text_input("Full name", key="signup_name", placeholder="e.g. Priya Sharma")
    username = st.text_input("Choose a username", key="signup_username", placeholder="e.g. priya.s")

    role = st.selectbox(
        "Select your role",
        ROLES,
        key="signup_role",
        format_func=lambda r: f"{ROLE_META[r]['icon']}  {r}",
    )

    col1, col2 = st.columns(2)

    with col1:
        password = st.text_input("Password", type="password", key="signup_password")

    with col2:
        confirm = st.text_input("Confirm password", type="password", key="signup_confirm")

    agree = st.checkbox(
        "I understand this is a prototype and my role selection is for demo purposes.",
        key="signup_agree",
    )

    if st.button("Create Account", type="primary", use_container_width=True, key="signup_btn"):

        if not agree:
            st.warning("Please confirm the checkbox above to continue.")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        ok, message = create_user(username, password, name, role)

        if ok:
            st.success(message + " Switch to the **Login** tab to sign in. ✅")
            st.snow()
        else:
            st.error(message)


# ============================================================
# LOGOUT
# ============================================================

def logout():
    for key in [
        "authenticated",
        "user_role",
        "username",
        "display_name",
        "gemini_chat",
        "chat_history",
    ]:
        st.session_state.pop(key, None)

    st.rerun()


# ============================================================
# ROLE HELPERS
# ============================================================

def get_role():
    return st.session_state.get("user_role")


def get_display_name():
    return st.session_state.get("display_name") or (st.session_state.get("username") or "").title()


def is_employee():
    return get_role() == "Employee / Worker"


def is_hse():
    return get_role() == "HSE Officer"


def is_management():
    return get_role() == "Management"
